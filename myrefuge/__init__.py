from __future__ import absolute_import

from django.conf import settings

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
# only on prod

if not settings.DEBUG:
    from .celery import app as celery_app  # noqa
