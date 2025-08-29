from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Grievance, Profile
from django.contrib.auth import logout

class HODDashboardView(LoginRequiredMixin, ListView):
    model = Grievance
    template_name = 'grievances/hod_dashboard.html'
    def get_queryset(self):
        return Grievance.objects.filter(assigned_to=self.request.user).order_by('-created_at')

class AESDashboardView(LoginRequiredMixin, ListView):
    model = Grievance
    template_name = 'grievances/aes_dashboard.html'
    def get_queryset(self):
        return Grievance.objects.filter(assigned_to__profile__role='AES').order_by('-created_at')

class ManagementDashboardView(LoginRequiredMixin, ListView):
    model = Grievance
    template_name = 'grievances/management_dashboard.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['management_grievances'] = Grievance.objects.filter(
            assigned_to__profile__role='MANAGEMENT'
        ).order_by('-created_at')
        context['all_other_grievances'] = Grievance.objects.exclude(
            assigned_to__profile__role='MANAGEMENT'
        ).order_by('-created_at')
        return context

@login_required
def dashboard_redirect_view(request):
    try:
        profile = request.user.profile
        if profile.role == 'HOD':
            return redirect('hod_dashboard')
        elif profile.role == 'AES':
            return redirect('aes_dashboard')
        elif profile.role == 'MANAGEMENT':
            return redirect('management_dashboard')
        else:
            logout(request)
            return redirect('login')
    except Profile.DoesNotExist:
        logout(request)
        return redirect('login')