# ubuntu 26.04

## network

### nic

```bash
ubuntu:~ # lspci -v
ubuntu:~ # ls -l /sys/class/net/
ubuntu:~ # ip link
```

### ip

`/etc/netplan/00-installer-config.yaml`

```yaml
network:
  ethernets:
    ens160:
      addresses:
        - 192.168.10.123/24
      match:
        macaddress: 00:11:22:33:44:55
      nameservers:
        addresses:
          - 8.8.8.8
          - 1.1.1.1
        search: []
      routes:
        - to: default
          via: 192.168.10.254
      set-name: ens160
    ens192:
      dhcp4: true
      dhcp6: true
      accept-ra: true
    ens224:
      dhcp4: false
      dhcp6: false
      accept-ra: false
      link-local: []
  version: 2
```

- ens160: up nic, static ip
- ens192: up nic, dhcp / dynamic ip
- ens224: up nic, no ip

```bash
ubuntu:~ # netplan try
ubuntu:~ # netplan apply
ubuntu:~ # ip addr
```

---

## service

### ssh

```bash
ubuntu:~ # apt install openssh-server

ubuntu:~ # systemctl enable sshd --now
ubuntu:~ # ufw allow OpenSSH
```

### rdp

```bash
ubuntu:~ # ufw allow 3389/tcp
ubuntu:~ # ufw allow 3390/tcp
```

---

### VM

### vmware

- 在 VMware開啟共用資料夾

1. 先將 Ubuntu 26.04 虛擬機關機。
2. 進入該虛擬機的「設定」(Settings) > 「共用」 (Sharing) 分頁。
3. 勾選 「啟用共用資料夾」 (Enable Shared Folders)。
4. 點擊「+」按鈕，選擇你想分享的 Mac 資料夾（例如取名為 Share）。
5. 點擊確定並將 Ubuntu 虛擬機開機。

- 在 Ubuntu 內安裝工具與掛載

1. 打開 Ubuntu 的終端機（Terminal）。
2. 安裝最新的開源版 VMware 工具

```bash
apt update
apt install open-vm-tools open-vm-tools-desktop
```

- open-vm-tools：核心基礎套件。處理底層系統與硬體整合，不論是伺服器（文字介面）還是桌面版都必須安裝。
  - 主機與虛擬機同步：讓 Mac 宿主機與 Ubuntu 虛擬機的時間保持完全同步。
  - 記憶體與電源管理：讓 VMware 能夠正常對 Ubuntu 進行安全關機、暫停（Suspend）或重啟，並優化記憶體動態分配（Memory Ballooning）。
  - 檔案系統共享（HGFS）：你目前最需要的功能！它內建了 vmhgfs-fuse 工具，負責讓 Ubuntu 能夠掛載 Mac 分享的資料夾。
  - 心跳偵測（Heartbeat）：向 VMware回報虛擬機的即時運行狀態與 IP 位址。

- open-vm-tools-desktop：擴充套件。專門處理圖形介面（GUI）與使用者體驗，只有在有安裝視窗系統的 Ubuntu 上才需要它。
  - 雙向剪貼簿（Clipboard Sharing）：讓你在 Mac 複製文字或圖片後，能直接在 Ubuntu 裡面貼上（或反過來）。
  - 檔案拖放（Drag and Drop）：可以直接把 Mac 桌面上的檔案，用滑鼠拖曳拉進 Ubuntu 桌面裡複製。
  - 解析度自動縮放（Dynamic Resolution）：當你用滑鼠去拉大、縮小 VMware 的視窗時，Ubuntu 的螢幕解析度會自動跟著變動，不會出現大黑邊或畫面模糊。
  - 滑鼠無縫無感切換：滑鼠游標可以直接移出、移入虛擬機視窗，不需要按快捷鍵釋放滑鼠。

3. 確認 Ubuntu 是否有成功讀取到 宿主主機 分享過來的目錄名稱：

```bash
ubuntu:~ # vmware-hgfsclient
```

4. 手動掛載測試

```bash
ubuntu:~ # mkdir -p /mnt/hgfs
ubuntu:~ # vmhgfs-fuse .host:/hgfs /mnt/hgfs -o allow_other,uid=1000,gid=1000

ubuntu:~ # mount | grep vmhgfs

ubuntu:~ # umount /mnt/hgfs
```

5. 寫入開機自動掛載

```bash
ubuntu:~ # cat /etc/fstab
.host:/hgfs /mnt/hgfs fuse.vmhgfs-fuse allow_other,uid=1000,gid=1000,defaults 0 0

ubuntu:~ # mount -a
```
