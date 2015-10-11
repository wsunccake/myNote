# Ruckus AP #


## list info ##

	rkscli: get version
	rkscli: get ipaddr wan
	rkscli: get wlanlist

	rkscli: get scg
	rkscli: get tunnelmgr

	rkscli: fw show all


## reboot & set factory##

	rkscli: reboot
	rkscli: set factory


## set scg ##

	rkscli: set scg ip scg_ip
	rkscli: set scg config interval 30
	rkscli: set scg status interval 30
	rkscli: set scg getconf


## update fw ##

	# by scg http
	rkscli: fw set proto http
	rkscli: fw set port 91
	rkscli: fw set host scg_ip
	rkscli: fw set control wsg/firmware/R300_3.4.0.0.139.rcks
	rkscli: fw update

	# by scg https
	rkscli: fw set proto https
	rkscli: fw set port 11443
	rkscli: fw set host scg_ip
	rkscli: fw set control wsg/firmware/R710_3.2.0.99.477.rcks
	rkscli: fw update

	# by tftp
	rkscli: fw set proto tftp
	rkscli: fw set port 69
	rkscli: fw set host tftp_ip
	rkscli: fw set control R710/rcks_fw.bl7
	rkscli: fw update


## log ##

	rkscli: set scg console 0xffff


## rfald ##

	rkscli: set rfald disable
	rkscli: set rfald peer ue_ip
	rkscli: set rfald enable
	rkscli: get rfald