# ICX

## basic

```bash
# User EXEC Mode
Router>

# Privileged EXEC Mode
Router> enable
Router#

Router# show running-config
Router# show version [| include <pattern> ]
Router# write memory
Router# reload

Router# configure terminal
Router(config)#

# Global Config Mode
Router(config)#
```

---

## setup network

```bash
# ip
Router(config)# interface management 1
Router(config-if-mgmt-1)# ip address <ip>/<mask>
# ip   : A.B.C.D
# mask : subnet mask length

## defaut gateway
Router(config)# ip route <dest ip>/<mask> <next hop ip>
# A.B.C.D or A.B.C.D/L : Destination IP address
# A.B.C.D              : Next hop IP address

## dns
Router(config)# ip dns server-address <dns ip>
# A.B.C.D              : DNS IP address
```

---

## join R1

```bash
Router(config)# manager registrar <registrar server>
# <registrar server>

Router# show manager status
```
