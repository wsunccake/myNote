# windows 11

## donwload

[下載 Windows 11](https://www.microsoft.com/zh-tw/software-download/windows11)

---

## activiation

[Windows-11-Activator](https://github.com/Boss-Man-Dev/Windows-11-Activator/tree/main)

---

## install

How would you like to set up the device -> Set up for work or school
Let's add your Microsoft account -> sign-option

---

## VM

### virtualbox

install "Guest Additions" to setup "resolution" and "shared folder"

---

## tool

### Microsoft store

```powershell
# launch microsoft store
PS C:\Users\user> Start-Process ms-windows-store:
```

- Visual Studio Code
  - Prettier - Code formatter
- PowerShell
- Windows Terminal
- RealVNC Viewer

### winget

```powershell
# git
PS C:User\user> winget install --id Git.Git -e --source winget

# neovim
PS C:\Users\user> winget install --id Neovim.Neovim
```

---

## WSL

```batch
:: 開啟 "windows 功能" 後點選 "Windows Subsystem for Linux" / "Windows 子系統 Linux 版"
optionalfeatures
```

```powershell
PS C:\Users\user> wsl --help
PS C:\Users\user> wsl --version

# list
PS C:\Users\user> wsl --list --all
PS C:\Users\user> wsl --list --online

# register / unregister
PS C:\Users\user> wsl --install [--distribution Ubuntu-24.04]
PS C:\Users\user> wsl --unregister <distro>

# launch
PS C:\Users\user> wsl [--distribution <distro>] [--user <user>]
```

---

## Docker Desktop

```powershell
# 確認安裝 wsl 2 也是 version: 2
PS C:\Users\user> wsl.exe -l -v
```

下載 [Docker Desktop](https://www.docker.com/products/docker-desktop/) 且安裝

- "Settings" \ "General" tab \ select "Use the WSL 2 based engine"
- "Settings" \ "Resources" tab \ select "WSL integrations"
