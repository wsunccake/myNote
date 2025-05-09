# gsettings

```bash
fedora:~ $ gsettings list-schemas
fedora:~ $ gsettings list-recursively org.gnome.desktop.remote-desktop.rdp
fedora:~ $ gsettings get org.gnome.desktop.remote-desktop.rdp enable
fedora:~ $ gsettings set org.gnome.desktop.remote-desktop.rdp view-only false

fedora:~ $ gsettings get <SCHEMA> <KEY>              # 查詢設定值
fedora:~ $ gsettings set <SCHEMA> <KEY> <VALUE>        # 設定新值
fedora:~ $ gsettings reset <SCHEMA> <KEY>            # 重設為預設值
```
