from rest_framework import serializers
from .models import ServiceRequest, ServiceConfig, WorkflowStep, User, MDA, AuditLog, Role

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class MDASerializer(serializers.ModelSerializer):
    class Meta:
        model = MDA
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    user_role_details = RoleSerializer(source='user_role', read_only=True)
    mda_details = MDASerializer(source='mda', read_only=True)
    user_role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), required=False, allow_null=True)
    mda = serializers.PrimaryKeyRelatedField(queryset=MDA.objects.all(), required=False, allow_null=True)
    
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'role', 'user_role', 'user_role_details', 'mda', 'mda_details', 'id_number', 'passport_number', 'phone_number', 'saved_documents')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class WorkflowStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowStep
        fields = '__all__'

class ServiceConfigSerializer(serializers.ModelSerializer):
    workflow_steps = WorkflowStepSerializer(many=True, read_only=True)

    class Meta:
        model = ServiceConfig
        fields = '__all__'

class ServiceRequestSerializer(serializers.ModelSerializer):
    assigned_to_details = UserSerializer(source='assigned_to', read_only=True)
    citizen_details = UserSerializer(source='citizen', read_only=True)
    
    class Meta:
        model = ServiceRequest
        fields = '__all__'
        depth = 1 # To show nested service_config and current_step details

class NestedServiceRequestSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service_config.service_name', read_only=True)
    class Meta:
        model = ServiceRequest
        fields = ('id', 'request_id', 'service_name')

class AuditLogSerializer(serializers.ModelSerializer):
    actor = UserSerializer(read_only=True)
    service_request = NestedServiceRequestSerializer(read_only=True)

    class Meta:
        model = AuditLog
        fields = '__all__'
