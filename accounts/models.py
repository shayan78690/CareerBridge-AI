from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('employer', 'Employer'),
        ('job_seeker', 'Job Seeker'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    company_description = models.TextField(blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    experience = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} Profile"