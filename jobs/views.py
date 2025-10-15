from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Job, JobApplication
from .serializers import JobSerializer, JobApplicationSerializer, JobCreateSerializer
from .filters import JobFilter

class IsEmployer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'employer'

class IsJobSeeker(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'job_seeker'

class JobListView(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = JobFilter
    
    def get_queryset(self):
        return Job.objects.filter(is_active=True).order_by('-created_at')

class JobDetailView(generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class JobCreateView(generics.CreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobCreateSerializer
    permission_classes = [IsEmployer]
    
    def perform_create(self, serializer):
        serializer.save(employer=self.request.user)

class JobUpdateView(generics.UpdateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobCreateSerializer
    permission_classes = [IsEmployer]
    
    def get_queryset(self):
        return Job.objects.filter(employer=self.request.user)

class JobDeleteView(generics.DestroyAPIView):
    queryset = Job.objects.all()
    permission_classes = [IsEmployer]
    
    def get_queryset(self):
        return Job.objects.filter(employer=self.request.user)

class JobApplicationCreateView(generics.CreateAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [IsJobSeeker]
    
    def perform_create(self, serializer):
        serializer.save(applicant=self.request.user)

class EmployerJobApplicationsView(generics.ListAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsEmployer]
    
    def get_queryset(self):
        return JobApplication.objects.filter(job__employer=self.request.user).order_by('-applied_at')

class JobSeekerApplicationsView(generics.ListAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsJobSeeker]
    
    def get_queryset(self):
        return JobApplication.objects.filter(applicant=self.request.user).order_by('-applied_at')

class ApplicationDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'employer':
            return JobApplication.objects.filter(job__employer=user)
        else:
            return JobApplication.objects.filter(applicant=user)

@api_view(['GET'])
@permission_classes([IsEmployer])
def employer_dashboard_stats(request):
    total_jobs = Job.objects.filter(employer=request.user).count()
    active_jobs = Job.objects.filter(employer=request.user, is_active=True).count()
    total_applications = JobApplication.objects.filter(job__employer=request.user).count()
    
    return Response({
        'total_jobs': total_jobs,
        'active_jobs': active_jobs,
        'total_applications': total_applications
    })