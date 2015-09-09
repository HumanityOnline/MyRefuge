# How-to get going

Make sure you're on a NIX machine. I have no idea how windows works, so try at your own peril.

`git clone` this repo, and `cd` into it.

If you don't have Bower installed, please check [bower.io](http://bower.io/) on how to install.

```
pip install fabric
fab install
```

Since this is being heavily devved and modded, I may ask you to delete the database and recreate.

```
rm myrefuge/db.sqlite3
fab install
```

To run the server:

`./manage.py runserver`

Visit the URL that pops up.

Happy devving!
