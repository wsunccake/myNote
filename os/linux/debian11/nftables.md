# nftables

## table

family

ip      iptables

ip6     ip6tables

inet	iptables and ip6tables

arp	    arptables

bridge	ebtables

netdev	Netdev address family, handling packets from ingress.

```bash
debian:~ # nft list tables [<family>]
debian:~ # nft create|add table <family> <table_name>
debian:~ # nft delete table <family> <table_name>
debian:~ # nft flush table <family> <table_name>

# ie
debian:~ # nft create table inet firewall
```


---

## chain

base chain  type, hook, priority, policy

regular chain

```bash
debian:~ # nft list chains
debian:~ # nft create|add chain <family> <table_name> <chain_name> { type <type> hook <hook> priority <value> \; [policy <policy>] }
debian:~ # nft 'create|add chain <family> <table_name> <chain_name> { type <type> hook <hook> priority <value> ; [policy <policy>] }'
debian:~ # nft delete chain <family> <table_name> <chain_name>
debian:~ # nft rename chain <family> <table_name> <chain_name> <new_chain_name>

# ie.
debian:~ # nft add chain inet firewall incoming                                                 # regular chain
debian:~ # nft 'add chain inet firewall {type filter hook input priority 0; policy drop; }'     # base chain
```


---

## rule

```bash
debian:~ # nft list ruleset
debian:~ # nft add rule [<family>] <table_name> <chain_name> <matches> <statements>
debian:~ # nft insert rule [<family>] <table_name> <chain_name> [position <position>] <matches> <statements>
debian:~ # nft replace rule [<family>] <table_name> <chain_name> [handle <handle>] <matches> <statements>
debian:~ # nft delete rule [<family>] <table_name> <chain_name> [handle <handle>]
debian:~ # nft flush ruleset
```


---

## example

```bash
# ie, input firewall
debian:~ # nft list ruleset
debian:~ # nft flush ruleset
debian:~ # nft add table inet firewall
debian:~ # nft 'add chain inet firewall incoming {type filter hook input priority 0; policy drop; }'
debian:~ # nft 'add rule inet firewall incoming iifname lo accept'
debian:~ # nft 'add rule inet firewall incoming ip saddr 192.168.1.0/24 accept'
debian:~ # nft 'add rule inet firewall incoming tcp dport {ssh, http} accept'

# ie, nat
debian:~ # nft add table nat
debian:~ # nft 'add chain nat postrouting { type nat hook postrouting priority 100 ; }'
debian:~ # nft add rule nat postrouting ip saddr 192.168.1.0/24 oif eth0
```


