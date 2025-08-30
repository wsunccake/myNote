# pxe

## history

PXE（Preboot eXecution Environment）的演進歷史可以追溯到上世紀 90 年代末，它從一個單純的網路開機技術，逐步演變成現代資料中心和雲端環境中不可或缺的自動化部署工具。

1. 早期網路開機技術（1980s-1990s）

在 PXE 出現之前，網路開機的概念就已經存在。早期的技術主要依賴於一些私有或非標準的協定，例如 RPL（Remote Initial Program Load）。RPL 允許客戶端從伺服器載入一個開機程式，但它通常受限於特定的硬體供應商，且缺乏互通性。這個階段的網路開機技術複雜且不通用，主要用於大型企業內部，用於啟動無硬碟工作站。

2. PXE 的誕生與標準化（1999）

PXE 技術的出現徹底改變了網路開機的生態。它由 Intel 和 SystemSoft 共同開發，並在 1999 年成為一個公開的行業標準。

- 核心創新： PXE 結合了 DHCP 和 TFTP 這兩個標準協定，實現了跨硬體平台的通用性。
  - DHCP： 用於自動獲取 IP 位址，並提供 TFTP 伺服器的位址及開機檔案名稱。
  - TFTP： 用於傳輸開機所需的輕量級檔案（如開機載入器、核心等）。
- 影響： 這一標準化讓任何符合 PXE 規範的硬體都可以透過網路開機。它不再局限於特定廠商，而是成為一個開放的、通用的技術，為後續的自動化部署奠定了基礎。

3. 擴展與應用普及（2000s-2010s）

隨著伺服器虛擬化和資料中心規模的擴大，PXE 的應用場景變得更加多元。

- 自動化安裝： 結合 Kickstart（Red Hat） 或 AutoYaST（SUSE） 這樣的自動化安裝工具，PXE 不僅能開機，還能實現全自動化的作業系統安裝，無需人工干預。這對於部署數百甚至數千台伺服器的資料中心來說，是極大的效率提升。
- 客製化開機環境： 開發者利用 PXE，可以輕鬆地載入各種客製化的開機環境，例如磁碟修復工具、記憶體測試程式（Memtest86+）或各種救援模式，這在系統維護和故障排除時非常有用。

4. 現代演進與 UEFI 整合（2010s-至今）

進入現代，隨著硬體架構從傳統的 BIOS 轉向 UEFI（Unified Extensible Firmware Interface），PXE 技術也隨之演進。

- iPXE 的出現： iPXE 是一個功能更強大的開源 PXE 韌體。它不僅支援傳統的 PXE 功能，還能直接支援 HTTP、iSCSI、AoE 等更多協定，甚至可以直接從 URL 載入開機檔案。這大大簡化了設定，並提升了傳輸速度。
- UEFI 上的 PXE： UEFI 上的網路開機稱為 UEFI Network Stack 或 PXE over IPv6。它基於相同的 DHCP 和 TFTP 概念，但使用 UEFI 規範來管理網路介面。這使得在現代伺服器上實現 PXE 成為可能，並提供了更快的開機速度和更強大的功能。
- 與雲端和容器技術的整合： 在現代雲端運算環境中，儘管大多數虛擬機的部署不再直接依賴 PXE，但 PXE 仍然是**裸機部署（Bare-Metal Provisioning）**的關鍵技術。許多 IaaS（Infrastructure as a Service）平台使用 PXE 來自動化部署底層的 Hypervisor 或作業系統，為虛擬化和容器化提供基礎。

## ISC-DHCP + TFTP + HTTP

tftp server: 192.168.0.1
isc-dhcp server: 192.168.0.1
http server: 192.168.0.1

### TFTP

[tftp](./tftp.md)

```bash
pxe:~ # mkdir -p /srv/tftpboot/sle15sp7
pxe:~ # mount -oloop SLE-15-SP7-Full-x86_64-GM-Media1.iso /mnt
pxe:~ # cp /mnt/boot/x86_64/loader/linux /srv/tftpboot/sle15sp7/.
pxe:~ # cp /mnt/boot/x86_64/loader/initrd /srv/tftpboot/sle15sp7/.

# PXE
pxe:~ # mkdir -p /srv/tftpboot/BIOS
pxe:~ # cp /usr/share/syslinux/pxelinux.0 /srv/tftpboot/BIOS/.
pxe:~ # cp -r /mnt/EFI /srv/tftpboot/
pxe:~ # mkdir -p /srv/tftpboot/pxelinux.cfg
pxe:~ # vi /srv/tftpboot/pxelinux.cfg/default

# permission
pxe:~ # chown -R tftp:tftp /srv/tftpboot
pxe:~ # chmod -R 755 /srv/tftpboot

# test
pxe:~ # tftp 192.168.0.1 -c get pxelinux.0
```

```conf
# /srv/tftpboot/pxelinux.cfg/default
DEFAULT linux
PROMPT 0
TIMEOUT 100
MENU TITLE SUSE Linux Enterprise Server 15

LABEL linux
    MENU LABEL SLES 15 Installation
    KERNEL sle15sp7/linux
    APPEND initrd=sle15sp7/initrd install=http://192.168.0.1/sle15/
```

### isc-dhcp

[isc-dhcp](./isc-dhcp.md)

```conf
# /etc/dhcpd.conf
# The following lines are optional
option domain-name "example.com";                     # domain name
option domain-name-servers 8.8.8.8;                   # dns
option routers 192.168.0.1;                           # default gw
option ntp-servers 192.168.0.1;                       # ntp
ddns-update-style none;
default-lease-time 3600;

# The following lines are required
option arch code 93 = unsigned integer 16;            # client system architecture type
subnet 192.168.0.0 netmask 255.255.255.0 {
  next-server 192.168.0.1;                            # tftp
  range dynamic-bootp 192.168.0.101 192.168.0.150;
  default-lease-time 14400;
  max-lease-time 172800;
  host hpc2 {
    fixed-address 192.168.0.11;
    hardware ethernet 52:54:00:93:fb:f4;
  }
#  filename "pxelinux.0";
  if option arch = 00:09 {
    filename "/EFI/BOOT/bootx64.efi";   # x86-64 UEFI clients to bootx64.efi
  } else {
    filename "pxelinux.0";              # BIOS clients to pxelinux.0
  }
}
```

### http

[apache2](./apache2.md)

```bash
pxe:~ # mount -oloop SLE-15-SP7-Full-x86_64-GM-Media1.iso /mnt
```

```conf
# /etc/apache2/conf.d/sle15.conf
Alias /sle15 "/mnt"

<Directory "/mnt">
    Options Indexes FollowSymLinks
    AllowOverride None
    Require all granted
</Directory>
```
