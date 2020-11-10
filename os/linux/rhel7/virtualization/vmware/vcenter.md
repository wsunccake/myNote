# vCenter

http://<vcenter_ip>/ui

## api

http://<vcenter_ip>/apiexplorer


---

## shell

```bash
linux:~ # curl -k -i -u <username>:<password> -X POST -c cookie.txt https://<vcenter_ip>/rest/com/vmware/cis/session

linux:~ # curl -k -i -b cookie.txt https://<vcenter_ip>/rest/vcenter/vm
linux:~ # curl -k -i -b cookie.txt https://<vcenter_ip>/rest/vcenter/dataceter
linux:~ # curl -k -i -b cookie.txt https://<vcenter_ip>/rest/vcenter/cluster
linux:~ # curl -k -i -b cookie.txt https://<vcenter_ip>/rest/vcenter/datastore
linux:~ # curl -k -i -b cookie.txt https://<vcenter_ip>/rest/vcenter/host
```


---

## python

`require`

```bash
linux:~ # git clone https://github.com/vmware/vsphere-automation-sdk-python.git
linux:~ # cd vsphere-automation-sdk-python
linux:~/vsphere-automation-sdk-python # python3.6 -m venv venv
linux:~/vsphere-automation-sdk-python # source venv/bin/activate
linux:~/vsphere-automation-sdk-python # pip3.6 install -r requirements.txt --extra-index-url file:///`pwd`/lib
```

`example`

```python
import requests
import urllib3
from vmware.vapi.vsphere.client import create_vsphere_client

session = requests.session()
session.verify = False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

vc_ip=<vcenter_ip>
vc_username=<username>
vc_password=<password>

vsphere_client = create_vsphere_client(server=vc_ip, username=vc_username, password=vc_password, session=session)

print(vsphere_client.vcenter.VM.list())
print(vsphere_client.vcenter.Datacenter.list())
print(vsphere_client.vcenter.Cluster.list())
print(vsphere_client.vcenter.Datastore.list())
print(vsphere_client.vcenter.Host.list())
```
