from django.urls import path
from .views import RegisterView, GrievanceListCreateView, MyGrievancesListView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Authentication Endpoints
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Grievance Endpoints
    path('grievances/', GrievanceListCreateView.as_view(), name='grievance-list-create'),
    path('grievances/my/', MyGrievancesListView.as_view(), name='my-grievances'),
]
