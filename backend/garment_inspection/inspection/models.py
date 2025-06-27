from django.db import models
from django.contrib.auth.models import User

class FabricDefect(models.Model):
    defect_type = models.CharField(max_length=255)
    severity = models.CharField(max_length=50)
    image = models.ImageField(upload_to='defect_images/', blank=True, null=True)
    detected_at = models.DateTimeField(auto_now_add=True)
    reviewed = models.BooleanField(default=False)  # Added for review_defect functionality
    
    def __str__(self):
        return f"{self.defect_type} - {self.severity}"

class CLIInspector(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Supervisor(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    department = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Inspection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Added user field
    cli_inspector = models.ForeignKey(CLIInspector, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
    fabric_defect = models.ForeignKey(FabricDefect, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Reviewed', 'Reviewed'), ('Resolved', 'Resolved')],
        default='Pending'
    )
    inspection_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inspection {self.id} - {self.status}"

# Operator model for flagging
class Operator(models.Model):
    operator_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255, blank=True)
    machine_no = models.CharField(max_length=10, blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.operator_id})" if self.name else f"Operator {self.operator_id}"

# Flag model
class Flag(models.Model):
    FLAG_TYPES = (
        ('RED', 'Red Flag'),
        ('GREEN', 'Green Flag'),
    )
    
    ISSUE_TYPES = (
        ('MACHINE', 'Machine Issue'),
        ('FABRIC', 'Fabric Issue'),
        ('ENVIRONMENTAL', 'Environmental Issue'),
        ('SYSTEM', 'System Issue'),
        ('OTHER', 'Other'),
    )
    
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE, related_name='flags')
    fabric_defect = models.ForeignKey(FabricDefect, on_delete=models.CASCADE, related_name='flags')
    inspector = models.ForeignKey(CLIInspector, on_delete=models.CASCADE, related_name='reported_flags')
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE, related_name='supervised_flags')
    
    flag_type = models.CharField(max_length=10, choices=FLAG_TYPES)
    issue_type = models.CharField(max_length=20, choices=ISSUE_TYPES, null=True, blank=True)
    custom_reason = models.TextField(null=True, blank=True)
    
    machine_no = models.CharField(max_length=10)
    date_of_inspection = models.DateField()
    time_of_inspection = models.TimeField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.flag_type} Flag - Operator {self.operator.operator_id} - {self.created_at.date()}"

# New Notification model
class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('FLAG', 'Operator Flag'),
        ('INSPECTION', 'Inspection Update'),
        ('SYSTEM', 'System Notification'),
    )
    
    recipient = models.ForeignKey(Supervisor, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    related_flag = models.ForeignKey(Flag, on_delete=models.SET_NULL, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.notification_type} for {self.recipient.name}"