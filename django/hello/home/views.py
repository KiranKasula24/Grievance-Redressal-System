from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Grievance

from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("This is the Home Page")


def about(request):
    return HttpResponse("This is the About Page.")

def contact(request):
    return HttpResponse("This is the Contact Page.")



# HOD Dashboard View (no changes)
class HODDashboardView(LoginRequiredMixin, ListView):
    model = Grievance
    template_name = 'grievances/hod_dashboard.html'
    def get_queryset(self):
        return Grievance.objects.filter(assigned_to=self.request.user).order_by('-created_at')

# AES Dashboard View (no changes)
class AESDashboardView(LoginRequiredMixin, ListView):
    model = Grievance
    template_name = 'grievances/aes_dashboard.html'
    def get_queryset(self):
        return Grievance.objects.filter(assigned_to__profile__role='AES').order_by('-created_at')

# --- NEW Management Dashboard View ---
class ManagementDashboardView(LoginRequiredMixin, ListView):
    model = Grievance
    template_name = 'grievances/management_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Query 1: Get grievances assigned directly to Management ("Other Issues")
        context['management_grievances'] = Grievance.objects.filter(
            assigned_to__profile__role='MANAGEMENT'
        ).order_by('-created_at')
        
        # Query 2: Get all grievances assigned to HODs and AES for oversight
        context['all_other_grievances'] = Grievance.objects.exclude(
            assigned_to__profile__role='MANAGEMENT'
        ).order_by('-created_at')
        
        return context

# Redirect View (no changes)
@login_required
def dashboard_redirect_view(request):
    profile = request.user.profile
    if profile.role == 'HOD':
        return redirect('hod_dashboard')
    elif profile.role == 'AES':
        return redirect('aes_dashboard')
    elif profile.role == 'MANAGEMENT':
        return redirect('management_dashboard')
    else:
        return redirect('login')