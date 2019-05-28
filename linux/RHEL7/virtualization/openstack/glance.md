# glance

## cli

```bash
op:~ # glance image-list
op:~ # glance image-show ef647309-d560-44bb-a159-6b423dc824ca

op:~ # glance image-create --name 'vsz-5.0.0.0.123' \
  --container-format bare \
  --disk-format qcow2 \
  --is-public true \
  --copy-from http://192.168.0.1/vsz-5.1.0.0.123.qcow2

op:~ # glance image-create --name 'vsz-5.0.0.0.123' \
  --container-format bare \
  --disk-format qcow2 \
  --is-public true \
  --file vsz-5.1.0.0.123.qcow2

op:~ # glance image-create --name 'vsz-5.0.0.0.123' \
  --container-format bare \
  --disk-format qcow2 \
  --is-public true \
  --progress < vsz-5.1.0.0.123.qcow2

op:~ # glance image-delete <img_id>
```

---

## disable swift / enable file

```bash
# stop glance
op:~ # service glance-api
op:~ # service glance-registry stop
op:~ # service glance-glare stop

# stop swift
op:~ # initctl stop swift-proxy
op:~ # initctl stop swift-account
op:~ # initctl stop swift-account-auditor
op:~ # initctl stop swift-account-reaper
op:~ # initctl stop swift-account-replicator
op:~ # initctl stop swift-container
op:~ # initctl stop swift-container-auditor
op:~ # initctl stop swift-container-replicator
op:~ # initctl stop swift-container-reconciler
op:~ # initctl stop swift-container-sync
op:~ # initctl stop swift-container-updater
op:~ # initctl stop swift-object
op:~ # initctl stop swift-object-auditor
op:~ # initctl stop swift-object-replicator
op:~ # initctl stop swift-object-updater
op:~ # initctl stop swift-object-reconstructor

# disable swift
op:~ # echo "manual" | tee /etc/init/swift-proxy.override
op:~ # echo "manual" | tee /etc/init/swift-account.override
op:~ # echo "manual" | tee /etc/init/swift-account-auditor.override
op:~ # echo "manual" | tee /etc/init/swift-account-reaper.override
op:~ # echo "manual" | tee /etc/init/swift-account-replicator.override
op:~ # echo "manual" | tee /etc/init/swift-container.override
op:~ # echo "manual" | tee /etc/init/swift-container-auditor.override
op:~ # echo "manual" | tee /etc/init/swift-container-replicator.override
op:~ # echo "manual" | tee /etc/init/swift-container-sync.override
op:~ # echo "manual" | tee /etc/init/swift-container-updater.override
op:~ # echo "manual" | tee /etc/init/swift-object.override
op:~ # echo "manual" | tee /etc/init/swift-object-auditor.override
op:~ # echo "manual" | tee /etc/init/swift-object-replicator.override
op:~ # echo "manual" | tee /etc/init/swift-object-updater.override
op:~ # echo "manual" | tee /etc/init/swift-object-reconstructor.override

# update glance config
op:~ # vi /etc/glance/glance-api.conf
stores = glance.store.swift.Store,glance.store.http.Store  ->  stores = file,http
default_store = swift  ->  default_store = file
filesystem_store_datadir = /var/lib/glance/images
...

op:~ # vi /etc/glance/glance-glare.conf
default_store = swift  ->  default_store = file
...

# regenerate glance database
op:~ # grep connection /etc/glance/glance-api.conf
connection = mysql://glance:<glance_password>@10.0.0.1/glance?charset=utf8&read_timeout=60

op:~ # mysql -u glance -p
mysql> drop database glance;
mysql> create database glance;

op:~ # /bin/sh -c "glance-manage db sync" glance

# start glance
op:~ # service glance-api start
op:~ # service glance-registry start
op:~ # service glance-glare start
```

