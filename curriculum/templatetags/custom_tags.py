from django import template
from ..models import Staff

register = template.Library()


@register.simple_tag
def staff_detail(user):
    staff = Staff.objects.filter(user=user).first()
    role = staff.role.name
    role = role.lower()
    return role
