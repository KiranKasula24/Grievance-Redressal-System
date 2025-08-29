# Inside api/serializers.py
from rest_framework import serializers
from .models import Grievance

class GrievanceTrackSerializer(serializers.ModelSerializer):
    """
    This serializer is for public tracking. 
    It only shows fields that are safe for the public to see.
    """
    class Meta:
        model = Grievance
        # This 'fields' list is a whitelist. ONLY these fields will be shown.
        fields = ['tracking_id', 'category', 'status', 'created_at']

class GrievanceCreateSerializer(serializers.ModelSerializer):
    """
    This serializer is for creating a new grievance.
    It only includes the fields that a user needs to provide.
    """
    class Meta:
        model = Grievance
        # The user only needs to submit the category and description.
        fields = ['category', 'description']