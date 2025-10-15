import os
import django
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_portal.settings')
django.setup()

def setup_project():
    # Create migrations
    execute_from_command_line(['manage.py', 'makemigrations'])
    
    # Apply migrations
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Create superuser (optional)
    print("Project setup completed!")
    print("Run 'python manage.py runserver' to start the development server.")

if __name__ == '__main__':
    setup_project()