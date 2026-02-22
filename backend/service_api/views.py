
from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError

def health_check(request):
    """Liveness probe: App is running."""
    return JsonResponse({"status": "healthy", "timestamp": "now"}, status=200)

def ready_check(request):
    """Readiness probe: App + DB are connected."""
    try:
        # Verify DB connection
        connections['default'].cursor()
    except OperationalError:
        return JsonResponse({"status": "unready", "reason": "database_connection_failed"}, status=503)
    return JsonResponse({"status": "ready"}, status=200)

from rest_framework import viewsets, permissions, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import (
    ServiceRequest, ServiceConfig, WorkflowStep, User, AuditLog, MDA, Role, 
    ServiceDomain, ServiceCategory, InterDepartmentalMemo, GovernmentFile, 
    OfficialLetter, CorrespondenceAction, DesktopReview,
    PaymentProvider, PaymentTransaction, RevenueSplit,
    ConsentRecord, DataPurpose, ConsentAccessLog, RegistryAdapter, RegistryEndpoint
)
from .serializers import (
    ServiceRequestSerializer, ServiceConfigSerializer, WorkflowStepSerializer, 
    UserSerializer, AuditLogSerializer, MDASerializer, RoleSerializer,
    ServiceDomainSerializer, ServiceCategorySerializer,
    InterDepartmentalMemoSerializer, GovernmentFileSerializer,
    OfficialLetterSerializer, CorrespondenceActionSerializer,
    DesktopReviewSerializer, PaymentProviderSerializer, PaymentTransactionSerializer,
    ConsentRecordSerializer, DataPurposeSerializer, ConsentAccessLogSerializer,
    RegistryAdapterSerializer, RegistryEndpointSerializer
)
from .services import PaymentService, ConsentService
from .permissions import IsAdminOrAuthenticatedReadOnly, IsParticipantOrAdmin, AuditLogPermission, IsSystemAdmin, IsClaimAuthorized
from .workflow import WorkflowEngine, send_notification

class RegistryAdapterViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Lists available Registry Adapters (e.g., CRS, IPRS) for configuration.
    """
    queryset = RegistryAdapter.objects.all()
    serializer_class = RegistryAdapterSerializer
    permission_classes = [permissions.IsAuthenticated]

class RegistryEndpointViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Lists API operations available on registries.
    Filterable by ?adapter_id=...
    """
    serializer_class = RegistryEndpointSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = RegistryEndpoint.objects.all()
        adapter_id = self.request.query_params.get('adapter_id')
        if adapter_id:
            queryset = queryset.filter(adapter_id=adapter_id)
        return queryset

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated or getattr(self, 'swagger_fake_view', False):
            return User.objects.none()
            
        if user.role in ['admin', 'system_admin'] or user.is_staff:
            return User.objects.all()
        
        perms = user.user_role.permissions if user.user_role else []
        if user.role == 'mda_admin' or 'mda_manage_users' in perms:
            return User.objects.filter(mda=user.mda)
            
        return User.objects.filter(id=user.id)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        
        # AUTO-LINKING LOGIC: If user is viewing their own profile and has no saved docs/ID
        # AND has an ID number, try to fetch Birth Record from CRS
        if instance == user and user.id_number:
             needs_linking = True
             if user.saved_documents:
                 for doc in user.saved_documents:
                     if doc.get('doctype') == 'BIRTH_CERTIFICATE':
                         needs_linking = False
                         break
             
             if needs_linking:
                 from .services import RegistryService
                 # Refactored: Use DB-driven RegistryService instead of hardcoded mock
                 result = RegistryService.query('CRS', user.id_number, 'child_id')
                 
                 if result['status'] == 'SUCCESS':
                     found_record = result['data']
                     # We need an ID for the doc, we'll try to find the key or use a default
                     found_ben = found_record.get('ben', 'BC-UNKNOWN')
                     
                     if not user.saved_documents:
                         user.saved_documents = []
                         
                     doc_entry = {
                        "doc_id": f"DOC-{found_ben}",
                        "doctype": "BIRTH_CERTIFICATE",
                        "title": f"Birth Certificate - {found_record.get('full_name', 'N/A')}",
                        "issue_date": found_record.get('date', 'N/A'),
                        "issuer": "Civil Registration Services",
                        "authoritative_id": found_ben,
                        "metadata": found_record
                     }
                     
                     user.saved_documents.append(doc_entry)
                     user.save()
                     instance = user # Refresh instance
                     print(f"AUTO-LINK: Linked Birth Cert {found_ben} to User {user.username}")

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if not username or not password or not email:
            return Response({'error': 'Username, Email, and Password are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Default to Citizen
            citizen_role = Role.objects.get(name='citizen')
            user = User.objects.create_user(
                username=username, 
                email=email, 
                password=password,
                role='citizen', 
                user_role=citizen_role
            )
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models import Q

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['role'] = user.role
        token['username'] = user.username
        if user.mda:
            token['mda_id'] = user.mda.id
        return token

    def validate(self, attrs):
        # Allow login with Username OR ID Number
        username_or_id = attrs.get('username')
        password = attrs.get('password')

        if username_or_id and password:
            # Check if user exists with this username
            user = User.objects.filter(username=username_or_id).first()
            
            # If not found, check if it's an ID Number
            if not user:
                user = User.objects.filter(id_number=username_or_id).first()
                if user:
                    # Found user by ID, swap 'username' in attrs to the actual username 
                    # so the parent serializer can validate the password correctly
                    attrs['username'] = user.username

        return super().validate(attrs)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsSystemAdmin] # Restricted to Platform Admins

class MDAViewSet(viewsets.ModelViewSet):
    queryset = MDA.objects.all()
    serializer_class = MDASerializer
    permission_classes = [IsAdminOrAuthenticatedReadOnly]

class ServiceDomainViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ServiceDomain.objects.all()
    serializer_class = ServiceDomainSerializer
    permission_classes = [permissions.AllowAny]

class ServiceCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    permission_classes = [permissions.AllowAny]

class ServiceCatalogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Public facing API for the Service Catalogue.
    """
    queryset = ServiceConfig.objects.filter(catalogue_visible=True, service_status='active').order_by('catalogue_order', 'service_name')
    serializer_class = ServiceConfigSerializer
    permission_classes = [permissions.AllowAny]
    search_fields = ['service_name', 'description', 'life_event_group']
    @action(detail=False, methods=['get'])
    def process_matrix(self, request):
        """
        Returns a hierarchical view: Domain -> Process (Category) -> Service -> Systems & Actors
        """
        domains = ServiceDomain.objects.prefetch_related('categories__services').all()
        data = []
        
        for domain in domains:
            domain_data = {
                "domain_name": domain.name,
                "processes": []
            }
            for category in domain.categories.all():
                process_data = {
                    "process_name": category.name,
                    "services": []
                }
                for service in category.services.filter(service_status='active'):
                    process_data["services"].append({
                        "id": service.id,
                        "service_code": service.service_code,
                        "service_name": service.service_name,
                        "description": service.description,
                        "systems": service.associated_systems,
                        "actors": service.associated_actors,
                        "mda": service.mda.name,
                        "mda_code": service.mda.code if service.mda.code else "",
                        "service_type": service.service_type,
                        "service_category": category.name,
                        "life_event_group": service.life_event_group,
                        "maturity": service.digitization_level,
                        "delivery_channels": service.delivery_channels,
                        "process_complexity": service.process_complexity,
                        "pain_points": service.pain_points,
                        "workflow_configured": service.workflow_steps.exists(),
                        "workflow_steps": list(service.workflow_steps.order_by('sequence').values('step_name', 'role', 'step_type', 'sequence', 'bpmn_element_type', 'lifecycle_stage'))
                    })
                if process_data["services"]:
                    domain_data["processes"].append(process_data)
            
            if domain_data["processes"]:
                data.append(domain_data)
                
        return Response(data)

class ServiceConfigViewSet(viewsets.ModelViewSet):
    queryset = ServiceConfig.objects.all()
    serializer_class = ServiceConfigSerializer
    permission_classes = [IsAdminOrAuthenticatedReadOnly]

class WorkflowStepViewSet(viewsets.ModelViewSet):
    queryset = WorkflowStep.objects.all()
    serializer_class = WorkflowStepSerializer
    permission_classes = [IsAdminOrAuthenticatedReadOnly]

    def get_queryset(self):
        queryset = WorkflowStep.objects.all()
        service_config_id = self.request.query_params.get('service_config')
        if service_config_id:
            queryset = queryset.filter(service_config_id=service_config_id)
        return queryset.order_by('sequence')

class ServiceRequestViewSet(viewsets.ModelViewSet):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
    permission_classes = [IsParticipantOrAdmin, IsClaimAuthorized]

    def get_queryset(self):
        user = self.request.user
        queryset = ServiceRequest.objects.all().select_related('service_config', 'current_step', 'service_config__mda')

        if not user.is_authenticated or getattr(self, 'swagger_fake_view', False):
            return queryset.none()

        if user.role == 'admin' or user.is_superuser:
            return queryset.order_by('-created_at')

        if user.role == 'citizen':
            return queryset.filter(citizen=user).order_by('-created_at')

        if user.role in ['officer', 'supervisor', 'mda_admin', 'registrar', 'GLOBAL_OFFICER', 'GLOBAL_SUPERVISOR', 'MDA_OFFICER', 'MDA_SUPERVISOR']:
            from django.db.models import Q
            
            # 1. Global / System Admin Bypass
            if user.role in ['GLOBAL_OFFICER', 'GLOBAL_SUPERVISOR', 'system_admin', 'admin'] or user.is_superuser:
                return queryset.order_by('-created_at')

            # 2. Scope Determination (Legacy MDA vs New Assigned MDAs)
            assigned_mda_ids = list(user.assigned_mdas.values_list('id', flat=True))
            if user.mda: assigned_mda_ids.append(user.mda.id)
            
            # Universal MDA Filter
            mda_filter = Q(service_config__mda_id__in=assigned_mda_ids) | Q(current_step__target_mda_id__in=assigned_mda_ids)
            
            # View-level (detail) bypass
            if self.action != 'list':
                return queryset.filter(mda_filter)

            # 3. List Filtering Logic
            # Higher Authority (Admins/Supervisors) - See Everything in Scope
            if self.request.query_params.get('all_mda') or \
               self.request.query_params.get('team_requests') or \
               user.role in ['mda_admin', 'MDA_SUPERVISOR', 'supervisor', 'registrar']:
                
                queryset = queryset.filter(mda_filter).exclude(status__in=['closed', 'approved', 'rejected'])
                
                if self.request.query_params.get('unassigned'):
                    queryset = queryset.filter(assigned_to__isnull=True)
                elif self.request.query_params.get('assigned_to_me'):
                     queryset = queryset.filter(assigned_to=user)
                elif self.request.query_params.get('is_escalated'):
                     queryset = queryset.filter(is_escalated=True)

            # Standard Officers - Restricted Pool
            elif user.role in ['officer', 'MDA_OFFICER']:
                if self.request.query_params.get('assigned_to_me'):
                    queryset = queryset.filter(mda_filter, assigned_to=user).exclude(status__in=['closed', 'approved', 'rejected'])
                elif self.request.query_params.get('unassigned'):
                    queryset = queryset.filter(mda_filter, assigned_to__isnull=True, current_step__role__icontains='officer').exclude(status__in=['closed', 'approved', 'rejected'])
                else:
                    # DEFAULT (Inbox): Only show what is assigned to ME
                    # Unless it's their own citizen request
                    queryset = queryset.filter(mda_filter).filter(Q(assigned_to=user) | Q(citizen=user)).exclude(status__in=['closed', 'approved', 'rejected'])
            
            else:
                # Catch-all for other MDA roles: basic visibility of assigned MDA requests
                # Default to assigned to ME for Inbox consistency
                queryset = queryset.filter(mda_filter, assigned_to=user).exclude(status__in=['closed', 'approved', 'rejected'])

            return queryset.order_by('-created_at', '-updated_at')

        return queryset.none()

    def create(self, request, *args, **kwargs):
        citizen = request.user
        service_code = request.data.get('service_code')
        payload = request.data.get('payload')

        if not service_code or not payload:
            return Response({"detail": "Service code and payload are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            service_config = ServiceConfig.objects.get(service_code=service_code)
        except ServiceConfig.DoesNotExist:
            return Response({"detail": "Service configuration not found."}, status=status.HTTP_404_NOT_FOUND)

        workflow_engine = WorkflowEngine()
        service_request = workflow_engine.create_service_request(citizen, service_config, payload)
        serializer = self.get_serializer(service_request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def complete_step(self, request, pk=None):
        service_request = self.get_object()
        user = request.user
        action_taken = request.data.get('action')
        details = request.data.get('details')

        if not action_taken:
            return Response({"detail": "Action is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Enforce that the person completing the step is the one it's assigned to
        if service_request.assigned_to != user and user.role != 'admin':
             return Response({"detail": "You must claim this task before you can complete it."}, status=status.HTTP_403_FORBIDDEN)

        workflow_engine = WorkflowEngine(request_id=service_request.request_id)
        try:
            workflow_engine.complete_manual_step(user, action_taken, details)
            service_request.refresh_from_db() # Refresh to get updated status
            
            # Clear assignment when step is completed so next step starts unassigned
            service_request.assigned_to = None
            service_request.save()
            
            serializer = self.get_serializer(service_request)
            return Response(serializer.data)
        except (ValueError, PermissionError) as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def escalate(self, request, pk=None):
        service_request = self.get_object()
        user = request.user

        service_request.is_escalated = True
        service_request.status = 'escalated'
        service_request.save()

        AuditLog.objects.create(
            service_request=service_request,
            actor=user,
            action='REQUEST_ESCALATED',
            details=f"Request escalated by {user.username}."
        )

        # Notify all supervisors
        supervisors = User.objects.filter(role='supervisor')
        for supervisor in supervisors:
            send_notification(
                supervisor,
                f"Service Request {service_request.request_id} has been escalated by {user.username}.",
                service_request
            )

        serializer = self.get_serializer(service_request)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def acknowledge_escalation(self, request, pk=None):
        service_request = self.get_object()
        user = request.user

        if user.role not in ['supervisor', 'admin']:
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        service_request.is_escalated = False
        service_request.save()

        AuditLog.objects.create(
            service_request=service_request,
            actor=user,
            action='ESCALATION_ACKNOWLEDGED',
            details=f"Escalation acknowledged by {user.username}."
        )

        serializer = self.get_serializer(service_request)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def claim(self, request, pk=None):
        service_request = self.get_object()
        user = request.user

        # 1. Enforce Role & Scope
        from .permissions import RBACScopeManager
        allowed, reason = RBACScopeManager.evaluate_claim(user, service_request)
        if not allowed:
            return Response({"detail": reason}, status=status.HTTP_403_FORBIDDEN)

        # 2. Check if already assigned
        if service_request.assigned_to and service_request.assigned_to != user:
             return Response({"detail": f"This task is already assigned to {service_request.assigned_to.username}"}, status=status.HTTP_400_BAD_REQUEST)

        service_request.assigned_to = user
        service_request.save()

        # Logging is handled by evaluate_claim automatically for the attempt, 
        # but we can add more context if successful.
        return Response(self.get_serializer(service_request).data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def release(self, request, pk=None):
        service_request = self.get_object()
        user = request.user

        if service_request.assigned_to != user and user.role != 'admin':
             return Response({"detail": "You cannot release a task that is not assigned to you."}, status=status.HTTP_403_FORBIDDEN)

        service_request.assigned_to = None
        service_request.save()

        AuditLog.objects.create(
            service_request=service_request,
            actor=user,
            action='TASK_RELEASED',
            details=f"Task released back to the pool by {user.username}."
        )

        serializer = self.get_serializer(service_request)
        return Response(serializer.data)

from rest_framework.views import APIView
from django.db.models import Count

class ReportSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        if request.user.role not in ['supervisor', 'mda_admin', 'admin', 'registrar']:
             return Response({"detail": "You do not have permission to access reports."}, status=status.HTTP_403_FORBIDDEN)

        # Base queryset for scoping
        user = request.user
        queryset = ServiceRequest.objects.all()
        
        if user.role != 'admin':
             queryset = queryset.filter(service_config__mda=user.mda)

        # 1. Volume Stats
        total_requests = queryset.count()
        requests_by_status = queryset.values('status').annotate(count=Count('status'))
        requests_per_service = queryset.values('service_config__service_name').annotate(count=Count('id'))

        # 2. SLA / Performance Stats
        # For POC, we treat 'updated_at' of a terminal status as the completion time.
        completed_requests = queryset.filter(status__in=['approved', 'rejected', 'closed'])
        total_completed = completed_requests.count()
        
        sla_met_count = 0
        total_duration_hours = 0
        
        # Calculate stats in memory for simplicity in POC (vs complex DB aggregation)
        for req in completed_requests:
            duration = req.updated_at - req.created_at
            hours = duration.total_seconds() / 3600
            total_duration_hours += hours
            
            # Mock SLA Target: 24 Hours
            if hours <= 24:
                sla_met_count += 1
                
        avg_processing_time = round(total_duration_hours / total_completed, 1) if total_completed else 0
        sla_compliance_rate = round((sla_met_count / total_completed) * 100, 1) if total_completed else 100

        # 3. Efficiency Stats (Avg Steps per Request)
        # Mocking this for now or could aggregate AuditLogs
        
        summary_data = {
            'total_requests': total_requests,
            'completed_requests': total_completed,
            'pending_requests': total_requests - total_completed,
            'requests_by_status': {item['status']: item['count'] for item in requests_by_status},
            'requests_per_service': {item['service_config__service_name']: item['count'] for item in requests_per_service},
            'performance': {
                'avg_processing_time_hours': avg_processing_time,
                'sla_compliance_rate': sla_compliance_rate,
                'sla_target_hours': 24
            }
        }
        return Response(summary_data)

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all().order_by('-timestamp')
    serializer_class = AuditLogSerializer
    permission_classes = [AuditLogPermission]

from .registries import get_registry

class RegistryQueryView(APIView):
    """
    Allow authenticated users to query registries (e.g., look up BEN or Notification Number from CRS).
    Refactored to use database-driven RegistryAdapter.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, registry_code=None, identifier=None):
        """
        Supports both:
        1. Admin dump (GET /api/registry/query/)
        2. Individual lookup (GET /api/registries/<code|mda>/<identifier>/)
        """
        if not registry_code:
            # Legacy Admin Dump behavior
            if request.user.role != 'admin':
                return Response({"detail": "Only admins can view registry dumps."}, status=403)
            
            from .models import RegistryAdapter
            adapters = RegistryAdapter.objects.all()
            dump = {}
            for adapter in adapters:
                dump[adapter.code] = {
                    "name": adapter.name,
                    "is_mock": adapter.is_mock,
                    "data": adapter.mock_data if adapter.is_mock else "LIVE_API"
                }
            return Response(dump)

        # Individual Lookup logic
        from .services import RegistryService
        
        # Mapping logic for common fields based on registry code
        field_map = {
            'IPRS': 'id',
            'KRA': 'id',
            'CRS': 'ben',
            'ARDHISASA': 'parcel_no',
            'NTSA': 'plate',
            'NEMIS': 'upi',
            'BRS': 'reg_no'
        }
        field = field_map.get(registry_code.upper(), 'id')
        
        # Override field from query params if needed
        query_field = request.query_params.get('field')
        if query_field:
            field = query_field

        result = RegistryService.query(registry_code.upper(), identifier, field)
        
        if result['status'] == 'NOT_FOUND':
            return Response(result, status=status.HTTP_404_NOT_FOUND)
            
        if result['status'] == 'ERROR':
            return Response(result, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response(result)

    def post(self, request):
        from .services import RegistryService
        
        # New Schematic Lookup Logic
        adapter_id = request.data.get('adapter_id')
        endpoint_id = request.data.get('endpoint_id')
        params = request.data.get('params')

        if adapter_id and endpoint_id:
            try:
                # Find the adapter and endpoint
                adapter = RegistryAdapter.objects.get(id=adapter_id)
                endpoint = RegistryEndpoint.objects.get(id=endpoint_id, adapter=adapter)

                # For POC, we'll map the 'query' or first param to the identifier logic 
                # or just pass through to the mockup logic.
                # In a real scenario, we'd construct the URL and headers based on endpoint.path/method
                
                # Simplified: Use the 'query' key from params as the main identifier
                identifier = params.get('query')
                if not identifier and params:
                    # Fallback: take first value
                    identifier = list(params.values())[0]

                if not identifier:
                     return Response({"detail": "Missing query parameter for lookup."}, status=400)

                # Execute query via service
                # We reuse RegistryService.query but mapped by Code from Adapter
                # We assume the mocked data structure handles the specific endpoint variation via 'field' 
                # or just general lookup.
                result = RegistryService.query(adapter.code, identifier)

                if result['status'] == 'NOT_FOUND':
                    # Fallback error message if mocked data misses
                    return Response({"status": "NOT_FOUND", "message": f"No record found in {adapter.name} for {identifier}"}, status=200) # Return 200 to let frontend handle 'not found' gracefully

                # Success
                return Response({"success": True, "status": "SUCCESS", "data": result.get('data', {})})

            except (RegistryAdapter.DoesNotExist, RegistryEndpoint.DoesNotExist):
                 return Response({"detail": "Invalid Registry or Endpoint configuration."}, status=404)
            except Exception as e:
                 return Response({"detail": str(e)}, status=500)

        # Legacy Logic (Keep for backward compatibility)
        registry_name = request.data.get('registry')
        identifier = request.data.get('identifier')
        field = request.data.get('field', 'id')
        
        if not registry_name or not identifier:
            return Response({"detail": "Registry name and identifier are required."}, status=400)
            
        # Refactored: Call RegistryService instead of legacy registries.py
        result = RegistryService.query(registry_name, identifier, field)
        
        if result['status'] == 'NOT_FOUND':
            return Response(result, status=404)
            
        return Response(result)

class GovernmentFileViewSet(viewsets.ModelViewSet):
    serializer_class = GovernmentFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated or getattr(self, 'swagger_fake_view', False):
            return GovernmentFile.objects.none()
            
        if user.role in ['admin', 'system_admin'] or user.is_staff:
            return GovernmentFile.objects.all()
        return GovernmentFile.objects.filter(owning_mda=user.mda)

    def perform_create(self, serializer):
        user = self.request.user
        if not user.mda:
            raise serializers.ValidationError("User must belong to an MDA.")
        serializer.save(owning_mda=user.mda)

class CorrespondenceActionViewSet(viewsets.ModelViewSet):
    queryset = CorrespondenceAction.objects.all()
    serializer_class = CorrespondenceActionSerializer
    permission_classes = [permissions.IsAuthenticated]

class OfficialLetterViewSet(viewsets.ModelViewSet):
    queryset = OfficialLetter.objects.all()
    serializer_class = OfficialLetterSerializer
    permission_classes = [permissions.IsAuthenticated]

class InterDepartmentalMemoViewSet(viewsets.ModelViewSet):
    serializer_class = InterDepartmentalMemoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated or getattr(self, 'swagger_fake_view', False):
            return InterDepartmentalMemo.objects.none()
            
        if user.role in ['admin', 'system_admin'] or user.is_staff:
            return InterDepartmentalMemo.objects.all().order_by('-created_at')
            
        if not user.mda:
            return InterDepartmentalMemo.objects.none()
        
        # Return memos where user's MDA is sender OR recipient
        return InterDepartmentalMemo.objects.filter(
            Q(sender_mda=user.mda) | Q(recipient_mda=user.mda)
        ).order_by('-created_at')

    def perform_create(self, serializer):
        user = self.request.user
        if not user.mda:
            raise serializers.ValidationError("User must belong to an MDA.")
        
        # Default to 'draft' status
        serializer.save(sender=user, sender_mda=user.mda, status='draft')

    @action(detail=True, methods=['post'])
    def request_review(self, request, pk=None):
        memo = self.get_object()
        if memo.status != 'draft':
            return Response({"detail": "Only drafts can be sent for review."}, status=400)
        memo.status = 'reviewing'
        memo.save()
        return Response({'status': 'sent for internal review'})

    @action(detail=True, methods=['post'])
    def approve_memo(self, request, pk=None):
        memo = self.get_object()
        if request.user.role not in ['supervisor', 'mda_admin', 'admin']:
             return Response({"detail": "Only Supervisors or MDA Admins can approve drafts."}, status=403)
        if memo.status != 'reviewing':
            return Response({"detail": "Memo must be in review to be approved."}, status=400)
        memo.status = 'approved'
        memo.save()
        return Response({'status': 'internally approved'})

    @action(detail=True, methods=['post'])
    def register_memo(self, request, pk=None):
        memo = self.get_object()
        if request.user.role not in ['registrar', 'admin']:
             return Response({"detail": "Only Registry Officers can register memos."}, status=403)
        
        if memo.status != 'approved':
             return Response({"detail": "Memo must be internally approved before registration."}, status=400)
        
        file_num = request.data.get('file_number')
        if not file_num:
             return Response({"detail": "File Number is required for registration."}, status=400)
             
        gov_file, _ = GovernmentFile.objects.get_or_create(
            file_number=file_num,
            defaults={'subject': memo.subject, 'owning_mda': memo.sender_mda}
        )
        
        memo.gov_file = gov_file
        memo.status = 'registered'
        import datetime
        year = datetime.datetime.now().year
        count = InterDepartmentalMemo.objects.filter(gov_file=gov_file).count() + 1
        memo.official_ref = f"{memo.sender_mda.code}/{file_num}/{year}/{count}"
        memo.save()
        return Response({'status': 'registered', 'official_ref': memo.official_ref})

    @action(detail=True, methods=['post'])
    def sign_memo(self, request, pk=None):
        memo = self.get_object()
        if request.user.role not in ['supervisor', 'mda_admin', 'admin']:
             return Response({"detail": "Only authorized signatories can sign official memos."}, status=403)
        
        if memo.status != 'registered':
             return Response({"detail": "Memo must be registered before signing."}, status=400)
             
        memo.digitally_signed = True
        memo.signed_by = request.user
        memo.status = 'actioning' # Once signed, it is issued to recipient
        memo.save()
        return Response({'status': 'signed and issued'})

    @action(detail=True, methods=['post'])
    def assign_action(self, request, pk=None):
        memo = self.get_object()
        user_id = request.data.get('assigned_to')
        instruction = request.data.get('instruction')
        
        action = CorrespondenceAction.objects.create(
            memo=memo,
            assigned_to_id=user_id,
            instruction=instruction
        )
        return Response({'status': 'action assigned', 'action_id': action.id})

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        memo = self.get_object()
        user = request.user
        
        if memo.recipient_mda != user.mda:
             return Response({"detail": "Not authorized."}, status=403)
             
        memo.is_read = True
        memo.save()
        return Response({'status': 'marked as read'})

class DesktopReviewViewSet(viewsets.ModelViewSet):
    queryset = DesktopReview.objects.all()
    serializer_class = DesktopReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Exposes Payment Aggregator (GPA) functionalities.
    """
    queryset = PaymentTransaction.objects.all()
    serializer_class = PaymentTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def initiate(self, request):
        """
        POST /api/payments/initiate/
        {
            "request_id": "REQ-123",
            "phone_number": "254700000000",
            "amount": 1500,
            "provider": "MPESA"
        }
        """
        request_id = request.data.get('request_id')
        phone = request.data.get('phone_number')
        amount = request.data.get('amount')
        provider = request.data.get('provider', 'MPESA')

        if not all([request_id, phone, amount]):
            return Response({"detail": "request_id, phone_number, and amount are required."}, status=400)

        result = PaymentService.initiate_stk_push(request_id, phone, amount, provider)
        if result['status'] == 'SUCCESS':
            return Response(result)
        return Response(result, status=400)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def callback(self, request):
        """
        Public endpoint for Payment Gateway webhooks.
        POST /api/payments/callback/
        {
            "provider_ref": "GPA-X",
            "status": "SUCCESS",
            "amount": 1500
        }
        """
        ref = request.data.get('provider_ref')
        status_code = request.data.get('status')
        
        if not ref or not status_code:
            return Response({"detail": "Invalid callback payload."}, status=400)

        result = PaymentService.process_callback(ref, status_code)
        if result['status'] == 'SUCCESS':
            return Response(result)
        return Response(result, status=400)

    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        """
        GET /api/payments/<id>/status/
        Checks the status of a specific transaction.
        """
        txn = self.get_object()
        return Response({
            "id": txn.id,
            "status": txn.status,
            "provider_ref": txn.provider_ref,
            "amount": txn.amount
        })

class ConsentViewSet(viewsets.ModelViewSet):
    """
    Manages citizen data processing consents.
    """
    serializer_class = ConsentRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated or getattr(self, 'swagger_fake_view', False):
            return ConsentRecord.objects.none()
            
        # Citizens only see their own consent records
        return ConsentRecord.objects.filter(user=user).order_by('-granted_at')

    @action(detail=False, methods=['post'])
    def grant(self, request):
        """
        POST /api/consent/grant/
        {
            "requester_id": 1,
            "scope": "identity.read",
            "purpose_code": "SERVICE_DELIVERY",
            "expires_in_days": 30
        }
        """
        requester_id = request.data.get('requester_id')
        scope = request.data.get('scope')
        purpose_code = request.data.get('purpose_code')
        days = request.data.get('expires_in_days', 30)

        if not all([requester_id, scope, purpose_code]):
            return Response({"detail": "requester_id, scope, and purpose_code are required."}, status=400)

        try:
            mda = MDA.objects.get(id=requester_id)
            consent = ConsentService.grant_consent(request.user, mda, scope, purpose_code, days)
            if consent:
                return Response(ConsentRecordSerializer(consent).data, status=201)
            return Response({"detail": "Failed to grant consent."}, status=400)
        except MDA.DoesNotExist:
            return Response({"detail": "MDA not found."}, status=404)

    @action(detail=True, methods=['post'])
    def revoke(self, request, pk=None):
        """
        POST /api/consent/{id}/revoke/
        """
        success = ConsentService.revoke_consent(pk, request.user)
        if success:
            return Response({"status": "REVOKED"})
        return Response({"detail": "Consent not found or unauthorized."}, status=404)

    @action(detail=False, methods=['get'])
    def check(self, request):
        """
        GET /api/consent/check/?scope=...&requester_code=...
        """
        scope = request.query_params.get('scope')
        requester_code = request.query_params.get('requester_code')

        if not scope or not requester_code:
            return Response({"detail": "scope and requester_code required."}, status=400)

        try:
            mda = MDA.objects.get(code=requester_code)
            consent = ConsentService.check_consent(request.user, mda, scope)
            if consent:
                return Response({
                    "has_consent": True,
                    "consent_id": consent.id,
                    "expires_at": consent.expires_at
                })
            return Response({"has_consent": False})
        except MDA.DoesNotExist:
            return Response({"detail": "MDA not found."}, status=404)

class LifecycleViewSet(viewsets.ViewSet):
    """
    Exposes Authoritative Lifecycle (Cradle-to-Grave) logic.
    Provides the 'Optimized To-Be' features for citizens and officers.
    """
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def journey_summary(self, request):
        """
        GET /api/lifecycle/journey_summary/
        Returns a high-level view of the citizen's life journey across registries.
        """
        from .services import LifecycleService
        summary = LifecycleService.get_citizen_journey_summary(request.user)
        return Response(summary)

    @action(detail=False, methods=['post'])
    def prefill(self, request):
        """
        POST /api/lifecycle/prefill/
        {
            "service_code": "IPRS-ID-001",
            "inputs": {
                "birth_certificate_number": "BC-111"
            }
        }
        """
        from .services import LifecycleService
        service_code = request.data.get('service_code')
        inputs = request.data.get('inputs', {})
        
        if not service_code:
            return Response({"detail": "service_code is required."}, status=400)
            
        prefilled_data = LifecycleService.prefill_service_application(service_code, request.user, inputs)
        return Response(prefilled_data)
