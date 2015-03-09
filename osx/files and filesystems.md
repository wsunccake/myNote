`hdiutil`

disk image utility

	osx:~ $ sudo hdiutil mountvol /dev/sdb1 # mount filesytem
	osx:~ $ sudo hdiutil unmount /mnt/pt # unmount filesystem
	osx:~ $ sudo hdiutil attach xxx.dmg # mount dmg
	osx:~ $ sudo hdiutil detach /Volumes/xxx # unmount dmg
	osx:~ $ sudo hdiutil create pkg.dmg -srcfolder dir # create dmg

`mount`

	osx:~ $ sudo mount -t hfs -o nosuid,-w,-m=755 /dev/disk2s9 /tmp
	osx:~ $ sudo /sbin/mount_hfs -o nosuid -w -m 755 /dev/disk2s9 /tmp