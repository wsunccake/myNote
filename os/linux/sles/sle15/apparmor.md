# apparmor

AppArmor 是一種 Linux 安全模組 (Linux Security Module, LSM)，它的核心思想是「最小權限原則」（Principle of Least Privilege）

AppArmor 會根據設定檔 (Profile)，嚴格限制它可以做哪些事、不能做哪些事。這些限制可能包含：

- 讀寫檔案：只能讀取特定目錄下的檔案，不能寫入其他地方。
- 網路連線：只能連線到特定的 IP 或 Port。
- 執行程式：不能呼叫其他不安全的程式。
- 使用功能：限制使用某些特定的系統功能。

AppArmor 的設定檔可以有三種狀態：

- Enforce (強制)：這是最安全的模式。AppArmor 會嚴格執行設定檔中的所有規則。如果程式的行為違反了規則，AppArmor 會直接阻擋它，並將違規行為記錄下來。
- Complain (抱怨)：這是用來建立設定檔的模式。AppArmor 不會阻擋任何違規行為，但會記錄所有違反規則的行為。這對新手來說非常有用，因為你可以先讓程式在正常運作的狀況下跑一陣子，再檢查這些紀錄來建立你的規則。
- Disable (停用)：AppArmor 不會對這個程式做任何限制。

| 指令        | 用途                                                                 |
| ----------- | -------------------------------------------------------------------- |
| aa-status   | 顯示目前所有 AppArmor 設定檔的狀態。                                 |
| aa-enforce  | 將設定檔從「抱怨」模式切換到「強制」模式。                           |
| aa-complain | 將設定檔從「強制」模式切換到「抱怨」模式。                           |
| aa-disable  | 停用一個設定檔。                                                     |
| aa-genprof  | 自動產生設定檔。這是 AppArmor 最強大的功能之一，我們稍後會詳細介紹。 |
| aa-logprof  | 讀取日誌，根據違規紀錄自動更新設定檔。                               |

---

## service

```bash
sle:~ # systemctl status apparmor
```

---

## profile

```bash
sle:~ # apparmor_status
sle:~ # ls /etc/apparmor.d
sle:~ # aa-status

# enforce/complain
sle:~ # aa-complain /etc/apparmor.d/usr.sbin.dnsmasq
sle:~ # aa-enforce /etc/apparmor.d/usr.sbin.dnsmasq
sle:~ # ps auxZ

# enable/disable
sle:~ # aa-disable /etc/apparmor.d/usr.sbin.dnsmasq
sle:~ # ls -l /etc/apparmor.d/disable/*
sle:~ # aa-enabled /etc/apparmor.d/usr.sbin.dnsmasq
sle:~ # ls -l /etc/apparmor.d/disable/*
```
