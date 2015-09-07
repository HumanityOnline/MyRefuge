import os
import dj_database_url
from .common import *

SECRET_KEY = os.environ.get('SECRET_KEY')
DATABASES = {
    'default': dj_database_url.config()
}

ALLOWED_HOSTS = ['myrefuge.herokuapp.com']

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

LOGGING = {
    'version': 1,
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers':['console'],
            'propagate': True,
            'level':'DEBUG',
        }
    },
}
