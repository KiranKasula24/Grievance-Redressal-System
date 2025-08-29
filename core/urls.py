# Inside core/urls.py
from django.contrib import admin
# Add 'include' to the import line
from django.urls import path, include 

urlpatterns = [
    path('admin/', admin.site.urls),
    # Add this new line below the admin path.
    # It tells Django that any URL starting with 'api/' should be
    # handled by the urls.py file inside our 'api' app.
    path('api/', include('api.urls')),
]