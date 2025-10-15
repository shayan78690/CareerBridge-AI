from rest_framework import serializers
from .models import Job, JobApplication
from accounts.serializers import UserSerializer

class JobSerializer(serializers.ModelSerializer):
    employer_details = UserSerializer(source='employer', read_only=True)
    application_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ('employer', 'created_at', 'updated_at')
    
    def get_application_count(self, obj):
        return obj.applications.count()

class JobApplicationSerializer(serializers.ModelSerializer):
    job_details = JobSerializer(source='job', read_only=True)
    applicant_details = UserSerializer(source='applicant', read_only=True)
    
    class Meta:
        model = JobApplication
        fields = '__all__'
        read_only_fields = ('applicant', 'applied_at', 'updated_at')

class JobCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ('employer',)