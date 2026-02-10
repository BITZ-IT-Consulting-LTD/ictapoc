from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, MDA, ServiceConfig, WorkflowStep, ServiceRequest, AuditLog

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'role')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')

@admin.register(MDA)
class MDAAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

class WorkflowStepInline(admin.TabularInline):
    model = WorkflowStep
    extra = 1

@admin.register(ServiceConfig)
class ServiceConfigAdmin(admin.ModelAdmin):
    list_display = ('service_code', 'service_name', 'mda')
    search_fields = ('service_code', 'service_name')
    list_filter = ('mda',)
    inlines = [WorkflowStepInline]

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('request_id', 'citizen', 'service_config', 'status', 'created_at')
    list_filter = ('status', 'service_config__mda', 'service_config')
    search_fields = ('request_id', 'citizen__username', 'service_config__service_name')
    raw_id_fields = ('citizen', 'service_config', 'current_step')

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('service_request', 'actor', 'action', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('service_request__request_id', 'actor__username', 'action')
    raw_id_fields = ('service_request', 'actor')