from django import template
from django.contrib import admin
from django.urls import reverse

register = template.Library()


@register.simple_tag
def link_to_edit(value):
    """
    :param value: Model object
    :return: Link of change view in admin interface
     or # if the model is not registered in the admin
    """
    try:
        admin.site._registry[value._meta.model]
        url = f'admin:{value._meta.app_label}_{value._meta.model_name}_change'
        return reverse(url, args=[value.id])
    except KeyError:
        return '#'
