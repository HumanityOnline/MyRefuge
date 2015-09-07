import os, uuid, pdb
from django.conf import settings
from django.utils.deconstruct import deconstructible

GENDER = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('U', 'Prefer not to say')
)

APPLICATION_STATUS = (
    ('P', 'Pending'),
    ('D', 'Denied'),
    ('A', 'Accepted'),
)

CITIZEN_REFUGE_ADDITIONAL = (
    (1, 'provide free food'),
    (2, 'share advice about the city and its services'),
    (3, 'hang out with the refugees'),
)

PROFILE_TYPES = (
    ('C', 'Citizen refuge'),
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
        return os.path.join(settings.MEDIA_ROOT, self.path, filename)
