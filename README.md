# How-to get going

Make sure you're on a NIX machine. I have no idea how windows works, so try at your own peril.

`git clone` this repo, and `cd` into it.

If you don't have Bower installed, please check [bower.io](http://bower.io/) on how to install.

Make sure you've installed postgres and postgis. On Ubuntu:

```
sudo apt-get -y install postgresql postgresql-client postgresql-contrib
sudo apt-get install -y postgis postgresql-9.3-postgis-2.1 postgresql-server-dev-9.3
```

```
pip install fabric
fab install
```

This will ask you to define a password, type in `myrefuge` twice.
The next steps will fail with horrible error messages.
This appears to be a rather nasty postgres related bug in Django.

The first time errors happen, run:

`./manage.py migrate auth`.

That will fail. Now run:

```
./manage.py migrate sites
./manage.py migrate address
./manage.py migrate
```

Finally, import the cities with:

`./manage.py cities --import=all`

This will take a while, but dev work can still happen.

To run the server:

`./manage.py runserver`

Visit the URL that pops up.

Happy devving!
