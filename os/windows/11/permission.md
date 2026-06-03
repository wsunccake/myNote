## RunAs

```pwsh
Start-Process powershell -Verb RunAs
Start-Process wt -ArgumentList "nt -p `"PowerShell`"" -Verb RunAs

[Security.Principal.WindowsPrincipal]::new([Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
```

## SID

```pwsh
whoami
whoami /user
whoami /all
[System.Security.Principal.WindowsIdentity]::GetCurrent().User.Value

Get-CimInstance Win32_UserAccount | Select-Object Name, SID

Name               SID
----               ---
Administrator      S-1-5-21-2188033810-1219498728-1659733183-500
DefaultAccount     S-1-5-21-2188033810-1219498728-1659733183-503
defaultuser0       S-1-5-21-2188033810-1219498728-1659733183-1001
Guest              S-1-5-21-2188033810-1219498728-1659733183-501
lcladmin           S-1-5-21-2188033810-1219498728-1659733183-1002
WDAGUtilityAccount S-1-5-21-2188033810-1219498728-1659733183-504

Get-Acl <file> | Format-List AccessToString

AccessToString : S-1-543210-0-12-1-4217871452-1076386199-4264589969-1715598323 Deny  FullControl
                 DOMAIAN\USER Allow  FullControl


takeown /f <file>

SUCCESS: The file (or folder): "C:\<file>" now owned by user "DOMAIAN\USER".
```

Windows 的 SID 就像是身分證字號，結構通常長這樣：S-1-5-21-XXXX-XXXX-XXXX-RID

- S：代表這串字串是一個 SID。
- 1：版本號（目前固定是 1）。
- 5：發行機構代碼（5 代表 NT Authority 權限機構）。
- 21：代表這是一個網域或本機帳號。
- 中間那一長串數字：是網域或本機電腦的唯一識別碼。
- 最後面的數字（RID，相對識別碼）：這是最關鍵的使用者專屬 ID。

例如：看到結尾是 -500，代表它是內建的系統管理員（Administrator）；若是一般使用者，通常會從 -1000 或 -1001 開始往後編。

---

## DACL

```pwsh
# 徹底重置檔案權限，將其還原為繼承自上層資料夾的預設狀態（會洗掉所有奇怪的 Deny/Allow）
icacls <file> /reset

# 確保斬斷繼承，並清除所有繼承下來的權限
icacls <file> /inheritance:r

# 確保切斷繼承，並保留現有權限轉為獨立權限
icacls <file> /inheritance:d

# 重新授予本人唯一的完全控制權限
icacls <file> /grant:r "$($env:USERNAME):F"

# 移除使用者
icacls <file> /remove "<sid>"
icacls <file> /remove "Everyone"        # 特定使用者
icacls <file> /remove "DOMAIN\User"     # 網域使用者

# 增加使用者
# :F  =  Full Control
# :M  =  Modify
# :RX =  Read & Execute
# :R  =  Read
# :W  =  Write
icacls <file> /grant "<sid>：<perm>"
icacls <file> /grant "Everyone:RX"      # 新權限累加進去
icacls <file> /grant:r "DOMAIN\User:R"  # 直接覆蓋權限
```

## Windows Attributes

`Mode 的 5 個字元位階`

```pwsh
Get-ChildItem
ls
dir
gci

Get-ChildItem $env:HOMEPATH | Select-Object -First 10

    Directory: C:\Users

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d----         2026/5/18 下午 02:01                Documents
d-r--          2026/6/3 上午 09:21                Downloads
-a---         2026/5/25 上午 12:05             20 .lesshst
```

| Position | Item          | Explain                                                  |
| -------- | ------------- | -------------------------------------------------------- |
| 1        | d / Directory | 資料夾顯示 d，一般檔案顯示 -                             |
| 2        | a / Archive   | 檔案已被修改，可以用於備份（通常新建或改過的檔案都有 a） |
| 3        | r / Read-only | 檔案被鎖定，無法直接被修改或刪除                         |
| 4        | h / Hidden    | 隱藏檔，預設一般瀏覽看不到                               |
| 5        | s / System    | Windows 作業系統核心使用的檔案                           |

```pwsh
# r = Read-only
# h = Hidden
# a = Archive
# s = System
attrib +r <file>
attrib -h -r <file>

# Normal   = -a---
# ReadOnly = -ar--
# Hidden   = -a-h-
# System   = -a--s
# Archive  = -a---
Set-ItemProperty -Path <file> -Name Attributes -Value ReadOnly
Set-ItemProperty -Path <file> -Name Attributes -Value "ReadOnly, Hidden"
```
