from django.contrib import admin
from .models import Grievance # Import your Grievance model

# This line registers your model with the admin site.
admin.site.register(Grievance)