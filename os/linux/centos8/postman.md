# postman

## install

```bash
[linux:~ ] $ vi ~/.local/share/applications/Postman.desktop
[Desktop Entry]
Encoding=UTF-8
Name=Postman
Exec=/opt/Postman/app/Postman %U
Icon=/opt/Postman/app/resources/app/assets/icon.png
Terminal=false
Type=Application
Categories=Development;
```


---

## newman

```bash
[linux:project ] $ npm install newman
[linux:project ] $ ./node_modules/newman/bin/newman.js run <collection>.json -k -e <environment>.json
```
