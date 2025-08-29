from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Grievance

class UserSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    class Meta:
        model = User
        # For a real app, you would use 'student_id' instead of 'username'
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Hash the password upon creation
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class GrievanceSerializer(serializers.ModelSerializer):
    """Serializer for creating and viewing grievances."""
    # This field will be used to display the user's username in read-only responses.
    user_username = serializers.CharField(source='user.username', read_only=True, default='Anonymous')

    class Meta:
        model = Grievance
        fields = ('id', 'user', 'user_username', 'category', 'subject', 'description', 'status', 'created_at')
        # The 'user' field is read-only because we set it in the view, not from user input.
        read_only_fields = ('user', 'status', 'created_at')
