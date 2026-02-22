from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenRefreshView
from service_api.views import CustomTokenObtainPairView, health_check, ready_check

api_info = openapi.Info(
    title="GoK Digital Services API",
    default_version='v1',
    description="API documentation for the Whole-of-Government Service Platform",
    terms_of_service="https://www.google.com/policies/terms/",
    contact=openapi.Contact(email="contact@ict.go.ke"),
    license=openapi.License(name="MIT License"),
)

schema_view = get_schema_view(
    api_info,
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health', health_check, name='health_liveness'),
    path('ready', ready_check, name='health_readiness'),
    
    # API Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    path('api/', include('service_api.urls')),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]