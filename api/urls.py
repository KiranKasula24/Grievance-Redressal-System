# Inside api/urls.py
from django.urls import path
# Import the new GrievanceSubmitView
from .views import GrievanceTrackView, SendOTPView, GrievanceSubmitView

urlpatterns = [
    path('grievances/track/<str:tracking_id>/', GrievanceTrackView.as_view(), name='track-grievance'),
    path('verify-email/', SendOTPView.as_view(), name='send-otp'),

    # --- ADD THIS NEW PATH BELOW ---
    path('grievances/submit/', GrievanceSubmitView.as_view(), name='submit-grievance'),
]