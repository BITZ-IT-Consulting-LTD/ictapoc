import django_filters
from .models import ServiceRequest, AuditLog, InterDepartmentalMemo, PaymentTransaction, WorkflowStepExecution

class ServiceRequestFilter(django_filters.FilterSet):
    assigned_to_me = django_filters.BooleanFilter(method='filter_assigned_to_me')
    unassigned = django_filters.BooleanFilter(method='filter_unassigned')
    mda = django_filters.NumberFilter(field_name='service_config__mda_id')
    
    class Meta:
        model = ServiceRequest
        fields = ['status', 'priority', 'service_config', 'is_escalated']

    def filter_assigned_to_me(self, queryset, name, value):
        if value:
            return queryset.filter(assigned_to=self.request.user)
        return queryset

    def filter_unassigned(self, queryset, name, value):
        if value:
            return queryset.filter(assigned_to__isnull=True)
        return queryset

class AuditLogFilter(django_filters.FilterSet):
    date_from = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='gte')
    date_to = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='lte')

    class Meta:
        model = AuditLog
        fields = ['actor', 'action', 'service_request']

class MemoFilter(django_filters.FilterSet):
    class Meta:
        model = InterDepartmentalMemo
        fields = ['status', 'sender_mda', 'recipient_mda', 'priority', 'memo_type']

class PaymentFilter(django_filters.FilterSet):
    class Meta:
        model = PaymentTransaction
        fields = ['status', 'provider', 'service_request']

class WorkflowExecutionFilter(django_filters.FilterSet):
    class Meta:
        model = WorkflowStepExecution
        fields = ['status', 'service_request', 'step', 'actor']
