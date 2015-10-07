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

INTERNAL_IPS = ('10.0.2.2', '127.0.0.1', '0.0.0.0')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'changethisinproduction'

MIDDLEWARE_CLASSES += (
    'django_pdb.middleware.PdbMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware'
)
