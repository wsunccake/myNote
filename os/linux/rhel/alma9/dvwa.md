# dvwa / damm vulnerable web applcation

## prepare

### repo

```bash
# repo
alma:~ # dnf clean all
alma:~ # dnf install epel-release -y
alma:~ # dnf update -y
```

### apache

```bash
# install
alma:~ # dnf install httpd httpd-tools -y

# service
alma:~ # systemctl start httpd
alma:~ # systemctl enable httpd
alma:~ # systemctl status httpd

# firewall
alma:~ # firewall-cmd --permanent --zone=public --add-service=http
alma:~ # firewall-cmd --permanent --zone=public --add-service=https
alma:~ # firewall-cmd --reload
alma:~ # firewall-cmd --list-services
alma:~ # firewall-cmd --list-all
```

### mariadb

```bash
# install
alma:~ # dnf install mariadb-server mariadb -y

# service
alma:~ # systemctl restart mariadb
alma:~ # systemctl status mariadb
alma:~ # systemctl enable mariadb

# setting
alma:~ # mysql_secure_installation

# testing
alma:~ # mysql -u root -p
```

### php

```bash
# install
alma:~ # dnf install php php-curl php-bcmath php-gd php-soap php-zip php-curl php-mbstring php-mysqlnd php-gd php-xml php-intl php-zip -y

# testing
alma:~ # php -v
alma:~ # cat << EOF >> /var/www/html/info.php
<?php
phpinfo ();
?>
EOF
alma:~ # systemctl restart httpd
alma:~ # http://localhost/info.php
```

### selinux

```bash
alma:~ # setsebool -P httpd_unified 1
alma:~ # setsebool -P httpd_can_network_connect 1
alma:~ # setsebool -P httpd_can_network_connect_db 1
```

---

## install

```bash
alma:~ # dnf install git -y

alma:~ # cd /var/www/html/
alma:~/var/www/html # git clone https://github.com/digininja/DVWA.git dvwa
alma:~/var/www/html # chmod -R 777 dvwa
alma:~/var/www/html # chown -R apache:apache dvwa

alma:~/var/www/html # cd dvwa/config/
alma:~/var/www/html/dvwa/config # cp config.inc.php.dist config.inc.php
alma:~/var/www/html/dvwa/config # more config.inc.php
$_DVWA = array();
$_DVWA[ 'db_server' ]   = '127.0.0.1';
$_DVWA[ 'db_database' ] = 'dvwa';
$_DVWA[ 'db_user' ]     = 'dvwa';
$_DVWA[ 'db_password' ] = 'p@ssw0rd';
$_DVWA[ 'db_port'] = '3306';
# https://www.google.com/recaptcha/admin
$_DVWA[ 'recaptcha_public_key' ]  = '';
$_DVWA[ 'recaptcha_private_key' ] = '';

# mysql / mariadb add user and password
alma:~ # mysql -u root -p
MariaDB [(none)]> create user 'dvwa'@'127.0.0.1' identified by 'p@ssw0rd';
MariaDB [(none)]> grant all privileges on dvwa.* to 'dvwa'@'127.0.0.1' identified by 'p@ssw0rd';
MariaDB [(none)]> flush privileges;
MariaDB [(none)]> quit;

# apache php module config
alma:~ # vi /etc/php.ini
allow_url_fopen = On
allow_url_include = On
display_errors = Off
alma:~ # systemctl restart httpd

alma:~ # curl http://localhost/dvwa
# default account: admin
# default password: password
```
