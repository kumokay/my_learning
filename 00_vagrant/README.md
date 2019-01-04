# How to use Vagrant

using vagrant 2.2.2

## Envornment setup

### install Vagrant from package (apt-get install will give you older versions)
```console
$ wget https://releases.hashicorp.com/vagrant/2.2.2/vagrant_2.2.2_x86_64.deb
$ sudo dpkg -i vagrant_2.2.2_x86_64.deb
$ vagrant -v
vagrant 2.2.2
```

To uninstall: `sudo dpkg -r vagrant`

### install VirtualBox
```console
$ wget https://download.virtualbox.org/virtualbox/6.0.0/virtualbox-6.0_6.0.0-127566~Ubuntu~xenial_amd64.deb
$ sudo dpkg -i virtualbox-6.0_6.0.0-127566~Ubuntu~xenial_amd64.deb
```

## Getting start

### create a new ubuntu vagrant box
```py
# init the project (if no Vagrantfile)
# pick a box from https://app.vagrantup.com/boxes/search
vagrant init ubuntu/trusty64

# modify the project file to configure your box.
# you can create a bootstrap.sh script to setup your box.
vim Vagrantfile

# start without UI
vagrant up

# ssh into the vm
vagrant ssh

# destroy/halt/suspend the vm
vagrant destroy
vagrant halt
vagrant suspend
```

### get ssh configuration of the box
```console
$ vagrant ssh-config
Host default
  HostName 127.0.0.1
  User vagrant
  Port 2222
  UserKnownHostsFile /dev/null
  StrictHostKeyChecking no
  PasswordAuthentication no
  IdentityFile /SOME_PATH/.vagrant/machines/default/virtualbox/private_key
  IdentitiesOnly yes
  LogLevel FATAL
```

## Use the box

### package the box
```
vagrant package --output ubuntu16_kubeadm.box
```

### add the box so vagrant can use it
```
vagrant box add --name kumokay/ubuntu16_kubeadm ubuntu16_kubeadm.box
```

### upload the box
go to https://app.vagrantup.com/ and create an account, upload your box

### use the box
```console
$ mkdir test && cd test
$ vagrant init "kumokay/ubuntu16_kubeadm" && vagrant up
$ vagrant vagrant ssh
$ vagrant destroy
```
