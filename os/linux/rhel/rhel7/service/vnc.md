# VNC #


## Configuration ##

	# vnc server run as daemon:
	rhel:~ # cp /usr/lib/systemd/system/vncserver@.service /etc/systemd/system/
	rhel:~ # vi /etc/systemd/system/vncserver@.service    # 將底下 <USER> 換成開啟 VNC Service 的使用者
	[Unit]
	Description=Remote desktop service (VNC)
	After=syslog.target network.target

	[Service]
	Type=forking
	# Clean any existing files in /tmp/.X11-unix environment
	ExecStartPre=/bin/sh -c '/usr/bin/vncserver -kill %i > /dev/null 2>&1 || :'
	ExecStart=/sbin/runuser -l <USER> -c "/usr/bin/vncserver %i"
	PIDFile=/home/<USER>/.vnc/%H%i.pid
	ExecStop=/bin/sh -c '/usr/bin/vncserver -kill %i > /dev/null 2>&1 || :'

	[Install]
	WantedBy=multi-user.target


## Service ##

	rhel:~ # vi /etc/systemd/system/vncserver@.service /etc/systemd/system/vncserver@:1.service
	rhel:~ # systemctl enable vncserver@:1.service   # 建立 5901 port 的 VNC Service
	rhel:~ # systemctl start vncserver@:1.service