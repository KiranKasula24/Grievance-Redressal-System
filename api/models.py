from django.db import models
import uuid

# This class is a blueprint for our 'grievance' database table.
class Grievance(models.Model):
    STATUS_CHOICES = (
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    )
    CATEGORY_CHOICES = (
        ('hr', 'Human Resources'),
        ('it', 'IT Department'),
        ('facilities', 'Facilities'),
        ('other', 'Other'),
    )

    # We are defining the columns of our database table here.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tracking_id = models.CharField(max_length=12, unique=True, editable=False)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # This special function runs every time a grievance is saved.
    def save(self, *args, **kwargs):
        # If the tracking_id field is empty, we generate a new one.
        if not self.tracking_id:
            self.tracking_id = f"GRV-{''.join(str(uuid.uuid4()).split('-')[1:3]).upper()}"
        super().save(*args, **kwargs) # This calls the original save method.

    # This tells Django how to display a grievance if we print it.
    def __str__(self):
        return self.tracking_id