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

---

## ssh

Bad owner or permissions

```powershell
# 定義檔案路徑
PS C:\> $ssh_config = "$env:USERPROFILE\.ssh\config"

# 1. 取得檔案的所有權 (確保有權更改權限)
PS C:\> takeown /f $ssh_config

# 2. 移除所有繼承權限，並清除所有現有的存取控制 (ACL)
PS C:\> icacls $ssh_config /reset

# 3. 再次停用繼承，並移除所有不相關的權限項目
PS C:\> icacls $ssh_config /inheritance:r

# 4. 只准許本人存取 (F 代表 Full Access)
PS C:\> icacls $ssh_config /grant:r "${env:USERNAME}:F"

# 5. (選填) 如果 SSH 還是抱怨，可以補上 SYSTEM 權限
PS C:\> icacls $ssh_config /grant:r "SYSTEM:F"

# 6. 驗證，輸出結果應該只會看到自己名字
PS C:\> icacls $ssh_config
```

---

## starship

- [Nerd Fonts](https://www.nerdfonts.com/)

1. 開啟 Windows Terminal，點擊標題列的 「∨」 圖示，選擇 「設定」。
2. 在左側側邊欄中，向下捲動找到 「設定檔」(Profiles) 區塊。
3. 點擊想修改的特定設定檔（例如：PowerShell、Command Prompt 或 Ubuntu）。
4. 點擊該設定檔右側介面中的 「外觀」 (Appearance) 分頁（這是在特定設定檔底下的外觀，不是左側清單最上方的那個）。
5. 在這個頁面中，會看到 「文字」

```pwsh
# install
PS C:\> winget install --id Starship.Starship

# setup
PS C:\> edit $PROFILE

# usage
PS C:\> starship.exe preset --list
PS C:\> starship.exe preset pastel-powerline -o ~/.config/starship.toml
```

`$PROFILE`

`~\Documents\PowerShell\Microsoft.PowerShell_profile.ps1` or `~/.config/powershell/Microsoft.PowerShell_profile.ps1`

```pwsh
Invoke-Expression (&starship init powershell)
```
