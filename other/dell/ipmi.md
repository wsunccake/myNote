# IPMI

IPMI（Intelligent Platform Management Interface，智慧平台管理介面）是一種獨立於作業系統之外的硬體管理介面，允許系統管理員遠端對伺服器進行監控、維護與管理（如開關機、查看硬體狀態、遠端 Console 等），即使伺服器處於關機或作業系統當機狀態下也能運作。


## Linux

在 Linux 中，最常用的 IPMI 管理工具是 ipmitool。


### install

```bash
linux:~ # apt install ipmitool      # Debian / Ubuntu:
linux:~ # dnf install ipmitool      # RHEL / CentOS / Rocky Linux

# load module
linux:~ # modprobe ipmi_msghandler
linux:~ # modprobe ipmi_devintf
linux:~ # modprobe ipmi_si
```

### syntax

```bash
# local
linux:~ # ipmitool -I open <command>

# remote
linux:~ # ipmitool -I <interface> -H <address> -U <username> -P <password> <command>
# interface:
# open              Linux OpenIPMI Interface [default]
# imb               Intel IMB Interface
# lan               IPMI v1.5 LAN Interface
# lanplus           IPMI v2.0 RMCP+ LAN Interface
# serial-terminal   Serial Interface, Terminal Mode
# serial-basic      Serial Interface, Basic Mode
# usb               IPMI USB Interface(OEM Interface for AMI Devices)

# example
linux:~ # impitool help
linux:~ # impitool <command>
linux:~ # impitool <command> help

linux:~ # IPMI_CMD="ipmitool -I lanplus -H <hostname> -U <username> -P <password>"
```

```bash
# 直接在本機印出目前的 BMC IP，馬上知道它是多少
sudo ipmitool lan print 1

# 直接在本機設定 IP，完全不用擔心斷線問題
sudo ipmitool lan set 1 ipsrc static
sudo ipmitool lan set 1 ipaddr 10.0.1.50
sudo ipmitool lan set 1 netmask 255.255.255.0
sudo ipmitool lan set 1 defgw ipaddr 10.0.1.1

# 忘記 BMC 管理員密碼，Web UI 進不去，能在本地強制覆蓋 BMC 密碼
sudo ipmitool user set password 2 "NewPassword123"
```


### Usage

- 網路與帳號管理 / LAN & User Config

```bash
# 查看 BMC 網路設定
ipmitool lan print

# 設定 BMC IP 為 static IP
ipmitool lan set 1 ipsrc static
ipmitool lan set 1 ipaddr 192.168.1.100
ipmitool lan set 1 netmask 255.255.255.0
ipmitool lan set 1 defgw ipaddr 192.168.1.1

# 查看使用者
ipmitool user list

# 修改管理員密碼
ipmitool user set password <User ID> <New Password>
```

- 電源控制 / Chassis Power Control

```bash
ipmitool chassis power status       # 電源狀態
ipmitool chassis power on           # 開機
ipmitool chassis power soft         # 正常關機
ipmitool chassis power off          # 強制關機
ipmitool chassis power cycle        # 強制重啟
```

- 開機順序設定 / Boot Options

```bash
ipmitool chassis bootdev bios       # 設定下次開機進入 BIOS
ipmitool chassis bootdev pxe        # 設定下次從 PXE 網路開機
ipmitool chassis bootdev cdrom      # 設定下次從 光碟/虛擬媒體 開機
```

- 硬體狀態監控 / Sensors & Health

```bash
ipmitool sdr list                   # 查看所有感測器數據（溫度、電壓、風扇轉速等）
ipmitool sensor list                # 查看詳細 Sensor 門檻值與目前數值
ipmitool chassis status             # 查看總體系統健康狀況
```

- 系統事件日誌 / System Event Log, SEL

```bash
ipmitool sel list                   # 查看事件日誌
ipmitool sel info                   # 查看 SEL 詳細資訊
ipmitool sel clear                  # 清空事件日誌
```

- 遠端 Console 文字介面 / Serial-over-LAN, SOL

```bash
# 啟動 SOL 連線
ipmitool -I lanplus -H <BMC_IP> -U <USERNAME> -P <PASSWORD> sol activate

# 結束 SOL 連線
# 輸入 ~. 組合鍵退出。

# 強制中斷正在使用的 SOL 連線
ipmitool -I lanplus -H <BMC_IP> -U <USERNAME> -P <PASSWORD> sol deactivate
```

---

## ESXi

ESXi Direct Console (DCUI) 按 F2 -> Troubleshooting Options -> 啟用 SSH。

```bash
esxcli <option> <namespace> <cmd> <cmd option>
# namespace
#   daemon                Commands for controlling daemons built with Daemon SDK (DSDK).
#   device                Device manager commands
#   esxcli                Commands that operate on the esxcli system itself allowing users to get additional information.
#   fcoe                  VMware FCOE commands.
#   graphics              VMware graphics commands.
#   hardware              VMKernel hardware properties and commands for configuring hardware.
#   iscsi                 VMware iSCSI commands.
#   network               Operations that pertain to the maintenance of networking on an ESX host. This includes a wide
#                         variety of commands to manipulate virtual networking components (vswitch, portgroup, etc) as well as
#                         local host IP, DNS and general host networking settings.
#   nvme                  VMware NVMe driver operations.
#   rdma                  Operations that pertain to remote direct memory access (RDMA) protocol stack on an ESX host.
#   sched                 VMKernel system properties and commands for configuring scheduling related functionality.
#   software              Manage the ESXi software image and packages
#   storage               VMware storage commands.
#   system                VMKernel system properties and commands for configuring properties of the kernel core system and
#                         related system services.
#   vm                    A small number of operations that allow a user to Control Virtual Machine operations.
#   vsan                  VMware vSAN commands

esxcli --verion
esxcli --help
esxcli hardware --help 
esxcli hardware ipmi bmc set --help

esxcli hardware ipmi bmc get
esxcli hardware ipmi bmc sdr list
esxcli hardware ipmi bmc sel list
```
