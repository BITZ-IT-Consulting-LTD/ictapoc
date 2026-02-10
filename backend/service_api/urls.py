from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'roles', views.RoleViewSet)
router.register(r'mdas', views.MDAViewSet)
router.register(r'service-configs', views.ServiceConfigViewSet)
router.register(r'workflow-steps', views.WorkflowStepViewSet)
router.register(r'service-requests', views.ServiceRequestViewSet)
router.register(r'audit-logs', views.AuditLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('reports/summary/', views.ReportSummaryView.as_view(), name='report-summary'),
    path('registry/query/', views.RegistryQueryView.as_view(), name='registry-query'),
]
