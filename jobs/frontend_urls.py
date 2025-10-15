from django.urls import path
from django.contrib.auth import views as auth_views
from . import frontend_views

urlpatterns = [
    path('', frontend_views.home, name='home'),
    path('jobs/', frontend_views.job_list, name='job_list'),
    path('jobs/<int:pk>/', frontend_views.job_detail, name='job_detail'),
    path('jobs/create/', frontend_views.job_create, name='job_create'),
    path('jobs/<int:pk>/apply/', frontend_views.job_apply, name='job_apply'),
    
    # Application Management URLs
    path('applications/<int:pk>/', frontend_views.application_detail, name='application_detail'),
    path('applications/<int:pk>/update-status/', frontend_views.update_application_status, name='update_application_status'),
    path('applications/<int:pk>/download-resume/', frontend_views.download_resume, name='download_resume'),
    path('employer/applications/', frontend_views.employer_application_list, name='employer_application_list'),
    path('employer/applications/job/<int:job_id>/', frontend_views.employer_application_list, name='employer_application_list_by_job'),
    
    path('employer/dashboard/', frontend_views.employer_dashboard, name='employer_dashboard'),
    path('my-applications/', frontend_views.my_applications, name='my_applications'),
    path('profile/', frontend_views.profile, name='profile'),
    
    # Authentication URLs
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('accounts/register/', frontend_views.register_view, name='register'),
]