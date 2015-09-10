import os
from .common import *

DEBUG = True
ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'myrefuge',
        'USER': 'myrefuge',
        'PASSWORD': 'myrefuge',
        'HOST': 'localhost',
    }
}

INSTALLED_APPS += (
    'django_extensions',
    'django_pdb',
    'debug_toolbar',
)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'changethisinproduction'

MIDDLEWARE_CLASSES += (
    'django_pdb.middleware.PdbMiddleware',
)

USERENA_MUGSHOT_PATH = os.path.join(MEDIA_ROOT, 'mugshots/')
