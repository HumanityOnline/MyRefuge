# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.network "forwarded_port", guest: 8000, host: 8001
  config.ssh.forward_agent = true
  config.ssh.forward_x11 = true

  config.vm.provision "ansible" do |ansible|
    ansible.extra_vars = {
      remote_user: 'vagrant',
    }
    ansible.sudo = true
    # ansible.tags = %w(foo) # to limit what tasks we run
    ansible.verbose = 'vv'
    ansible.playbook = 'ansible/dev.yml'
  end
end
