from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'company_name', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'phone_number', 'profile_picture', 
                      'company_name', 'company_description', 'resume', 
                      'skills', 'experience')
        }),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)