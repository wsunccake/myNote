# VirtualBox #


## VM ##

	# list
	rhel:~ # VBoxManage list vms
	rhel:~ # VBoxManage list runningvms
	rhel:~ # VBoxManage list ostypes

	# create vm
	rhel:~ # VBoxManage createvm --name <vm_name>                    # 建立 xml
	rhel:~ # VBoxManage modifyvm <vm_name> --cpus 1 --memory 1024
	rhel:~ # VBoxManage modifyvm --ostype RedHat_64 --boot1 dvd
	rhel:~ # VBoxManage modifyvm --nic1 nat --macaddress1 <mac_addr>
	rhel:~ # VBoxManage modifyvm --acpi on 

	# control vm
	rhel:~ # VBoxManager startvm <vm_name>
	rhel:~ # VBoxManage controlvm <vm_name> poweroff

	# show vm
	rhel:~ # VBoxManage showvminfo <vm_name>

	# register vm
	rhel:~ # VBoxManage registervm /<path>/<vm_name>.vbox

	# delete/unregister vm
	rhel:~ # VBoxManage unregistervm <vm_name>


## Disk ##

	# create disk
	rhel:~ # VBoxManage createmedium disk --filename <vm_disk> --format VMDK --size 40000

	# attach disk
	rhel:~ # VBoxManage storagectl <vm_name>  --name <controller_name> --add sata --controller IntelAHCI
	rhel:~ # VBoxManage storageattach <vm_name> --storagectl <controller_name> --port 0 --device 0 --type hdd --medium <vm_disk>


## CD/DVD ##

	rhel:~ # VBoxManage storagectl <vm_name> --name <controller_name> --add ide

	# mount cd/dvd
	rhel:~ # VBoxManage storageattach <vm_name> --storagectl <controller_name> --port 1 --device 0 --type dvddrive --medium <iso>

	# umount cd/dvd
	rhel:~ # VBoxManage storageattach <vm_name> --storagectl <controller_name> --port 1 --device 0 --type dvddrive --medium none


## Network ##

	# port forwarding
	rhel:~ # VBoxManage modifyvm <vm_name> --natpf1 "<rule_name>,tcp,,2222,,22"
	rhel:~ # VBoxManage modifyvm <vm_name> --natpf1 delete <rule_name>


## Shared folder ##

In Host OS

	rhel:~ # VBoxManage sharedfolder add <vm_name> --name <folder_nane> --hostpath <host_path>   # 新增 shared folder
	rhel:~ # VBoxManage sharedfolder remove <vm_name> --name <folder_nane>                       # 移除 shared folder

In Guest OS

	guest:~ # yum install gcc kernel-headers kernel-devel    # 安裝 kernel lib 及 compiler
	guest:~ # guest:~ # mount /dev/cdrom /mnt
	guest:~ # /mnt/VBoxLinuxAdditions.run
	guest:~ # lsmod | grep vboxfs                            # 確認產生 vboxfs module
	guest:~ # mount -t vboxsf  <folder_nane> <mount_point>   # 掛載 shared folder




https://help.github.com/enterprise/11.10.340/admin/articles/installing-virtualbox-guest-additions/