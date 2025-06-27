from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import FabricDefect, Inspection, Operator, Flag, CLIInspector, Supervisor, Notification

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
        extra_kwargs = {
            'email': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

# FabricDefect Serializer
class FabricDefectSerializer(serializers.ModelSerializer):
    class Meta:
        model = FabricDefect
        fields = '__all__'

# Inspection Serializer
class InspectionSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Inspection
        fields = '__all__'

# CLI Inspector Serializer
class CLIInspectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CLIInspector
        fields = '__all__'

# Supervisor Serializer
class SupervisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supervisor
        fields = '__all__'

# Operator Serializer
class OperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = '__all__'

# Flag Serializer
class FlagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flag
        fields = '__all__'

# Detailed Flag Serializer
class DetailedFlagSerializer(serializers.ModelSerializer):
    operator_id = serializers.CharField(source='operator.operator_id')
    operator_name = serializers.CharField(source='operator.name', allow_null=True)
    defect_type = serializers.CharField(source='fabric_defect.defect_type')
    inspector_name = serializers.CharField(source='inspector.name')
    supervisor_name = serializers.CharField(source='supervisor.name')

    class Meta:
        model = Flag
        fields = ['id', 'operator_id', 'operator_name', 'defect_type', 'inspector_name', 
                  'supervisor_name', 'flag_type', 'issue_type', 'custom_reason', 
                  'machine_no', 'date_of_inspection', 'time_of_inspection', 'created_at']

# Notification Serializer
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'notification_type', 'title', 'message', 'is_read', 'created_at']
        
# Notification Detail Serializer
class NotificationDetailSerializer(serializers.ModelSerializer):
    related_flag = FlagSerializer(read_only=True)
    
    class Meta:
        model = Notification
        fields = ['id', 'notification_type', 'title', 'message', 'related_flag', 'is_read', 'created_at']

# At the end of serializers.py
__all__ = [
    'UserSerializer', 
    'InspectionSerializer', 
    'FabricDefectSerializer', 
    'OperatorSerializer', 
    'FlagSerializer', 
    'DetailedFlagSerializer', 
    'CLIInspectorSerializer', 
    'SupervisorSerializer', 
    'NotificationSerializer', 
    'NotificationDetailSerializer'
]
