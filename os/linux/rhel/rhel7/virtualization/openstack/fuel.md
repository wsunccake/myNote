## Upgrade fuel 9.0 to 9.2

```bash
# upgrade version
fuel:~ # yum install -y http://mirror.fuel-infra.org/mos-repos/centos/mos9.0-centos7/9.2-updates/x86_64/Packages/mos-release-9.2-1.el7.x86_64.rpm
fuel:~ # yum clean all
fuel:~ # yum install -y mos-playbooks
fuel:~ # cd /root/mos_playbooks/mos_mu
fuel:/root/mos_playbooks/mos_mu # ansible-playbook playbooks/mos9_prepare_fuel.yml
fuel:/root/mos_playbooks/mos_mu # ansible-playbook playbooks/update_fuel.yml -e '{"rebuild_bootstrap":false}'
fuel:/root/mos_playbooks/mos_mu # ansible-playbook playbooks/mos9_fuel_upgrade_kernel_4.4.yml

# check version
fuel:~ # fuel fuel-version

# create mirror
fuel:~ # fuel-createmirror
fuel:~ # fuel-mirror create --pattern=ubuntu --group mos ubuntu
```

