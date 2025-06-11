# windows 10

## network

```batch
smb
SMB 1.0/CIFS 檔案共用支援
SMB 直接傳輸

Windows + S，搜尋 控制台，然後進入 網路和共享中心 \ 變更進階共享設定
```

---

## develop

```batch
:: git
C:\Users\user> winget install --id Git.Git

:: neovim
C:\Users\user> winget install--id Neovim.Neovim

:: weztermial
C:\Users\user> winget install wez.wezterm
C:\Users\user> nvim $env:USERPROFILE\.wezterm.lua
return {
  default_prog = { "pwsh.exe", "-NoLogo", "-NoExit" },
}
```

```powershell
# launch microsoft store
PS C:\Users\user> Start-Process ms-windows-store:

# python3

# vscode

# windows terminal
# powershell

# firefox
## Video DownloadHelper
## AdBlock for Firefox
```

---

## cli

```batch
:: ssh
C:\Users\user> dir %USERPROFILE%\.ssh

:: shutdown
C:\Users\user> shutdown /r /t 0
C:\Users\user> shutdown /s /t 0
```
