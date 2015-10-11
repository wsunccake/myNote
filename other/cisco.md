# CISCO #


## enable privilege ##

	CISCO>enable
	CISCO#


## list ##

	CISCO# show interfaces summary
	CISCO# show interfaces status
	CISCO# show interfaces
	CISCO# show configuration
	CISCO# show spanning-tree interface TenGigabitEthernet 1/1


## setup vlan ##

	# enable vlan for interface
	CISCO# configure terminal
	CISCO(config)# interface TenGigabitEthernet 1/1
	CISCO(config-if)# switchport access vlan 10
	CISCO(config-if)# no shutdown

	# disable vlan for interface
	CISCO# no switchport access vlan 10
	CISCO# no shutdown

	# check vlan for interface
	CISCO# show spanning-tree interface TenGigabitEthernet 1/1