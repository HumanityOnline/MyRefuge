from django import template
from django.conf import settings

register = template.Library()

@register.filter
def get_item(dictionary, key):
    if type(dictionary) is tuple:
        dictionary = dict(dictionary)
    return dictionary.get(key)


@register.filter
def mkrange(number):
    return range(1, number)

@register.filter
def if_none(current, expect):
    return expect if current is None else current
