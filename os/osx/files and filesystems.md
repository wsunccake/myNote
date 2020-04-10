`hdiutil`

disk image utility

	osx:~ $ sudo hdiutil mountvol /dev/sdb1 # mount filesytem
	osx:~ $ sudo hdiutil unmount /mnt/pt # unmount filesystem
	osx:~ $ sudo hdiutil attach xxx.dmg # mount dmg
	osx:~ $ sudo hdiutil info # show mount dmg info
	osx:~ $ sudo hdiutil detach /Volumes/xxx # unmount dmg
	osx:~ $ sudo hdiutil create pkg.dmg -srcfolder dir # create dmg


`mount`

	osx:~ $ sudo mount -t hfs -o nosuid,-w,-m=755 /dev/disk2s9 /tmp
	osx:~ $ sudo /sbin/mount_hfs -o nosuid -w -m 755 /dev/disk2s9 /tmp


`pkgutil`

相當是 rpm, dpkg

	osx:~ $ pkgutil --pkgs # rpm -qa
	osx:~ $ pkgutil --files pkg # rpm -ql pkg
	osx:~ $ pkgutil --files-info path # rpm -qf path


`installer`

Mac os x 安裝軟體同常有兩種格式, 一是 .app, 另一種是 .pkg. .app 直接複製到 /Applications 目錄下即可使用; 而 .pkg 需透過 installer 指令安裝

	osx:~ $ sudo installer -pkg foo.pkg -target "/Volumes/Macintosh HD"
	osx:~ $ sudo cp -r foo.app /Applications


`pkgbuild`


`ls`

`GetFileInfo`

`SetFile`

`xattr`