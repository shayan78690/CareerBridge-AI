from django import template

register = template.Library()

@register.filter
def status_count(applications, status):
    """Count applications by status"""
    return applications.filter(status=status).count()