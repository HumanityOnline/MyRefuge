from django import template
from django.conf import settings

register = template.Library()

@register.filter
def get_item(dictionary, key):
    if type(dictionary) is tuple:
        dictionary = dict(dictionary)
    return dictionary.get(key)


@register.filter
def media(path):
    """convert /absolute/mediafiles/abc/xyz.jpg to MEDIA_PATH/abc/xyz.jpg"""
    to_find = settings.MEDIA_ROOT.split('/')[-1]  # 'mediafiles'
    start = path.find(to_find)
    return '{media_url}{location}'.format(media_url=settings.MEDIA_URL,
                                          location=path[(start + len(to_find) + 1):])
