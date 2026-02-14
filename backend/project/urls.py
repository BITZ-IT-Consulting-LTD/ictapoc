from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from service_api.views import CustomTokenObtainPairView, health_check, ready_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health', health_check, name='health_liveness'),
    path('ready', ready_check, name='health_readiness'),
    path('api/', include('service_api.urls')),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]