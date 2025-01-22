# wsl

Windows Subsystem for Linux

## content

- [setting](#setting)
- [distro](#distro)
- [config](#config)
- [ref](#ref)

---

```batch
:: 開啟 "windows 功能" 後點選 "Windows Subsystem for Linux" / "Windows 子系統 Linux 版"
optionalfeatures
```

## setting

```batch
C:\Users\user> wsl --help
C:\Users\user> wsl --version

:: setup wsl versio: 1 or 2
C:\Users\user> wsl --set-default-version 1|2
C:\Users\user> wsl --set-version 1|2

:: remove wsl kernel
C:\Users\user> wsl --uninstall

:: update/install wsl kernel
C:\Users\user> wsl --update
```

---

## distro

```batch
:: default
C:\Users\user> wsl --set-default <distro>
C:\Users\user> wsl --status

:: register/un-register
C:\Users\user> wsl --install [--distribution <distro>]
C:\Users\user> wsl --unregister <distro>

:: launch
C:\Users\user> wsl [--distribution <distro>] [--user <user>]

:: list
C:\Users\user> wsl --list --verbose
C:\Users\user> wsl --list --all
C:\Users\user> wsl --list --online
```

---

## config

```ini
# C:\Users\user\.wslconfig
[wsl2]
localhostForwarding=true
automount=true
mountFsTab=true
root=/my/custom/mountpoint
```

---

## ref

- [Windows Subsystem for Linux Documentation](https://learn.microsoft.com/en-us/windows/wsl/)/[適用於 Linux 的 Windows 子系統文件](https://learn.microsoft.com/zh-tw/windows/wsl/)
