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

urlpatterns = [
    path('', include(router.urls)),
    path('reports/summary/', views.ReportSummaryView.as_view(), name='report-summary'),
    path('registry/query/', views.RegistryQueryView.as_view(), name='registry-query'),
]
