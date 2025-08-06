# kvm

## introduction

Linux 虛擬化技術的發展, 是為了更有效地利用硬體資源、提高系統隔離性與彈性而逐步演進的. 從早期的軟體模擬到現在的硬體輔助虛擬化, 每一步都帶來了性能和效率的顯著提升.

1. 早期概念與軟體模擬

   虛擬化的概念其實很早就有了, 但在 Linux 環境下真正普及應用是從軟體模擬開始.
   此時主要特點:

   - 軟體層次實現: 主要透過軟體來模擬或轉譯 CPU 指令、記憶體和周邊設備.
   - 性能損耗較大: 由於需要額外的模擬或轉譯開銷.
   - 用途: 主要用於開發、測試、舊系統兼容性或在桌面環境中運行多個作業系統.

- Bochs (約 1997 年):

  Bochs 是一個開源的、高度可移植的 x86 模擬器. 它透過純軟體的方式模擬整個 PC 硬體, 讓你在一個作業系統（宿主機）中運行另一個作業系統（客戶機）, 即使兩者的指令集不同. 這種方式雖然靈活, 但由於完全模擬硬體, 性能非常低, 主要用於開發和測試目的, 而非生產環境.

- VMware Workstation (首發於 1999 年):

  VMware 是虛擬化領域的先驅之一. 他們的 Workstation 產品在 Linux 和 Windows 上都能運行. VMware 採用了更先進的技術, 介於純軟體模擬和硬體輔助虛擬化之間, 通常稱為二進位轉譯 (Binary Translation). 它會即時地將客戶機的特權指令轉譯成宿主機可以執行的指令, 而將非特權指令直接執行. 這種技術比 Bochs 快很多, 使得虛擬機在桌面上運行成為可能, 但仍存在一定的性能開銷. VMware 的成功證明了虛擬化在一般使用者和開發者中的潛力.

2. 半虛擬化 (Paravirtualization) - Xen 的崛起

   隨著虛擬化需求的增長, 人們開始尋找提升性能的方法. 半虛擬化應運而生, 它不要求客戶機完全不修改, 而是讓客戶機「意識」到自己運行在虛擬化環境中, 並對核心進行一些修改以直接與虛擬化層通信, 從而減少模擬開銷.

- Xen (首發於 2003 年):

  Xen 是一個具有里程碑意義的開源虛擬機器監視器 (Hypervisor). 它採用了半虛擬化 (Paravirtualization) 技術.

  - 工作原理: Xen 直接運行在硬體之上, 作為 Type-1 Hypervisor. 客戶機的作業系統核心需要經過修改（即「Xen-aware」）才能運行在 Xen 之上. 這些修改允許客戶機直接呼叫 Hypervisor 提供的 API 來執行特權操作, 而不是透過軟體模擬或二進位轉譯, 從而顯著提高了性能.
  - 優勢: 相較於完全軟體模擬, Xen 的半虛擬化提供了接近原生的性能, 特別適用於伺服器虛擬化.
  - 挑戰: 需要修改客戶機作業系統, 這限制了對未經修改的作業系統（如 Windows）的支援, 或需要結合完全虛擬化 (Full Virtualization) 技術來實現.

3. 硬體輔助虛擬化與整合入 Linux 核心

   隨著 Intel VT-x (2005 年) 和 AMD-V (2006 年) 等硬體虛擬化技術的出現, 虛擬化進入了一個新紀元. 這些 CPU 擴展指令集允許 Hypervisor 更高效地捕獲和處理客戶機的特權指令, 無需修改客戶機作業系統.

- QEMU (首發於 2003 年):

  QEMU 是一個開源的通用虛擬機器模擬器和模擬器.

  - 獨立運行時: QEMU 可以在沒有硬體虛擬化技術的情況下, 透過純軟體模擬來運行客戶機（類似 Bochs, 但更高效）. 它能夠模擬多種 CPU 架構, 所以可以用於跨平台虛擬化（例如在 x86 機器上模擬 ARM 處理器來運行 ARM Linux）.
  - 與 KVM 結合時: QEMU 的真正威力在於它作為一個虛擬機管理工具, 與 KVM 緊密結合. 當 QEMU 檢測到 KVM 模組可用時, 它會將客戶機的 CPU 指令執行委託給 KVM 處理, 而自己則負責模擬其他硬體設備（如網路卡、儲存控制器等）.

- KVM (Kernel-based Virtual Machine) (2007 年整合入 Linux 核心):

  KVM 是 Linux 虛擬化歷史上的一個重大突破.

  - 工作原理: KVM 是一個 Linux 核心模組, 它將 Linux 核心本身轉變為一個 Type-2 (Hosted) Hypervisor. KVM 利用了 Intel VT-x 和 AMD-V 等硬體輔助虛擬化技術. 這意味著客戶機的 CPU 指令可以直接在宿主機的 CPU 上執行, 而無需任何軟體模擬或二進位轉譯（除了少數需要 Hypervisor 介入的特權指令）, 因此提供了接近原生的性能.
    - 優勢:
      - 原生性能: 由於利用硬體特性, 性能損耗極小.
      - 無需修改客戶機: 可以運行任何未經修改的作業系統（包括 Windows 和各種 Linux 發行版）.
      - 深度整合 Linux 核心: KVM 作為核心模組, 可以直接利用 Linux 核心的排程器、記憶體管理和設備驅動等成熟功能, 簡化了虛擬化管理.
      - 開源且免費: 成為主流的開源虛擬化解決方案.
  - 與 QEMU 的關係: KVM 提供核心層的虛擬化功能, 而 QEMU 提供使用者空間的虛擬機管理和設備模擬. 兩者結合, 形成了一個完整的、高效的虛擬化解決方案.

---

## virsh

```bash
[host:~ ] # grep -E 'svm|vmx' /proc/cpuinfo
[host:~ ] # apt install qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils virtinst virt-manager
[host:~ ] # modprobe vhost_net
[host:~ ] # lsmod | grep vhost
[host:~ ] # echo "vhost_net" | tee -a /etc/modules

[host:~ ] # systemctl start libvirtd
[host:~ ] # systemctl enable libvirtd
[host:~ ] # systemctl status libvirtd

[host:~ ] # usermod -aG libvirt <user>
[host:~ ] # usermod -aG kvm <user>
```

```bash
[host:~ ] # virsh
[host:~ ] # virsh help
[host:~ ] # virsh nodeinfo
[host:~ ] # virsh list --all
[host:~ ] # virsh dumpxml <vm_id>|<vm_name>
[host:~ ] # virsh create <vm>.xml
[host:~ ] # virsh define <vm>.xml
[host:~ ] # virsh edit <vm_id>|<vm_name>
[host:~ ] # virsh undefine <vm_id>|<vm_name>

[host:~ ] # virsh start <vm_id>|<vm_name>
[host:~ ] # virsh autostart [--disable] <vm_id>|<vm_name>
[host:~ ] # virsh dominfo <vm_id>|<vm_name>
[host:~ ] # virsh shutdown <vm_id>|<vm_name>
[host:~ ] # virsh destroy <vm_id>|<vm_name>
[host:~ ] # virsh console <vm_id>|<vm_name>     # ctrl + ] to exit
```

### setup serial console

```bash
# for systemctl
[guest:~ ] # systemctl enable serial-getty@ttyS0
[guest:~ ] # systemctl start serial-getty@ttyS0
[guest:~ ] # systemctl status serial-getty@ttyS0
```

### setup vnc

```bash
[host:~ ] # virsh edit <vm_id>|<vm_name>
    <graphics type='spice' autoport='yes'>
      ...
    </graphics>
->
    <graphics type='vnc' port='-1' autoport='yes' listen='0.0.0.0'>
      <listen type='address' address='0.0.0.0'/>
    </graphics>

[host:~ ] # virsh vncdisplay <vm_id>|<vm_name>
[host:~ ] # virsh domdisplay <vm_id>|<vm_name>
```

---

## qemu

```bash
[host:~ ] # qemu-img convert -f qcow2 -O raw image.qcow2 image.img    # qcow2 -> raw
[host:~ ] # qemu-img convert -f vmdk -O raw image.vmdk image.img      # vmdk -> raw
[host:~ ] # qemu-img convert -f raw -O qcow2 image.img image.qcow2    # raw -> qcow2
[host:~ ] # qemu-img convert -f vmdk -O qcow2 image.vmdk image.qcow2  # vmdk -> qcow2
[host:~ ] # qemu-img info image.qcow2  # disk info
```
