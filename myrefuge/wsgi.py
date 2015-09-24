"""
WSGI config for myrefuge project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from rednoise import DjangoRedNoise

# Fix django closing connection to MemCachier after every request (#11331)
# https://devcenter.heroku.com/articles/django-memcache#optimize-performance
from django.core.cache.backends.memcached import BaseMemcachedCache
BaseMemcachedCache.close = lambda self, **kwargs: None

application = get_wsgi_application()
application = DjangoRedNoise(application)
