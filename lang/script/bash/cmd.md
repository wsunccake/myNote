# common command

## curl

### with ftp

```bash
# login
linux:~ # curl -v -u <username>:<password> "ftp://<ftp ip>/<path>/"

# upload
linux:~ # curl -v -u <username>:<password> "ftp://<ftp ip>/<path>/" -T "<file>" --ftp-create-dirs

# download
linux:~ # curl -v -u <username>:<password> "ftp://<ftp ip>/<path>/<file>" -o "<file>"

# rename
linux:~ # curl -v -u <username>:<password> "ftp://<ftp ip>/<path>" -Q "-RNFR <old file>"  -Q "-RNTO <new file>"

# remove
linux:~ # curl -v -u <username>:<password> "ftp://<ftp ip>/<path>" -Q "-DELE <file>"

# mkdir
linux:~ # curl -v -u <username>:<password> "ftp://<ftp ip>/<path>/" --ftp-create-dirs
linux:~ # curl -v -u <username>:<password> "ftp://<ftp ip>/" -Q "-MKD <path>"

# rmdir
linux:~ # curl -v -u <username>:<password> "ftp://<ftp ip>/" -Q "-RMD <path>"
```


---

## content

```bash
linux:~ # csplit /etc/passwd 10
linux:~ # csplit /etc/passwd 10 {2}
linux:~ # csplit /etc/passwd 10 // '{*}'

linux:~ # sort /etc/passwd
linux:~ # sort -r /etc/passwd
linux:~ # sort -t: -k3 -n /etc/passwd

linux:~ # shuf /etc/passwd

linux:~ # uniq
```
