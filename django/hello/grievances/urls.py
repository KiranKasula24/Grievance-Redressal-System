from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    dashboard_redirect_view,
    HODDashboardView,
    AESDashboardView,
    ManagementDashboardView,
)

urlpatterns = [
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', dashboard_redirect_view, name='dashboard_redirect'),
    path('dashboard/hod/', HODDashboardView.as_view(), name='hod_dashboard'),
    path('dashboard/aes/', AESDashboardView.as_view(), name='aes_dashboard'),
    path('dashboard/management/', ManagementDashboardView.as_view(), name='management_dashboard'),
]