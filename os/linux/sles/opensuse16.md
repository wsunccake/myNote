# opensuse leap 16

## system

```bash
opensuse:~ # zypper lr
opensuse:~ # zypper mr -e openSUSE:repo-non-oss
opensuse:~ # zypper ref

# add repo from ymp
opensuse:~ # grep -E 'name|url' <package>.ymp | sed 's/<[^>]*>//g' | tac | sed -n '2,$'p | xargs -n2 zypper ar -fc $1 $2
# https://software.opensuse.org/
```

```bash
opensuse:~ # zypper in neovim
opensuse:~ # zypper in zsh
```

---

## service

`sshd`

```bash
opensuse:~ # ls /etc/ssh
opensuse:~ # ls /usr/etc/ssh

opensuse:~ # firewall-cmd --add-service=ssh --permanent
opensuse:~ # firewall-cmd --add-service=ssh --reload

opensuse:~ # systemctl enable sshd --now
opensuse:~ # systemctl status sshd
```

`cockpit`

download from [cockpit](https://software.opensuse.org/package/cockpit) [sscg](https://software.opensuse.org/package/sscg)

```bash
opensuse:~ # zypper in sscg
opensuse:~ # zypper in cockpit

opensuse:~ # firewall-cmd --add-service=cockpit
opensuse:~ # firewall-cmd --add-service=cockpit --permanent

opensuse:~ # systemctl enable cockpit --now
opensuse:~ # systemctl status cockpit

# plugin
opensuse:~ # zypper in cockpit-repos
opensuse:~ # zypper in cockpit-packages
```
