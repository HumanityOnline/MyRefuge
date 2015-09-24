import os
import uuid

from django.conf import settings
from django.utils.deconstruct import deconstructible

from unidecode import unidecode

GENDER = (
    ('', 'Gender'),
    ('M', 'Male'),
    ('F', 'Female'),
    ('U', 'Prefer not to say')
)

APPLICATION_STATUS = (
    ('P', 'Pending'),
    ('D', 'Denied'),
    ('A', 'Accepted'),
)

CITIZEN_SPACE_ADDITIONAL = (
    ('1', 'wifi available'),
    ('2', 'provide free food'),
    ('3', 'share advice about the city and its services'),
    ('4', 'hang out with the refugees'),
)

CITIZEN_SPACE_ADDITIONAL_SHORT = (
    ('1', 'Wifi'),
    ('2', 'Free food'),
    ('3', 'Advice'),
    ('4', 'Socialise'),
)

PROFILE_TYPES = (
    ('C', 'Refuge provider'),
    ('R', 'Refugee'),
)


@deconstructible
class UniqueMediaPath(object):
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # set filename as random string
        filename = '{}.{}'.format(uuid.uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)


def normalize_name(name):
    """
    convert to ascii lower case no white space only
    """
    return unidecode(name).lower().replace(' ', '')
