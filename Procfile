web: newrelic-admin run-program gunicorn myrefuge.wsgi --log-file -
worker: celery -A myrefuge worker -B -l info
