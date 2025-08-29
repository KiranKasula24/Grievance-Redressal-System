# Inside api/views.py
import random
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Grievance
from .serializers import GrievanceTrackSerializer, GrievanceCreateSerializer 

class GrievanceTrackView(APIView):
    """
    This View handles requests to track a specific grievance.
    """
    def get(self, request, tracking_id, *args, **kwargs):
        # This 'try...except' block is for error handling.
        try:
            # This is the database query: find a Grievance with this tracking_id.
            grievance = Grievance.objects.get(tracking_id=tracking_id)
            # We pass the found grievance object to our serializer.
            serializer = GrievanceTrackSerializer(grievance)
            # The serializer converts it to JSON, and we return it in a Response.
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Grievance.DoesNotExist:
            # If no grievance is found, we return a "Not Found" error.
            return Response({'error': 'Grievance not found.'}, status=status.HTTP_404_NOT_FOUND)




class SendOTPView(APIView):
    """
    This View handles the first step: Verifying a user's email.
    It receives an email, generates an OTP, and stores it temporarily.
    """
    def post(self, request, *args, **kwargs):
        # Get the email from the incoming request data.
        email = request.data.get('email')

        # IMPORTANT: Check if the email belongs to your organization's domain.
        if not email or not email.endswith('@yourcollege.edu'): # <-- CHANGE THIS DOMAIN!
            return Response(
                {'error': 'A valid college email address is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Generate a random 6-digit OTP.
        otp = str(random.randint(100000, 999999))

        # For a hackathon, we use Django's cache to store the OTP for 5 minutes.
        # The email is the key, and the OTP is the value.
        cache.set(email, otp, timeout=300)

        # In a real app, you would email the OTP. For now, we'll just print it
        # to the terminal where your server is running. This is for easy testing.
        print(f"--- OTP for {email} is: {otp} (This would be emailed in production) ---")

        return Response(
            {'message': 'OTP generated successfully. Please check your terminal for the code.'},
            status=status.HTTP_200_OK
        )


# --- ADD THIS NEW CLASS AT THE BOTTOM OF api/views.py ---
class GrievanceSubmitView(APIView):
    """
    This is the final step of the submission.
    It receives the grievance details + the OTP, verifies, and saves.
    """
    def post(self, request, *args, **kwargs):
        # Get all the data from the request
        email = request.data.get('email')
        otp = request.data.get('otp')

        # 1. Verify the OTP
        cached_otp = cache.get(email)
        if not cached_otp or cached_otp != otp:
            return Response({'error': 'Invalid or expired OTP.'}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Validate the grievance data using our new serializer
        serializer = GrievanceCreateSerializer(data=request.data)
        if serializer.is_valid():
            # 3. If data is valid, save it to the database.
            # The model's save() method will create the tracking_id automatically.
            grievance = serializer.save()

            # 4. Clean up: Delete the OTP so it can't be used again.
            cache.delete(email)

            # 5. Return a success message with the new tracking_id!
            return Response(
                {'message': 'Grievance submitted successfully.', 'tracking_id': grievance.tracking_id},
                status=status.HTTP_201_CREATED
            )

        # If the data is not valid (e.g., bad category), return an error.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)