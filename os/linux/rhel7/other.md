## curl

```bash
# GET method
centos:~ # curl "http://localhost/get.php?name_php=aaa&age_php=12"

# POST method
centos:~ # curl -X POST -d "NAME_PHP=aaa&AGE_PHP=12" "http://localhost/post.php"
# POST method with json data
centos:~ # curl -X POST -d '{"name": "abc", "age": 123}' http://localhost/json.php

# Upload file, upload_file 為 <input type="file" name="upload_file" id="file_id">
centos:~ # curl -F upload_file=@local_file http://localhost/upload.php

# Save cookie
centos:~ # curl -X POST -d 'usernam=account' -d 'password=password' -c tmp.cookie "http://localhost/login.php"
# Use cookie
centos:~ # curl -b tmp.cookie "http://localhost/action.php"

# Redirect
centos:~ # curl -L "http://localhost/action.php"

# Download
centos:~ # curl [-o file] -L -O http://localhost/file
# Resume Download
centos:~ # curl [-o file] -L -O -C - http://localhost/action.php

# FTP download
centos:~ # curl ftp://user:password@host/download_file -o filename
# FTP upload
centos:~ # curl --ftp-create-dirs -T upload_file ftp://user:password@host/file
```

---

## loop device

```bash
# loop file: /dev/loop0
# image file: sd.img

centos:~ # losetup -al                          # list loop device
centos:~ # losetup <loop device> <image file>   # attach image file to loop device
centos:~ # losetup -d <loop device>             # deattch loop device
centos:~ # losetup -D                           # deattch all loop device
centos:~ # losetup -f

centos:~ # kpartx -lv <loop device>             # list partition table map
centos:~ # kpartx -av <loop device>             # add partition table map
centos:~ # kpartx -dv <loop device>             # del partition table map

centos:~ # dmsetup info
centos:~ # dmsetup ls
centos:~ # dmsetup remove /dev/loop0
```

---

## mail

```bash
centos:~ # mail -s "title" someone@example.com << EOF
message body
EOF

centos:~ # echo "message body" | mail -s "title" someone@example.com [-aFrom:sender@exmaple.com]
```

---

## usb

```bash
centos:~ # echo "blacklist usb-storage" >> /etc/modprobe.d/blacklist.conf
```

---

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
