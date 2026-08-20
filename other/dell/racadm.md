# RACADM

RACADM (Remote Access Controller Admin) 是 Dell 專為 iDRAC 開發的命令列管理工具。簡單來說，它就是「不用開 Web 網頁介面，直接用 Terminal / Command Line 控制 Dell 伺服器」的工具。
可以直接透過 SSH 連線到 iDRAC 執行 RACADM。在 Rocky Linux 10 本地端需安裝 Dell 官方套件。

## install

OS: Rocky Linux 10

```bash
rocky:~ # wget -q -O - https://linux.dell.com/repo/hardware/dsu/bootstrap.cgi | bash
rocky:~ # dnf install -y srvadmin-idracadm7 [--nogpgcheck]

rocky:~ # ln -s /opt/dell/srvadmin/bin/idracadm7 /usr/local/bin/racadm
rocky:~ # racadm version
rocky:~ # racadm help
```

## Usage

`iDrac 7`

```bash
admin1 -> racadm help
admin1 -> racadm help <subcommand>
```

`Rocky Linux 10`

```bash
# Local RACADM
rocky:~ # racadm help
rocky:~ # racadm help <subcommand>

# Remote RACADM
rocky:~ # racadm -r <IDRAC_HOST> -u <IDRAC_USER> -p <IDRAC_PASS> help
rocky:~ # racadm -r <IDRAC_HOST> -u <IDRAC_USER> -p <IDRAC_PASS> help <subcommand>

# => combine
rocky:~ # RACADM_BIN=racadm
rocky:~ # RACADM_BIN="racadm -r <IDRAC_HOST> -u <IDRAC_USER> -p <IDRAC_PASS>"
```

---

## Info

```bash
racadm help <subcommand>

racadm getsvctag                    # 查詢 Service Tag (ST)
racadm getsysinfo                   # 查詢伺服器型號、網卡、BIOS 版本等概況
racadm getsensorinfo                # 查詢硬體健康狀態 (風扇、電源、溫度)
racadm serveraction powerstatus     # 查詢當前開機/關機狀態
racadm swinventory                  # 列出伺服器上所有組件的軟韌體版本
```

```bash
racadm serveraction powerup         # 開機
racadm serveraction powercycle      # 重啟
```

```bash
# Job Queue
racadm jobqueue view
racadm jobqueue delete -j
racadm jobqueue delete -j ALL

# Remote Image
racadm remoteimage -s                                   # Show Status
racadm remoteimage -c -l http://<IP>/<file>.iso         # Connect Image
racadm remoteimage -d                                   # Disconnect Image

# Boot from VCD
racadm set iDRAC.ServerBoot.BootOnce 1
racadm set iDRAC.ServerBoot.FirstBootDevice VCD-DVD

# Reboot
racadm serveraction powercycle
```

---

## Q & A

OSD35: Lifecycle Controller is not enabled. To enable Lifecycle Controller, reboot the server. During POST, press F2 to enter System Setup. Go to iDRAC Settings -> Lifecycle Controller, select enable, and save the changes. 

```bash
racadm set LifecycleController.LCAttributes.LifecycleControllerState 1
racadm racreset soft
```
