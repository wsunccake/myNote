# SCG #


## on KVM


### SCG on KVM

* Processor: 4+

* Memory: 14+ GB

* NIC: 3, virtio (1st, control; 2nd, cluster; 3rd, manamgement)

* Disk: 50+ GB, IDE


### SZ/vSZ on KVM

* Processor: 4+

* Memory: 14+ GB

* NIC: 1, virtio (control, cluster, manamgement in one)

* Disk: 50+ GB, IDE


## vDP on KVM

* Processor: 4+

* Memory: 9+ GB

* NIC: 1, e1000 (control plane)
       1, dpdk (data plane)

* Disk: 50GB+, IDE


## prividge mode

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


## SCG Cassandra Web

	# method 1.
	SCG# debug
	SCG(debug)# web-debug

	# method 2.
	-bash-4.1$ sudo /opt/ruckuswireless/wsg/cli/bin/tomcat.py -D start

https://<scg_manamgement_ip>:8443/CassandraWeb/

	# CLI
	-bash-4.1$ sudo /opt/ruckuswireless/wsg/cli/bin/cassandra.py --cli

	# CQL
	-bash-4.1$ sudo /opt/ruckuswireless/3rdparty/cassandra/bin/cqlsh


## setup and initial

	SCG# rbd SCG200 SCG200 00001 11:22:33:44:55:66 32 ruckus
	#       <board>  <model> <sn> <mac> <mac-count> <customer>
	# board/model: SZ104, SZ124, SCG200

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


## public api

	check public api version in control package
	rpm -ql control-3.4.0.0-196.x86_64 | grep json-schema | grep json

https://<scg_manamgement_ip>:7443/api