# VMware


## Shared folder

Guest 需安裝 VMware Tools, 在 Virtual Machaine \ Install VMware Tools 選項點選

在安裝 VMware Tools 前, 需確認以安裝 gcc

	guest:~ # yum install gcc kernel-headers kernel-devel    # 安裝 kernel lib 及 compiler

	guest:~ # mount /dev/cdrom /mnt/
	guest:~ # tar zxf /mnt/VMwareTools-9.9.2-2496486.tar.gz -C .
	guest:~ # umount /mnt
	guest:~ # vmware-tools-distrib/vmware-install.pl

vmware-install.pl 基本上編譯 vmware module 進目前的 kernel

	guest:~ # vmware-hgfsclient                              # 顯示 Host 分享的目錄
	guest:~ # ls /mnt/hgfs                                   # 分享目錄位於 /mnt/hgfs 底下
