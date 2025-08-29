from django.db import models

# This model is unique to the 'home' app, so it should stay.
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name

# The Profile and Grievance models have been REMOVED from this file
# because their main versions exist in the 'grievances' app.