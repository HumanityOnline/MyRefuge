from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    if type(dictionary) is tuple:
        dictionary = dict(dictionary)
    return dictionary.get(key)

