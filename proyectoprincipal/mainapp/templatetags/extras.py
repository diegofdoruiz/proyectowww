from django import template
from rolepermissions.checkers import has_permission, has_role
from django.contrib.staticfiles.templatetags.staticfiles import static

register = template.Library()

@register.simple_tag
def user_has_permission(user, permission):
    return has_permission(user, permission)

@register.simple_tag
def user_has_role(user, role):
    return has_role(user, role)

@register.simple_tag
def get_url_image(number):
    return static('images/promotion/'+number+'.jpg')