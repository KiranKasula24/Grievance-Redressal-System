import uuid
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = (
        ('STUDENT', 'Student'),
        ('HOD', 'Head of Department'),
        ('AES', 'Administrative/Examination Section'),
        ('MANAGEMENT', 'Management'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    department = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

class Grievance(models.Model):
    CATEGORY_CHOICES = (
        ('ACADEMIC', 'Academic Related'),
        ('FEES_EXAM', 'Fees or Exam Related'),
        ('OTHER', 'Other Issues'),
    )
    STATUS_CHOICES = (
        ('Submitted', 'Submitted'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    )
    grievance_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tracking_id = models.CharField(max_length=15, unique=True, blank=True)
    title = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    is_anonymous = models.BooleanField(default=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submitted_grievances")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Submitted')
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_grievances")

    def save(self, *args, **kwargs):
        if not self.tracking_id:
            self.tracking_id = f"GRV-{str(self.grievance_id).split('-')[-1].upper()}"
        if not self.pk:
            try:
                if self.title == 'ACADEMIC':
                    student_dept = self.student.profile.department
                    hod = User.objects.get(profile__role='HOD', profile__department=student_dept)
                    self.assigned_to = hod
                elif self.title == 'FEES_EXAM':
                    aes_user = User.objects.filter(profile__role='AES').first()
                    self.assigned_to = aes_user
                elif self.title == 'OTHER':
                    management_user = User.objects.filter(profile__role='MANAGEMENT').first()
                    self.assigned_to = management_user
            except (User.DoesNotExist, Profile.DoesNotExist):
                self.assigned_to = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tracking_id} - {self.title}"