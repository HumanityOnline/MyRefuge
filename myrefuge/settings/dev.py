import os
from .common import *

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

INSTALLED_APPS += (
    'django_extensions',
    'django_pdb',
)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'changethisinproduction'

MIDDLEWARE_CLASSES += (
    'django_pdb.middleware.PdbMiddleware',
)

MEDIA_PATH = os.path.join(BASE_DIR, 'media')
USERENA_MUGSHOT_PATH = os.path.join(MEDIA_PATH, 'mugshots/')
