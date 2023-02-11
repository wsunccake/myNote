# fortios - fortigate

## default

default IP address/subnet of port1 is 192.168.1.99/255.255.255.0

```
Serial line  : COM1
Speed (baud) : 9600
Data bits	 : 8
Stop bits	 : 1
Parity	     : None
Flow control : None
```

```bash
# for connect console port
linux:~ # screen /dev/ttyUSB0 9600
```

```bash
###
### scope
###

+-------------------------------+
|config system interface        |
|    edit port1                 |
|    +-------------------+      |
|    |   set status up   |      |
|    |   next            |      |
|    +-------------------+      |
|end                            |
+-------------------------------+

fortios # config system interface
fortios (interface) # edit port1
fortios (port1) # set status up
fortios (port1) # next
fortios (interface) # end
fortios #


###
### filter
###

show | grep -A|-B|-C <n> <pattern>

fortios # show | grep -C 5 port1
```

---

## info

```bash
# system status and config
get system status
show full-configuration


# set factory
execute factoryreset


# global setting
config system global
    set admintimeout 30                         # extend timeout
    set internal-switch-mode interface|switch   # interface / switch mode
end


# output mode
configure system console
    set output standard|more
    set baudrate 9600|19200|38400|57600|115200
end


# shutdown
execute shutdown


# reboot
execute reboot
```

---

## interface

```bash
get system interface physical
show system interface

# ip
show system interface <port>
config system interface
    edit <port>
    set mode static|dhcp|pppoe
    set ip <ip_address> <netmask>
    set allowaccess (http https ping ssh telnet)
end

fortios # config system interface
fortios (interface) # edit port1
fortios (port1) # set mode static
fortios (port1) # set ip 192.168.100.159 255.255.255.0
fortios (port1) # set allowaccess allowaccess ping https ssh
fortios (port1) # end
fortios # show system interface port1


# vlan
config system interface
    edit <vlan>
        set vdom root
        set type vlan
        set vlanid <vlan id>
        set ip <ip_address> <netmask>
        set interface <int>
    next
end

fortios # config system interface
fortios (interface) # edit vlan123
fortios (vlan123) # set vdom root
fortios (vlan123) # set type vlan
fortios (vlan123) # set vlanid 123
fortios (vlan123) # set ip
fortios (vlan123) # set ip 192.168.123.1 255.255.255.0
fortios (vlan123) # set interface switch
fortios (vlan123) # next
fortios (interface) #end
```

---

## dns

```bash
config system dns
    set primary <dns-server_ip>
    set secondary <dns-server_ip>
end
show system dns
get system dns

fortios # config system dns
fortios (dns) # set primary <dns-server_ip>
fortios (dns) # set secondary <dns-server_ip>
fortios (dns) # end
fortios # show system dns
fortios # get system dns
```

---

# gateway

```bash
# for 7.x
config system route
    edit <seq_num>
    set device <port>
    set gateway <gateway_ip>
end

# for 6.x
show router policy
config router policy
    edit 15
        set input-device "ssl.root"
        set src "0.0.0.0/0.0.0.0"
        set dst "10.10.123.0/255.255.255.0"
        set gateway 192.168.123.253
        set output-device "vlan123"
    next
end
```

---

# ntp

```bash
config system ntp
    set server <server_ip>
    set status (enable | disable)
end
show system ntp
get system ntp

fortios # config system ntp
fortios (ntp) # set server 172.30.62.81
fortios (ntp) # set status enable
fortios # end
fortios # show system ntp
fortios # get system ntp
```

---

## dhcp server

```bash
show system dhcp server
config system dhcp server
    edit <dhcp server id>
        set dns-service default
        set default-gateway <gw>
        set netmask <netmask>
        set interface <interface>
            config ip-range
                edit <ip-range id>
                    set start-ip <ip_start>
                    set end-ip <ip_end>
                next
            end
        set timezone-option default
    next
end

fortios # config system dhcp server
fortios (server) # edit 1
fortios (1) # set dns-service default
fortios (1) # set default-gateway 192.168.99.255
fortios (1) # set netmask 255.255.255.0
fortios (1) # set interface "switch"
fortios (1) # config ip-range
fortios (ip-range) # edit 1
fortios (1) # set start-ip 192.168.99.100
fortios (1) # set end-ip 192.168.99.150
fortios (1) # next
fortios (ip-range) # end
fortios (1) # set timezone-option default
fortios (1) # next
fortios # end
```

---

## firewall

```bash
# address
show firewall address
config firewall address
    edit "FIREWALL_AUTH_PORTAL_ADDRESS"
        set uuid 5ff80da2-e1d4-51ea-00c6-c9384e9e1c10
        set visibility disable
    next
    edit "SSLVPN_TUNNEL"
        set uuid 6c7504c2-71ed-51e7-1a8a-91c63f745a3d
        set type iprange
        set start-ip 172.16.0.100
        set end-ip 172.16.0.200
    next
    edit "all"
        set uuid 6c74bd46-71ed-51e7-bc9c-c673e68717ea
    next
    edit "none"
        set uuid 6c63a574-71ed-51e7-acdd-186d4c358b78
        set subnet 0.0.0.0 255.255.255.255
    next
    edit "*.live.com"
        set uuid 6c63fbc8-71ed-51e7-3174-2ee39148a83e
        set type wildcard-fqdn
        set wildcard-fqdn "*.live.com"
    next
    edit "vlan123"
        set uuid 89c3fcb2-71ee-51e7-5691-8c241ffd964a
        set associated-interface "vlan123"
        set subnet 192.168.123.0 255.255.255.0
    next
end


# virtual ip forwarding
show firewall vip
config firewall vip
    edit "PC1tovlan192"
        set uuid 129872f6-54c6-51e8-af64-a1c5088357cc
        set extip 172.16.0.101
        set extintf "wan1"
        set mappedip "192.168.123.7"
    next
    edit "DEVICE1tovlan123"
        set uuid 53d53ef2-fb61-51ec-a793-8c4bc802861e
        set extip 172.16.0.102
        set extintf "any"
        set mappedip "192.168.123.8"
    next
end


# policy
show firewall policy
config firewall policy
    edit 19
        set uuid 6c7bbeee-7a66-51e7-2fcb-2b4feaef86b8
        set srcintf "vlan123"
        set dstintf "wan1"
        set srcaddr "all"
        set dstaddr "all"
        set action accept
        set schedule "always"
        set service "ALL"
        set logtraffic disable
        set ippool enable
        set poolname "192_to_wan1"
        set nat enable
    next
    edit 20
        set uuid 859055b6-7a66-51e7-8694-10bd204cc72c
        set srcintf "vlan123"
        set dstintf "wan1"
        set srcaddr "all"
        set dstaddr "1.1.1.0" "10.10.0.0"
        set schedule "always"
        set service "ALL"
        set logtraffic all
    next
end
```
