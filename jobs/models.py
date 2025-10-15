from django.db import models
from django.conf import settings

class Job(models.Model):
    EXPERIENCE_LEVELS = (
        ('entry', 'Entry Level'),
        ('mid', 'Mid Level'),
        ('senior', 'Senior Level'),
        ('executive', 'Executive'),
    )
    
    JOB_TYPES = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('remote', 'Remote'),
    )
    
    employer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='jobs')
    company_name = models.CharField(max_length=255)
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    position = models.CharField(max_length=255)
    experience_required = models.CharField(max_length=20, choices=EXPERIENCE_LEVELS)
    job_type = models.CharField(max_length=20, choices=JOB_TYPES, default='full_time')
    skills_required = models.TextField()
    job_description = models.TextField()
    requirements = models.TextField()
    responsibilities = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    salary_currency = models.CharField(max_length=10, default='USD')
    location = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.position} at {self.company_name}"

class JobApplication(models.Model):
    APPLICATION_STATUS = (
        ('applied', 'Applied'),
        ('under_review', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('interview', 'Interview Scheduled'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
    )
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    resume = models.FileField(upload_to='application_resumes/')
    cover_letter = models.TextField()
    years_of_experience = models.IntegerField(default=0)
    expected_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS, default='applied')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    employer_notes = models.TextField(blank=True, null=True)  # Notes from employer
    
    class Meta:
        unique_together = ['job', 'applicant']
    
    def __str__(self):
        return f"{self.applicant.username} - {self.job.position}"