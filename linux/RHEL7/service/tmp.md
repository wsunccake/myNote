# tmpfiles #

## Configuration ##

	rhel:~ # cat /usr/lib/systemd/system/systemd-tmpfiles-clean.timer
	#  This file is part of systemd.
	#
	#  systemd is free software; you can redistribute it and/or modify it
	#  under the terms of the GNU Lesser General Public License as published by
	#  the Free Software Foundation; either version 2.1 of the License, or
	#  (at your option) any later version.

	[Unit]
	Description=Daily Cleanup of Temporary Directories
	Documentation=man:tmpfiles.d(5) man:systemd-tmpfiles(8)

	[Timer]
	OnBootSec=15min
	OnUnitActiveSec=1d

	rhel:~ # cat /etc/tmpfiles.d/tmp.conf
	#Type Path        Mode UID  GID  Age Argument
    d    /tmp/        1755 root root 7d6h -

	rhel:~ # systemd-tmpfiles --create [<config>.conf]    # create path via config
	rhel:~ # systemd-tmpfiles --clean [<config>.conf]     # clean path via config


## Service ##

	rhel:~ # systemctl start systemd-tmpfiles-clean.timer
	rhel:~ # systemctl status systemd-tmpfiles-clean.timer


# tmpwatch #

## Package ##

	rhel:~ # yum install tmpwatch

## Configuration ##

	rhel:~ # tmpwatch -umct 1 /tmp    # 刪除超過 1 小時未存取的檔案資料夾
	# u: atime
	# m: mtime
	# c: ctime
	# t: 僅 test 不真正執行

在 rhel 6 時, 沒有 systemd-tmpfiles-clean, 清除 tmp file 基本上是使用 tmpwatch + crontab

	# 配合 crontab
	rhel:~ # cat /etc/cron.daily/tmpwatch 
	flags=-umc
	/usr/sbin/tmpwatch "$flags" -x /tmp/.X11-unix -x /tmp/.XIM-unix \
	        -x /tmp/.font-unix -x /tmp/.ICE-unix -x /tmp/.Test-unix \
	        -X '/tmp/hsperfdata_*' 240 /tmp
	/usr/sbin/tmpwatch "$flags" 720 /var/tmp
	for d in /var/{cache/man,catman}/{cat?,X11R6/cat?,local/cat?}; do
	    if [ -d "$d" ]; then
	        /usr/sbin/tmpwatch "$flags" -f 720 "$d"
	    fi
	done