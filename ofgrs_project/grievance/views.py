from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from .models import Grievance
from .serializers import UserSerializer, GrievanceSerializer

# 1. User Registration View
class RegisterView(generics.CreateAPIView):
    """
    Endpoint for user registration.
    In a real system, you would add logic here to verify the student ID against a college database.
    """
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

# 2. Grievance Submission and Viewing (for Admins)
class GrievanceListCreateView(generics.ListCreateAPIView):
    """
    Endpoint for:
    - Authenticated users to submit a grievance (POST).
    - Admins to view all grievances (GET).
    """
    queryset = Grievance.objects.all().order_by('-created_at')
    serializer_class = GrievanceSerializer

    def get_permissions(self):
        """Set permissions based on request method."""
        if self.request.method == 'POST':
            # Any authenticated user can create a grievance.
            return [permissions.IsAuthenticated()]
        # Only admins can view the full list.
        return [permissions.IsAdminUser()]

    def perform_create(self, serializer):
        """
        Handle anonymous vs. non-anonymous submission.
        This is the core logic for your assigned role.
        """
        # The frontend will send 'isAnonymous: true' in the request body.
        is_anonymous = self.request.data.get('isAnonymous', False)
        
        if is_anonymous:
            # If anonymous, save the grievance without linking the user.
            serializer.save(user=None)
        else:
            # If not anonymous, link the grievance to the currently authenticated user.
            serializer.save(user=self.request.user)

# 3. View My Submitted Grievances
class MyGrievancesListView(generics.ListAPIView):
    """
    Endpoint for a user to see only their own non-anonymous submissions.
    """
    serializer_class = GrievanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """This view should return a list of all grievances for the currently authenticated user."""
        user = self.request.user
        return Grievance.objects.filter(user=user).order_by('-created_at')

