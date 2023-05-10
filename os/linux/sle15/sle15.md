# SLE15

## validate

```bash
sle:~ # ls SLE-15-SP2-Full-x86_64-GM-Media1.iso SLE-15-SP2-Full-x86_64-GM-Media2.iso

sle:~ # vi sle15sp2_sha256.txt
938dd99becf3bf29d0948a52d04bcd1952ea72621a334f33ddb5e83909116b55  SLE-15-SP2-Full-x86_64-GM-Media1.iso
c4c9393c35feffd3ffaea4a8860ae7428fe7bf996d202c4582a3abc1c4228604  SLE-15-SP2-Full-x86_64-GM-Media2.iso

sle:~ # sha256sum -c sle15sp2_sha256.txt
sle:~ # sha256sum SLE-15-SP2-Full-x86_64-GM-Media1.iso
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
sle:~ # grub2-mkconfig -o > /boot/grub2/grub.cfg
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
