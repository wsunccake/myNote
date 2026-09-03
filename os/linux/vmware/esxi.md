# ESXi

```bash
~ # vmware -vl
```

http://<esxi_ip>/ui

---

## file format

### `VMDK` (Virtual Machine Disk)

    VMDK 是 虛擬硬碟檔案，它是虛擬機器的核心。一個 VMDK 檔案就像是實體電腦的硬碟一樣，裡面包含了作業系統、應用程式和所有資料。

    - 儲存虛擬資料：VMDK 檔案儲存著虛擬機器的一切資料。
    - 多種格式：VMDK 格式有很多種，例如 thin-provisioned（精簡配置，用多少佔多少）、thick-provisioned（厚配置，一次佔滿所有空間）等。
    - 平台通用性：儘管最初由 VMware 開發，但因為其廣泛應用，現在許多其他虛擬化平台（如 VirtualBox）也支援這種格式。

### `OVF` (Open Virtualization Format)

    OVF 是一種 開放標準的虛擬機器描述檔。它不是虛擬硬碟，而是一個 XML 格式的文字檔案，扮演著「說明書」的角色。

    - 描述虛擬機器：OVF 檔案會詳細說明虛擬機器的組態，例如：
        - 需要多少 CPU 和記憶體。
        - 虛擬硬碟的名稱和類型。
        - 虛擬網路卡的數量和組態。
        - 作業系統的類型和版本。
    - 獨立於平台：OVF 的目的是讓虛擬機器能夠在不同虛擬化平台之間輕鬆遷移。當您從 vSphere 匯出一個 OVF 範本，它可以被 VirtualBox 或其他支援 OVF 的軟體匯入。
    - 一個 OVF 範本通常包含多個檔案：一個 OVF 範本不只有 ovf 檔案本身，還會包括 .vmdk 和 .mf 檔案。

### `OVA` (Open Virtual Appliance)

    OVA 是單一檔案的虛擬設備，它是將 OVF 範本的所有相關檔案打包成一個 .tar 壓縮檔。

    - 簡化傳輸與部署：OVA 的主要優點是方便。由於所有組件（ovf、vmdk、mf）都被壓縮在一個 .ova 檔案中，因此更容易進行下載、上傳和部署。
    - 就是 OVF 的壓縮包：您可以將一個 .ova 檔案想成是一個資料夾，裡面包含了所有必要的 .ovf、.vmdk 和 .mf 檔案，只是這個資料夾被壓縮成單一檔案了。

### `MF` (Manifest)

    MF 是驗證檔案完整性的清單。它是一個小型的文字檔案，用來確保 OVF 範本在傳輸過程中沒有被惡意篡改或損壞。

    - 包含雜湊值：.mf 檔案會列出 OVF 範本中所有檔案（包括 .ovf 和 .vmdk）的 SHA 雜湊值。
    - 防止竄改：當您部署 OVA/OVF 檔案時，虛擬化軟體會重新計算每個檔案的 SHA 雜湊值，並與 .mf 檔案中記錄的值進行比對。如果兩者不符，就會出現 SHA digest does not match 錯誤，這代表檔案可能已被修改，部署就會被中止以確保安全。

### `VMX` (VMware Virtual Machine Configuration File )

    VMX 主要作用是告訴 VMware 的虛擬化平臺（如 ESXi、vCenter、Workstation 等）如何配置和啟動一個虛擬機器。

    - 格式非常簡單，採用**鍵值對（key = "value"）**的形式。以下是一些常見的內容範例：
    - 虛擬硬體版本：virtualHW.version = "17"
        這個值非常重要，它定義了虛擬機器的硬體相容性版本，例如 "17" 代表 vmx-17，與 ESXi 7.0 相容。這是您在部署 vmx-21 的 OVA 檔案時，遇到錯誤的根本原因。
    - 虛擬機器基本資訊：
        displayName = "我的伺服器"：虛擬機器在介面中顯示的名稱。
        guestOS = "windows10-64"：客體作業系統的類型。
    - 硬體資源配置：
        memsize = "8192"：分配的記憶體大小，單位為 MB。
        numvcpus = "4"：分配的虛擬 CPU 數量。
    - 儲存與裝置配置：
        scsi0:0.fileName = "MyDisk.vmdk"：指定虛擬硬碟檔案的名稱和路徑。
        ethernet0.networkName = "VM Network"：虛擬網卡所連接的網路名稱。
        usb.present = "TRUE"：是否啟用 USB 控制器。

---

## tip

```bash
# change prompt
esxi: ~ # echo 'PS1="\w # "' >> /etc/profile.local

# change password policy
esxi: ~ # vi /etc/pam.d/passwd

#password   requisite    /lib/security/$ISA/pam_passwdqc.so retry=3 min=disabled,disabled,disabled,7,7
#password   sufficient   /lib/security/$ISA/pam_unix.so use_authtok nullok shadow sha512
password   sufficient   /lib/security/$ISA/pam_unix.so nullok shadow sha512
password   required     /lib/security/$ISA/pam_deny.so

# ssh public key
esxi: ~ # cat /etc/ssh/keys-root/authorized_keys

# network
esxi: ~ # esxcli network nic list
esxi: ~ # esxcli network ip interface ipv4 get
```

---

## ovftool

```bash
linux:~ # ovftool vi://<username>:<password>@<esxi_ip>

# update ova
linux:~ # ovftool --acceptAllEulas --noSSLVerify --diskMode=thin --name=<vm_name> --datastore=<data_store> --network=<vm_network> <vm>.ova vi://<username>:<password>@<esxi_ip>

# the provided manifest file is invalid
linux:~ # tar xf <xxx>.ova
linux:~ # rm <xxx>.mf               # SHA digest: the manifest validates
linux:~ # vi <xxx>.ovf              # a
linux:~ # ovftool <xxx>.ovf <new_xxx>.ova
```

---

## usage

```bash
# help message
esxi:~ # vim-cmd -h

# list version
esxi:~ # vim-cmd -v

# list vm
esxi:~ # vim-cmd vmsvc/getallvms

# power state
esxi:~ # vim-cmd vmsvc/power.getstate <vm_id>

# update vm config
esxi:~ # ls /vmfs/volumes/<data_store>/<vm_name>
esxi:~ # vi /vmfs/volumes/<data_store>/<vm_name>/<vm_name>.vmx
# setup cpu
numvcpus = "1"
sched.cpu.affinity = "all"
sched.cpu.htsharing = "any"

# setup mem
sched.mem.min = "1024"
sched.mem.affinity = "all"
sched.mem.shares = "normal"

# setup nic
ethernet0.address = "00:11:22:33:44:55"
ethernet0.checkMACAddress = "FALSE"
ethernet0.addressType = "static"         # generated, vpx, static
# ethernet0.generatedAddress

# enable svm or vmx
vhv.enable = "TRUE"

# lauch vm
esxi:~ # vim-cmd vmsvc/power.on <vm_id>

# delete vm
esxi:~ # vim-cmd vmsvc/power.off <vm_id>
esxi:~ # vim-cmd vmsvc/destroy <vm_id>
esxi:~ # ls /vmfs/volumes/<data_store>/<vm_name>

# other
esxi: ~ # vim-cmd hostsvc/net/info | grep "mac ="
```

---

## clone vm

```bash
esxi:~ # cd /vmfs/volumes/datastore1
esxi:~/vmfs/volumes/datastore1 # mkdir new_vm
esxi:~/vmfs/volumes/datastore1 # vmkfstools -i ./origin/origin.vmdk ./new_vm/new_vm.vmdk -d thin -a buslogic
```

```text
Click "Create / Register VM" show "New virtual machine" on web ui

1. Select create type => Create a new virtual machine

...

6 Customize settings  => Add hard disk => Existing hard disk
(Select new_vm.vmdk)
```
