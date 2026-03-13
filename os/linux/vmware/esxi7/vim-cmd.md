# vim-cmd

在 ESXi 的世界裡，vim-cmd 是管理虛擬機最強大、最直接的命令列工具。當 Web 介面卡住、或是 Shell Script 自動化測試時，它是首選。

Virtual Infrastructure Management Compact Command Line。


```bash
vim-cmd [<option>]  [<command>]

vim-cmd -h
vim-cmd -v
```

## `vmsvc/` (Virtual Machine Service)

用來管理虛擬機的生命週期

```bash
vim-cmd vmsvc/getallvms
vim-cmd vmsvc/get.config <vm_id>

vim-cmd vmsvc/power.on <vm_id>
vim-cmd vmsvc/power.off <vm_id>

vim-cmd vmsvc/destrory <vm_id>

# vmx
VMX_FILE=/vmfs/volumes/<datastore>/<vm>/<vmx_file>
ls $VMX_FILE
grep numvcpus $VMX_FILE
greo memSize $VMX_FILE
grep ethernet0 $VMX_FILE
```

---

## `hostsvc/` (Host Service)

用來管理這台 ESXi 實體主機本身的資源。

```bash
vim-cmd hostsvc/datastore/listsummary   # all datastore
vim-cmd hostsvc/datastore/info <datastore>

hostsvc/maintenance_mode_enter：進入維護模式。
hostsvc/net/query_networkhint：查看實體網卡連到了哪台 Switch。
hostsvc/runtimeinfo：查看 CPU/Memory 使用率。
```
---

## `solo/` (Standalone/Local Service)

處理單機環境下的環境變數與登入權限。

---

## `vimsvc/` (Virtual Infrastructure Management)

更底層的 VIM 服務控制。

---

## `hbrsvc/` (Host Based Replication)

處理虛擬機的複寫與災難恢復（Replication）。