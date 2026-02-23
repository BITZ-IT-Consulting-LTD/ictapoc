from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'catalog/domains', views.ServiceDomainViewSet)
router.register(r'catalog/categories', views.ServiceCategoryViewSet)
router.register(r'catalog/services', views.ServiceCatalogViewSet, basename='service-catalog')

router.register(r'users', views.UserViewSet)
router.register(r'roles', views.RoleViewSet)
router.register(r'mdas', views.MDAViewSet)
router.register(r'service-configs', views.ServiceConfigViewSet, basename='service-config')
router.register(r'workflow-steps', views.WorkflowStepViewSet)
router.register(r'service-requests', views.ServiceRequestViewSet)
router.register(r'audit-logs', views.AuditLogViewSet)
router.register(r'memos', views.InterDepartmentalMemoViewSet, basename='memos')
router.register(r'government-files', views.GovernmentFileViewSet, basename='government-files')
router.register(r'official-letters', views.OfficialLetterViewSet, basename='official-letters')
router.register(r'correspondence-actions', views.CorrespondenceActionViewSet, basename='correspondence-actions')
router.register(r'desktop-reviews', views.DesktopReviewViewSet)
router.register(r'payments', views.PaymentViewSet, basename='payments')
router.register(r'consent', views.ConsentViewSet, basename='consent')
router.register(r'lifecycle', views.LifecycleViewSet, basename='lifecycle')

# Registry Config
router.register(r'registries', views.RegistryAdapterViewSet)
router.register(r'registry-endpoints', views.RegistryEndpointViewSet, basename='registry-endpoints')



urlpatterns = [
    path('', include(router.urls)),
    path('reports/summary/', views.ReportSummaryView.as_view(), name='report-summary'),
    path('registry/query/', views.RegistryQueryView.as_view(), name='registry-query'),
    
    # Priority GEA Registry Endpoints
    path('registries/iprs/<str:identifier>/', views.RegistryQueryView.as_view(), {'registry_code': 'IPRS'}),
    path('registries/kra/<str:identifier>/', views.RegistryQueryView.as_view(), {'registry_code': 'KRA'}),
    path('registries/crs/<str:identifier>/', views.RegistryQueryView.as_view(), {'registry_code': 'CRS'}),
    path('registries/lands/<str:identifier>/', views.RegistryQueryView.as_view(), {'registry_code': 'ARDHISASA'}),
    path('registries/ntsa/<str:identifier>/', views.RegistryQueryView.as_view(), {'registry_code': 'NTSA'}),
    path('registries/brs/<str:identifier>/', views.RegistryQueryView.as_view(), {'registry_code': 'BRS'}),
    path('registries/nemis/<str:identifier>/', views.RegistryQueryView.as_view(), {'registry_code': 'NEMIS'}),
    path('registries/immigration/<str:identifier>/', views.RegistryQueryView.as_view(), {'registry_code': 'IMMIGRATION'}),
]
