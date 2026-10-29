# Edge

## Mode & Maintenance

```bash
# 進入特權模式
Edge> enable

# 進入特權模式提示字元
Edge#

# 查看設備序號 (Serial Number)
Edge# show serial

# 啟動 SSH 服務
Edge# set ssh start

# 特殊維護模式 (Internal Shell)
Edge# !v54!
```

---

## Network Setup

```bash
# 進入網路設定模式
Edge# network

# 查看目前介面 IP 位址與網路狀態
Network# show interface address

# 設定介面 IP 位址
Network# set interface ip address
```

---

## DRS Configuration

```bash
# 進入代理程式連線設定模式
Edge# connect-agent

# 設定 DRS 伺服器網址 (預設或指定 DRS 位址)
(connect-agent)# set drs-addr drs.ruckuswireless.com

# 檢查代理程式連線與運作狀態
(connect-agent)# show status
```

---

## RuckusOne Enrollment

```bash
# 執行設備註冊 (請將 <OTP> 替換為 RuckusOne 產生的驗證碼)
Edge# enroll <OTP>
```
