from django.contrib import admin
from .models import FabricDefect, CLIInspector, Supervisor, Inspection, Operator, Flag, Notification

@admin.register(FabricDefect)
class FabricDefectAdmin(admin.ModelAdmin):
    list_display = ('id', 'defect_type', 'severity', 'detected_at')

@admin.register(CLIInspector)
class CLIInspectorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'date_joined')

@admin.register(Supervisor)
class SupervisorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'department')

@admin.register(Inspection)
class InspectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'cli_inspector', 'supervisor', 'status', 'inspection_date')

@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    list_display = ('id', 'operator_id', 'name', 'machine_no')
    search_fields = ('operator_id', 'name')

@admin.register(Flag)
class FlagAdmin(admin.ModelAdmin):
    list_display = ('id', 'operator', 'flag_type', 'issue_type', 'inspector', 'supervisor', 'date_of_inspection')
    list_filter = ('flag_type', 'issue_type', 'date_of_inspection')
    search_fields = ('operator__operator_id', 'operator__name', 'inspector__name', 'supervisor__name')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipient', 'notification_type', 'title', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read')
    search_fields = ('title', 'message', 'recipient__name')