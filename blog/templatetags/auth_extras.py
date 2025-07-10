from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    """Check if user belongs to a specific group"""
    if not user.is_authenticated:
        return False
    return user.groups.filter(name=group_name).exists()

@register.filter(name='in_groups')
def in_groups(user, group_names):
    """Check if user belongs to any of the specified groups (comma-separated)"""
    if not user.is_authenticated:
        return False
    
    group_list = [name.strip() for name in group_names.split(',')]
    return user.groups.filter(name__in=group_list).exists()
