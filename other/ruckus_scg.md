# SCG #


## SCG on KVM ##

* Processor: 4+

* Memory: 14+ GB

* NIC: 3, virtio (1st, control; 2nd, cluster; 3rd, manamgement)

* Disk: 50+ GB, IDE


## SZ/vSZ on KVM ##

* Processor: 4+

* Memory: 14+ GB

* NIC: 1, virtio (control, cluster, manamgement in one)

* Disk: 50+ GB, IDE


# vDP #


## vDP on KVM ##

* Processor: 4+

* Memory: 9+ GB

* NIC: 1, e1000 (control plane)
       1, dpdk (data plane)

* Disk: 50GB+, IDE


## prividge mode ##

	# prividge mode
	vSZ-D> enable 
	vSZ-D#

	# config mode
	vSZ-D# config
	vSZ-D(config)#

	# shell mode
	vSZ-D# !v54!
	-bash-4.1$ sudo su -
	[root@vSZ-D ~]#



## setup and initial ##

	vSZ-D# setup
	vSZ-D# set-factory
	vSZ-D#


## list info ##

	vSZ-D# show version
	vSZ-D# show interface
	vSZ-D# show status
	vSZ-D# show ip
	vSZ-D# show controller


## vSZ approve vDP ##

	vSZ# show data-plane

	vSZ(config)# data-plane <dp_name>@<dp_mac> approve
	vSZ(config)# no data-plane <dp_name>@<dp_mac>


## AP join vSZ with vDP (tunnel mode) ##

	rkscli: get tunnelmgr

	rkscli: set scg ip <scg_control_ip>
	rkscli: set scg config interval 30
	rkscli: set scg status interval 30
	rkscli: set scg getconf

	# vDP shell mode
	[root@vSZ-D ~]# tunnelmgr_cli -s all
	[root@vSZ-D ~]# datacore arp
