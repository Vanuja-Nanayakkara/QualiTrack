# inspection/urls.py
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views  # Make sure this import is present
from .views import (
    get_user_role,
    assign_user_role,
    # Remove or comment out functions that don't exist yet
    # inspector_defect_summary,
    # supervisor_team_overview,
)

urlpatterns = [
    # Auth URLs
    path('register/', views.UserRegistration.as_view(), name='user-register'),
    path('login/', views.UserLogin.as_view(), name='user-login'),
    path('api/user/delete/', views.delete_my_account, name='delete-my-account'),
    
    # User role endpoints
    path('api/user/role/', get_user_role, name='get_user_role'),
    path('api/user/assign-role/', assign_user_role, name='assign_user_role'),
    
    # Inspection URLs
    path('inspections/', views.InspectionListCreateView.as_view(), name='inspections'),
    path('inspections/<int:pk>/', views.InspectionDetailView.as_view(), name='inspection-detail'),
    
    # Defect URLs
    path('defects/', views.FabricDefectListCreateView.as_view(), name='defects'),
    path('defects/<int:pk>/', views.FabricDefectDetailView.as_view(), name='defect-detail'),
    path('defects/review/<int:defect_id>/', views.review_defect, name='review-defect'),
    path('defects/analyze/', views.analyze_defect_image, name='analyze-defect'),
    
    # Home URL
    path('', views.home, name='home'),
    
    # Operator Management URLs
    path('operators/direct-create/', views.direct_create_operator, name='direct-operator-create'),
    path('operators/raw-create/', views.raw_operator_create, name='raw-operator-create'),
    path('operators/<str:operator_id>/', views.OperatorDetailView.as_view(), name='operator-detail'),
    path('operators/create/', views.OperatorCreateUpdateView.as_view(), name='operator-create-update'),
    path('operators/search/', views.search_operators, name='search-operators'),
    
    # Flag Management URLs
    path('flags/', views.FlagListView.as_view(), name='flag-list'),
    path('flags/create/', views.create_flag, name='create-flag'),
    path('flags/statistics/', views.get_flag_statistics, name='flag-statistics'),
    path('flags/issue-types/', views.get_issue_types, name='flag-issue-types'),
    
    # Dashboard URLs
    path('inspectors/dashboard/', views.get_inspector_dashboard, name='inspector-dashboard'),
    path('supervisors/dashboard/', views.get_supervisor_dashboard, name='supervisor-dashboard'),
    
    # List all supervisors
    path('supervisors/list/', views.SupervisorListView.as_view(), name='supervisor-list'),
    
    # Notification Endpoints
    path('notifications/', views.get_notifications, name='get-notifications'),
    path('notifications/<int:notification_id>/', views.get_notification_detail, name='notification-detail'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark-notification-read'),
    path('notifications/read-all/', views.mark_all_notifications_read, name='mark-all-notifications-read'),
    
    # Comment out URLs for functions that don't exist yet
    # path('api/inspector/defect-summary/', inspector_defect_summary, name='inspector_defect_summary'),
    # path('api/supervisor/team-overview/', supervisor_team_overview, name='supervisor_team_overview'),
    # path('enhance-garment-image/', views.enhance_garment_image, name='enhance_garment_image'),
    # path('enhance-and-detect-defects/', views.enhance_and_detect_defects, name='enhance_and_detect_defects'),
]