# wxPython


## Other


### Install wxPython on MacOSX 11.12

```
# downlaod wxPython
osx:~ $ wget http://downloads.sourceforge.net/wxpython/wxPython3.0-osx-3.0.2.0-cocoa-py2.7.dmg

# copy packacge
osx:~ $ mkdir repack_wxpython
osx:~ $ cd repack_wx
osx:~/repack_wxpython $ hdiutil attach ~/Downloads/wxPython3.0-osx-3.0.2.0-cocoa-py2.7.dmg
osx:~/repack_wxpython $ cp -r /Volumes/wxPython3.0-osx-3.0.2.0-cocoa-py2.7/wxPython3.0-osx-cocoa-py2.7.pkg .

# prepare install resource
osx:~/repack_wxpython $ mkdir pkg_root
osx:~/repack_wxpython $ cd pkg_root
osx:~/repack_wxpython/cd pkg_root $ pax -f ../wxPython3.0-osx-cocoa-py2.7.pkg/Contents/Resources/wxPython3.0-osx-cocoa-py2.7.pax.gz -z -r

osx:~/repack_wxpython $ mkdir scripts
osx:~/repack_wxpython $ cp wxPython3.0-osx-cocoa-py2.7.pkg/Contents/Resources/preflight scripts/preinstall
osx:~/repack_wxpython $ cp wxPython3.0-osx-cocoa-py2.7.pkg/Contents/Resources/postflight scripts/postinstall
osx:~/repack_wxpython $ hdiutil detach /Volumes/wxPython3.0-osx-3.0.2.0-cocoa-py2.7

# package
osx:~/repack_wxpython $ pkgbuild --root ./pkg_root --scripts ./scripts --identifier com.wxwidgets.wxpython wxPython3.0-py2.7.pkg

# install
osx:~/repack_wxpython $ installer -pkg wxPython3.0-py2.7.pkg -target "/Volumes/Macintosh HD"
```


### Run wxPython on MacOSX virtualenv

```
# create virtualenv project
osx:~ $ virtualenv --python=python2 py2env
osx:~ $ ln -s /Library/Python/2.7/site-packages/wxredirect.pth ~/py2env/lib/python2.7/site-packages/.

# source virtualenv environment
osx:~ $ source ~/py2env/bin/active
(py2env)osx:~ $ export PYTHONHOME=~/py2env
(py2env)osx:~ $ pip show wxPython

# run wx on virtualenv
(py2env)osx:~ $ /usr/bin/python wx_demo.py

```