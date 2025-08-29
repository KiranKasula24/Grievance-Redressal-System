from django.contrib import admin
from .models import Profile, Grievance # Import your models

# Register your models here
admin.site.register(Profile)
admin.site.register(Grievance)