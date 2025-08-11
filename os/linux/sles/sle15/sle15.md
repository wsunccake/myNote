# SLE 15

## introdution

SUSE (Software und System-Entwicklung) 是最早的商業 Linux 發行版之一，起源於德國，在歐洲和企業級市場擁有深厚的影響力。

1. 早期成立與德語市場的開拓 (1992 - 1990 年代末)

- 1992 年： SUSE 由 Roland Dyroff、Thomas Fehr、Burchard Steinbild 和 Hubert Mantel 在德國紐倫堡成立。最初，SUSE 是一家 UNIX 顧問公司，提供軟體服務並為德語市場銷售 UNIX 工具和發行版 (如 Slackware 和 S.u.S.E. Linux 0.98，一個修改過的 SLS 版本)。
- 1994 年： 發布了第一個完整的 SUSE Linux 發行版 (S.u.S.E. Linux 1.0)，這是一個基於 Slackware 且德語化的版本。這標誌著 SUSE 從販賣其他發行版轉向開發自己的發行版。
- 1996 年： 發布了第一個完全獨立開發的 SUSE Linux 發行版 (S.u.S.E. Linux 4.2)。這個版本引入了著名的 YaST (Yet another Setup Tool)，這是一個強大且易於使用的系統管理工具，成為 SUSE 的標誌性特色。YaST 讓複雜的 Linux 系統設定變得更加簡單直觀。

2. 商業化與企業級市場的擴張 (2000 年代初期)

進入 2000 年代，SUSE 開始更加注重企業級市場，提供商業支援和企業級解決方案。

- 2000 年： SUSE 成為第一家在 IBM 大型主機上提供 Linux 支援的企業，顯示其在企業級市場的雄心。
- 2001 年： 將其企業產品線重新命名為 SUSE Linux Enterprise Server (SLES)，明確區分其針對伺服器和企業客戶的版本。SLES 以其穩定性、可靠性、長期支援和對各種硬體架構的良好兼容性而聞名。

3. 所有權的變遷與持續發展 (2000 年代中期 - 至今)

SUSE 的歷史充滿了所有權的變動，但其對 Linux 和開源的承諾始終未變。

- 2003 年： 被美國軟體巨頭 Novell 收購。這次收購為 SUSE 帶來了更多資源和市場機會，但也引起了開源社群的一些關注。
- 2005 年： Novell 為了促進社群參與，推出了 openSUSE 計畫，將 SUSE Linux 的開發過程透明化並向社群開放，類似於 Red Hat 與 Fedora 的關係。openSUSE Leap 是一個基於 SLES 程式碼的穩定發行版，而 openSUSE Tumbleweed 則是一個滾動發行版，提供最新的軟體。
- 2011 年： Novell 及其資產（包括 SUSE）被 Attachmate Group 收購。在此期間，SUSE 作為一個獨立的業務部門繼續運營。
- 2014 年： Attachmate Group 被英國軟體公司 Micro Focus 收購。SUSE 再次成為 Micro Focus 旗下的一個業務部門。
- 2018 年： SUSE 被投資公司 EQT Partners 收購，成為一家完全獨立的軟體公司。這為 SUSE 帶來了更大的自主權，使其能夠更專注於其核心業務和開源創新。
- 2021 年： SUSE 成功在法蘭克福證券交易所上市，證明了其作為獨立開源公司在市場上的地位和價值。

---

## validate

```bash
sle:~ # ls SLE-15-SP2-Full-x86_64-GM-Media1.iso SLE-15-SP2-Full-x86_64-GM-Media2.iso

sle:~ # vi sle15sp2_sha256.txt
938dd99becf3bf29d0948a52d04bcd1952ea72621a334f33ddb5e83909116b55  SLE-15-SP2-Full-x86_64-GM-Media1.iso
c4c9393c35feffd3ffaea4a8860ae7428fe7bf996d202c4582a3abc1c4228604  SLE-15-SP2-Full-x86_64-GM-Media2.iso

sle:~ # sha256sum -c sle15sp2_sha256.txt
sle:~ # sha256sum SLE-15-SP2-Full-x86_64-GM-Media1.iso

sle:~ # sha256 SLE-15-SP2-Full-x86_64-GM-Media1.iso
```

---

## install

安裝時, 預設 filesystem 為 btrfs, 建議使用 xfs (效能較佳)

---

## setup

`repository`

```bash
# on local
sle:~ # mount /dev/sr0 /mnt
sle:~ # zypper rr -a
sle:~ # zypper ar /mnt/Module-Basesystem Basesystem
sle:~ # ls -d /mnt/{M,P}* | xargs -i zypper ar {} `basename {}`
sle:~ # zypper lr
sle:~ # ls /etc/zypp/repos.d/
sle:~ # yast repositories


# on http for apache2
sle:~ # zypper in apache2
sle:~ # systecmctl enable apache2
sle:~ # systecmctl start apache2
sle:~ # vi /etc/apache2/conf.d/repo.conf
Alias "/repo" "/mnt/"
<Directory "/mnt/">
	Options Indexes

	<IfModule !mod_access_compat.c>
		Require all granted
	</IfModule>
	<IfModule mod_access_compat.c>
		Order allow,deny
		Allow from all
	</IfModule>
</Directory>

sle:~ # systecmctl restart apache2
sle:~ # curl http://127.0.0.1/repo/
sel:~ # zypper ar http://127.0.0.1/repo/Module-Basesystem/ Module-Basesystem


# on http for nginx
sle:~ # zypper in ngin
sle:~ # systecmctl enable nginx
sle:~ # systecmctl start nginx
sle:~ # vi /etc/nginx/conf.d/repo.conf
server {
        listen 8080;
        listen [::]:8080;

        server_name .example.com;
        root /mnt;

        location / {
                autoindex on;
        }
}

sle:~ # systecmctl restart nginx
sle:~ # curl http://127.0.0.1:8080/
sle:~ # zypper ar http://127.0.0.1/Module-Basesystem/ Module-Basesystem


# on ftp
# on nfs
```

`firewall`

```bash
sle:~ # firewall-cmd --add-service=ssh,http --permament
sle:~ # firewall-cmd --add-ports=8080/tcp --permament
sle:~ # firewall-cmd --reload

sle:~ # yast firewall
```

`package`

```bash
sle:~ # zypper in vim mlocate
sle:~ # zypper in iputils psmisc
sle:~ # zypper in bash-completion
sle:~ # zypper in -t pattern yast2_basis

sle:~ # yast sw_single
```

`network`

```bash
sle:~ # yast lan

sle:~ # ls /etc/sysconfig/network/ifcfg-<nic>    # nic ip
sle:~ # ls /etc/sysconfig/network/ifroute-<nic>  # nic route
sle:~ # ls /etc/sysconfig/network/route          # default route

sle:~ # vi /etc/sysconfig/network/ifcfg-eth0
# for dhcp
NAME=''
BOOTPROTO='dhcp'
STARTMODE='auto'
ZONE=''

# for static
BOOTPROTO='static'
STARTMODE='auto'
IPADDR='192.168.1.1/24'
MTU='9000'
ZONE=''

sle:~ # ls /etc/sysconfig/network/route
# for static
default 192.168.0.1 - -


sle:~ # systemctl status wicked
sle:~ # systemctl status wickedd

sle:~ # wicked --help
sle:~ # wicked show all
sle:~ # wicked ifstatus all

sle:~ # wicked ifup eth0
sle:~ # wicked ifdown eth0
sle:~ # wicked show-config eth0

sle:~ # ifup eth0
sle:~ # ifdown eth0
sle:~ # ifstatus eth0
sle:~ # ifprobe eth0
```

`sys log`

```bash
sle:~ # zypper in rsyslog
sle:~ # systemctl enable rsyslog
sle:~ # systemctl start rsyslog

sle:~ # vi /etc/systemd/journald.conf
ForwardToSyslog=yes
...

sle:~ # systemctl restart systemd-journald

sle:~ # journalctl -f
sle:~ # journalctl -n 100 -f
# log level: "emerg" (0), "alert" (1), "crit" (2), "err" (3), "warning" (4), "notice" (5), "info" (6), "debug" (7)
sle:~ # journalctl -p err
sle:~ # journalctl -p 3
```

`fs`

```bash
sle:~ # vi /etc/fstab
sle:~ # mount -a
sle:~ # mount /dev/sda1 <mnt>
sle:~ # mount -oloop image.iso <mnt>
sle:~ # mount -oremount,rw <mnt>
sle:~ # mount -oremount,ro <mnt>
sle:~ # mount -t iso9660 /dev/sr0 <mnt>
sle:~ # cat /etc/mtab
sle:~ # cat /proc/mounts
sle:~ # umount <mnt>
sle:~ # fuser -l
sle:~ # fuser -mv <mnt>
sle:~ # fuser -mk <mnt>
sle:~ # fusermount /dev/sda1 <mnt>
sle:~ # fusermount -u <mnt>

sle:~ # lsblk [-fs|-p]
sle:~ # df -h
sle:~ # du -hs [.|*]
sle:~ # cat /proc/partitions

sle:~ # fdisk [-l] /dev/sda
sle:~ # gdisk [-l] /dev/sda
sle:~ # parted [-l] /dev/sda
sle:~ # partprobe

sle:~ # mkfs -t xfs /dev/sda1
sle:~ # mkfs.xfs /dev/sda1
sle:~ # mkswap  /dev/sda2
```

`serial`

```bash
sle:~ # rpm -ql systemd
sle:~ # ls -l /etc/systemd/system/getty.target.wants/serial-getty@ttyS0.service
# -> /usr/lib/systemd/system/serial-getty@.service

sle:~ # systemctl enable serial-getty@ttyS0.service --now
```

---

## security

### fail2ban

```bash
sle:~ # zypper addrepo https://download.opensuse.org/repositories/network:utilities/SLE_15_SP2/network:utilities.repo
sle:~ # zypper refresh
sle:~ # zypper install python-pyinotify

sle:~ # zypper addrepo https://download.opensuse.org/repositories/security/SLE_15_SP2/security.repo
sle:~ # zypper refresh
sle:~ # zypper install fail2ban

sle:~ # systemctl enable fail2ban --now
```

---

## hardware

### intel cpu

`cpu`

P-States: Performance States

T-States: Throttling States

S-States: Sleeping States

G-States: Global States

C-States: CPU States

```bash
# package
sle:~ # zypper in util-linux
sle:~ # zypper in cpupower

# command
## cpu state
sle:~ # cat /proc/cpuinfo
sle:~ # lscpu
sle:~ # lscpu -ae

## cpu frequency governor
sle:~ # cpupower frequency-info
sle:~ # cpupower frequency-info --governors
sle:~ # cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
sle:~ # cpupower frequency-set -g performance

## cpu frequency set
sle:~ # dmesg|grep 'MHz processor'

sle:~ # cat /sys/devices/system/cpu/cpufreq/policy*/scaling_available_frequencies
sle:~ # cat /sys/devices/system/cpu/cpufreq/policy*/scaling_available_governors
sle:~ # cat /sys/devices/system/cpu/cpufreq/policy*/scaling_cur_freq
sle:~ # cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_max_freq

sle:~ # cpupower frequency-info --driver
sle:~ # cpupower frequency-info --governors

sle:~ # cpupower [-c all|0|0-2|0,2] frequency-info
sle:~ # cpupower frequency-set -f 2.1GHz
sle:~ # cpupower monitor -m Mperf
sle:~ # cpupower monitor -l
sle:~ # turbostat

# intel p_state
sle:~ # grep CONFIG_X86_AMD_PSTATE=y /boot/config-*
sle:~ # grep CONFIG_X86_INTEL_PSTATE=y /boot/config-*
sle:~ # dmesg | grep pstate
sle:~ # lsmod | grep -E 'intel_pstate|acpi_cpufreq'
sle:~ # lsmod | grep -E 'rapl|powerclamp|cpufreq'

## enable pstate when boot (grub2)
sle:~ # vi /etc/default/grub
GRUB_CMDLINE_LINUX="intel_idle.max_cstate=1 intel_pstate=enable processor.max_cstate=1"
GRUB_CMDLINE_LINUX_DEFAULT="fbcon=scrollback:1024k"
sle:~ # grub2-mkconfig -o /boot/grub2/grub.cfg
sle:~ # reboot

## intel p_state - performance
sle:~ # cat /sys/devices/system/cpu/intel_pstate/status
sle:~ # echo active > /sys/devices/system/cpu/intel_pstate/status
sle:~ # cat /sys/devices/system/cpu/intel_pstate/no_turbo
sle:~ # echo 1 > /sys/devices/system/cpu/intel_pstate/no_turbo

sle:~ # x86_energy_perf_policy
sle:~ # x86_energy_perf_policy performance

# enable when booting
sle:~ # cat << EOF >> /etc/init.d/boot.local
sleep 60
cpupower frequency-set -g performance
EOF

sle:~ # chmod +x /etc/init.d/boot.local
sle:~ # reboot
```

```conf
# /boot/grub2/grub.cfg.

# Uncomment to set your own custom distributor. If you leave it unset or empty, the default
# policy is to determine the value from /etc/os-release
GRUB_DISTRIBUTOR=
GRUB_DEFAULT=saved
GRUB_HIDDEN_TIMEOUT=0
GRUB_HIDDEN_TIMEOUT_QUIET=true
GRUB_TIMEOUT=8
GRUB_CMDLINE_LINUX_DEFAULT="splash=silent resume=/dev/disk/by-uuid/12345678-1234-1234-1234-123456789abc mitigations=auto quiet security=apparmor crashkernel=334M,high crashkernel=72M,low"
GRUB_CMDLINE_LINUX=""

# Uncomment to automatically save last booted menu entry in GRUB2 environment

# variable `saved_entry'
# GRUB_SAVEDEFAULT="true"

# This works with Linux (no patch required) and with any kernel that obtains
# the memory map information from GRUB (GNU Mach, kernel of FreeBSD ...)
# GRUB_BADRAM="0x01234567,0xfefefefe,0x89abcdef,0xefefefef"
#Uncomment to disable graphical terminal (grub-pc only)

GRUB_TERMINAL="gfxterm"
# The resolution used on graphical terminal
#note that you can use only modes which your graphic card supports via VBE

# you can see them in real GRUB with the command `vbeinfo'
GRUB_GFXMODE="auto"
# Uncomment if you don't want GRUB to pass "root=UUID=xxx" parameter to Linux
# GRUB_DISABLE_LINUX_UUID=true
#Uncomment to disable generation of recovery mode menu entries

# GRUB_DISABLE_RECOVERY="true"
#Uncomment to get a beep at grub start

# GRUB_INIT_TUNE="480 440 1"
GRUB_BACKGROUND=/boot/grub2/themes/SLE/background.png
GRUB_THEME=/boot/grub2/themes/SLE/theme.txt
SUSE_BTRFS_SNAPSHOT_BOOTING="true"
GRUB_DISABLE_OS_PROBER="true"
GRUB_ENABLE_CRYPTODISK="n"
GRUB_CMDLINE_XEN_DEFAULT="vga=gfx-1024x768x16 crashkernel=406M\<4G"
```

---

## compiler

### gnu

```bash
sle:~ # zypper se -t pattern devel_basis
sle:~ # zypper info -t pattern devel_basis
sle:~ # zypper in -t pattern devel_basis
```

### intel

```bash
# intel oneAPI Base Toolkit
sle:~ # sh l_BaseKit_p_2023.1.0.46401_offline.sh
# -> Math Kernel Library / MKL

# intel oneAPI HPC Toolkit
sle:~ # sh l_HPCKit_p_2023.1.0.46346_offline.sh
# -> intel C++ Compiler Classic
# -> intel Fortran Compiler
# -> intel Fortran Compiler Classic
# -> intel MPI Library
```

```bash
# usage
sle:~ $ ls /opt/intel/oneapi

# set variable
sle:~ $ source /opt/intel/oneapi/setvars.sh

sle:~ $ source /opt/intel/oneapi/compiler/latest/env/vars.sh
sle:~ $ source /opt/intel/oneapi/mpi/latest/env/vars.sh
sle:~ $ source /opt/intel/oneapi/mkl/latest/env/vars.sh

# create module file
sle:~ $ /opt/intel/oneapi/modulefiles-setup.sh
```

`c compiler`

```bash
sle:~ $ cat << EOF >> hello.c
#include <stdio.h>

int main() {
printf("hello\n");
return 0;
}
EOF
sle:~ $ icc -o hello hello.c
sle:~ $ ./hello
```

`fortran compiler`

```bash
sle:~ $ cat << EOF >> hello.f
write ( \*, '(a)' ) 'hello'

      stop
      end

EOF
sle:~ $ ifort -o hello hello.f
sle:~ $ ./hello
```

`mpi`

```bash
sle:~ $ cat << EOF >> hello_mpi.c
#include <mpi.h>
#include <stdio.h>

int main(int argc, char\*\* argv) {
MPI_Init(NULL, NULL);

    int world_size;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

    int world_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

    char processor_name[MPI_MAX_PROCESSOR_NAME];
    int name_len;
    MPI_Get_processor_name(processor_name, &name_len);

    printf("Hello world from processor %s, rank %d out of %d processors\n",
           processor_name, world_rank, world_size);

    MPI_Finalize();

}
EOF
sle:~ $ mpicc -o hello_mpi hello_mpi.c
sle:~ $ mpirun -np 2 ./hello_mpi

# other command
sle:~ $ cpuinfo
sle:~ $ impi_info -a
```

---

## other

### term

```bash
sle:~ # infocmp -D
/etc/terminfo
/usr/share/terminfo

sle:~ # ls /etc/terminfo
sle:~ # ls /usr/share/terminfo/*

# garbled character
# method 1. setup TERM
sle:~ # env TERM=vt100|xterm yast

# method 2. setup NCURSES
sle:~ # export NCURSES_NO_UTF8_ACS=1
sle:~ # yast
```
