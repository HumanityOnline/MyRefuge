Heroku Staging Deployment
=========================

#install heroku toolbelt

update initial-data.json and prod.py for the right domain

# Fill heroku password here

```
$ heroku login
```
# and then:

```
$ heroku apps:create myrefuge_test
$ heroku addons:create newrelic
$ heroku addons:create memcachier:dev
$ heroku addons:create cloudamqp:lemur
```

#To use with postgresql

```
$ heroku config:set DATABASE_URL="postgres://<username>:<password>@host:5432/databasename"
```

# Settings

```
$ heroku config:set NEW_RELIC_LICENSE_KEY="xxxx" NEW_RELIC_LOG="xxxx"
```

and:

- DJANGO_SETTINGS_MODULE=myrefuge.settings.prod
- SECRET_KEY
- ADMIN_NAME
- ADMIN_EMAIL
- EMAIL_HOST_USER (gmail account)
- EMAIL_HOST_PASSWORD (gmail password)

Note: temporary use gmail for email, will support others later.

# Amazon S3 Setup

We use Amazon S3 to keep and save media files, need to set these environment variables:

- S3_BUCKET_NAME
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY

Refer to:

- https://www.caktusgroup.com/blog/2014/11/10/Using-Amazon-S3-to-store-your-Django-sites-static-and-media-files/

# Google Maps Geocoding API

- Need to set `GEO_API_KEY` for standard usage
- For premier usage, need to set `GEO_CLIENT_ID` and `GEO_SECRET_KEY`

Refer to:

- https://developers.google.com/maps/documentation/geocoding/get-api-key#key 

# Celery

- Need to set `BROKER_URL` provided from cloudamqp addons above.
- and start worker: `$ heroku ps:scale worker=1`

# Finally:

```
$ heroku config:set BUILDPACK_URL=https://github.com/ddollar/heroku-buildpack-multi.git

$ git push heroku master

$ heroku run python manage.py migrate
$ heroku run python manage.py migrate auth
$ heroku run python manage.py migrate sites
$ heroku run python manage.py migrate address
$ heroku run python manage.py migrate
$ heroku run python manage.py check_permissions
```

Note: migrate could have some errors, just ignore it and continue.
