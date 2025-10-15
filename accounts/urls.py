from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('api/register/', views.api_register_view, name='api_register'),
    path('api/login/', views.login_view, name='api_login'),
    path('api/logout/', views.logout_view, name='api_logout'),
    path('api/profile/', views.UserProfileView.as_view(), name='api_profile'),
]