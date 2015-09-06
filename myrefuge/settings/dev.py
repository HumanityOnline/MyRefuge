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
)

EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'changethisinproduction'
