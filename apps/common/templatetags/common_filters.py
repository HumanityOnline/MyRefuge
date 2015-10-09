from django import template
from django.conf import settings
import random
import math

register = template.Library()

@register.filter
def get_item(dictionary, key):
    if type(dictionary) is tuple:
        dictionary = dict(dictionary)
    return dictionary.get(key)

@register.filter
def mkrange(number):
    return range(1, number+1)

@register.filter
def if_none(current, expect):
    return expect if current is None else current

@register.filter
def get_list_item(list, key):
    return list[key]

@register.filter
def display(val):
    #print(dir(val))
    return val

# maybe support min_distance later?
#_min_distance = settings.RANDOM_COORDS_MIN_DISTANCE # meters
#_max_distance = settings.RANDOM_COORDS_MAX_DISTANCE
#ref: http://gis.stackexchange.com/questions/25877/how-to-generate-random-locations-nearby-my-location
def random_coords(x0, y0, max_distance=None):
    """generate random coordinates nearby a specified coordinates"""
    if max_distance is None:
        max_distance = settings.RANDOM_COORDS_MAX_DISTANCE

    u = random.random()
    v = random.random()
    r = max_distance / 111300.0
    w = r * math.sqrt(u)
    t = 2 * math.pi * v
    x = w * math.cos(t)
    y = w * math.sin(t)
    return x+x0, y+y0
