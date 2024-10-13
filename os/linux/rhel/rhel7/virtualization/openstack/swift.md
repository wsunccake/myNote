# swift

## cli

```bash
op:~ # swift stat
op:~ # swift list
op:~ # swift list --lh
```


---

## auth

```bash
# get token for swift
op:~ # vi /etc/swift/proxy-server.conf
[filter:authtoken]
log_name = swift
signing_dir = /var/cache/swift
paste.filter_factory = keystonemiddleware.auth_token:filter_factory

auth_uri = http://1.2.3.4:5000/
identity_uri = http://1.2.3.4:35357/
admin_tenant_name = services
admin_user = swift
admin_password = <swift_password>
delay_auth_decision = 1
cache = swift.cache
include_service_catalog = False

op:~ # swift --os-auth-url http://1.2.3.4:5000//v3 \
--auth-version 3 \
--os-project-name services \
--os-username swift \
--os-password <swift_password> \
auth

# get token for glance
op:~ # cat /etc/glance/glance-swift.conf
user = services:glance
key = <glance_password>
auth_version = 3
auth_address = http://1.2.3.4:5000//v3
user_domain_id=default
project_domain_id=default

op:~ # swift --os-auth-url http://1.2.3.4:5000//v3 \
--auth-version 3 \
--os-project-name services \
--os-username glance \
--os-password  <glance_password> \
auth
```

