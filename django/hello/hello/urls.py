from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView # Import the RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Add this new line to handle the homepage
    # It redirects anyone visiting the root URL ('') to the '/login/' page.
    path('', RedirectView.as_view(url='login/', permanent=False), name='home'),
    
    # This line can stay, but the one above is more specific for the root URL
    path('', include('grievances.urls')), 
]