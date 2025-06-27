import logging
import os
import tempfile
import datetime
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import models
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

import requests
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework_simplejwt.tokens import RefreshToken

from .fabric_preprocessing import enhance_for_defect_detection
from .models import FabricDefect, Inspection, Operator, Flag, CLIInspector, Supervisor, Notification
from .serializers import (
    UserSerializer,
    InspectionSerializer,
    FabricDefectSerializer,
    OperatorSerializer,
    FlagSerializer,
    DetailedFlagSerializer,
    CLIInspectorSerializer,
    SupervisorSerializer,
    NotificationSerializer,
    NotificationDetailSerializer,
)
from .permissions import IsInspector, IsSupervisor, IsInspectorOrSupervisor

# User Registration View
class UserRegistration(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'User registered successfully',
                'user': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User Login View
class UserLogin(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Login successful',
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user_id': user.id
            }, status=status.HTTP_200_OK)
        
        return Response({
            'error': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)

# Inspection List and Create View
class InspectionListCreateView(generics.ListCreateAPIView):
    queryset = Inspection.objects.all()
    serializer_class = InspectionSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Inspection Detail, Update, and Delete View
class InspectionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Inspection.objects.all()
    serializer_class = InspectionSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

# FabricDefect List and Create View
class FabricDefectListCreateView(generics.ListCreateAPIView):
    queryset = FabricDefect.objects.all()
    serializer_class = FabricDefectSerializer
    permission_classes = [IsAuthenticated]
    
    # def perform_create(self, serializer):
    #     inspection_id = self.request.data.get('inspection')
    #     inspection = Inspection.objects.get(id=inspection_id)
    #     serializer.save(inspection=inspection)

# FabricDefect Detail, Update, and Delete View
class FabricDefectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FabricDefect.objects.all()
    serializer_class = FabricDefectSerializer
    permission_classes = [IsAuthenticated]
    
class SupervisorListView(generics.ListAPIView):
    queryset = Supervisor.objects.all()
    serializer_class = SupervisorSerializer
    permission_classes = [IsAuthenticated]

# Review Defect View
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def review_defect(request, defect_id):
    try:
        defect = FabricDefect.objects.get(id=defect_id)
    except FabricDefect.DoesNotExist:
        return Response({
            "error": "Defect not found"
        }, status=status.HTTP_404_NOT_FOUND)
    
    defect.reviewed = True
    defect.save()
    
    return Response({
        "message": "Defect reviewed successfully",
        "defect_id": defect.id,
        "reviewed": defect.reviewed
    }, status=status.HTTP_200_OK)

def home(request):
    return HttpResponse("Welcome to the Garment Inspection System")

# New function to analyze images with Azure Custom Vision
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def analyze_defect_image(request):
    """
    Analyze a captured image using Azure Custom Vision to identify garment defects.
    """
    try:
        # Check if image is provided in the request
        if 'image' not in request.FILES:
            return Response(
                {"error": "No image provided. Please capture an image first."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        image_file = request.FILES['image']
        
        # Get the prediction URL from settings
        prediction_url = settings.AZURE_PREDICTION_URL
        
        # The URL from settings should already have "/image" suffix based on azure.env
        # No need to add it again, but we'll check just to be safe
        if not prediction_url.endswith('/image'):
            prediction_url += '/image'
            
        # Prepare headers for Azure API call
        headers = {
            'Prediction-Key': settings.AZURE_CUSTOM_VISION_KEY,
            'Content-Type': 'application/octet-stream'
        }
        
        # Send the image to Azure Custom Vision
        try:
            # Read image data
            image_data = image_file.read()
            
            response = requests.post(
                prediction_url,
                headers=headers,
                data=image_data
            )
        except requests.RequestException as e:
            return Response(
                {"error": f"Error communicating with Azure Custom Vision: {str(e)}"}, 
                status=status.HTTP_502_BAD_GATEWAY
            )
        
        # Process Azure response
        if response.status_code == 200:
            prediction_results = response.json()
            
            # Get the most likely defect type from Azure predictions
            defect_type = "Unknown Defect"
            severity = "Low"
            confidence = 0.0
            
            if 'predictions' in prediction_results and prediction_results['predictions']:
                # Sort predictions by probability and get the top one
                top_prediction = sorted(
                    prediction_results['predictions'], 
                    key=lambda x: x['probability'], 
                    reverse=True
                )[0]
                
                # Use predictions if confidence is above threshold
                if top_prediction['probability'] > 0.5:
                    defect_type = top_prediction['tagName']
                    confidence = top_prediction['probability']
                    
                    # Set severity based on confidence level
                    if confidence > 0.85:
                        severity = "High"
                    elif confidence > 0.65:
                        severity = "Medium"
                    else:
                        severity = "Low"
            
            # Reset file pointer to beginning for saving
            image_file.seek(0)
            
            # Create defect record
            defect = FabricDefect.objects.create(
                defect_type=defect_type,
                severity=severity,
                image=image_file,
                reviewed=False
            )
            
            # Handle inspection association if provided
            inspection_id = request.data.get('inspection_id')
            if inspection_id:
                try:
                    # Find the inspection to associate with this defect
                    inspection = Inspection.objects.get(id=inspection_id)
                    
                    # Update the fabric_defect field of the inspection
                    # Note: This assumes your model relationship is set up correctly
                    inspection.fabric_defect = defect
                    inspection.save()
                except Inspection.DoesNotExist:
                    pass  # Silently ignore if inspection doesn't exist
            
            # Return success response with Azure predictions
            return Response({
                "message": "Image analyzed successfully",
                "defect": {
                    "id": defect.id,
                    "type": defect_type,
                    "severity": severity,
                    "confidence": round(confidence * 100, 2)  # As percentage
                },
                "predictions": prediction_results['predictions']
            }, status=status.HTTP_200_OK)
        else:
            # Azure returned an error
            return Response({
                "error": "Azure Custom Vision analysis failed",
                "details": response.text
            }, status=status.HTTP_502_BAD_GATEWAY)
    
    except Exception as e:
        # General exception handling
        import logging
        logger = logging.getLogger('inspection')
        logger.error(f"Error in analyze_defect_image: {str(e)}")
        
        return Response(
            {"error": f"An unexpected error occurred: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
def get_total_inspections(date):
    # Ensure the date is a datetime.date object
    if isinstance(date, str):
        date = timezone.datetime.strptime(date, '%Y-%m-%d').date()

    # Filter inspections by the date part of the inspection_date field
    total_inspections = Inspection.objects.filter(
        inspection_date__date=date
    ).count()
    return total_inspections

# New views for operator flagging feature

# Get operator by ID
class OperatorDetailView(generics.RetrieveAPIView):
    queryset = Operator.objects.all()
    serializer_class = OperatorSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'operator_id'

# Create or update operator - REPLACED with class-based view
class OperatorCreateUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            operator_id = request.data.get('operator_id')
            if not operator_id:
                return Response({"error": "Operator ID is required"}, status=status.HTTP_400_BAD_REQUEST)
                
            operator, created = Operator.objects.get_or_create(
                operator_id=operator_id,
                defaults={
                    'name': request.data.get('name', ''),
                    'machine_no': request.data.get('machine_no', '')
                }
            )
            
            # Update existing operator if found
            if not created:
                if 'name' in request.data:
                    operator.name = request.data['name']
                if 'machine_no' in request.data:
                    operator.machine_no = request.data['machine_no']
                operator.save()
                
            return Response({
                'message': f"Operator {'created' if created else 'updated'} successfully",
                'operator_id': operator.operator_id,
                'created': created
            }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Create a flag - Modified to create notification
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser, MultiPartParser, FormParser])
def create_flag(request):
    """Create a flag for an operator"""
    try:
        # Validate required fields
        required_fields = ['operator_id', 'machine_no', 'defect', 'inspected_by', 
                         'supervisor_in_charge', 'date_of_inspection', 'time_of_inspection', 'flag_type']
                         
        for field in required_fields:
            if field not in request.data:
                return Response({"error": f"Field '{field}' is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Get or create operator
        operator_id = request.data.get('operator_id')
        operator, created = Operator.objects.get_or_create(
            operator_id=operator_id,
            defaults={'machine_no': request.data.get('machine_no', '')}
        )
        
        if not created and not operator.machine_no:
            operator.machine_no = request.data.get('machine_no', '')
            operator.save()
            
        # Get or create inspector
        inspector_name = request.data.get('inspected_by')
        inspectors = CLIInspector.objects.filter(name=inspector_name)
        if inspectors.exists():
            inspector = inspectors.first()  # Just use the first one found
        else:
            # Create a new inspector if none exists
            inspector = CLIInspector.objects.create(
                name=inspector_name,
                email=f'{inspector_name.lower().replace(" ", ".")}@example.com',
                phone=''
            )
        
        # Get or create supervisor
        supervisor_name = request.data.get('supervisor_in_charge')
        supervisors = Supervisor.objects.filter(name=supervisor_name)
        if supervisors.exists():
            supervisor = supervisors.first()  # Just use the first one found
        else:
            # Create a new supervisor if none exists
            supervisor = Supervisor.objects.create(
                name=supervisor_name,
                email=f'{supervisor_name.lower().replace(" ", ".")}@example.com',
                phone='',
                department='Quality Control'
            )
        
        # Get or create defect
        defect_type = request.data.get('defect')
        defect = FabricDefect.objects.filter(defect_type=defect_type).first()
        if not defect:
            defect = FabricDefect.objects.create(defect_type=defect_type, severity='Medium')

        # Format date and time
        date_str = request.data.get('date_of_inspection')
        time_str = request.data.get('time_of_inspection')
        
        inspection_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date() if isinstance(date_str, str) else date_str
        
        if isinstance(time_str, str):
            try:
                inspection_time = datetime.datetime.strptime(time_str, '%H:%M%p').time()
            except ValueError:
                try:
                    inspection_time = datetime.datetime.strptime(time_str, '%H:%M').time()
                except ValueError:
                    return Response({"error": "Invalid time format. Use HH:MM or HH:MMam/pm"}, 
                                   status=status.HTTP_400_BAD_REQUEST)
        else:
            inspection_time = time_str
            
        # Create the flag
        flag = Flag.objects.create(
            operator=operator,
            fabric_defect=defect,
            inspector=inspector,
            supervisor=supervisor,
            flag_type=request.data.get('flag_type'),
            issue_type=request.data.get('issue_type'),
            custom_reason=request.data.get('custom_reason'),
            machine_no=request.data.get('machine_no'),
            date_of_inspection=inspection_date,
            time_of_inspection=inspection_time
        )
        
        # Create notification for the supervisor
        notification_title = f"New {flag.flag_type} Flag"
        notification_message = f"Operator {operator.operator_id} has been flagged for {defect.defect_type} on machine {flag.machine_no}."
        
        Notification.objects.create(
            recipient=supervisor,
            notification_type='FLAG',
            title=notification_title,
            message=notification_message,
            related_flag=flag
        )
        
        return Response({
            'message': 'Flag created successfully',
            'flag_id': flag.id,
            'flag_type': flag.flag_type
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        import traceback
        return Response({
            'error': str(e),
            'traceback': traceback.format_exc()
        }, status=status.HTTP_400_BAD_REQUEST)

# Get all flags (with filtering options)
class FlagListView(generics.ListAPIView):
    serializer_class = DetailedFlagSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Flag.objects.all().order_by('-created_at')
        
        # Filter options
        operator_id = self.request.query_params.get('operator_id')
        flag_type = self.request.query_params.get('flag_type')
        issue_type = self.request.query_params.get('issue_type')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if operator_id:
            queryset = queryset.filter(operator__operator_id=operator_id)
        if flag_type:
            queryset = queryset.filter(flag_type=flag_type)
        if issue_type:
            queryset = queryset.filter(issue_type=issue_type)
        if start_date:
            queryset = queryset.filter(date_of_inspection__gte=start_date)
        if end_date:
            queryset = queryset.filter(date_of_inspection__lte=end_date)
            
        return queryset

# Flag statistics
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_flag_statistics(request):
    """
    Get statistics about operator flags
    """
    try:
        # Get date range parameters (default to last 30 days)
        end_date = timezone.now().date()
        start_date = end_date - datetime.timedelta(days=30)
        
        if 'start_date' in request.query_params:
            start_date = datetime.datetime.strptime(request.query_params['start_date'], '%Y-%m-%d').date()
        if 'end_date' in request.query_params:
            end_date = datetime.datetime.strptime(request.query_params['end_date'], '%Y-%m-%d').date()
        
        # Get flags in date range
        flags = Flag.objects.filter(date_of_inspection__gte=start_date, date_of_inspection__lte=end_date)
        
        # Calculate statistics
        total_flags = flags.count()
        red_flags = flags.filter(flag_type='RED').count()
        green_flags = flags.filter(flag_type='GREEN').count()
        
        # Get flags by issue type
        issue_type_counts = {}
        for issue_choice in Flag.ISSUE_TYPES:
            issue_code = issue_choice[0]
            issue_type_counts[issue_code] = flags.filter(issue_type=issue_code).count()
        
        # Top operators with most flags
        from django.db.models import Count
        top_operators = (flags.values('operator__operator_id', 'operator__name')
                          .annotate(flag_count=Count('id'))
                          .order_by('-flag_count')[:5])
        
        return Response({
            'total_flags': total_flags,
            'red_flags': red_flags,
            'green_flags': green_flags,
            'issue_type_counts': issue_type_counts,
            'top_operators': list(top_operators),
            'date_range': {
                'start_date': start_date,
                'end_date': end_date
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

# User Registration View
class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'User registered successfully',
                'user': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Add this to your views.py
@csrf_exempt
def direct_create_operator(request):
    """Simple direct function for operator creation"""
    if request.method == 'POST':
        import json
        try:
            data = json.loads(request.body)
            operator_id = data.get('operator_id')
            if not operator_id:
                return JsonResponse({"error": "Operator ID is required"}, status=400)
                
            operator, created = Operator.objects.get_or_create(
                operator_id=operator_id,
                defaults={
                    'name': data.get('name', ''),
                    'machine_no': data.get('machine_no', '')
                }
            )
            
            # Update existing operator if found
            if not created:
                if 'name' in data:
                    operator.name = data['name']
                if 'machine_no' in data:
                    operator.machine_no = data['machine_no']
                operator.save()
                
            return JsonResponse({
                'message': f"Operator {'created' if created else 'updated'} successfully",
                'operator_id': operator.operator_id,
                'created': created
            }, status=201 if created else 200)
            
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Use POST method"}, status=405)

@api_view(['POST'])
@csrf_exempt
def raw_operator_create(request):
    """Emergency operator creation endpoint"""
    try:
        operator_id = request.data.get('operator_id')
        name = request.data.get('name', '')
        machine_no = request.data.get('machine_no', '')
        
        if not operator_id:
            return Response({"error": "Operator ID is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        operator, created = Operator.objects.get_or_create(
            operator_id=operator_id,
            defaults={
                'name': name,
                'machine_no': machine_no
            }
        )
        
        # Update existing operator if found
        if not created:
            operator.name = name
            operator.machine_no = machine_no
            operator.save()
            
        return Response({
            'message': f"Operator {'created' if created else 'updated'} successfully",
            'operator_id': operator.operator_id,
            'created': created
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Search for operators by ID or name
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_operators(request):
    """Search for operators by ID or name"""
    query = request.query_params.get('q', '')
    
    if not query:
        return Response([], status=status.HTTP_200_OK)
    
    operators = Operator.objects.filter(
        models.Q(operator_id__icontains=query) | 
        models.Q(name__icontains=query)
    )[:10]  # Limit to 10 results
    
    serializer = OperatorSerializer(operators, many=True)
    return Response(serializer.data)

# Get issue types
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_issue_types(request):
    """Get all available issue types for flagging"""
    issue_types = [
        {'code': choice[0], 'name': choice[1]} 
        for choice in Flag.ISSUE_TYPES
    ]
    return Response(issue_types)

# Get inspector dashboard
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_inspector_dashboard(request):
    """Get dashboard statistics for a CLI Inspector"""
    try:
        # Get parameters
        inspector_id = request.query_params.get('inspector_id')
        date_str = request.query_params.get('date', timezone.now().date().isoformat())
        
        if not inspector_id:
            return Response({"error": "Inspector ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Parse date
        if isinstance(date_str, str):
            try:
                date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, 
                              status=status.HTTP_400_BAD_REQUEST)
        else:
            date = date_str
        
        # Find the inspector
        try:
            inspector = CLIInspector.objects.get(id=inspector_id)
        except CLIInspector.DoesNotExist:
            return Response({"error": "Inspector not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Get inspections done by this inspector on the specified date
        inspections = Inspection.objects.filter(
            cli_inspector=inspector,
            inspection_date__date=date
        )
        total_inspections = inspections.count()
        
        # Get flags raised by this inspector on the specified date
        flags = Flag.objects.filter(
            inspector=inspector,
            date_of_inspection=date
        )
        total_flags = flags.count()
        
        # Calculate defect percentage
        if total_inspections > 0:
            # Count inspections with defects
            inspections_with_defects = inspections.exclude(fabric_defect=None).count()
            defect_percentage = (inspections_with_defects / total_inspections) * 100
        else:
            defect_percentage = 0
            
        # Get flag breakdown by type
        red_flags = flags.filter(flag_type='RED').count()
        green_flags = flags.filter(flag_type='GREEN').count()
        
        # Return dashboard data
        return Response({
            'total_inspections': total_inspections,
            'total_flags': total_flags,
            'defect_percentage': round(defect_percentage, 1),
            'red_flags': red_flags,
            'green_flags': green_flags,
            'inspector': {
                'id': inspector.id,
                'name': inspector.name
            },
            'date': date.isoformat()
        }, status=status.HTTP_200_OK)
            
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Get supervisor dashboard
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_supervisor_dashboard(request):
    """Get dashboard statistics for a Supervisor"""
    try:
        # Get parameters
        supervisor_id = request.query_params.get('supervisor_id')
        date_str = request.query_params.get('date', timezone.now().date().isoformat())
        
        if not supervisor_id:
            return Response({"error": "Supervisor ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Parse date
        if isinstance(date_str, str):
            try:
                date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, 
                              status=status.HTTP_400_BAD_REQUEST)
        else:
            date = date_str
        
        # Find the supervisor
        try:
            supervisor = Supervisor.objects.get(id=supervisor_id)
        except Supervisor.DoesNotExist:
            return Response({"error": "Supervisor not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Get inspections supervised by this supervisor on the specified date
        inspections = Inspection.objects.filter(
            supervisor=supervisor,
            inspection_date__date=date
        )
        total_inspections = inspections.count()
        
        # Get flags associated with this supervisor on the specified date
        flags = Flag.objects.filter(
            supervisor=supervisor,
            date_of_inspection=date
        )
        total_flags = flags.count()
        
        # Calculate inspection statuses
        pending_inspections = inspections.filter(status='Pending').count()
        reviewed_inspections = inspections.filter(status='Reviewed').count()
        resolved_inspections = inspections.filter(status='Resolved').count()
        
        # Get flag breakdown by type
        red_flags = flags.filter(flag_type='RED').count()
        green_flags = flags.filter(flag_type='GREEN').count()
        
        # Get team performance - find all inspectors who worked with this supervisor
        team_inspectors = CLIInspector.objects.filter(
            inspection__supervisor=supervisor,
            inspection__inspection_date__date=date
        ).distinct()
        
        inspector_stats = []
        for inspector in team_inspectors:
            inspector_inspections = Inspection.objects.filter(
                cli_inspector=inspector,
                supervisor=supervisor,
                inspection_date__date=date
            )
            
            inspector_flags = Flag.objects.filter(
                inspector=inspector,
                supervisor=supervisor,
                date_of_inspection=date
            )
            
            inspector_stats.append({
                'inspector_id': inspector.id,
                'inspector_name': inspector.name,
                'inspections_count': inspector_inspections.count(),
                'flags_count': inspector_flags.count()
            })
        
        # Return dashboard data
        return Response({
            'total_inspections': total_inspections,
            'total_flags': total_flags,
            'inspection_status': {
                'pending': pending_inspections,
                'reviewed': reviewed_inspections,
                'resolved': resolved_inspections
            },
            'flags': {
                'red_flags': red_flags,
                'green_flags': green_flags
            },
            'team_performance': inspector_stats,
            'supervisor': {
                'id': supervisor.id,
                'name': supervisor.name,
                'department': supervisor.department
            },
            'date': date.isoformat()
        }, status=status.HTTP_200_OK)
            
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Notification Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notifications(request):
    """Get notifications for a supervisor"""
    try:
        supervisor_id = request.query_params.get('supervisor_id')
        
        if not supervisor_id:
            return Response({"error": "Supervisor ID is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            supervisor = Supervisor.objects.get(id=supervisor_id)
        except Supervisor.DoesNotExist:
            return Response({"error": "Supervisor not found"}, status=status.HTTP_404_NOT_FOUND)
            
        # Get unread count
        unread_count = Notification.objects.filter(recipient=supervisor, is_read=False).count()
        
        # Get paginated notifications
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        
        notifications = Notification.objects.filter(recipient=supervisor)
        total_count = notifications.count()
        
        notifications = notifications[start_index:end_index]
        serializer = NotificationSerializer(notifications, many=True)
        
        return Response({
            'notifications': serializer.data,
            'unread_count': unread_count,
            'total_count': total_count,
            'page': page,
            'page_size': page_size,
            'total_pages': (total_count + page_size - 1) // page_size
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notification_detail(request, notification_id):
    """Get detailed information about a notification"""
    try:
        notification = Notification.objects.get(id=notification_id)
        serializer = NotificationDetailSerializer(notification)
        return Response(serializer.data)
    except Notification.DoesNotExist:
        return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_notification_read(request, notification_id):
    """Mark a notification as read"""
    try:
        notification = Notification.objects.get(id=notification_id)
        notification.is_read = True
        notification.save()
        return Response({"message": "Notification marked as read"})
    except Notification.DoesNotExist:
        return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_all_notifications_read(request):
    """Mark all notifications for a supervisor as read"""
    try:
        supervisor_id = request.data.get('supervisor_id')
        
        if not supervisor_id:
            return Response({"error": "Supervisor ID is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        Notification.objects.filter(recipient_id=supervisor_id, is_read=False).update(is_read=True)
        
        return Response({"message": "All notifications marked as read"})
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_role(request):
    """
    Get the role of the authenticated user.
    Returns the role type and user details.
    """
    try:
        user = request.user
        user_data = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email
        }
        
        # Check if user is a CLI Inspector
        cli_inspectors = CLIInspector.objects.filter(email=user.email)
        if cli_inspectors.exists():
            inspector = cli_inspectors.first()
            return Response({
                'role': 'inspector',
                'user': user_data,
                'details': CLIInspectorSerializer(inspector).data
            })
            
        # Check if user is a Supervisor
        supervisors = Supervisor.objects.filter(email=user.email)
        if supervisors.exists():
            supervisor = supervisors.first()
            return Response({
                'role': 'supervisor',
                'user': user_data,
                'details': SupervisorSerializer(supervisor).data
            })
        
        # User exists but doesn't have a specific role
        return Response({
            'role': 'undefined',
            'user': user_data,
            'message': 'User exists but is not assigned to a role.'
        })
        
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assign_user_role(request):
    """
    Assign a role to the authenticated user.
    Required parameters:
    - role_type: 'inspector' or 'supervisor'
    - name: Full name of the user
    - phone: Phone number
    - department: (only for supervisor role)
    """
    try:
        user = request.user
        role_type = request.data.get('role_type')
        name = request.data.get('name')
        phone = request.data.get('phone')
        
        if not role_type or not name:
            return Response({
                'error': 'Required fields missing: role_type and name are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user already has a role
        existing_inspector = CLIInspector.objects.filter(email=user.email).first()
        existing_supervisor = Supervisor.objects.filter(email=user.email).first()
        
        if existing_inspector or existing_supervisor:
            return Response({
                'error': 'User already has an assigned role',
                'current_role': 'inspector' if existing_inspector else 'supervisor'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Assign the requested role
        if role_type.lower() == 'inspector':
            inspector = CLIInspector.objects.create(
                name=name,
                email=user.email,
                phone=phone
            )
            return Response({
                'message': 'User assigned as CLI Inspector successfully',
                'role': 'inspector',
                'details': CLIInspectorSerializer(inspector).data
            }, status=status.HTTP_201_CREATED)
            
        elif role_type.lower() == 'supervisor':
            department = request.data.get('department')
            if not department:
                return Response({
                    'error': 'Department is required for supervisor role'
                }, status=status.HTTP_400_BAD_REQUEST)
                
            supervisor = Supervisor.objects.create(
                name=name,
                email=user.email,
                phone=phone,
                department=department
            )
            return Response({
                'message': 'User assigned as Supervisor successfully',
                'role': 'supervisor',
                'details': SupervisorSerializer(supervisor).data
            }, status=status.HTTP_201_CREATED)
            
        else:
            return Response({
                'error': 'Invalid role type. Must be "inspector" or "supervisor"'
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsInspector])
def inspector_defect_summary(request):
    """
    Get a summary of fabric defects found by the authenticated CLI Inspector.
    Only accessible to users with the CLI Inspector role.
    """
    try:
        # Get the CLI Inspector profile for the authenticated user
        inspector = CLIInspector.objects.get(email=request.user.email)
        
        # Get inspections performed by this inspector
        inspections = inspector.inspection_set.all()
        
        # Calculate defect statistics
        total_inspections = inspections.count()
        defects_found = 0
        defect_type_counts = {}
        
        for inspection in inspections:
            if hasattr(inspection, 'fabric_defect') and inspection.fabric_defect:
                defects_found += 1
                
                # Count by defect type
                defect_type = inspection.fabric_defect.defect_type
                if defect_type in defect_type_counts:
                    defect_type_counts[defect_type] += 1
                else:
                    defect_type_counts[defect_type] = 1
        
        # Get recent defects (last 10)
        recent_defect_ids = [
            insp.fabric_defect.id for insp in inspections 
            if hasattr(insp, 'fabric_defect') and insp.fabric_defect
        ][:10]
        recent_defects = FabricDefect.objects.filter(id__in=recent_defect_ids)
        
        # Calculate defect ratio
        defect_ratio = 0
        if total_inspections > 0:
            defect_ratio = (defects_found / total_inspections) * 100
        
        return Response({
            'inspector_name': inspector.name,
            'total_inspections': total_inspections,
            'defects_found': defects_found,
            'defect_ratio': round(defect_ratio, 2),
            'defect_types': [
                {'type': defect_type, 'count': count}
                for defect_type, count in defect_type_counts.items()
            ],
            'recent_defects': [
                {
                    'id': defect.id,
                    'type': defect.defect_type,
                    'severity': defect.severity,
                    'date': defect.detected_at.strftime('%Y-%m-%d %H:%M')
                }
                for defect in recent_defects
            ]
        })
        
    except CLIInspector.DoesNotExist:
        return Response({
            'error': 'You are not registered as a CLI Inspector'
        }, status=status.HTTP_403_FORBIDDEN)
        
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([IsSupervisor])
def supervisor_team_overview(request):
    """
    Get a overview of the supervisor's team performance.
    Only accessible to users with the Supervisor role.
    """
    try:
        # Get the Supervisor profile for the authenticated user
        supervisor = Supervisor.objects.get(email=request.user.email)
        
        # Get date range (default to last 7 days)
        end_date = timezone.now().date()
        days = int(request.query_params.get('days', '7'))
        start_date = end_date - datetime.timedelta(days=days)
        
        # Get inspections supervised by this supervisor in date range
        inspections = Inspection.objects.filter(
            supervisor=supervisor,
            inspection_date__date__gte=start_date,
            inspection_date__date__lte=end_date
        )
        
        # Get flags associated with this supervisor in date range
        flags = Flag.objects.filter(
            supervisor=supervisor,
            date_of_inspection__gte=start_date,
            date_of_inspection__lte=end_date
        )
        
        # Get team members (inspectors) who worked with this supervisor
        inspectors = CLIInspector.objects.filter(
            inspection__supervisor=supervisor,
            inspection__inspection_date__date__gte=start_date,
            inspection__inspection_date__date__lte=end_date
        ).distinct()
        
        # Calculate team statistics
        inspector_stats = []
        for inspector in inspectors:
            inspector_inspections = inspections.filter(cli_inspector=inspector)
            inspector_flags = flags.filter(inspector=inspector)
            
            # Calculate inspection efficiency
            total_insp = inspector_inspections.count()
            resolved_insp = inspector_inspections.filter(status='Resolved').count()
            efficiency = 0
            if total_insp > 0:
                efficiency = (resolved_insp / total_insp) * 100
            
            inspector_stats.append({
                'inspector_id': inspector.id,
                'inspector_name': inspector.name,
                'total_inspections': total_insp,
                'resolved_inspections': resolved_insp,
                'efficiency': round(efficiency, 2),
                'red_flags': inspector_flags.filter(flag_type='RED').count(),
                'green_flags': inspector_flags.filter(flag_type='GREEN').count(),
            })
        
        # Calculate overall statistics
        total_inspections = inspections.count()
        pending_inspections = inspections.filter(status='Pending').count()
        reviewed_inspections = inspections.filter(status='Reviewed').count()
        resolved_inspections = inspections.filter(status='Resolved').count()
        
        # Get flags by day (for trend analysis)
        flags_by_day = {}
        for i in range(days):
            day = start_date + datetime.timedelta(days=i)
            day_flags = flags.filter(date_of_inspection=day)
            flags_by_day[day.isoformat()] = {
                'total': day_flags.count(),
                'red': day_flags.filter(flag_type='RED').count(),
                'green': day_flags.filter(flag_type='GREEN').count()
            }
        
        return Response({
            'supervisor': {
                'id': supervisor.id,
                'name': supervisor.name,
                'department': supervisor.department
            },
            'date_range': {
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat(),
                'days': days
            },
            'overall_statistics': {
                'total_inspections': total_inspections,
                'pending_inspections': pending_inspections,
                'reviewed_inspections': reviewed_inspections,
                'resolved_inspections': resolved_inspections,
                'completion_rate': round(resolved_inspections / total_inspections * 100, 2) if total_inspections > 0 else 0,
                'total_flags': flags.count(),
                'red_flags': flags.filter(flag_type='RED').count(),
                'green_flags': flags.filter(flag_type='GREEN').count()
            },
            'team_performance': sorted(inspector_stats, key=lambda x: x['total_inspections'], reverse=True),
            'flags_trend': flags_by_day
        })
        
    except Supervisor.DoesNotExist:
        return Response({
            'error': 'You are not registered as a Supervisor'
        }, status=status.HTTP_403_FORBIDDEN)
        
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
logger = logging.getLogger('inspection')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def enhance_fabric_image(request):
    """
    Enhance a fabric image for better defect detection.
    """
    try:
        # Check if image is provided
        if 'image' not in request.FILES:
            return Response({
                "error": "No image provided. Please upload an image to enhance."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        image_file = request.FILES['image']
        
        # Save the uploaded image to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
            input_path = tmp_file.name
            for chunk in image_file.chunks():
                tmp_file.write(chunk)
        
        # Set enhancement method from request or default to "all"
        method = request.data.get('method', 'all')
        
        # Apply enhancement
        enhanced_path = enhance_for_defect_detection(input_path, method=method)
        
        if not enhanced_path:
            return Response({
                "error": "Failed to enhance the image."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Return the image as a response (or save to storage)
        with open(enhanced_path, 'rb') as f:
            enhanced_image = f.read()
            
        # Clean up temporary files
        try:
            os.unlink(input_path)
            os.unlink(enhanced_path)
        except Exception:
            pass
            
        return HttpResponse(
            enhanced_image, 
            content_type='image/jpeg'
        )
        
    except Exception as e:
        return Response({
            "error": f"An error occurred: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([AllowAny])       # you can tighten this later
@parser_classes([JSONParser])         # so request.data works on DELETE
def delete_my_account(request):
    """
    Delete your own account.  Supply JSON body:
      { "username": "yourname", "password": "secret" }
    """
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response(
            {"error": "Provide both username and password."},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(username=username, password=password)
    if user is None:
        return Response(
            {"error": "Invalid credentials."},
            status=status.HTTP_401_UNAUTHORIZED
        )

    user.delete()
    return Response(
        {"message": f"User '{username}' has been deleted."},
        status=status.HTTP_204_NO_CONTENT
    )