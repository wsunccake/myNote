# Vagrant #


## Package ##

	# Install Virtualbox
	rhel:~ # wget http://download.virtualbox.org/virtualbox/rpm/rhel/virtualbox.repo -O /etc/yum.repo.d/virtualbox.repo
	rhel:~ # yum install VirtualBox-5.0

	# Install Vagrant
	rhel:~ # wget https://releases.hashicorp.com/vagrant/1.7.4/vagrant_1.7.4_x86_64.rpm
	rhel:~ # rpm -ivh vagrant_1.7.4_x86_64.rpm


## Usage ##

	# box uage
	rhel:~ # vagrant box list                       # list box
	rhel:~ # vagrant box add hashicorp/precise64    # add box
	rhel:~ # vagrant init hashicorp/precise64       # create Vagrantfile

	# vm usage
	rhel:~ # vagrant up [vm]                   # start vm
	rhel:~ # vagrant half [vm]                 # stop vm
	rhel:~ # vagrant status [vm]               # list vm status
	rhel:~ # vagrant ssh [vm]                  # ssh login vm
	rhel:~ # vagrant detroy [-f] [vm]          # delete vm
	rhel:~ $ vagrant global-status


## Vagrantfile ##


### default ###

	# -*- mode: ruby -*-
	# vi: set ft=ruby :                        # vi 支援語法

	Vagrant.configure(2) do |config|           # 2 指的是 version 2
		config.vm.box = "hashicorp/precise64"
		config.ssh.username = "vagrant"        # vm login account
		config.ssh.password = "vagrant"        # vm login password
	end


### multi-vm ###

	VAGRANTFILE_API_VERSION = 2
	$vm_mem = 1024
	$vm_cpu = 2

	Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

		config.vm.define "app" do |app|
			app.vm.box = "hashicorp/precise64"
			app.vm.host_name = "app"
		end

		config.vm.define :db do |db|
			db.vm.box = "hashicorp/precise64"
			db.vm.host_name = "db"
			db.vm.provider :virtualbox do |vb|
				vb.memory = $vm_mem
				vb.cpus = $vm_cpu
			end
		end
	end

ruby 語法, `$`variable 表示 global variable, `:`variable 表示 symbol


### many-vm ###

	Vagrant.configure(2) do |config|
		(1..3).each do |i|
			config.vm.define "node-#{i}" do |node|
				node.vm.box = "hashicorp/precise64"
			end
		end
	end


### network ###

	Vagrant.configure(2) do |config|           # 2 指的是 version 2
		config.vm.box = "hashicorp/precise64"

		config.vm.define "app" do |app|
			app.vm.host_name = "app"
			app.vm.network "private_network", ip: "1.2.3.4", virtualbox__intnet: true
		end

		config.vm.define :db do |db|
			db.vm.host_name = "db"
			db.vm.network :private_network, virtualbox__intnet: true
		end
	end

public_network, private_network


## Box ##

	rhel:~ # ls ~/.vagrant.d/boxes   # box 會存到此目錄下




VBox
VBoxAutostart
VBoxBalloonCtrl
VBoxHeadless
VBoxManage
VBoxSDL
VBoxTunctl
VBoxVRDP


http://www.vagrantbox.es/
vagrant box add {title} {url}
vagrant init {title}
vagrant up