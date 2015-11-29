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

vagrant up on Virtualbox 流程:

1. 使用 vagrant 帳號登入 (~/.ssh/authorized_keys)

	config.ssh.private_key_path, config.ssh.username, config.ssh.password

2. 設定 port forwarding

3. 在 guest os 產生 /vagrant (sudo mkdir -p /varant)

4. 掛載 host os <shared_foler> 到 guest os 的 /vagrant (sudo mount vboxfs <shared_foler> /vagrant)

以上 guest os 系統指令皆透過 sudo 執行


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


### Build Linux Box On VirtualBox ###

In Guest

step 1, 設定 root passwd 為 vagrant

	guest:~ # passwd

step 2, 新增使用者名稱 vagrant, 密碼為 vagrant

	guest:~ # useradd vagrant
	guest:~ # passwd vagrant

step 3, 設定 sudo 免密碼

	guest:~ # visudo
	...
	# Add the following line to the end of the file.
	vagrant ALL=(ALL) NOPASSWD:ALL  # 新增此行, 使用 sudo 免密碼
	...
	#Defaults    requiretty         # 註解此行, 可在 inactive mode 使用 sudo
	...

step 4, 設定 NIC

	guest:~ # vi /etc/sysconfig/network-srcipts/ifcfg-<interface>
	...
	ONBOOT=yes   # 設定開機後自動啟動
	...

step 5, 啟動 sshd

	guest:~ # systemctl enable sshd.service

step 6, 安裝 VBoxGuestAdditions

掛載 /usr/share/virtualbox/VBoxGuestAdditions.iso

	guest:~ # yum install gcc kernel-headers kernel-devel
	guest:~ # mount /dev/cdrom /mnt
	guest:~ # /mnt/VBoxLinuxAdditions.run

step 7, 安裝 insecure public key

	guest:~ # mkdir -p ~vagrant/.ssh
	guest:~ # curl https://raw.githubusercontent.com/mitchellh/vagrant/master/keys/vagrant.pub > ~vagrant/.ssh/authorized_keys
	guest:~ # chown -R vagrant:vagrant ~vagrant/.ssh

In Host

	rhel:~ # vagrant pacakge --output <vagrant_vm>.box --base <vbox_vm>  # 產生 <vagrant_vm>.box 檔案
	rhel:~ # vagrant box add <vagrant_vm>.box --name <vm_name>           # 將 <vagrant_vm>.box 匯入


### Build Windows Box On VirtualBox ###


### Other ###

	rhel:~ # ls ~/.vagrant.d/boxes   # box 會存到此目錄下


https://dennypc.wordpress.com/2014/06/09/creating-a-windows-box-with-vagrant-1-6/

http://www.vagrantbox.es/
vagrant box add {title} {url}
vagrant init {title}
vagrant up