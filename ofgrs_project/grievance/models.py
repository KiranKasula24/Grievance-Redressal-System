from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Grievance(models.Model):
    """
    Represents a grievance submission.
    The 'user' field is nullable to support anonymous submissions.
    """
    CATEGORY_CHOICES = [
        ('HR', 'Human Resources'),
        ('IT', 'IT Department'),
        ('Administration', 'Administration'),
        ('Facility', 'Facility & Maintenance'),
        ('Other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('New', 'New'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ]

    # The user who submitted the grievance. Can be NULL for anonymous posts.
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    
    # In a real app, you would use FileField for attachments.
    # attachment = models.FileField(upload_to='attachments/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
