# ngrok 2.x

## install

```bash
sle:~ # unzip ngrok-stable-linux-amd64.zip 
sle:~ # ./ngrok version
sle:~ # ./ngrok help
```


---

## forwarding http

```bash
# console 1
centos:~ # ./ngrok http 8000

# console 2
centos:~ # python3 -m http.server 8000
```


---

## ref

[ngrok](https://ngrok.com/)
