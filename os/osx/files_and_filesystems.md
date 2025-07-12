`diskutil`

```bash
osx:~ # diskutil list
osx:~ # diskutil info -all
osx:~ # diskutil eraseDisk MS-DOS "WIN10" MBR /dev/disk2
osx:~ # diskutil eraseDisk ExFAT "WIN10" GPT /dev/disk2
osx:~ # diskutil unmount /dev/disk2s2
osx:~ # diskutil unmountDisk /dev/disk2
osx:~ # diskutil eject /dev/disk2
```

`hdiutil`

disk image utility

```bash
osx:~ # hdiutil mountvol /dev/sdb1 				# mount filesytem
osx:~ # hdiutil mount win.iso 					# mount iso
osx:~ # hdiutil unmount /mnt/pt 				# unmount filesystem
osx:~ # hdiutil attach xxx.dmg 					# mount dmg
osx:~ # hdiutil info 							# show mount dmg info
osx:~ # hdiutil detach /Volumes/xxx 			# unmount dmg
osx:~ # hdiutil create pkg.dmg -srcfolder dir # create dmg
```

`dd`

```bash
# build usb linux boot
osx:~ # dd if=linux.iso of=/dev/rdisk2 bs=1m status=progress
```

`mount`

```bash
osx:~ # mount -t hfs -o nosuid,-w,-m=755 /dev/disk2s9 /tmp
osx:~ # /sbin/mount_hfs -o nosuid -w -m 755 /dev/disk2s9 /tmp
```

`pkgutil`

相當是 rpm, dpkg

```bash
osx:~ # pkgutil --pkgs 				# rpm -qa
osx:~ # pkgutil --files pkg 		# rpm -ql pkg
osx:~ # pkgutil --files-info path 	# rpm -qf path
```

`installer`

Mac os x 安裝軟體同常有兩種格式, 一是 .app, 另一種是 .pkg. .app 直接複製到 /Applications 目錄下即可使用; 而 .pkg 需透過 installer 指令安裝

```bash
osx:~ # installer -pkg foo.pkg -target "/Volumes/Macintosh HD"
osx:~ # cp -r foo.app /Applications
```

`pkgbuild`

`ls`

`GetFileInfo`

`SetFile`

`xattr`
