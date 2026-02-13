from rest_framework import serializers
from .models import (
    ServiceRequest, ServiceConfig, WorkflowStep, User, MDA, AuditLog, Role, 
    ServiceDomain, ServiceCategory, InterDepartmentalMemo, GovernmentFile, 
    OfficialLetter, CorrespondenceAction
)

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

class ServiceDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceDomain
        fields = '__all__'

class ServiceCategorySerializer(serializers.ModelSerializer):
    domain = ServiceDomainSerializer(read_only=True)
    class Meta:
        model = ServiceCategory
        fields = '__all__'

class ServiceConfigSerializer(serializers.ModelSerializer):
    workflow_steps = WorkflowStepSerializer(many=True, read_only=True)
    category_details = ServiceCategorySerializer(source='category', read_only=True)

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

class GovernmentFileSerializer(serializers.ModelSerializer):
    owning_mda_details = MDASerializer(source='owning_mda', read_only=True)
    
    class Meta:
        model = GovernmentFile
        fields = '__all__'

class CorrespondenceActionSerializer(serializers.ModelSerializer):
    assigned_to_details = UserSerializer(source='assigned_to', read_only=True)
    
    class Meta:
        model = CorrespondenceAction
        fields = '__all__'

class OfficialLetterSerializer(serializers.ModelSerializer):
    sender_details = UserSerializer(source='sender', read_only=True)
    
    class Meta:
        model = OfficialLetter
        fields = '__all__'

class InterDepartmentalMemoSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    sender_mda = MDASerializer(read_only=True)
    recipient_mda_details = MDASerializer(source='recipient_mda', read_only=True)
    actions = CorrespondenceActionSerializer(many=True, read_only=True)
    gov_file_details = GovernmentFileSerializer(source='gov_file', read_only=True)
    
    class Meta:
        model = InterDepartmentalMemo
        fields = '__all__'
        read_only_fields = ('sender', 'sender_mda', 'created_at', 'updated_at', 'official_ref', 'digitally_signed', 'signed_by')

    def create(self, validated_data):
        user = self.context['request'].user
        if not user.mda:
            raise serializers.ValidationError("You must belong to an MDA to initiate a memo.")
        
        validated_data['sender'] = user
        validated_data['sender_mda'] = user.mda
        # Default status is 'draft' as per model, or user can set to 'internal_approval'
        return super().create(validated_data)
