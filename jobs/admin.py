from django.contrib import admin
from .models import Job, JobApplication

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('position', 'company_name', 'employer', 'location', 'experience_required', 'is_active', 'created_at')
    list_filter = ('experience_required', 'job_type', 'is_active', 'created_at')
    search_fields = ('position', 'company_name', 'location')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'job', 'status', 'applied_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('applicant__username', 'job__position', 'job__company_name')
    readonly_fields = ('applied_at', 'updated_at')