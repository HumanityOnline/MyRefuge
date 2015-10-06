Debugging
=========

ipdb
----

//TODO: update this section


PyCharm (IntelliJ with Python plugin installed)
-----------------------------------------------

Note: instruction on Mac but should also apply on other platforms.

It's assumed that the project is put under `/workspace/MyRefuge` path and `$ vagrant up` works.

#. Check vagrant ssh-config

```
$ cd /workspace/MyRefuge
$ vagrant ssh-config
```

- and you should see something like this:

```
Host default
  HostName 127.0.0.1
  User vagrant
  Port 2222
  UserKnownHostsFile /dev/null
  StrictHostKeyChecking no
  PasswordAuthentication no
  IdentityFile /workspace/MyRefuge/.vagrant/machines/default/virtualbox/private_key
  IdentitiesOnly yes
  LogLevel FATAL
  ForwardAgent yes
  ForwardX11 yes
```

And take note the HostName, Port, User to use later.

#. Import `MyRefuge` as a Django project

#. Set Project Interpreter (or SDK with IntelliJ) 

- PyCharm: Settings -> Project:MyRefuge -> Project Interpreter -> Add Remote  
- IntelliJ: File -> Project Structure -> Project SDK -> New Python SDK -> Add Remote

Fill in HostName, Port, User and password `vagrant`.

#. Configure Run/Debug Configuration for Django project 

- Fill in the follow information (uncheck or unfill in others):

+ Host: 0.0.0.0
+ Port: 8000
+ Working Directory: /workspace/MyRefuge (change to your actual path)
+ Path mappings: /workspace/MyRefuge (as local) -> /vagrant (as remote)

And you're done, try to click on Run or Debug to start developing.