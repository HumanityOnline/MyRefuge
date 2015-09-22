Heroku Deployment
=================

#install heroku toolbelt

update inital-data.json and prod.py for the right domain

# Fill heroku password here

```
$ heroku login
```
# and then:

```
$ heroku apps:create myrefuge_test
$ heroku addons:create newrelic
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

# Finally:

```
$ heroku config:set BUILDPACK_URL=https://github.com/ddollar/heroku-buildpack-multi.git

$ git push heroku master

$ heroku run python manage.py migrate;
$ heroku run python manage.py migrate auth;
$ heroku run python manage.py migrate sites;
$ heroku run python manage.py migrate address;
$ heroku run python manage.py migrate;
$ heroku run python manage.py check_permissions
```

Note: migrate could have some errors, just ignore it and continue.
