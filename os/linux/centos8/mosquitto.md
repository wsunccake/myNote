# mosquitto


## install

```bash
centos:~ # dnf install mosquitto
centos:~ # systemctl enable --now mosquitto

centos:~ # ss -lutnp | grep 1883
```

---

## subscribe

```bash
centos:~ # mosquitto_sub -h <mosquitto_ip> -t test
```


---

## publish

```bash
centos:~ # mosquitto_pub -h <mosquitto_ip> -t test -m "hello world"
```
