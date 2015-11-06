import dj_database_url
from .common import *

SECRET_KEY = os.environ.get('SECRET_KEY')
DATABASES = {
    'default': dj_database_url.config(engine='django.contrib.gis.db.backends.postgis'),
}

INSTALLED_APPS += (
    'djcelery_email',
)

EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'

ALLOWED_HOSTS = ['demo.myrefuge.terapp.com']

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


LOGGING = {
    'version': 1,
    'handlers': {
        # Include the default Django email handler for errors
        # This is what you'd get without configuring logging at all.
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': 'ERROR',
            # But the emails are plain text by default - HTML is nicer
            'include_html': True,
        },
        'console':{
            'level':'ERROR',
            'class':'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            # Again, default Django configuration to email unhandled exceptions
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True,
            }
        }
    },
}


# Email settings
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

MIGRATION_MODULES = {
    'userena': 'delete_when_userena_commits.migrations'
}

ADMINS = (
    (os.environ.get('ADMIN_NAME'), os.environ.get('ADMIN_EMAIL')),
)

#TODO(hoatle): allow multiple admins, managers
# ADMINS = ('name', 'email'), ('name', 'email')
# import re
# from ast import literal_eval as make_tuple
# admins = re.findall('\[[^\]]*\]|\([^\)]*\)|\"[^\"]*\"|\S+', os.environ.get('ADMINS'))
# for admin in admins:
#     ADMINS += make_tuple(admin)


MANAGERS = ADMINS + (
    (os.environ.get('MANAGER_NAME'), os.environ.get('MANAGER_EMAIL')),
)

# amazon S3 for storing and serving media files
AWS_STORAGE_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
MEDIA_URL = 'https://%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
# this breaks DjangoRedNoise
MEDIA_ROOT = 'media'
USERENA_MUGSHOT_PATH = '/media/mugshots/'
