from django import template

register = template.Library()

@register.inclusion_tag('test_app/user.html')
def user_profile(user):
    context = {'user': user}
    return context