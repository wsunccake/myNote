# snapper

snapper list-configs

Disable snapper's timeline snapshots

snapper -c root set-config "TIMELINE_CREATE=no"
snapper -c root set-config "TIMELINE_CREATE=yes"

Disable YaST snapshots

vi /etc/sysconfig/yast2
USE_SNAPPER=no
