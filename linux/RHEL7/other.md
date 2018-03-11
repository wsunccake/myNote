## screenfetch

```bash
centos:~ # git clone git://github.com/KittyKatt/screenFetch.git /usr/local/screenfetch
centos:~ # cp /usr/local/screenfetch/screenfetch-dev /usr/bin/screenfetch
centos:~ # chmod +x /usr/bin/screenfetch
centos:~ # screenfetch

# anyone alway show info when login 
centos:~ # echo /usr/bin/screenfetch >> /etc/profile

# myself alway show info when login
centos:~ # echo /usr/bin/screenfetch >> ~/.bashrc
```

---

## cowsay

```bash
centos:~ # yum install fortune-mod cowsay
centos:~ # fortune | cowsay -pn
centos:~ # cowsay -l
centos:~ # fortune | cowsay -pn -f stegosaurus

# anyone alway show info when login 
centos:~ # echo "fortune | cowsay -pn" >> /etc/profile

# myself alway show info when login
centos:~ # echo "fortune | cowsay -pn" >> ~/.bashrc
```

## mail

```bash
centos:~ # mail -s "title" someone@example.com << EOF
message body
EOF

centos:~ # echo "message body" | mail -s "title" someone@example.com [-aFrom:sender@exmaple.com]
```

## usb

```bash
echo "blacklist usb-storage" >> /etc/modprobe.d/blacklist.conf
```