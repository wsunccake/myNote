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

---

# Windows 11 VM on ESXi

## TPM 2.0 阻擋限制

在 VMware ESXi 7.0 中安裝 Windows 11 時，最常遇到的兩個核心問題是：ESXi 7.0 的客群作業系統（Guest OS）選單中沒有 Windows 11 選項，以及安裝時會跳出 「這台電腦無法執行 Windows 11」 的 TPM 2.0 阻擋限制。

### 方法一：使用登錄表繞過 TPM 檢查（最簡單，免 vCenter）

如果是單機版 ESXi 主機（無 vCenter 架構），直接在安裝過程中「修改登錄表」是最快速的做法。

1. 建立虛擬機器配置客群作業系統版本：

- 由於選單無 Windows 11，請選擇 Microsoft Windows 10 (64 位元)。
- 引導方式（Boot Option）：必須確保選用 EFI 並勾選 「安全啟動（Secure Boot）」。
- 核心配置：配置至少 2 vCPU、4 GB 記憶體 與 64 GB 儲存空間（Windows 11 的最低硬體標準）。
- 掛載 ISO：在 CD/DVD 驅動器掛載您的 Windows 11 ISO 映像檔。

2. 在安裝程式中繞過檢測

2-1. 啟動虛擬機器電源，進入 Windows 安裝初始畫面（選擇語系頁面）。
2-2. ⚠️ 在點擊「現在安裝」之前，同時按下鍵盤上的 Shift + F10 鍵，這會呼叫出 CMD 命令提示字元視窗。
2-3. 在視窗中輸入 regedit 並按下 Enter 鍵以開啟登錄表編輯器。
2-4. 導航至以下路徑：`HKEY_LOCAL_MACHINE\SYSTEM\Setup`
2-5. 右鍵點擊 Setup 資料夾 -> 新增 -> 機碼，命名為 LabConfig（注意大小寫）。
2-6. 點進 LabConfig 資料夾，在右側空白處右鍵 -> 新增 -> DWORD (32位元) 值：

- 名稱：BypassTPMCheck，數值資料改為 1。
- (選填，若 CPU 不支援可額外新增) 名稱：BypassCPUCheck，數值資料改為 1。
- (選填，若未開啟安全啟動可額外新增) 名稱：BypassSecureBootCheck，數值資料改為 1。

2-7. 關閉登錄表與 CMD 視窗，依正常程序點擊「現在安裝」，即可順利跳過阻擋並看到授權合約頁面。

### 方法二：透過 vCenter 啟用 vTPM（適合企業/原生環境）

如果擁有 vCenter Server 7.0 管理環境，可以使用官方支援的虛擬可信平台模組 (vTPM) 功能。這需要將虛擬機器加密，但實體伺服器本身並不需要裝有實體 TPM 晶片。

1. 在 vCenter 啟用「本機金鑰提供程序」

1-1. 登入 vSphere Client。導航至 vCenter Server -> 「配置」 頁籤 -> 展開 「安全」 -> 選擇 「金鑰提供程序」。
1-2. 點擊 「添加」 -> 選擇 「添加本機金鑰提供程序 (Add Native Key Provider)」。
1-3. 設定一個名稱，並取消勾選「僅對受 TPM 保護的 ESXi 主機使用金鑰提供程序」（這樣沒有實體 TPM 的主機也能使用）。
1-4. 建立後，狀態會顯示未備份。點擊 「備份」，保存下載產生的 .p12 備份密鑰文件，完成後狀態會轉為「活動」。

2. 建立具備 vTPM 的虛擬機器

2-1. 新建虛擬機器，相容性同樣選擇 Windows 10 (64 位元)。
2-2. 在「選擇儲存」步驟中，勾選加密此虛擬機器，且儲存策略必須選擇 VM Encryption Policy。
2-3. 前往「自訂硬體」頁面，點擊右上角的 「添加新設備 (Add New Device)」。
2-4. 下拉選單中選擇 「受信任平台模組 (Trusted Platform Module)」。
2-5. 確定引導韌體為 EFI 並啟用 Secure Boot，即可掛載 ISO 檔正常引導並安裝 Windows 11。

### 安裝後必做：安裝 VMware Tools

不論使用上述哪種方法，在 Windows 11 安裝完成並進入桌面後，請務必點擊 `ESXi/vCenter` 控制台的 **動作 -> 客群作業系統 -> 安裝 VMware Tools**。進入 Windows 的虛擬光碟機執行 setup.exe 完成安裝並重啟，這能解決螢幕解析度無法調整與網路驅動丟失的問題。

## 卡在 Windows 11 的 OOBE（首次開機設定）網路連線畫面！

因為 Windows 11 強制要求連網才能完成設定，加上目前缺少網卡驅動，就會陷入死胡同。使用以下「跳過網路檢查」的標準秘訣，先進入桌面再補裝驅動：

### 步驟一：

1. 強制跳過網路檢查在目前卡住的網路連線畫面中，同時按下鍵盤上的 Shift + F10（某些筆電或環境可能需要按 Fn + Shift + F10）。
2. 此時畫面上會跳出一個 CMD 黑色命令提示字元視窗。
3. 在視窗中輸入以下指令（注意：反斜線是 \，字母不分大小寫）：

```cmd
OOBE\BYPASSNRO
```

4. 輸入完畢後按下 Enter 鍵。
5. 虛擬機器將會自動重新啟動。

### 步驟二：使用「本機帳號」進入桌面

1. 重新開機後，再次走一遍前面的語言與鍵盤配置設定。
2. 來到網路連線畫面時，右下角會多出一個 「我沒有網際網路 (I don't have internet)」 的超連結選項，請果斷點擊它。
3. 接下來點擊 「繼續進行有限設定 (Continue with limited setup)」。
4. 這樣就能直接設定「本機使用者名稱」與「密碼」，順利跳過微軟帳號登入，直接進入 Windows 11 桌面。

### 步驟三：進入桌面後補裝網卡驅動

進到桌面後，網路依舊是斷開的，此時請立刻補裝 VMware Tools：

1. 在 ESXi / vCenter 控制台，點擊該虛擬機器的 「動作 (Actions)」 -> 「客群作業系統 (Guest OS)」 -> 「安裝 VMware Tools」。
2. 開啟 Windows 11 內的「本機（這台電腦）」，雙擊進入 VMware Tools 虛擬光碟機。
3. 執行 setup64.exe 並一路點擊「下一步」完成典型安裝。
4. 安裝完成後，原本的 VMXNET3 高速虛擬網卡驅動就會瞬間載入，右下角的網路圖示就會恢復正常連線了！
