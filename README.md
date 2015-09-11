# How-to get going

Make sure you're on a NIX machine. I have no idea how windows works, so try at your own peril.

# Requirements

- [virtualbox.org](http://virtualbox.org)
- [vagrant](https://www.vagrantup.com/)
- [ansible](http://ansible.com)
- [git](https://git-scm.com)

```
git clone [this repo]
cd [this repo]
vagrant up --provision
```

That will trundle along, do its thing for a while. When complete:

```
vagrant ssh
cd /vagrant
./manage.py runserver 0.0.0.0:8000
```

Now navigate to `http://localhost:8001` and there's the site :)

You can dev locally as the repo is mounted onto the vagrant box.
