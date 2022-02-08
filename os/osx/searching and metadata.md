# seasrching and metadata

## Spotlight

osx 中, `Spotlight` 會建立 metadata database, 將檔案資料記錄, 方便系統使用. 一般 importer 路徑為 /System/Library/Spotlight/, /Library/Spotlight/.
按 ⌃ Space 開啟 `Spotlight`


---

## mdfind

使用 `Spotlight` 尋找檔案

```bash
osx:~ $ mdfind Terminal.app # 找尋 metadata 含有該字串的檔案
osx:~ $ mdfind -onlyin /Applications Terminal.app # 指定搜尋路徑
osx:~ $ mdfind "kMDItemCFBundleIdentifier == com.apple.*" # 找尋特定 attribute
osx:~ $ mdfind "kMDItemCFBundleIdentifier == 'com.apple.*' && kMDItemDisplayName != 'Terminal*'"
```


---

## mdls

顯示檔案所有 Attribute

```bash
osx:~ $ mdls /Applications/Utilities/Terminal.app
```


---

## mdutil

`Spotlight` 建立 index 工具

```bash
osx:~ $ sudo mdutil -s /Volumes/Macintosh\ HD # 顯示 indexing 狀態
osx:~ $ sudo mdutil -i off /Volumes/Macintosh\ HD # 關閉 indexing
osx:~ $ sudo mdutil -i on /Volumes/Macintosh\ HD # 開啟 indexing
```


---

## mdiport

```bash
osx:~ $ mdiport -L
osx:~ $ mdiport -A
```


---

## ls

```bash
osx:~ $ ls -l
osx:~ $ ls -l@
```


---

## GetFileInfo

```bash
osx:~ $ GetFileInfo /etc/hosts
```


---

## SetFile

```bash
osx:~ # SetFile -a v /etc/hosts
osx:~ # SetFile -a V /etc/hosts
```
