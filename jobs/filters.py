import django_filters
from .models import Job

class JobFilter(django_filters.FilterSet):
    position = django_filters.CharFilter(lookup_expr='icontains')
    company_name = django_filters.CharFilter(lookup_expr='icontains')
    location = django_filters.CharFilter(lookup_expr='icontains')
    experience_required = django_filters.ChoiceFilter(choices=Job.EXPERIENCE_LEVELS)
    job_type = django_filters.ChoiceFilter(choices=Job.JOB_TYPES)
    
    class Meta:
        model = Job
        fields = ['position', 'company_name', 'location', 'experience_required', 'job_type']