# CRON #

## Package ##

	rhel:~ # yum install cronie


## Configuration ##

	# white and black list for user
	rhel:~ # cat /etc/cron.allow
	rhel:~ # cat /etc/cron.deny

	# white and black list for job
	rhel:~ # cat /etc/cron.daily/jobs.allow
	rhel:~ # cat /etc/cron.daily/jobs.deny

	# crontab
	rhel:~ # ls /etc/crontab
	SHELL=/bin/bash
	PATH=/sbin:/bin:/usr/sbin:/usr/bin
	MAILTO=root
	HOME=/
	# For details see man 4 crontabs
	# Example of job definition:
	# .---------------- minute (0 - 59)
	# | .------------- hour (0 - 23)
	# | | .---------- day of month (1 - 31)
	# | | | .------- month (1 - 12) OR jan,feb,mar,apr ...
	# | | | | .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
	# | | | | |
	# * * * * * user-name command to be executed
	0 * * * * root ps axo etime,pid,cmd | awk '/tcpdump/ && $1 !~ /^[0-9][0-9]:[0-9][0-9]$/{print $2}' | xargs -i kill -9 {}
	0 * * * * root find /pcap_dir -name "*.pcap" -amin +60 -exec rm {} \;
	0 0 * * * root find /img_dir -type f -not -name '*.img' -ctime +14 -exec rm {} \;
	

	rhel:~ # ls /etc/cron.d

	# crontab by time
	rhel:~ # ls /etc/cron.hourly
	rhel:~ # ls /etc/cron.daily
	rhel:~ # ls /etc/cron.monthly
	rhel:~ # ls /etc/cron.weekly

	# cron command
	rhel:~ # crontab -e                # edit crontab
	0 0 * * * find /tmp_dir -type d -empty -exec rmdir "{}" \;
	rhel:~ # crontab -l                # list crontab
	rhel:~ # crontab -u [<user>] -r    # remove crontab

	rhel:~ # ls /var/spool/cron        # save all users crontab


## Service ##

	rhel:~ # systemctl start crond.service
	rhel:~ # systemctl enable crond.service
	rhel:~ # systemctl status crond.service


# Anacron #

## Package ##

	rhel:~ # yum install cronie-anacron


## Configuration ##

	cat /etc/anacrontab
	SHELL=/bin/sh
	PATH=/sbin:/bin:/usr/sbin:/usr/bin
	MAILTO=root
	# the maximal random delay added to the base delay of the jobs
	RANDOM_DELAY=45
	# the jobs will be started during the following hours only
	START_HOURS_RANGE=3-22
	#period in days   delay in minutes   job-identifier   command
	1         5     cron.daily    nice run-parts /etc/cron.daily
	7         25    cron.weekly   nice run-parts /etc/cron.weekly
	@monthly  45    cron.monthly  nice run-parts /etc/cron.monthly


# AT #

## Package ##

	rhel:~ # yum install at


## Configuration ##

	# white and black list for user
	rhel:~ # cat /etc/at.allow
	rhel:~ # cat /etc/at.deny

	rhel:~ # at now + 5days
	at> date
	at> # 輸入 Ctrl^D 離開

	rhel:~ # at 13:25 -f halt.sh
	rhel:~ # cat halt.sh
	/sbin/shutdown -h 0

	# at command
	rhel:~ # at -l
	rhel:~ # atq
	rhel:~ # at -c at_id
	rhel:~ # at -r at_id


## Service ##

	rhel:~ # systemctl start atd.service
	rhel:~ # systemctl enable atd.service
	rhel:~ # systemctl status atd.service

