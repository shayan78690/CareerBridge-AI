from django.urls import path
from . import views

urlpatterns = [
    # Job URLs
    path('', views.JobListView.as_view(), name='job-list'),
    path('create/', views.JobCreateView.as_view(), name='job-create'),
    path('<int:pk>/', views.JobDetailView.as_view(), name='job-detail'),
    path('<int:pk>/update/', views.JobUpdateView.as_view(), name='job-update'),
    path('<int:pk>/delete/', views.JobDeleteView.as_view(), name='job-delete'),
    
    # Application URLs
    path('applications/create/', views.JobApplicationCreateView.as_view(), name='application-create'),
    path('applications/employer/', views.EmployerJobApplicationsView.as_view(), name='employer-applications'),
    path('applications/my/', views.JobSeekerApplicationsView.as_view(), name='my-applications'),
    path('applications/<int:pk>/', views.ApplicationDetailView.as_view(), name='application-detail'),
    
    # Dashboard
    path('dashboard/stats/', views.employer_dashboard_stats, name='employer-dashboard-stats'),
]