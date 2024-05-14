# environment modules

## install

```bash
debian:~ # apt install environment-modules
```

---

## usage

```bash
linux:~ $ module avail
linux:~ $ module list
linux:~ $ module add|load <modulefile>
linux:~ $ module rm|unload <modulefile>
linux:~ $ module purge
linux:~ $ module reload

linux:~ $ module help <modulefile>
linux:~ $ module path <modulefile>
linux:~ $ module show <modulefile>
```

---

## environment variable

```bash
linux:~ $ echo $MODULESHOME
linux:~ $ echo $MODULEPATH
linux:~ $ echo $MODULEPATH_modshare
linux:~ $ echo $MODULES_CMD
```

default path: /usr/share/modules/modulefiles

---

## modulefile

```bash
linux:~ # mkdir -p /usr/local/foo/{bin,lib}
linux:~ # echo 'echo "Now: $(date)"' > /usr/local/foo/now
linux:~ # chmod +x /usr/local/foo/bin/now
linux:~ # /usr/local/foo/bin/now

linux:~ # vi $MODULESHOME/modulefiles
#%Module1.0
##
## foo modulefile
##
proc ModulesHelp { } {
    puts stderr "\tfoo module\n"
}

module-whatis   "set /usr/local/foo to FOO_HOME environment variable"

#conflict        bar
#prereq          baz

set             foo_home            /usr/local/foo
setenv          FOO_HOME            ${foo_home}

append-path     PATH                ${foo_home}/bin
prepend-path    LD_LIBRARY_PATH     ${foo_home}/lib
```

---

## ref

[Environment Modules](http://modules.sourceforge.net/)
