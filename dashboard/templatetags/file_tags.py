from django import template
import os

register = template.Library()

@register.filter
def endswith(value, arg):
    return value.endswith(arg)

@register.filter
def split(value, arg):
    return value.split(arg)