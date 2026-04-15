# kali tools

## wordlists

wordlists（字典檔）是滲透測試的靈魂。無論是破解密碼、爆破目錄還是攻擊無線網路，工具都需要一份強大的「名單」來進行比對。預設將這些字典統一存放在： `/usr/share/wordlists/`

```bash
kali:~ # apt install wordlists

kali:~ # ls /usr/share/wordlists/rockyou.txt.gz
kali:~ # gzip -d /usr/share/wordlists/rockyou.txt.gz
```

| 目錄/檔案     | 用途說明                                                     | 常用配合工具      |
| ------------- | ------------------------------------------------------------ | ----------------- |
| dirb/         | Web 目錄與檔案掃描。包含 common.txt, big.txt, small.txt 等。 | dirb, gobuster    |
| dirbuster/    | 專為目錄掃描設計，內容比 dirb 更豐富。                       | DirBuster, ffuf   |
| fern-wifi/    | 針對 Wi-Fi 破解的常用密碼字典。                              | Fern WiFi Cracker |
| metasploit/   | "包含服務預設密碼、用戶名（如 SSH, Telnet, HTTP）。"         | msfconsole        |
| fasttrack.txt | 包含前 200 個最常見的密碼，適合進行「快速測試」。            | hydra, nmap       |
| wfuzz/        | 用於 Fuzzing（模糊測試）的各種 Payload。                     | wfuzz, ffuf       |

---

## dirb

dirb: Web Content Scanner, 透過「字典攻擊」（Dictionary-based attack）的方式，對 Web 伺服器進行暴力破解，藉此尋找隱藏的目錄、檔案或敏感路徑

```bash
kali:~ # apt install wordlists

kali:~ $ dirb http://<web> [<wordlist_file>]
```

| 參數 | 說明                                                       | 範例                                     |
| ---- | ---------------------------------------------------------- | ---------------------------------------- |
| -a   | 定義 User-Agent 標頭（偽裝成瀏覽器）。                     | dirb http://url -a "Mozilla/5.0"         |
| -X   | 在每個字典單字後加上特定的副檔名。                         | dirb http://url -X .php,.html            |
| -o   | 將掃描結果儲存到檔案中。                                   | dirb http://url -o result.txt            |
| -p   | 使用代理伺服器（Proxy）。                                  | dirb http://url -p 127.0.0.1:8080        |
| -c   | 設定 Cookie（用於需要登入後的掃描）。                      | dirb http://url -c "ID=123; SESSION=xyz" |
| -z   | 設定掃描延遲（毫秒），防止請求過快被防火牆封鎖。           | dirb http://url -z 100                   |
| -r   | 非遞迴掃描（預設 DIRB 會自動對發現的子目錄進行遞迴掃描）。 | dirb http://url -r                       |
| -i   | 忽略大小寫。                                               | dirb http://url -i                       |

DIRB 經典且穩定，但與其他現代工具相比有其優缺點：

- 優點：簡單易用、內建遞迴掃描、Kali 原生支援。
- 缺點：速度較慢（非非同步 I/O）、輸出介面較傳統。
- 替代方案：
  - **ffuf**：目前最快、功能最強大的 Fuzzing 工具（Go 編寫）。
  - **dirsearch**：Python 編寫，配色清楚且支援多線程。
  - **Gobuster**：使用 Go 編寫，速度極快，適合處理大字典。

---

## hydra

hydra: kali 最著名且功能最強大的 連線協議暴力破解工具。如果說 DIRB 是用來找「路徑」，那麼 Hydra 就是用來找「門票」（帳號密碼）。它支援超過 50 種協議，包括 SSH、FTP、Telnet、MySQL、HTTP-Form-Post、RDP 等，速度極快且支援並行（Parallel）連線。

```bash
kali:~ $ hydra [-l <username> | -L <username_file>] [-p <password> | -P <password_file>] [-t <thread_num>] [service://<target_ip>[:<port>][/<url>]]
# service://<target_ip>[:<port>][/<url>], ssh, rdp, ftp, http
```

---

## john

John the Ripper（簡稱 John 或 JtR）是 Kali Linux 中最頂級的 離線密碼破解工具。如果說 Hydra 是在門口不斷猜帳密試圖「登入」，那麼 John 就是在你已經拿到對方的密碼加密檔（Hash）後，在自己的電腦上瘋狂計算比對，直到還原出原始密碼為止。

1. Wordlist Mode（字典模式）

最常用的模式。讀取一個單字列表（如 rockyou.txt），將每個單字加密後比對 Hash。

```bash
kali:~ $ john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
```

2. Single Crack Mode（單一模式）

這招非常聰明。它會利用使用者名稱（Username）或其變體來進行破解。例如帳號是 john，它會試 john123、John! 等。這是破解弱密碼最快的方法。

```bash
kali:~ $ john --single hash.txt
```

3. Incremental Mode（增量模式 / 暴力破解）

當字典都沒效時的最後手段。它會嘗試所有可能的字元組合（a, b, c... aa, ab...），直到找到為止。極度耗時。

```bash
kali:~ $ john --incremental hash.txt
```
