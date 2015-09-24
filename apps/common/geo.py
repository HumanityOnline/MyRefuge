from django.conf import settings
from django.core.cache import cache
from geopy.geocoders import get_geocoder_for_service

# use google by default
_geocoder_service = get_geocoder_for_service(getattr(settings, 'GEO_SERVICE', 'google'))
# a dictionary of key, value for kwargs
_geocoder_settings = getattr(settings, 'GEO_SETTINGS', {})

geocoder = _geocoder_service(**_geocoder_settings)


def address_to_location(address):
    """convert a raw address to location"""
    address = address.encode('utf-8')

    location = cache.get(address)

    if location is None:
        location = geocoder.geocode(address)
        cache.set(address, location)

    return location


def location_to_latlon(location):
    """find latitude, longitude from provided location"""
    return location[1]


def location_to_city(location):
    """find city name from location"""
    # TODO(hoatle): currently support google only, add more support
    address_components = location.raw['address_components']
    for component in address_components:
        if u'administrative_area_level_1' in component['types']:
            return component['long_name']
    return None


def location_to_country(location):
    """find county name from location"""
    # TODO(hoatle): currently support google only, add more support
    address_components = location.raw['address_components']
    for component in address_components:
        if u'country' in component['types']:
            return component['long_name']
    return None
