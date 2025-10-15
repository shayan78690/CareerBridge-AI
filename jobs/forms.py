from django import forms
from .models import Job, JobApplication

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'company_name', 'company_logo', 'position', 'experience_required',
            'job_type', 'skills_required', 'job_description', 'requirements',
            'responsibilities', 'salary', 'salary_currency', 'location'
        ]
        widgets = {
            'skills_required': forms.Textarea(attrs={'rows': 3}),
            'job_description': forms.Textarea(attrs={'rows': 5}),
            'requirements': forms.Textarea(attrs={'rows': 5}),
            'responsibilities': forms.Textarea(attrs={'rows': 5}),
        }

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['resume', 'cover_letter', 'years_of_experience', 'expected_salary']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 6}),
        }