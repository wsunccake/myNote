# ovftool 5

## introdution

`ovftool`（VMware OVF Tool）是一個強大的命令列公用程式，專門用於在不同虛擬化平台之間匯入、匯出及轉換虛擬機器鏡像。它支援 OVF (Open Virtualization Format) 與 OVA (Open Virtualization Archive) 標準。

1. `ovftool` 功能介紹

`ovftool` 的核心作用是充當不同格式與平台間的「轉譯器」。

- 跨平台遷移：將虛擬機器從 VMware vSphere 遷移到 VMware Workstation、Fusion，或是相反路徑。
- 格式轉換：
  - VMX/VMDK -> OVF/OVA（適合分發與歸檔）。
  - OVF/OVA -> vSphere/vCloud Director（部署至雲端環境）。
- 自動化與 CI/CD：由於是命令列工具，它被廣泛用於自動化測試流程、基礎設施即代碼（IaC）以及 Jenkins 等流水線中的虛擬機部署。
- 封裝與驗證：在封裝過程中，它會檢查 OVF 檔案的完整性與 XML 結構是否符合標準。

2. 演進歷史與技術背景

**第一階段：標準的誕生 (2007 - 2009)**

在早期的虛擬化市場中，每個供應商（VMware, Microsoft, Citrix）都有自己的私有格式。為了實現互操作性，VMware 與 Dell、HP、IBM 及 Microsoft 共同向 DMTF（分散式管理任務組）提交了 OVF 規範。

- 2007年：OVF 1.0 規範發佈。
- 2009年：ovftool 隨之成為 VMware 推廣 OVF 標準的主要工具，取代了早期功能較單一的匯入導出精靈。

### 第二階段：雲端與大數據時代 (2010 - 2015)

隨著 vCloud Director 與 vSphere 的成熟，ovftool 增加了對雲端環境的支援：

- 支援 vApp：開始支援包含多個虛擬機的複雜層級結構。
- 安全性增強：引入了對 SHA-1 與 SHA-256 簽署驗證的支持，確保下載的鏡像未經篡改。
- OVF 2.0 發佈 (2013)：增加了對網路配置、硬體拓撲及更高級儲存策略的支援，ovftool 也同步更新以相容新標準。

### 第三階段：現代自動化與容器化競爭 (2016 至今)

在現今的環境中，雖然容器技術（Docker/K8s）盛行，但 ovftool 依然是企業級虛擬機管理的基石：

- 效能優化：針對大型虛擬磁碟（數 TB 等級）的傳輸進行了並行化與壓縮優化。
- REST API 整合：雖然它本身是 CLI，但其後台邏輯與 VMware Cloud 的自動化部署深度整合。
- 跨架構支援：持續更新以支援最新的硬體版本（Hardware Version 21+）以及 NVMe 控制器等新硬體模擬。

3. 至今仍然重要

儘管現在有許多 GUI 工具（如 vSphere Client），但 ovftool 具備以下不可替代的優勢：

- 穩定性：在大文件傳輸中比瀏覽器上傳更穩定，支援斷點續傳。
- 參數控制：可以精確指定目標儲存（Datastore）、網路映射（Network Mapping）以及部署屬性（Deployment Option）。
- 無頭操作 (Headless)：適合在沒有圖形介面的 Linux 伺服器上執行任務。

---

## require

```bash
# rocky 10
linux:~ # dnf install libxcrypt-compat libnsl

# debian 13
linux:~ # apt install libcrypt1 libnsl2
```

---

## downlaod

[Open Virtualization Format (OVF) Tool](https://developer.broadcom.com/tools/open-virtualization-format-ovf-tool/latest)

---

## install

```bash
linux:~ # unzip VMware-ovftool-5.0.0-24781994-lin.x86_64.zip -d /opt
linux:~ # ls /opt/ovftool
linux:~ # ln -s /opt/ovftool/ovftool /usr/local/bin/.
linux:~ # which ovftool
```

---

## usage

```bash
linux:~ # ovftool vi://<username>:<password>@<esxi_ip>
```

```bash
export ESXI_IP=<esxi_server>
export ESXI_USERNAME=<esxi_username>
export ESXI_PASSWORD=<esxi_password>
export ESXI_URL=vi://${EXSI_USERNAME}:${ESXI_PASSWORD}@${ESXI_IP}
# export ESXI_URL=vi://${EXSI_USERNAME}@${ESXI_IP}
# export ESXI_URL=vi://${ESXI_IP}

export DATASTORE="datastore1"
export PORT_GROUP="VM Network"
export OVF_NIC_CONNECTION="bridged"
export OVF_FILE=<ova_file>

show_version() {
  ovftool --version
}

show_ova() {
  local ova=$1
  ovftool $OVF_FILE
}

show_vm() {
  local vm=$1
  ovftool $ESXI_URL/$vm
}

import_ova() {
  local vm=$1
  ovftool --noSSLVerify \
    --acceptAllEulas \
    --name="$vm" \
    --datastore="$DATASTORE" \
    --net:"$OVF_NIC_CONNECTION"="$PORT_GROUP" \
    --diskMode=thin \
    --diskSize:0=1024 \
    $OVF_FILE \
    $ESXI_URL
}
```

---

## qcow2 to ova

```bash
# rocky 10
linux:~ # dnf install qemu-img

# debian 13
linux:~ # apt install qemu-utils
```

```bash
linux:~ # curl -OL https://download.cirros-cloud.net/0.6.2/cirros-0.6.2-x86_64-disk.img
linux:~ # ls cirros-0.6.2-x86_64-disk.img

# QCOW2 -> VMDK
linux:~ # qemu-img convert -f qcow2 -O vmdk \
  -o subformat=streamOptimized \
  cirros-0.6.2-x86_64-disk.img \
  cirros-0.6.2.vmdk

# create VMX file
linux:~ # vi cirros.vmx

# pack to OVA
linux:~ # ovftool cirros.vmx cirros-0.6.2.ova

# check OVA
linux:~ # ovftool --verifyOnly cirros-0.6.2.ova

# import OVA
linux:~ # ovftool --noSSLVerify \
  --acceptAllEulas \
  --datastore="datastore1" \
  --name="CirrOS-062" \
  --net:"bridged"="VM Network" \
  cirros-0.6.2.ova \
  vi://<ESXi_IP>

linux:~ # ovftool --noSSLVerify \
  --powerOn \
  vi://<ESXi_IP>/CirrOS-062"
```

`cirros.vmx`

```conf
.encoding = "UTF-8"
config.version = "8"
virtualHW.version = "10"
guestOS = "otherlinux-64"
memsize = "256"
numvcpus = "1"
scsi0.present = "TRUE"
scsi0.virtualDev = "lsilogic"
scsi0:0.present = "TRUE"
scsi0:0.fileName = "cirros-0.6.2.vmdk"
ethernet0.present = "TRUE"
ethernet0.virtualDev = "e1000"
ethernet0.startConnected = "TRUE"
ethernet0.addressType = "generated"
```
