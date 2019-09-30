# Ganglia


```
gweb  --- gmetad ---  gmond1
                      gmond2
                      ...
```


## gmetad

```bash
# package
gmetad:~ # zypper in ganglia-gmetad

# service
gmetad:~ # systemctl enable gmetad
gmetad:~ # systemctl start gmetad

# port
gmetad:~ # ss -lutnp | grep 8652

# config
gmetad:~ # vi /etc/ganglia/gmetad.conf
data_source "my cluster" localhost <gmond1_ip> ...
```


---

## web

```bash
# package
gweb:~ # zypper in ganglia-web

# service
gweb:~ # a2enmod php7
gweb:~ # systemctl enable apache2
gweb:~ # systemctl start apache2

# port
gweb:~ # ss -lutnp | grep 80

# config
gweb:~ # vi /etc/apache2/conf.d/ganglia-web.conf

gweb:~ # ls /srv/www/htdocs/ganglia-web
gweb:~ # /srv/www/htdocs/ganglia-web/conf_default.php
$conf['ganglia_ip'] = "127.0.0.1";
$conf['ganglia_port'] = 8652;

```


---

## gmond

```bash
# package
gmond:~ # zypper in ganglia-gmond ganglia-gmond-modules-python

# service
gmond:~ # systemctl enable gmond
gmond:~ # systemctl start gmond

# port
gmond:~ # ss -lutnp | grep 8649

# config
gmond:~ # ls /etc/ganglia/gmond.conf
```
