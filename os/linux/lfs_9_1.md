# LFS 9.1 

## prepare

### verify package

```bash
host:~ # cat > version-check.sh << "EOF"
#!/bin/bash
# Simple script to list version numbers of critical development tools
export LC_ALL=C
bash --version | head -n1 | cut -d" " -f2-4
MYSH=$(readlink -f /bin/sh)
echo "/bin/sh -> $MYSH"
echo $MYSH | grep -q bash || echo "ERROR: /bin/sh does not point to bash"
unset MYSH

echo -n "Binutils: "; ld --version | head -n1 | cut -d" " -f3-
bison --version | head -n1

if [ -h /usr/bin/yacc ]; then
  echo "/usr/bin/yacc -> `readlink -f /usr/bin/yacc`";
elif [ -x /usr/bin/yacc ]; then
  echo yacc is `/usr/bin/yacc --version | head -n1`
else
  echo "yacc not found" 
fi

bzip2 --version 2>&1 < /dev/null | head -n1 | cut -d" " -f1,6-
echo -n "Coreutils: "; chown --version | head -n1 | cut -d")" -f2
diff --version | head -n1
find --version | head -n1
gawk --version | head -n1

if [ -h /usr/bin/awk ]; then
  echo "/usr/bin/awk -> `readlink -f /usr/bin/awk`";
elif [ -x /usr/bin/awk ]; then
  echo awk is `/usr/bin/awk --version | head -n1`
else 
  echo "awk not found" 
fi

gcc --version | head -n1
g++ --version | head -n1
ldd --version | head -n1 | cut -d" " -f2-  # glibc version
grep --version | head -n1
gzip --version | head -n1
cat /proc/version
m4 --version | head -n1
make --version | head -n1
patch --version | head -n1
echo Perl `perl -V:version`
python3 --version
sed --version | head -n1
tar --version | head -n1
makeinfo --version | head -n1  # texinfo version
xz --version | head -n1

echo 'int main(){}' > dummy.c && g++ -o dummy dummy.c
if [ -x dummy ]
  then echo "g++ compilation OK";
  else echo "g++ compilation failed"; fi
rm -f dummy.c dummy
EOF

host:~ # bash version-check.sh
```

---

### require pacakge

#### centos 8

```bash
centos:~ # dnf install epel-release
centos:~ # dnf install dnf-plugins-core
centos:~ # dnf config-manager --set-enabled PowerTools
centos:~ # dnf install @'Development Tools'
centos:~ # dnf install bison texinfo
```


#### kali

```bash
kali:~ $ sudo su -

kali:~ # rm /bin/sh
kali:~ # ln -s /bin/sh /bin/bash
kali:~ # apt install bison
kali:~ # apt install texinfo
```


### partition

#### format disk

```bash
root:~ # lsblk

# fdisk
root:~ # fdisk /dev/<disk>

# parted
root:~ # parted /dev/<disk>
(parted) help
(parted) unit
(parted) mklable [msdos]
(parted) mkpart [primary linux-swap 512B 2GiB]
(parted) mkpart [primary ext4 2GiB -1]
(parted) print

root:~ # parted -s /dev/sda mklabel msdos
root:~ # parted -s /dev/sda mkpart primary linux-swap 512B 2GiB
root:~ # parted -s /dev/sda mkpart primary ext4 2GiB 100%
```

#### make filesystem

```bash
root:~ # mkswap /dev/sda1 
root:~ # mkfs.ext4 /dev/sda2

# mount disk
root:~ # export LFS=/mnt/lfs
root:~ # mkdir -pv $LFS
root:~ # mount -v -t ext4 /dev/<disk> $LFS

root:~ # swapon /dev/sda1
```


### download package

```bash
root:~ # mkdir -v $LFS/sources
root:~ # chmod -v a+wt $LFS/sources
root:~ # wget http://linuxfromscratch.org/lfs/view/stable-systemd/wget-list
root:~ # wget --input-file=wget-list --continue --directory-prefix=$LFS/sources

root:~ # wget http://linuxfromscratch.org/lfs/view/stable-systemd/md5sums --directory-prefix=$LFS/sources
root:~ # pushd $LFS/sources
root:sources # md5sum -c md5sums
root:~ # popd
```


### lfs user

#### create user

```bash
root:~ # mkdir -v $LFS/tools
root:~ # ln -sv $LFS/tools /

root:~ # groupadd lfs
root:~ # useradd -s /bin/bash -g lfs -m -k /dev/null lfs
root:~ # passwd lfs
root:~ # chown -v lfs $LFS/tools
root:~ # chown -v lfs $LFS/sources
root:~ # su - lfs
```


#### change user

```bash
lfs:~ $ cat > ~/.bash_profile << "EOF"
exec env -i HOME=$HOME TERM=$TERM PS1='\u:\w\$ ' /bin/bash
EOF

lfs:~ $ cat > ~/.bashrc << "EOF"
set +h
umask 022
LFS=/mnt/lfs
LC_ALL=POSIX
LFS_TGT=$(uname -m)-lfs-linux-gnu
PATH=/tools/bin:/bin:/usr/bin
export LFS LC_ALL LFS_TGT PATH
EOF

lfs:~ $ source ~/.bash_profile
echo $LFS
```

```
Important

The build instructions assume that the Host System Requirements, including symbolic links, have been set properly:

bash is the shell in use.

sh is a symbolic link to bash.

/usr/bin/awk is a symbolic link to gawk.

/usr/bin/yacc is a symbolic link to bison or a small script that executes bison.
```

```
Important

To re-emphasize the build process:

Place all the sources and patches in a directory that will be accessible from the chroot environment such as /mnt/lfs/sources/. Do not put sources in /mnt/lfs/tools/.

Change to the sources directory.

For each package:

Using the tar program, extract the package to be built. In Chapter 5, ensure you are the lfs user when extracting the package.

Change to the directory created when the package was extracted.

Follow the book's instructions for building the package.

Change back to the sources directory.

Delete the extracted source directory unless instructed otherwise.
```


---

## temporary system

### binutils pass1

```bash
lfs:/mnt/lfs/sources $ mkdir -v -p binutils-2.34-pass1/build
lfs:/mnt/lfs/sources $ tar xvf binutils-2.34.tar.xz -C binutils-2.34-pass1/

lfs:/mnt/lfs/sources $ cd binutils-2.34-pass1/build
lfs:/mnt/lfs/sources/binutils-2.34-pass1/build $ ../binutils-2.34/configure \
 --prefix=/tools            \
 --with-sysroot=$LFS        \
 --with-lib-path=/tools/lib \
 --target=$LFS_TGT          \
 --disable-nls              \
 --disable-werror
lfs:/mnt/lfs/sources/binutils-2.34-pass1/build $ make
lfs:/mnt/lfs/sources/binutils-2.34-pass1/build $ case $(uname -m) in
  x86_64) mkdir -v /tools/lib && ln -sv lib /tools/lib64 ;;
esac
lfs:/mnt/lfs/sources/binutils-2.34-pass1/build $ make install
```

### gcc pass1

```bash
lfs:/mnt/lfs/sources $ mkdir -v -p gcc-9.2.0-pass1/build
lfs:/mnt/lfs/sources $ tar xvf gcc-9.2.0.tar.xz -C gcc-9.2.0-pass1/
lfs:/mnt/lfs/sources $ tar xvf mpfr-4.0.2.tar.xz
lfs:/mnt/lfs/sources $ mv -v mpfr-4.0.2 gcc-9.2.0-pass1/gcc-9.2.0/mpfr
lfs:/mnt/lfs/sources $ tar xvf gmp-6.2.0.tar.xz
lfs:/mnt/lfs/sources $ mv -v gmp-6.2.0 gcc-9.2.0-pass1/gcc-9.2.0/gmp
lfs:/mnt/lfs/sources $ tar xvf mpc-1.1.0.tar.gz
lfs:/mnt/lfs/sources $ mv -v mpc-1.1.0 gcc-9.2.0-pass1/gcc-9.2.0/mpc

lfs:/mnt/lfs/sources $ cd gcc-9.2.0-pass1/gcc-9.2.0/
lfs:/mnt/lfs/sources/gcc-9.2.0-pass1/gcc-9.2.0 $ for file in gcc/config/{linux,i386/linux{,64}}.h
do
  cp -uv $file{,.orig}
  sed -e 's@/lib\(64\)\?\(32\)\?/ld@/tools&@g' \
      -e 's@/usr@/tools@g' $file.orig > $file
  echo '
#undef STANDARD_STARTFILE_PREFIX_1
#undef STANDARD_STARTFILE_PREFIX_2
#define STANDARD_STARTFILE_PREFIX_1 "/tools/lib/"
#define STANDARD_STARTFILE_PREFIX_2 ""' >> $file
  touch $file.orig
done

lfs:/mnt/lfs/sources/gcc-9.2.0-pass1/gcc-9.2.0 $ case $(uname -m) in
  x86_64)
    sed -e '/m64=/s/lib64/lib/' \
        -i.orig gcc/config/i386/t-linux64
 ;;
esac

lfs:/mnt/lfs/sources $ cd gcc-9.2.0-pass1/build
lfs:/mnt/lfs/sources/gcc-9.2.0-pass1/build $ ../gcc-9.2.0/configure \
    --target=$LFS_TGT                              \
    --prefix=/tools                                \
    --with-glibc-version=2.11                      \
    --with-sysroot=$LFS                            \
    --with-newlib                                  \
    --without-headers                              \
    --with-local-prefix=/tools                     \
    --with-native-system-header-dir=/tools/include \
    --disable-nls                                  \
    --disable-shared                               \
    --disable-multilib                             \
    --disable-decimal-float                        \
    --disable-threads                              \
    --disable-libatomic                            \
    --disable-libgomp                              \
    --disable-libquadmath                          \
    --disable-libssp                               \
    --disable-libvtv                               \
    --disable-libstdcxx                            \
    --enable-languages=c,c++
lfs:/mnt/lfs/sources/gcc-9.2.0-pass1/build $ make
lfs:/mnt/lfs/sources/gcc-9.2.0-pass1/build $ make install
```

### linux header api

```bash
lfs:/mnt/lfs/sources $ tar xvf linux-5.5.3.tar.xz

lfs:/mnt/lfs/sources $ cd linux-5.5.3
lfs:/mnt/lfs/sources/linux-5.5.3 $ make mrproper
lfs:/mnt/lfs/sources/linux-5.5.3 $ make headers
lfs:/mnt/lfs/sources/linux-5.5.3 $ cp -rv usr/include/* /tools/include
```

### glibc

```bash
lfs:/mnt/lfs/sources $ tar xf glibc-2.31.tar.xz
lfs:/mnt/lfs/sources $ cd glibc-2.31
lfs:/mnt/lfs/sources/glibc-2.31 $ mkdir build

lfs:/mnt/lfs/sources/glibc-2.31 $ cd build
lfs:/mnt/lfs/sources/glibc-2.31/build $ ../configure \
    --prefix=/tools                    \
    --host=$LFS_TGT                    \
    --build=$(../scripts/config.guess) \
    --enable-kernel=3.2                \
    --with-headers=/tools/include
lfs:/mnt/lfs/sources/glibc-2.31/build $ make
lfs:/mnt/lfs/sources/glibc-2.31/build $ make install

lfs:/mnt/lfs/sources/glibc-2.31/build $ echo 'int main(){}' > dummy.c
lfs:/mnt/lfs/sources/glibc-2.31/build $ $LFS_TGT-gcc dummy.c
lfs:/mnt/lfs/sources/glibc-2.31/build $ ldd a.out | grep /tools
lfs:/mnt/lfs/sources/glibc-2.31/build $ readelf -l a.out | grep ': /tools'
```

### libstdc++

```bash
lfs:/mnt/lfs/sources/gcc-9.2.0-pass1/gcc-9.2.0 $ mkdir build

lfs:/mnt/lfs/sources/gcc-9.2.0-pass1/gcc-9.2.0 $ cd build/
lfs:/mnt/lfs/sources/gcc-9.2.0-pass1/gcc-9.2.0/build $ ../libstdc++-v3/configure \
    --host=$LFS_TGT                 \
    --prefix=/tools                 \
    --disable-multilib              \
    --disable-nls                   \
    --disable-libstdcxx-threads     \
    --disable-libstdcxx-pch         \
    --with-gxx-include-dir=/tools/$LFS_TGT/include/c++/9.2.0
lfs:/mnt/lfs/sources/gcc-9.2.0-pass1/gcc-9.2.0/build $ make
lfs:/mnt/lfs/sources/gcc-9.2.0-pass1/gcc-9.2.0/build $ make install
```

### binutils pass2

```bash
lfs:/mnt/lfs/sources $ mkdir -v -p binutils-2.34-pass2/build
lfs:/mnt/lfs/sources $ tar xvf binutils-2.34.tar.xz -C binutils-2.34-pass2/

lfs:/mnt/lfs/sources $ cd binutils-2.34-pass2/build
lfs:/mnt/lfs/sources/binutils-2.34-pass2/build $ CC=$LFS_TGT-gcc
AR=$LFS_TGT-ar                 \
RANLIB=$LFS_TGT-ranlib         \
../binutils-2.34/configure     \
  --prefix=/tools              \
  --disable-nls                \
  --disable-werror             \
  --with-lib-path=/tools/lib   \
  --with-sysroot
lfs:/mnt/lfs/sources/binutils-2.34-pass2/build $ make
lfs:/mnt/lfs/sources/binutils-2.34-pass2/build $ make install
lfs:/mnt/lfs/sources/binutils-2.34-pass2/build $ make -C ld clean
lfs:/mnt/lfs/sources/binutils-2.34-pass2/build $ make -C ld LIB_PATH=/usr/lib:/lib
lfs:/mnt/lfs/sources/binutils-2.34-pass2/build $ cp -v ld/ld-new /tools/bin
```

### gcc pass2

```bash
lfs:/mnt/lfs/sources $ mkdir -v -p gcc-9.2.0-pass2/build
lfs:/mnt/lfs/sources $ tar xvf gcc-9.2.0.tar.xz -C gcc-9.2.0-pass2/

lfs:/mnt/lfs/sources $ cd gcc-9.2.0-pass2/gcc-9.2.0/
lfs:/mnt/lfs/sources/gcc-9.2.0-pass2/gcc-9.2.0 $ cat gcc/limitx.h gcc/glimits.h gcc/limity.h > `dirname $($LFS_TGT-gcc -print-libgcc-file-name)`/include-fixed/limits.h
lfs:/mnt/lfs/sources/gcc-9.2.0-pass2/gcc-9.2.0 $ for file in gcc/config/{linux,i386/linux{,64}}.h
do
  cp -uv $file{,.orig}
  sed -e 's@/lib\(64\)\?\(32\)\?/ld@/tools&@g' \
      -e 's@/usr@/tools@g' $file.orig > $file
  echo '
#undef STANDARD_STARTFILE_PREFIX_1
#undef STANDARD_STARTFILE_PREFIX_2
#define STANDARD_STARTFILE_PREFIX_1 "/tools/lib/"
#define STANDARD_STARTFILE_PREFIX_2 ""' >> $file
  touch $file.orig
done
lfs:/mnt/lfs/sources/gcc-9.2.0-pass2/gcc-9.2.0 $ case $(uname -m) in
  x86_64)
    sed -e '/m64=/s/lib64/lib/' \
        -i.orig gcc/config/i386/t-linux64
  ;;
esac
lfs:/mnt/lfs/sources/gcc-9.2.0-pass2/gcc-9.2.0 $ tar xvf ../../mpfr-4.0.2.tar.xz 
lfs:/mnt/lfs/sources/gcc-9.2.0-pass2/gcc-9.2.0 $ mv mpfr-4.0.2/ mpfr
lfs:/mnt/lfs/sources/gcc-9.2.0-pass2/gcc-9.2.0 $ tar xvf ../../gmp-6.2.0.tar.xz 
lfs:/mnt/lfs/sources/gcc-9.2.0-pass2/gcc-9.2.0 $ mv gmp-6.2.0 gmp 
lfs:/mnt/lfs/sources/gcc-9.2.0-pass2/gcc-9.2.0 $ tar xvf ../../mpc-1.1.0.tar.gz 
lfs:/mnt/lfs/sources/gcc-9.2.0-pass2/gcc-9.2.0 $ mv mpc-1.1.0 mpc 
lfs:/mnt/lfs/sources/gcc-9.2.0-pass2/gcc-9.2.0 $ sed -e '1161 s|^|//|' -i libsanitizer/sanitizer_common/sanitizer_platform_limits_posix.cc

lfs:/mnt/lfs/sources/gcc-9.2.0-pass2 $ cd build
lfs:/mnt/lfs/sources/gcc-9.2.0-pass2/build $ CC=$LFS_TGT-gcc \
CXX=$LFS_TGT-g++                                   \
AR=$LFS_TGT-ar                                     \
RANLIB=$LFS_TGT-ranlib                             \
../gcc-9.2.0/configure                             \
  --prefix=/tools                                  \
  --with-local-prefix=/tools                       \
  --with-native-system-header-dir=/tools/include   \
  --enable-languages=c,c++                         \
  --disable-libstdcxx-pch                          \
  --disable-multilib                               \
  --disable-bootstrap                              \
  --disable-libgomp
lfs:/mnt/lfs/sources/gcc-9.2.0-pass2/build $ make
lfs:/mnt/lfs/sources/gcc-9.2.0-pass2/build $ make install

lfs:/mnt/lfs/sources/gcc-9.2.0-pass2/build $ ln -sv gcc /tools/bin/cc
lfs:/mnt/lfs/sources/gcc-9.2.0-pass2/build $ echo 'int main(){}' > dummy.c
lfs:/mnt/lfs/sources/gcc-9.2.0-pass2/build $ cc dummy.c
lfs:/mnt/lfs/sources/gcc-9.2.0-pass2/build $ ldd a.out | grep /tools
lfs:/mnt/lfs/sources/gcc-9.2.0-pass2/build $ readelf -l a.out | grep ': /tools'
```

### tcl

```bash
lfs:/mnt/lfs/sources $ tar xvf tcl8.6.10-src.tar.gz 
lfs:/mnt/lfs/sources $ cd tcl8.6.10
lfs:/mnt/lfs/sources/tcl8.6.10 $ cd unix/
lfs:/mnt/lfs/sources/tcl8.6.10/unix $ ./configure --prefix=/tools
lfs:/mnt/lfs/sources/tcl8.6.10/unix $ make
lfs:/mnt/lfs/sources/tcl8.6.10/unix $ TZ=UTC make test
lfs:/mnt/lfs/sources/tcl8.6.10/unix $ make install
lfs:/mnt/lfs/sources/tcl8.6.10/unix $ chmod -v u+w /tools/lib/libtcl8.6.so
lfs:/mnt/lfs/sources/tcl8.6.10/unix $ make install-private-headers
lfs:/mnt/lfs/sources/tcl8.6.10/unix $ ln -sv tclsh8.6 /tools/bin/tclsh
```

### expect

```bash
lfs:/mnt/lfs/sources $ tar xvf expect5.45.4.tar.gz 
lfs:/mnt/lfs/sources $ cd expect5.45.4
lfs:/mnt/lfs/sources/expect5.45.4 $ cp -v configure{,.orig}
lfs:/mnt/lfs/sources/expect5.45.4 $ sed 's:/usr/local/bin:/bin:' configure.orig > configure
lfs:/mnt/lfs/sources/expect5.45.4 $ ./configure --prefix=/tools \
  --with-tcl=/tools/lib \
  --with-tclinclude=/tools/include
lfs:/mnt/lfs/sources/expect5.45.4 $ make
lfs:/mnt/lfs/sources/expect5.45.4 $ make test
lfs:/mnt/lfs/sources/expect5.45.4 $ make SCRIPTS="" install
```

### deja gnu

```bash
lfs:/mnt/lfs/sources $ tar xvf dejagnu-1.6.2.tar.gz 
lfs:/mnt/lfs/sources $ cd dejagnu-1.6.2
lfs:/mnt/lfs/sources/dejagnu-1.6.2 $ ./configure --prefix=/tools
lfs:/mnt/lfs/sources/dejagnu-1.6.2 $ make
lfs:/mnt/lfs/sources/dejagnu-1.6.2 $ make install
```

### m4

```bash
lfs:/mnt/lfs/sources $ tar xvf m4-1.4.18.tar.xz 
lfs:/mnt/lfs/sources $ cd m4-1.4.18
lfs:/mnt/lfs/sources/m4-1.4.18 $ sed -i 's/IO_ftrylockfile/IO_EOF_SEEN/' lib/*.c
lfs:/mnt/lfs/sources/m4-1.4.18 $ echo "#define _IO_IN_BACKUP 0x100" >> lib/stdio-impl.h
lfs:/mnt/lfs/sources/m4-1.4.18 $ ./configure --prefix=/tools
lfs:/mnt/lfs/sources/m4-1.4.18 $ make
lfs:/mnt/lfs/sources/m4-1.4.18 $ make check
lfs:/mnt/lfs/sources/m4-1.4.18 $ make install
```

### ncurses

```bash
lfs:/mnt/lfs/sources $ tar xvf ncurses-6.2.tar.gz 
lfs:/mnt/lfs/sources $ cd ncurses-6.2
lfs:/mnt/lfs/sources/ncurses-6.2 $ sed -i s/mawk// configure
lfs:/mnt/lfs/sources/ncurses-6.2 $ ./configure --prefix=/tools \
  --with-shared   \
  --without-debug \
  --without-ada   \
  --enable-widec  \
  --enable-overwrite
lfs:/mnt/lfs/sources/ncurses-6.2 $ make
lfs:/mnt/lfs/sources/ncurses-6.2 $ make install
lfs:/mnt/lfs/sources/ncurses-6.2 $ ln -s libncursesw.so /tools/lib/libncurses.so
```

### bash

```bash
lfs:/mnt/lfs/sources $ tar xvf bash-5.0.tar.gz 
lfs:/mnt/lfs/sources $ cd bash-5.0
lfs:/mnt/lfs/sources/bash-5.0 $ ./configure --prefix=/tools --without-bash-malloc
lfs:/mnt/lfs/sources/bash-5.0 $ make
lfs:/mnt/lfs/sources/bash-5.0 $ make tests
lfs:/mnt/lfs/sources/bash-5.0 $ make install
lfs:/mnt/lfs/sources/bash-5.0 $ ln -sv bash /tools/bin/sh
```

### bison

```bash
lfs:/mnt/lfs/sources $ tar xvf bison-3.5.2.tar.xz 
lfs:/mnt/lfs/sources $ cd bison-3.5.2
lfs:/mnt/lfs/sources/bison-3.5.2 $ ./configure --prefix=/tools
lfs:/mnt/lfs/sources/bison-3.5.2$ make
lfs:/mnt/lfs/sources/bison-3.5.2$ make check
lfs:/mnt/lfs/sources/bison-3.5.2$ make install
```

### bzip

```bash
lfs:/mnt/lfs/sources $ tar xvf bzip2-1.0.8.tar.gz 
lfs:/mnt/lfs/sources $ cd bzip2-1.0.8
lfs:/mnt/lfs/sources/bzip2-1.0.8 $ make -f Makefile-libbz2_so
lfs:/mnt/lfs/sources/bzip2-1.0.8 $ make clean
lfs:/mnt/lfs/sources/bzip2-1.0.8 $ make
lfs:/mnt/lfs/sources/bzip2-1.0.8 $ make PREFIX=/tools install
lfs:/mnt/lfs/sources/bzip2-1.0.8 $ cp -v bzip2-shared /tools/bin/bzip2
lfs:/mnt/lfs/sources/bzip2-1.0.8 $ cp -av libbz2.so* /tools/lib
lfs:/mnt/lfs/sources/bzip2-1.0.8 $ ln -sv libbz2.so.1.0 /tools/lib/libbz2.so
```

### coreutils

```bash
lfs:/mnt/lfs/sources $ tar xvf coreutils-8.31.tar.xz 
lfs:/mnt/lfs/sources $ cd coreutils-8.31
lfs:/mnt/lfs/sources/coreutils-8.31 $ ./configure --prefix=/tools --enable-install-program=hostname
lfs:/mnt/lfs/sources/coreutils-8.31 $ make
lfs:/mnt/lfs/sources/coreutils-8.31 $ make RUN_EXPENSIVE_TESTS=yes check
lfs:/mnt/lfs/sources/coreutils-8.31 $ make install
```

### diffutils

```bash
lfs:/mnt/lfs/sources $ tar xvf diffutils-3.7.tar.xz 
lfs:/mnt/lfs/sources $ cd diffutils-3.7
lfs:/mnt/lfs/sources/diffutils-3.7 $ ./configure --prefix=/tools
lfs:/mnt/lfs/sources/diffutils-3.7 $ make
lfs:/mnt/lfs/sources/diffutils-3.7 $ make check
lfs:/mnt/lfs/sources/diffutils-3.7 $ make install
```

### file

```bash
lfs:/mnt/lfs/sources $ tar xvf file-5.38.tar.gz 
lfs:/mnt/lfs/sources $ cd file-5.38
lfs:/mnt/lfs/sources/file-5.38 $ ./configure --prefix=/tools
lfs:/mnt/lfs/sources/file-5.38 $ make
lfs:/mnt/lfs/sources/file-5.38 $ make check
lfs:/mnt/lfs/sources/file-5.38 $ make install
```

### findutils

```bash
lfs:/mnt/lfs/sources $ tar xvf findutils-4.7.0.tar.xz 
lfs:/mnt/lfs/sources $ cd findutils-4.7.0
lfs:/mnt/lfs/sources/findutils-4.7.0 $ ./configure --prefix=/tools
lfs:/mnt/lfs/sources/findutils-4.7.0 $ make
lfs:/mnt/lfs/sources/findutils-4.7.0 $ make check
lfs:/mnt/lfs/sources/findutils-4.7.0 $ make install
```

### gawk

```bash
lfs:/mnt/lfs/sources $ tar xvf gawk-5.0.1.tar.xz 
lfs:/mnt/lfs/sources $ cd gawk-5.0.1
lfs:/mnt/lfs/sources/gawk-5.0.1 $ ./configure --prefix=/tools
lfs:/mnt/lfs/sources/gawk-5.0.1 $ make
lfs:/mnt/lfs/sources/gawk-5.0.1 $ make check
lfs:/mnt/lfs/sources/gawk-5.0.1 $ make install
```

### gettext

```bash
lfs:/mnt/lfs/sources $ tar xvf gettext-0.20.1.tar.xz 
lfs:/mnt/lfs/sources $ cd gettext-0.20.1
lfs:/mnt/lfs/sources/gettext-0.20.1 $ ./configure --disable-shared
lfs:/mnt/lfs/sources/gettext-0.20.1 $ make
lfs:/mnt/lfs/sources/gettext-0.20.1 $ cp -v gettext-tools/src/{msgfmt,msgmerge,xgettext} /tools/bin
```

### grep

```bash
lfs:/mnt/lfs/sources $ tar xvf grep-3.4.tar.xz 
lfs:/mnt/lfs/sources $ cd grep-3.4
lfs:/mnt/lfs/sources/grep-3.4 $ ./configure --prefix=/tools
lfs:/mnt/lfs/sources/grep-3.4 $ make
lfs:/mnt/lfs/sources/grep-3.4 $ make check
lfs:/mnt/lfs/sources/grep-3.4 $ make install
```

### gzip

```bash
lfs:/mnt/lfs/sources $ tar xvf gzip-1.10.tar.xz 
lfs:/mnt/lfs/sources $ cd gzip-1.10
lfs:/mnt/lfs/sources/gzip-1.10 $ ./configure --prefix=/tools
lfs:/mnt/lfs/sources/gzip-1.10 $ make
lfs:/mnt/lfs/sources/gzip-1.10 $ make check
lfs:/mnt/lfs/sources/gzip-1.10 $ make install
```

### make

```bash
lfs:/mnt/lfs/sources$ tar xvf make-4.3.tar.gz 
lfs:/mnt/lfs/sources$ cd make-4.3 
lfs:/mnt/lfs/sources/make-4.3 $ ./configure --prefix=/tools --without-guile
lfs:/mnt/lfs/sources/make-4.3 $ make
lfs:/mnt/lfs/sources/make-4.3 $ make check
lfs:/mnt/lfs/sources/make-4.3 $ make install
```

### patch

```bash
lfs:/mnt/lfs/sources $ tar xvf patch-2.7.6.tar.xz 
lfs:/mnt/lfs/sources $ cd patch-2.7.6
lfs:/mnt/lfs/sources/patch-2.7.6 $ ./configure --prefix=/tools
lfs:/mnt/lfs/sources/patch-2.7.6 $ make
lfs:/mnt/lfs/sources/patch-2.7.6 $ make check
lfs:/mnt/lfs/sources/patch-2.7.6 $ make install
```

### perl

```bash
lfs:/mnt/lfs/sources $ tar xvf perl-5.30.1.tar.xz 
lfs:/mnt/lfs/sources $ cd perl-5.30.1
lfs:/mnt/lfs/sources/perl-5.30.1 $ sh Configure -des -Dprefix=/tools -Dlibs=-lm -Uloclibpth -Ulocincpth
lfs:/mnt/lfs/sources/perl-5.30.1 $ make
lfs:/mnt/lfs/sources/perl-5.30.1 $ cp -v perl cpan/podlators/scripts/pod2man /tools/bin
lfs:/mnt/lfs/sources/perl-5.30.1 $ mkdir -pv /tools/lib/perl5/5.30.1
lfs:/mnt/lfs/sources/perl-5.30.1 $ cp -Rv lib/* /tools/lib/perl5/5.30.1
```

### python

```bash
lfs:/mnt/lfs/sources $ tar xf Python-3.8.1.tar.xz 
lfs:/mnt/lfs/sources $ cd Python-3.8.1
lfs:/mnt/lfs/sources/Python-3.8.1 $ sed -i '/def add_multiarch_paths/a \        return' setup.py
lfs:/mnt/lfs/sources/Python-3.8.1 $ ./configure --prefix=/tools --without-ensurepip
lfs:/mnt/lfs/sources/Python-3.8.1 $ make
lfs:/mnt/lfs/sources/Python-3.8.1 $ make install
```

### sed

```bash
lfs:/mnt/lfs/sources $ tar xf sed-4.8.tar.xz 
lfs:/mnt/lfs/sources $ cd sed-4.8
lfs:/mnt/lfs/sources/sed-4.8 $ ./configure --prefix=/tools
lfs:/mnt/lfs/sources/sed-4.8 $ make
lfs:/mnt/lfs/sources/sed-4.8 $ make check
lfs:/mnt/lfs/sources/sed-4.8 $ make install
```

### tar

```bash
lfs:/mnt/lfs/sources $ tar xf tar-1.32.tar.xz 
lfs:/mnt/lfs/sources $ cd tar-1.32
lfs:/mnt/lfs/sources/tar-1.32 $ ./configure --prefix=/tools
lfs:/mnt/lfs/sources/tar-1.32 $ make
lfs:/mnt/lfs/sources/tar-1.32 $ make check
lfs:/mnt/lfs/sources/tar-1.32 $ make install
```

### texinfo

```bash
lfs:/mnt/lfs/sources $ tar xf texinfo-6.7.tar.xz 
lfs:/mnt/lfs/sources $ cd texinfo-6.7
lfs:/mnt/lfs/sources/texinfo-6.7 $ ./configure --prefix=/tools
lfs:/mnt/lfs/sources/texinfo-6.7 $ make
lfs:/mnt/lfs/sources/texinfo-6.7 $ make check
lfs:/mnt/lfs/sources/texinfo-6.7 $ make install
```

### util-linux

```bash
lfs:/mnt/lfs/sources $ tar xf util-linux-2.35.1.tar.xz 
lfs:/mnt/lfs/sources $ cd util-linux-2.35.1
lfs:/mnt/lfs/sources/util-linux-2.35.1 $ ./configure --prefix=/tools \
  --without-python               \
  --disable-makeinstall-chown    \
  --without-systemdsystemunitdir \
  --without-ncurses              \
  PKG_CONFIG=""
lfs:/mnt/lfs/sources/util-linux-2.35.1 $ make
lfs:/mnt/lfs/sources/util-linux-2.35.1 $ make install
```

### xz

```bash
lfs:/mnt/lfs/sources $ tar xf xz-5.2.4.tar.xz 
lfs:/mnt/lfs/sources $ cd xz-5.2.4
lfs:/mnt/lfs/sources/xz-5.2.4 $ ./configure --prefix=/tools
lfs:/mnt/lfs/sources/xz-5.2.4 $ make
lfs:/mnt/lfs/sources/xz-5.2.4 $ make check
lfs:/mnt/lfs/sources/xz-5.2.4 $ make install
```

### stripping

```bash
lfs@kali:/mnt/lfs/sources $ du -hs /tools/lib
lfs@kali:/mnt/lfs/sources $ strip --strip-debug /tools/lib/*

lfs@kali:/mnt/lfs/sources $ du -hs /tools/bin
lfs@kali:/mnt/lfs/sources $ du -hs /tools/sbin
lfs@kali:/mnt/lfs/sources $ /usr/bin/strip --strip-unneeded /tools/{,s}bin/*

lfs@kali:/mnt/lfs/sources $ rm -rf /tools/{,share}/{info,man,doc}
lfs@kali:/mnt/lfs/sources $ find /tools/{lib,libexec} -name \*.la -delete
```

### ownership

```bash
root:~ # chown -R root:root /mnt/lfs/tools
```


---

## build system

### preparing virtual kernel file system

```bash
root:~ # mkdir -pv $LFS/{dev,proc,sys,run}
root:~ # mknod -m 600 $LFS/dev/console c 5 1
root:~ # mknod -m 666 $LFS/dev/null c 1 3
root:~ # mount -v --bind /dev $LFS/dev
root:~ # mount -vt devpts devpts $LFS/dev/pts -o gid=5,mode=620
root:~ # mount -vt proc proc $LFS/proc
root:~ # mount -vt sysfs sysfs $LFS/sys
root:~ # mount -vt tmpfs tmpfs $LFS/run
root:~ # if [ -h $LFS/dev/shm ]; then
  mkdir -pv $LFS/$(readlink $LFS/dev/shm)
fi
```


### package management

```bash
root:foo # ./configure --prefix=/usr/pkg/libfoo/1.1
root:foo # make
root:foo # make install

root:foo # ./configure --prefix=/usr
root:foo # make
root:foo # make DESTDIR=/usr/pkg/libfoo/1.1 install
```


### chroot environment

```bash
root:~ # chroot "$LFS" /tools/bin/env -i \
  HOME=/root                  \
  TERM="$TERM"                \
  PS1='(lfs chroot) \u:\w\$ ' \
  PATH=/bin:/usr/bin:/sbin:/usr/sbin:/tools/bin \
  /tools/bin/bash --login +h
```


### create directory

```bash
(lfs chroot) I have no name!:~ # mkdir -pv /{bin,boot,etc/{opt,sysconfig},home,lib/firmware,mnt,opt}
(lfs chroot) I have no name!:~ # mkdir -pv /{media/{floppy,cdrom},sbin,srv,var}
(lfs chroot) I have no name!:~ # install -dv -m 0750 /root
(lfs chroot) I have no name!:~ # install -dv -m 1777 /tmp /var/tmp
(lfs chroot) I have no name!:~ # mkdir -pv /usr/{,local/}{bin,include,lib,sbin,src}
(lfs chroot) I have no name!:~ # mkdir -pv /usr/{,local/}share/{color,dict,doc,info,locale,man}
(lfs chroot) I have no name!:~ # mkdir -v  /usr/{,local/}share/{misc,terminfo,zoneinfo}
(lfs chroot) I have no name!:~ # mkdir -v  /usr/libexec
(lfs chroot) I have no name!:~ # mkdir -pv /usr/{,local/}share/man/man{1..8}
(lfs chroot) I have no name!:~ # mkdir -v  /usr/lib/pkgconfig

(lfs chroot) I have no name!:~ # case $(uname -m) in
 x86_64) mkdir -v /lib64 ;;
esac

(lfs chroot) I have no name!:~ # mkdir -v /var/{log,mail,spool}
(lfs chroot) I have no name!:~ # ln -sv /run /var/run
(lfs chroot) I have no name!:~ # ln -sv /run/lock /var/lock
(lfs chroot) I have no name!:~ # mkdir -pv /var/{opt,cache,lib/{color,misc,locate},local}
```


### creating essential files and symlinks

```bash
(lfs chroot) I have no name!:~ # ln -sv /tools/bin/{bash,cat,chmod,dd,echo,ln,mkdir,pwd,rm,stty,touch} /bin
(lfs chroot) I have no name!:~ # ln -sv /tools/bin/{env,install,perl,printf}         /usr/bin
(lfs chroot) I have no name!:~ # ln -sv /tools/lib/libgcc_s.so{,.1}                  /usr/lib
(lfs chroot) I have no name!:~ # ln -sv /tools/lib/libstdc++.{a,so{,.6}}             /usr/lib
(lfs chroot) I have no name!:~ # ln -sv /tools/lib/ld-linux-x86-64.so.2              /lib64 
(lfs chroot) I have no name!:~ # ln -sv bash /bin/sh
(lfs chroot) I have no name!:~ # ln -sv /proc/self/mounts /etc/mtab
(lfs chroot) I have no name!:~ # cat > /etc/passwd << "EOF"
root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/dev/null:/bin/false
daemon:x:6:6:Daemon User:/dev/null:/bin/false
messagebus:x:18:18:D-Bus Message Daemon User:/var/run/dbus:/bin/false
nobody:x:99:99:Unprivileged User:/dev/null:/bin/false
EOF

(lfs chroot) I have no name!:~ # cat > /etc/group << "EOF"
root:x:0:
bin:x:1:daemon
sys:x:2:
kmem:x:3:
tape:x:4:
tty:x:5:
daemon:x:6:
floppy:x:7:
disk:x:8:
lp:x:9:
dialout:x:10:
audio:x:11:
video:x:12:
utmp:x:13:
usb:x:14:
cdrom:x:15:
adm:x:16:
messagebus:x:18:
input:x:24:
mail:x:34:
kvm:x:61:
wheel:x:97:
nogroup:x:99:
users:x:999:
EOF

(lfs chroot) I have no name!:~ # exec /tools/bin/bash --login +h
(lfs chroot) root:~ # touch /var/log/{btmp,lastlog,faillog,wtmp}
(lfs chroot) root:~ # chgrp -v utmp /var/log/lastlog
(lfs chroot) root:~ # chmod -v 664  /var/log/lastlog
(lfs chroot) root:~ # chmod -v 600  /var/log/btmp
```


### linux header api

```bash
(lfs chroot) root:/sources # tar xf linux-5.5.3.tar.xz 
(lfs chroot) root:/sources # cd linux-5.5.3
(lfs chroot) root:/sources/linux-5.5.3 # make mrproper
(lfs chroot) root:/sources/linux-5.5.3 # make headers
(lfs chroot) root:/sources/linux-5.5.3 # find usr/include -name '.*' -delete
(lfs chroot) root:/sources/linux-5.5.3 # rm usr/include/Makefile
(lfs chroot) root:/sources/linux-5.5.3 # cp -rv usr/include/* /usr/include
```


### man-pages

```bash
(lfs chroot) root:/sources # tar xf man-pages-5.05.tar.xz 
(lfs chroot) root:/sources # cd man-pages-5.05
(lfs chroot) root:/sources/man-pages-5.05 # make install
```


### glibc

```bash
(lfs chroot) root:/sources # tar xf glibc-2.31.tar.xz 
(lfs chroot) root:/sources # cd glibc-2.31 
(lfs chroot) root:/sources/glibc-2.31 # patch -Np1 -i ../glibc-2.31-fhs-1.patch
(lfs chroot) root:/sources/glibc-2.31 # make build
(lfs chroot) root:/sources/glibc-2.31 # cd build
(lfs chroot) root:/sources/glibc-2.31/build # CC="gcc -ffile-prefix-map=/tools=/usr" \
  ../configure --prefix=/usr             \
  --disable-werror                       \
  --enable-kernel=3.2                    \
  --enable-stack-protector=strong        \
  --with-headers=/usr/include            \
  libc_cv_slibdir=/lib
(lfs chroot) root:/sources/glibc-2.31/build # make
(lfs chroot) root:/sources/glibc-2.31/build # case $(uname -m) in
  i?86)   ln -sfnv $PWD/elf/ld-linux.so.2        /lib ;;
  x86_64) ln -sfnv $PWD/elf/ld-linux-x86-64.so.2 /lib ;;
esac
(lfs chroot) root:/sources/glibc-2.31/build # make check
(lfs chroot) root:/sources/glibc-2.31/build # touch /etc/ld.so.conf
(lfs chroot) root:/sources/glibc-2.31/build # sed '/test-installation/s@$(PERL)@echo not running@' -i ../Makefile
(lfs chroot) root:/sources/glibc-2.31/build # make install
(lfs chroot) root:/sources/glibc-2.31/build # cp -v ../nscd/nscd.conf /etc/nscd.conf
(lfs chroot) root:/sources/glibc-2.31/build # mkdir -pv /var/cache/nscd
(lfs chroot) root:/sources/glibc-2.31/build # install -v -Dm644 ../nscd/nscd.tmpfiles /usr/lib/tmpfiles.d/nscd.conf
(lfs chroot) root:/sources/glibc-2.31/build # install -v -Dm644 ../nscd/nscd.service /lib/systemd/system/nscd.service
(lfs chroot) root:/sources/glibc-2.31/build # mkdir -pv /usr/lib/locale
(lfs chroot) root:/sources/glibc-2.31/build # localedef -i POSIX -f UTF-8 C.UTF-8 2> /dev/null || true
(lfs chroot) root:/sources/glibc-2.31/build # localedef -i cs_CZ -f UTF-8 cs_CZ.UTF-8
(lfs chroot) root:/sources/glibc-2.31/build # localedef -i de_DE -f ISO-8859-1 de_DE
(lfs chroot) root:/sources/glibc-2.31/build # localedef -i de_DE@euro -f ISO-8859-15 de_DE@euro
(lfs chroot) root:/sources/glibc-2.31/build # localedef -i de_DE -f UTF-8 de_DE.UTF-8
(lfs chroot) root:/sources/glibc-2.31/build # localedef -i el_GR -f ISO-8859-7 el_GR
(lfs chroot) root:/sources/glibc-2.31/build # localedef -i en_GB -f UTF-8 en_GB.UTF-8
(lfs chroot) root:/sources/glibc-2.31/build # localedef -i en_HK -f ISO-8859-1 en_HK
(lfs chroot) root:/sources/glibc-2.31/build # localedef -i en_PH -f ISO-8859-1 en_PH
(lfs chroot) root:/sources/glibc-2.31/build # localedef -i en_US -f ISO-8859-1 en_US
(lfs chroot) root:/sources/glibc-2.31/build # localedef -i en_US -f UTF-8 en_US.UTF-8
(lfs chroot) root:/sources/glibc-2.31/build # localedef -i es_MX -f ISO-8859-1 es_MX
(lfs chroot) root:/sources/glibc-2.31/build # localedef -i fa_IR -f UTF-8 fa_IR
(lfs chroot) root:/sources/glibc-2.31/build # localedef -i fr_FR -f ISO-8859-1 fr_FR
(lfs chroot) root:/sources/glibc-2.31/build # localedef -i fr_FR@euro -f ISO-8859-15 fr_FR@euro
(lfs chroot) root:/sources/glibc-2.31/build # localedef -i fr_FR -f UTF-8 fr_FR.UTF-8
(lfs chroot) root:/sources/glibc-2.31/build # localedef -i it_IT -f ISO-8859-1 it_IT
(lfs chroot) root:/sources/glibc-2.31/build # localedef -i it_IT -f UTF-8 it_IT.UTF-8
(lfs chroot) root:/sources/glibc-2.31/build # localedef -i ja_JP -f EUC-JP ja_JP
(lfs chroot) root:/sources/glibc-2.31/build # localedef -i ja_JP -f SHIFT_JIS ja_JP.SIJS 2> /dev/null || true
(lfs chroot) root:/sources/glibc-2.31/build # localedef -i ja_JP -f UTF-8 ja_JP.UTF-8
(lfs chroot) root:/sources/glibc-2.31/build # localedef -i ru_RU -f KOI8-R ru_RU.KOI8-R
(lfs chroot) root:/sources/glibc-2.31/build # localedef -i ru_RU -f UTF-8 ru_RU.UTF-8
(lfs chroot) root:/sources/glibc-2.31/build # localedef -i tr_TR -f UTF-8 tr_TR.UTF-8
(lfs chroot) root:/sources/glibc-2.31/build # localedef -i zh_CN -f GB18030 zh_CN.GB18030
(lfs chroot) root:/sources/glibc-2.31/build # localedef -i zh_HK -f BIG5-HKSCS zh_HK.BIG5-HKSCS
(lfs chroot) root:/sources/glibc-2.31/build # make localedata/install-locales
```

```bash
(lfs chroot) root:~ # mv /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2.tools
(lfs chroot) root:~ # case $(uname -m) in
    i?86)   ln -sfv ld-linux.so.2 /lib/ld-lsb.so.3
    ;;
    x86_64) ln -sfv ../lib/ld-linux-x86-64.so.2 /lib64
            ln -sfv ../lib/ld-linux-x86-64.so.2 /lib64/ld-lsb-x86-64.so.3
    ;;
esac

(lfs chroot) root:~ # cat > /etc/nsswitch.conf << "EOF"
# Begin /etc/nsswitch.conf

passwd: files
group: files
shadow: files

hosts: files dns
networks: files

protocols: files
services: files
ethers: files
rpc: files

# End /etc/nsswitch.conf
EOF

(lfs chroot) root:~ # cat > /etc/ld.so.conf << "EOF"
/usr/local/lib
/opt/lib

include /etc/ld.so.conf.d/*.conf

EOF
(lfs chroot) root:~ # mkdir -pv /etc/ld.so.conf.d

(lfs chroot) root:/sources # mkdir tz
(lfs chroot) root:/sources # tar xf tzdata2019c.tar.gz -C tz
(lfs chroot) root:/sources # cd tz
(lfs chroot) root:/sources/tz # ZONEINFO=/usr/share/zoneinfo
(lfs chroot) root:/sources/tz # mkdir -pv $ZONEINFO/{posix,right}
(lfs chroot) root:/sources/tz # for tz in etcetera southamerica northamerica europe africa antarctica  \
          asia australasia backward pacificnew systemv; do
    zic -L /dev/null   -d $ZONEINFO       ${tz}
    zic -L /dev/null   -d $ZONEINFO/posix ${tz}
    zic -L leapseconds -d $ZONEINFO/right ${tz}
done

(lfs chroot) root:/sources/tz # cp -v zone.tab zone1970.tab iso3166.tab $ZONEINFO
(lfs chroot) root:/sources/tz # zic -d $ZONEINFO -p America/New_York
(lfs chroot) root:/sources/tz # unset ZONEINFO

(lfs chroot) root:~ # tzselect
(lfs chroot) root:~ # ln -sfv /usr/share/zoneinfo/<xxx> /etc/localtime
```


### adjust toolchain

```bash
(lfs chroot) root:~ # mv -v /tools/bin/{ld,ld-old}
(lfs chroot) root:~ # mv -v /tools/$(uname -m)-pc-linux-gnu/bin/{ld,ld-old}
(lfs chroot) root:~ # mv -v /tools/bin/{ld-new,ld}
(lfs chroot) root:~ # ln -sv /tools/bin/ld /tools/$(uname -m)-pc-linux-gnu/bin/ld
(lfs chroot) root:~ # gcc -dumpspecs | sed -e 's@/tools@@g' \
  -e '/\*startfile_prefix_spec:/{n;s@.*@/usr/lib/ @}' \
  -e '/\*cpp:/{n;s@$@ -isystem /usr/include@}' >      \
  `dirname $(gcc --print-libgcc-file-name)`/specs
(lfs chroot) root:~ # echo 'int main(){}' > dummy.c
(lfs chroot) root:~ # cc dummy.c -v -Wl,--verbose &> dummy.log
(lfs chroot) root:~ # ldd a.out

(lfs chroot) root:~ # readelf -l a.out | grep ': /lib'
(lfs chroot) root:~ # grep -o '/usr/lib.*/crt[1in].*succeeded' dummy.log
(lfs chroot) root:~ # grep -B1 '^ /usr/include' dummy.log
(lfs chroot) root:~ # grep 'SEARCH.*/usr/lib' dummy.log |sed 's|; |\n|g'
(lfs chroot) root:~ # grep "/lib.*/libc.so.6 " dummy.log
(lfs chroot) root:~ # grep found dummy.log
(lfs chroot) root:~ # rm -v dummy.c a.out dummy.log
```


### zlib

```bash
(lfs chroot) root:/sources # tar xf zlib-1.2.11.tar.xz 
(lfs chroot) root:/sources # cd zlib-1.2.11
(lfs chroot) root:/sources/zlib-1.2.11 # ./configure --prefix=/usr
(lfs chroot) root:/sources/zlib-1.2.11 # make
(lfs chroot) root:/sources/zlib-1.2.11 # make check
(lfs chroot) root:/sources/zlib-1.2.11 # make install
(lfs chroot) root:/sources/zlib-1.2.11 # mv -v /usr/lib/libz.so.* /lib
(lfs chroot) root:/sources/zlib-1.2.11 # ln -sfv ../../lib/$(readlink /usr/lib/libz.so) /usr/lib/libz.so
```


### bzip2

```bash
(lfs chroot) root:/sources # tar xf bzip2-1.0.8.tar.gz 
(lfs chroot) root:/sources # cd bzip2-1.0.8
(lfs chroot) root:/sources/bzip2-1.0.8 # patch -Np1 -i ../bzip2-1.0.8-install_docs-1.patch
(lfs chroot) root:/sources/bzip2-1.0.8 # sed -i 's@\(ln -s -f \)$(PREFIX)/bin/@\1@' Makefile
(lfs chroot) root:/sources/bzip2-1.0.8 # sed -i "s@(PREFIX)/man@(PREFIX)/share/man@g" Makefile
(lfs chroot) root:/sources/bzip2-1.0.8 # make -f Makefile-libbz2_so
(lfs chroot) root:/sources/bzip2-1.0.8 # make clean
(lfs chroot) root:/sources/bzip2-1.0.8 # make
(lfs chroot) root:/sources/bzip2-1.0.8 # make PREFIX=/usr install
(lfs chroot) root:/sources/bzip2-1.0.8 # cp -v bzip2-shared /bin/bzip2
(lfs chroot) root:/sources/bzip2-1.0.8 # cp -av libbz2.so* /lib
(lfs chroot) root:/sources/bzip2-1.0.8 # ln -sv ../../lib/libbz2.so.1.0 /usr/lib/libbz2.so
(lfs chroot) root:/sources/bzip2-1.0.8 # rm -v /usr/bin/{bunzip2,bzcat,bzip2}
(lfs chroot) root:/sources/bzip2-1.0.8 # ln -sv bzip2 /bin/bunzip2
(lfs chroot) root:/sources/bzip2-1.0.8 # ln -sv bzip2 /bin/bzcat
```


### xz

```bash
(lfs chroot) root:/sources # tar xf xz-5.2.4.tar.xz 
(lfs chroot) root:/sources # cd xz-5.2.4
(lfs chroot) root:/sources/xz-5.2.4 # ./configure --prefix=/usr  \
  --disable-static \
  --docdir=/usr/share/doc/xz-5.2.4
(lfs chroot) root:/sources/xz-5.2.4 # make
(lfs chroot) root:/sources/xz-5.2.4 # make check
(lfs chroot) root:/sources/xz-5.2.4 # make install
(lfs chroot) root:/sources/xz-5.2.4 # mv -v   /usr/bin/{lzma,unlzma,lzcat,xz,unxz,xzcat} /bin
(lfs chroot) root:/sources/xz-5.2.4 # mv -v /usr/lib/liblzma.so.* /lib
(lfs chroot) root:/sources/xz-5.2.4 # ln -svf ../../lib/$(readlink /usr/lib/liblzma.so) /usr/lib/liblzma.so
```


### file

```bash
(lfs chroot) root:/sources # tar xf file-5.38.tar.gz 
(lfs chroot) root:/sources # cd file-5.38
(lfs chroot) root:/sources/file-5.38 # ./configure --prefix=/usr
(lfs chroot) root:/sources/file-5.38 # make
(lfs chroot) root:/sources/file-5.38 # make install
```


### readline

```bash
(lfs chroot) root:/sources # tar xf readline-8.0.tar.gz 
(lfs chroot) root:/sources # cd readline-8.0
(lfs chroot) root:/sources/readline-8.0 # sed -i '/MV.*old/d' Makefile.in
(lfs chroot) root:/sources/readline-8.0 # sed -i '/{OLDSUFF}/c:' support/shlib-install
(lfs chroot) root:/sources/readline-8.0 # ./configure --prefix=/usr  \
  --disable-static \
  --docdir=/usr/share/doc/readline-8.0
(lfs chroot) root:/sources/readline-8.0 # make SHLIB_LIBS="-L/tools/lib -lncursesw"
(lfs chroot) root:/sources/readline-8.0 # make SHLIB_LIBS="-L/tools/lib -lncursesw" install
(lfs chroot) root:/sources/readline-8.0 # mv -v /usr/lib/lib{readline,history}.so.* /lib
(lfs chroot) root:/sources/readline-8.0 # chmod -v u+w /lib/lib{readline,history}.so.*
(lfs chroot) root:/sources/readline-8.0 # ln -sfv ../../lib/$(readlink /usr/lib/libreadline.so) /usr/lib/libreadline.so
(lfs chroot) root:/sources/readline-8.0 # ln -sfv ../../lib/$(readlink /usr/lib/libhistory.so ) /usr/lib/libhistory.so
(lfs chroot) root:/sources/readline-8.0 # install -v -m644 doc/*.{ps,pdf,html,dvi} /usr/share/doc/readline-8.0
```


### m4

```bash
(lfs chroot) root:/sources # tar xf m4-1.4.18.tar.xz 
(lfs chroot) root:/sources # cd m4-1.4.18
(lfs chroot) root:/sources/m4-1.4.18 # sed -i 's/IO_ftrylockfile/IO_EOF_SEEN/' lib/*.c
(lfs chroot) root:/sources/m4-1.4.18 # echo "#define _IO_IN_BACKUP 0x100" >> lib/stdio-impl.h
(lfs chroot) root:/sources/m4-1.4.18 # ./configure --prefix=/usr
(lfs chroot) root:/sources/m4-1.4.18 # make
(lfs chroot) root:/sources/m4-1.4.18 # make check
(lfs chroot) root:/sources/m4-1.4.18 # make install
```


### bc

```bash
(lfs chroot) root:/sources # tar xf bc-2.5.3.tar.gz 
(lfs chroot) root:/sources # cd bc-2.5.3
(lfs chroot) root:/sources/bc-2.5.3 # PREFIX=/usr CC=gcc CFLAGS="-std=c99" ./configure.sh -G -O3
(lfs chroot) root:/sources/bc-2.5.3 # make
(lfs chroot) root:/sources/bc-2.5.3 # make test
(lfs chroot) root:/sources/bc-2.5.3 # make install
```


### binutils

```bash
(lfs chroot) root:/sources # expect -c "spawn ls"
(lfs chroot) root:/sources # tar xf binutils-2.34.tar.xz 
(lfs chroot) root:/sources # cd binutils-2.34
(lfs chroot) root:/sources/binutils-2.34 # sed -i '/@\tincremental_copy/d' gold/testsuite/Makefile.in
(lfs chroot) root:/sources/binutils-2.34 # mkdir build
(lfs chroot) root:/sources/binutils-2.34 # cd build
(lfs chroot) root:/sources/binutils-2.34/build # ../configure --prefix=/usr  \
  --enable-gold       \
  --enable-ld=default \
  --enable-plugins    \
  --enable-shared     \
  --disable-werror    \
  --enable-64-bit-bfd \
  --with-system-zlib
(lfs chroot) root:/sources/binutils-2.34/build # make tooldir=/usr
(lfs chroot) root:/sources/binutils-2.34/build # make -k check
(lfs chroot) root:/sources/binutils-2.34/build # make tooldir=/usr install
```


### gmp

```bash
(lfs chroot) root:/sources # tar xf gmp-6.2.0.tar.xz 
(lfs chroot) root:/sources # cd gmp-6.2.0

# not optimized host processor
(lfs chroot) root:/sources/gmp-6.2.0 # cp -v configfsf.guess config.guess
(lfs chroot) root:/sources/gmp-6.2.0 # cp -v configfsf.sub   config.sub

(lfs chroot) root:/sources/gmp-6.2.0 # ./configure --prefix=/usr    \
  --enable-cxx     \
  --disable-static \
  --docdir=/usr/share/doc/gmp-6.2.0
(lfs chroot) root:/sources/gmp-6.2.0 # make
(lfs chroot) root:/sources/gmp-6.2.0 # make html
(lfs chroot) root:/sources/gmp-6.2.0 # make check 2>&1 | tee gmp-check-log
(lfs chroot) root:/sources/gmp-6.2.0 # awk '/# PASS:/{total+=$3} ; END{print total}' gmp-check-log
(lfs chroot) root:/sources/gmp-6.2.0 # make install
(lfs chroot) root:/sources/gmp-6.2.0 # make install-html
```


### mpfr

```bash
(lfs chroot) root:/sources # tar xf mpfr-4.0.2.tar.xz 
(lfs chroot) root:/sources # cd mpfr-4.0.2
(lfs chroot) root:/sources/mpfr-4.0.2 # ./configure --prefix=/usr        \
  --disable-static     \
  --enable-thread-safe \
  --docdir=/usr/share/doc/mpfr-4.0.2
(lfs chroot) root:/sources/mpfr-4.0.2 # make check
(lfs chroot) root:/sources/mpfr-4.0.2 # make install
(lfs chroot) root:/sources/mpfr-4.0.2 # make install-html
```


### mpc

```bash
(lfs chroot) root:/sources # tar xf mpc-1.1.0.tar.gz 
(lfs chroot) root:/sources # cd mpc-1.1.0
(lfs chroot) root:/sources/mpc-1.1.0 # ./configure --prefix=/usr    \
  --disable-static \
  --docdir=/usr/share/doc/mpc-1.1.0
(lfs chroot) root:/sources/mpc-1.1.0 # make
(lfs chroot) root:/sources/mpc-1.1.0 # make html
(lfs chroot) root:/sources/mpc-1.1.0 # make check
(lfs chroot) root:/sources/mpc-1.1.0 # make install
(lfs chroot) root:/sources/mpc-1.1.0 # make install-html
```


### attr

```bash
(lfs chroot) root:/sources # tar xf attr-2.4.48.tar.gz 
(lfs chroot) root:/sources # cd attr-2.4.48
(lfs chroot) root:/sources/attr-2.4.48 # ./configure --prefix=/usr     \
  --bindir=/bin     \
  --disable-static  \
  --sysconfdir=/etc \
  --docdir=/usr/share/doc/attr-2.4.48
(lfs chroot) root:/sources/attr-2.4.48 # make
(lfs chroot) root:/sources/attr-2.4.48 # make check
(lfs chroot) root:/sources/attr-2.4.48 # make install
(lfs chroot) root:/sources/attr-2.4.48 # mv -v /usr/lib/libattr.so.* /lib
(lfs chroot) root:/sources/attr-2.4.48 # ln -sfv ../../lib/$(readlink /usr/lib/libattr.so) /usr/lib/libattr.so
```


### acl

```bash
(lfs chroot) root:/sources # tar xf acl-2.2.53.tar.gz 
(lfs chroot) root:/sources # cd acl-2.2.53
(lfs chroot) root:/sources/acl-2.2.53 # ./configure --prefix=/usr         \
  --bindir=/bin         \
  --disable-static      \
  --libexecdir=/usr/lib \
  --docdir=/usr/share/doc/acl-2.2.53
(lfs chroot) root:/sources/acl-2.2.53 # make
(lfs chroot) root:/sources/acl-2.2.53 # make install
(lfs chroot) root:/sources/acl-2.2.53 # mv -v /usr/lib/libacl.so.* /lib
(lfs chroot) root:/sources/acl-2.2.53 # ln -sfv ../../lib/$(readlink /usr/lib/libacl.so) /usr/lib/libacl.so
```

### shadow

```bash
(lfs chroot) root:/sources # tar xf shadow-4.8.1.tar.xz 
(lfs chroot) root:/sources # cd shadow-4.8.1
(lfs chroot) root:/sources/shadow-4.8.1 # sed -i 's/groups$(EXEEXT) //' src/Makefile.in
(lfs chroot) root:/sources/shadow-4.8.1 # find man -name Makefile.in -exec sed -i 's/groups\.1 / /'   {} \;
(lfs chroot) root:/sources/shadow-4.8.1 # find man -name Makefile.in -exec sed -i 's/getspnam\.3 / /' {} \;
(lfs chroot) root:/sources/shadow-4.8.1 # find man -name Makefile.in -exec sed -i 's/passwd\.5 / /'   {} \;
(lfs chroot) root:/sources/shadow-4.8.1 # sed -i -e 's@#ENCRYPT_METHOD DES@ENCRYPT_METHOD SHA512@' \
       -e 's@/var/spool/mail@/var/mail@' etc/login.defs
(lfs chroot) root:/sources/shadow-4.8.1 # sed -i 's/1000/999/' etc/useradd
(lfs chroot) root:/sources/shadow-4.8.1 # ./configure --sysconfdir=/etc --with-group-name-max-length=32
(lfs chroot) root:/sources/shadow-4.8.1 # make
(lfs chroot) root:/sources/shadow-4.8.1 # make install
```

```bash
(lfs chroot) root:~ # pwconv
(lfs chroot) root:~ # cat /etc/passwd
(lfs chroot) root:~ # cat /etc/shadow

(lfs chroot) root:~ # grpconv
(lfs chroot) root:~ # cat /etc/group
(lfs chroot) root:~ # cat /etc/gshadow

(lfs chroot) root:~ # sed -i 's/yes/no/' /etc/default/useradd
(lfs chroot) root:~ # passwd root
```


### gcc

```bash
(lfs chroot) root:/sources # tar xf gcc-9.2.0.tar.xz 
(lfs chroot) root:/sources # cd gcc-9.2.0
(lfs chroot) root:/sources/gcc-9.2.0 # case $(uname -m) in
  x86_64)
    sed -e '/m64=/s/lib64/lib/' \
        -i.orig gcc/config/i386/t-linux64
  ;;
esac
(lfs chroot) root:/sources/gcc-9.2.0 # sed -e '1161 s|^|//|' \
    -i libsanitizer/sanitizer_common/sanitizer_platform_limits_posix.cc

(lfs chroot) root:/sources/gcc-9.2.0 # mkdir build
(lfs chroot) root:/sources/gcc-9.2.0 # cd build/
(lfs chroot) root:/sources/gcc-9.2.0/build #  SED=sed                               \
../configure --prefix=/usr            \
             --enable-languages=c,c++ \
             --disable-multilib       \
             --disable-bootstrap      \
             --with-system-zlib
(lfs chroot) root:/sources/gcc-9.2.0/build # make
(lfs chroot) root:/sources/gcc-9.2.0/build # ulimit -s 32768
(lfs chroot) root:/sources/gcc-9.2.0/build # chown -Rv nobody . 
(lfs chroot) root:/sources/gcc-9.2.0/build # su nobody -s /bin/bash -c "PATH=$PATH make -k check"
(lfs chroot) root:/sources/gcc-9.2.0/build # ../contrib/test_summary
(lfs chroot) root:/sources/gcc-9.2.0/build # make install
(lfs chroot) root:/sources/gcc-9.2.0/build # rm -rf /usr/lib/gcc/$(gcc -dumpmachine)/9.2.0/include-fixed/bits/
(lfs chroot) root:/sources/gcc-9.2.0/build # chown -v -R root:root /usr/lib/gcc/*linux-gnu/9.2.0/include{,-fixed}
(lfs chroot) root:/sources/gcc-9.2.0/build # ln -sv ../usr/bin/cpp /lib
(lfs chroot) root:/sources/gcc-9.2.0/build # ln -sv gcc /usr/bin/cc
(lfs chroot) root:/sources/gcc-9.2.0/build # install -v -dm755 /usr/lib/bfd-plugins
(lfs chroot) root:/sources/gcc-9.2.0/build # ln -sfv ../../libexec/gcc/$(gcc -dumpmachine)/9.2.0/liblto_plugin.so /usr/lib/bfd-plugins/

(lfs chroot) root:/sources/gcc-9.2.0/build # echo 'int main(){}' > dummy.c
(lfs chroot) root:/sources/gcc-9.2.0/build # cc dummy.c -v -Wl,--verbose &> dummy.log
(lfs chroot) root:/sources/gcc-9.2.0/build # readelf -l a.out | grep ': /lib'
(lfs chroot) root:/sources/gcc-9.2.0/build # grep -o '/usr/lib.*/crt[1in].*succeeded' dummy.log
(lfs chroot) root:/sources/gcc-9.2.0/build # grep -B4 '^ /usr/include' dummy.log
(lfs chroot) root:/sources/gcc-9.2.0/build # grep 'SEARCH.*/usr/lib' dummy.log |sed 's|; |\n|g'
(lfs chroot) root:/sources/gcc-9.2.0/build # grep "/lib.*/libc.so.6 " dummy.log
(lfs chroot) root:/sources/gcc-9.2.0/build # grep found dummy.log
(lfs chroot) root:/sources/gcc-9.2.0/build # rm -v dummy.c a.out dummy.log

(lfs chroot) root:/sources/gcc-9.2.0/build # mkdir -pv /usr/share/gdb/auto-load/usr/lib
(lfs chroot) root:/sources/gcc-9.2.0/build # mv -v /usr/lib/*gdb.py /usr/share/gdb/auto-load/usr/lib
```


### pkg-config

```bash
(lfs chroot) root:/sources # tar xf pkg-config-0.29.2.tar.gz 
(lfs chroot) root:/sources # cd pkg-config-0.29.2
(lfs chroot) root:/sources/pkg-config-0.29.2 # ./configure --prefix=/usr \
  --with-internal-glib       \
  --disable-host-tool        \
  --docdir=/usr/share/doc/pkg-config-0.29.2
(lfs chroot) root:/sources/pkg-config-0.29.2 # make
(lfs chroot) root:/sources/pkg-config-0.29.2 # make check
(lfs chroot) root:/sources/pkg-config-0.29.2 # make install
```


### ncurses

```bash
(lfs chroot) root:/sources # tar xf ncurses-6.2.tar.gz 
(lfs chroot) root:/sources # cd ncurses-6.2
(lfs chroot) root:/sources/ncurses-6.2 # sed -i '/LIBTOOL_INSTALL/d' c++/Makefile.in
(lfs chroot) root:/sources/ncurses-6.2 # ./configure --prefix=/usr \
  --mandir=/usr/share/man \
  --with-shared           \
  --without-debug         \
  --without-normal        \
  --enable-pc-files       \
  --enable-widec 
(lfs chroot) root:/sources/ncurses-6.2 # make
(lfs chroot) root:/sources/ncurses-6.2 # make install


(lfs chroot) root:/sources/ncurses-6.2 # mv -v /usr/lib/libncursesw.so.6* /lib
(lfs chroot) root:/sources/ncurses-6.2 # ln -sfv ../../lib/$(readlink /usr/lib/libncursesw.so) /usr/lib/libncursesw.so
(lfs chroot) root:/sources/ncurses-6.2 # for lib in ncurses form panel menu ; do
    rm -vf                    /usr/lib/lib${lib}.so
    echo "INPUT(-l${lib}w)" > /usr/lib/lib${lib}.so
    ln -sfv ${lib}w.pc        /usr/lib/pkgconfig/${lib}.pc
done
(lfs chroot) root:/sources/ncurses-6.2 # rm -vf                     /usr/lib/libcursesw.so
(lfs chroot) root:/sources/ncurses-6.2 # echo "INPUT(-lncursesw)" > /usr/lib/libcursesw.so
(lfs chroot) root:/sources/ncurses-6.2 # ln -sfv libncurses.so      /usr/lib/libcurses.so
(lfs chroot) root:/sources/ncurses-6.2 # mkdir -v       /usr/share/doc/ncurses-6.2
(lfs chroot) root:/sources/ncurses-6.2 # cp -v -R doc/* /usr/share/doc/ncurses-6.2
```


### libcap

```bash
(lfs chroot) root:/sources # tar xf libcap-2.31.tar.xz 
(lfs chroot) root:/sources # cd libcap-2.31
(lfs chroot) root:/sources/libcap-2.31 # sed -i '/install.*STA...LIBNAME/d' libcap/Makefile
(lfs chroot) root:/sources/libcap-2.31 # make lib=lib
(lfs chroot) root:/sources/libcap-2.31 # make test
(lfs chroot) root:/sources/libcap-2.31 # make lib=lib install
(lfs chroot) root:/sources/libcap-2.31 # chmod -v 755 /lib/libcap.so.2.31
```


### sed

```bash
(lfs chroot) root:/sources # tar xf sed-4.8.tar.xz 
(lfs chroot) root:/sources # cd sed-4.8
(lfs chroot) root:/sources/sed-4.8 # sed -i 's/usr/tools/'                 build-aux/help2man
(lfs chroot) root:/sources/sed-4.8 # sed -i 's/testsuite.panic-tests.sh//' Makefile.in
(lfs chroot) root:/sources/sed-4.8 # ./configure --prefix=/usr --bindir=/bin
(lfs chroot) root:/sources/sed-4.8 # make
(lfs chroot) root:/sources/sed-4.8 # make html
(lfs chroot) root:/sources/sed-4.8 # make check
(lfs chroot) root:/sources/sed-4.8 # make install
(lfs chroot) root:/sources/sed-4.8 # install -d -m755           /usr/share/doc/sed-4.8
(lfs chroot) root:/sources/sed-4.8 # install -m644 doc/sed.html /usr/share/doc/sed-4.8
```


### psmisc

```bash
(lfs chroot) root:/sources # tar xf psmisc-23.2.tar.xz 
(lfs chroot) root:/sources # cd psmisc-23.2
(lfs chroot) root:/sources/psmisc-23.2 # ./configure --prefix=/usr
(lfs chroot) root:/sources/psmisc-23.2 # make
(lfs chroot) root:/sources/psmisc-23.2 # make install
(lfs chroot) root:/sources/psmisc-23.2 # mv -v /usr/bin/fuser   /bin
(lfs chroot) root:/sources/psmisc-23.2 # mv -v /usr/bin/killall /bin
```


### iana-etc

```bash
(lfs chroot) root:/sources # tar xf iana-etc-2.30.tar.bz2 
(lfs chroot) root:/sources # cd iana-etc-2.30
(lfs chroot) root:/sources/iana-etc-2.30 # make
(lfs chroot) root:/sources/iana-etc-2.30 # make install
```

### bison

```bash
(lfs chroot) root:/sources # tar xf bison-3.5.2.tar.xz 
(lfs chroot) root:/sources # cd bison-3.5.2
(lfs chroot) root:/sources/bison-3.5.2 # ./configure --prefix=/usr --docdir=/usr/share/doc/bison-3.5.2
(lfs chroot) root:/sources/bison-3.5.2 # make
(lfs chroot) root:/sources/bison-3.5.2 # make install
```


### flex

```bash
(lfs chroot) root:/sources # tar xf flex-2.6.4.tar.gz 
(lfs chroot) root:/sources # cd flex-2.6.4
(lfs chroot) root:/sources/flex-2.6.4 # sed -i "/math.h/a #include <malloc.h>" src/flexdef.h
(lfs chroot) root:/sources/flex-2.6.4 # HELP2MAN=/tools/bin/true ./configure --prefix=/usr --docdir=/usr/share/doc/flex-2.6.4
(lfs chroot) root:/sources/flex-2.6.4 # make
(lfs chroot) root:/sources/flex-2.6.4 # make check
(lfs chroot) root:/sources/flex-2.6.4 # make install
(lfs chroot) root:/sources/flex-2.6.4 # ln -sv flex /usr/bin/lex
```


### grep

```bash
(lfs chroot) root:/sources # tar xf grep-3.4.tar.xz 
(lfs chroot) root:/sources # cd grep-3.4
(lfs chroot) root:/sources/grep-3.4 # ./configure --prefix=/usr --bindir=/bin
(lfs chroot) root:/sources/grep-3.4 # make
(lfs chroot) root:/sources/grep-3.4 # make check
(lfs chroot) root:/sources/grep-3.4 # make install
```


### bash

```bash
(lfs chroot) root:/sources # tar xf bash-5.0.tar.gz 
(lfs chroot) root:/sources # cd bash-5.0
(lfs chroot) root:/sources/bash-5.0 # patch -Np1 -i ../bash-5.0-upstream_fixes-1.patch
(lfs chroot) root:/sources/bash-5.0 # ./configure --prefix=/usr \
  --docdir=/usr/share/doc/bash-5.0 \
  --without-bash-malloc            \
  --with-installed-readline
(lfs chroot) root:/sources/bash-5.0 # make 
(lfs chroot) root:/sources/bash-5.0 # chown -Rv nobody .
(lfs chroot) root:/sources/bash-5.0 # su nobody -s /bin/bash -c "PATH=$PATH HOME=/home make tests"
(lfs chroot) root:/sources/bash-5.0 # make install
(lfs chroot) root:/sources/bash-5.0 # mv -vf /usr/bin/bash /bin
(lfs chroot) root:/sources/bash-5.0 # exec /bin/bash --login +h
```


### libtool

```bash
(lfs chroot) root:/sources # tar xf libtool-2.4.6.tar.xz 
(lfs chroot) root:/sources # cd libtool-2.4.6
(lfs chroot) root:/sources/libtool-2.4.6 # ./configure --prefix=/usr
(lfs chroot) root:/sources/libtool-2.4.6 # make
(lfs chroot) root:/sources/libtool-2.4.6 # make check
(lfs chroot) root:/sources/libtool-2.4.6 # make install
```


### gdbm

```bash
(lfs chroot) root:/sources # tar xf gdbm-1.18.1.tar.gz 
(lfs chroot) root:/sources # cd gdbm-1.18.1
(lfs chroot) root:/sources/gdbm-1.18.1 # ./configure --prefix=/usr    \
  --disable-static \
  --enable-libgdbm-compat
(lfs chroot) root:/sources/gdbm-1.18.1 # make
(lfs chroot) root:/sources/gdbm-1.18.1 # make check
(lfs chroot) root:/sources/gdbm-1.18.1 # make install
```


### gperf

```bash
(lfs chroot) root:/sources # tar xf gperf-3.1.tar.gz 
(lfs chroot) root:/sources # cd gperf-3.1
(lfs chroot) root:/sources/gperf-3.1 # ./configure --prefix=/usr --docdir=/usr/share/doc/gperf-3.1
(lfs chroot) root:/sources/gperf-3.1 # make
(lfs chroot) root:/sources/gperf-3.1 # make -j1 check
(lfs chroot) root:/sources/gperf-3.1 # make install
```


### expat

```bash
(lfs chroot) root:/sources # tar xf expat-2.2.9.tar.xz 
(lfs chroot) root:/sources # cd expat-2.2.9
(lfs chroot) root:/sources/expat-2.2.9 # sed -i 's|usr/bin/env |bin/|' run.sh.in
(lfs chroot) root:/sources/expat-2.2.9 # ./configure --prefix=/usr \
  --disable-static \
  --docdir=/usr/share/doc/expat-2.2.9
(lfs chroot) root:/sources/expat-2.2.9 # make
(lfs chroot) root:/sources/expat-2.2.9 # make check
(lfs chroot) root:/sources/expat-2.2.9 # make install
(lfs chroot) root:/sources/expat-2.2.9 # install -v -m644 doc/*.{html,png,css} /usr/share/doc/expat-2.2.9
```


### inetutils

```bash
(lfs chroot) root:/sources # tar xf inetutils-1.9.4.tar.xz 
(lfs chroot) root:/sources # cd inetutils-1.9.4
(lfs chroot) root:/sources/inetutils-1.9.4 # ./configure --prefix=/usr \
  --localstatedir=/var \
  --disable-logger     \
  --disable-whois      \
  --disable-rcp        \
  --disable-rexec      \
  --disable-rlogin     \
  --disable-rsh        \
  --disable-servers
(lfs chroot) root:/sources/inetutils-1.9.4 # make
(lfs chroot) root:/sources/inetutils-1.9.4 # make check
(lfs chroot) root:/sources/inetutils-1.9.4 # make install
(lfs chroot) root:/sources/inetutils-1.9.4 # mv -v /usr/bin/{hostname,ping,ping6,traceroute} /bin
(lfs chroot) root:/sources/inetutils-1.9.4 # mv -v /usr/bin/ifconfig /sbin
```


### perl

```bash
(lfs chroot) root:/sources # tar xf perl-5.30.1.tar.xz 
(lfs chroot) root:/sources # cd perl-5.30.1
(lfs chroot) root:/sources/perl-5.30.1 # echo "127.0.0.1 localhost $(hostname)" > /etc/hosts
(lfs chroot) root:/sources/perl-5.30.1 # export BUILD_ZLIB=False
(lfs chroot) root:/sources/perl-5.30.1 # export BUILD_BZIP2=0
(lfs chroot) root:/sources/perl-5.30.1 # sh Configure -des -Dprefix=/usr                 \
  -Dvendorprefix=/usr           \
  -Dman1dir=/usr/share/man/man1 \
  -Dman3dir=/usr/share/man/man3 \
  -Dpager="/usr/bin/less -isR"  \
  -Duseshrplib                  \
  -Dusethreads
(lfs chroot) root:/sources/perl-5.30.1 # make
(lfs chroot) root:/sources/perl-5.30.1 # make test
(lfs chroot) root:/sources/perl-5.30.1 # make install
(lfs chroot) root:/sources/perl-5.30.1 # unset BUILD_ZLIB BUILD_BZIP2
```


### xml

```bash
(lfs chroot) root:/sources # tar xf XML-Parser-2.46.tar.gz 
(lfs chroot) root:/sources # cd XML-Parser-2.46
(lfs chroot) root:/sources/XML-Parser-2.46 # perl Makefile.PL
(lfs chroot) root:/sources/XML-Parser-2.46 # make
(lfs chroot) root:/sources/XML-Parser-2.46 # make test
(lfs chroot) root:/sources/XML-Parser-2.46 # make install
```


### intltool

```bash
(lfs chroot) root:/sources # tar xf intltool-0.51.0.tar.gz 
(lfs chroot) root:/sources # cd intltool-0.51.0
(lfs chroot) root:/sources/intltool-0.51.0 # sed -i 's:\\\${:\\\$\\{:' intltool-update.in
(lfs chroot) root:/sources/intltool-0.51.0 # ./configure --prefix=/usr
(lfs chroot) root:/sources/intltool-0.51.0 # make
(lfs chroot) root:/sources/intltool-0.51.0 # make check
(lfs chroot) root:/sources/intltool-0.51.0 # make install
(lfs chroot) root:/sources/intltool-0.51.0 # install -v -Dm644 doc/I18N-HOWTO /usr/share/doc/intltool-0.51.0/I18N-HOWTO
```


### autoconf

```bash
(lfs chroot) root:/sources # tar xf autoconf-2.69.tar.xz 
(lfs chroot) root:/sources # cd autoconf-2.69
(lfs chroot) root:/sources/autoconf-2.69 # sed '361 s/{/\\{/' -i bin/autoscan.in
(lfs chroot) root:/sources/autoconf-2.69 # ./configure --prefix=/usr
(lfs chroot) root:/sources/autoconf-2.69 # make
(lfs chroot) root:/sources/autoconf-2.69 # make check
(lfs chroot) root:/sources/autoconf-2.69 # make install
```


### automake

```bash
(lfs chroot) root:/sources # tar xf automake-1.16.1.tar.xz
(lfs chroot) root:/sources # cd automake-1.16.1
(lfs chroot) root:/sources/automake-1.16.1 # ./configure --prefix=/usr --docdir=/usr/share/doc/automake-1.16.1
(lfs chroot) root:/sources/automake-1.16.1 # make
(lfs chroot) root:/sources/automake-1.16.1 # make -j4 check
(lfs chroot) root:/sources/automake-1.16.1 # make install
```


### kmod

```bash
(lfs chroot) root:/sources # tar xf kmod-26.tar.xz 
(lfs chroot) root:/sources # cd kmod-26
(lfs chroot) root:/sources/kmod-26 # ./configure --prefix=/usr \
  --bindir=/bin          \
  --sysconfdir=/etc      \
  --with-rootlibdir=/lib \
  --with-xz              \
  --with-zlib
(lfs chroot) root:/sources/kmod-26 # make
(lfs chroot) root:/sources/kmod-26 # make install
(lfs chroot) root:/sources/kmod-26 # for target in depmod insmod lsmod modinfo modprobe rmmod; do
  ln -sfv ../bin/kmod /sbin/$target
done
(lfs chroot) root:/sources/kmod-26 # ln -sfv kmod /bin/lsmod
```


### gettext

```bash
(lfs chroot) root:/sources # tar xf gettext-0.20.1.tar.xz 
(lfs chroot) root:/sources # cd gettext-0.20.1
(lfs chroot) root:/sources/gettext-0.20.1 # ./configure --prefix=/usr    \
  --disable-static \
  --docdir=/usr/share/doc/gettext-0.20.1
(lfs chroot) root:/sources/gettext-0.20.1 # make
(lfs chroot) root:/sources/gettext-0.20.1 # make check
(lfs chroot) root:/sources/gettext-0.20.1 # make install
(lfs chroot) root:/sources/gettext-0.20.1 # chmod -v 0755 /usr/lib/preloadable_libintl.so
```


### elfutils

```bash
(lfs chroot) root:/sources # tar xf elfutils-0.178.tar.bz2 
(lfs chroot) root:/sources # cd elfutils-0.178
(lfs chroot) root:/sources/elfutils-0.178 # ./configure --prefix=/usr --disable-debuginfod
(lfs chroot) root:/sources/elfutils-0.178 # make
(lfs chroot) root:/sources/elfutils-0.178 # make check
(lfs chroot) root:/sources/elfutils-0.178 # make -C libelf install
(lfs chroot) root:/sources/elfutils-0.178 # install -vm644 config/libelf.pc /usr/lib/pkgconfig
(lfs chroot) root:/sources/elfutils-0.178 # rm /usr/lib/libelf.a
```


### libffi

```bash
(lfs chroot) root:/sources # tar xf libffi-3.3.tar.gz 
(lfs chroot) root:/sources # cd libffi-3.3
(lfs chroot) root:/sources/libffi-3.3 # ./configure --prefix=/usr --disable-static --with-gcc-arch=native
(lfs chroot) root:/sources/libffi-3.3 # make
(lfs chroot) root:/sources/libffi-3.3 # make check
(lfs chroot) root:/sources/libffi-3.3 # make install
```


### openssl

```bash
(lfs chroot) root:/sources # tar xf openssl-1.1.1d.tar.gz 
(lfs chroot) root:/sources # cd openssl-1.1.1d
(lfs chroot) root:/sources/openssl-1.1.1d # ./config --prefix=/usr \
  --openssldir=/etc/ssl \
  --libdir=lib          \
  shared                \
  zlib-dynamic
(lfs chroot) root:/sources/openssl-1.1.1d # make
(lfs chroot) root:/sources/openssl-1.1.1d # make test
(lfs chroot) root:/sources/openssl-1.1.1d # sed -i '/INSTALL_LIBS/s/libcrypto.a libssl.a//' Makefile
(lfs chroot) root:/sources/openssl-1.1.1d # make MANSUFFIX=ssl install
(lfs chroot) root:/sources/openssl-1.1.1d # mv -v /usr/share/doc/openssl /usr/share/doc/openssl-1.1.1d
(lfs chroot) root:/sources/openssl-1.1.1d # cp -vfr doc/* /usr/share/doc/openssl-1.1.1d
```


### python

```bash
(lfs chroot) root:/sources # tar xf Python-3.8.1.tar.xz 
(lfs chroot) root:/sources # cd Python-3.8.1
(lfs chroot) root:/sources/Python-3.8.1 # ./configure --prefix=/usr \
  --enable-shared     \
  --with-system-expat \
  --with-system-ffi   \
  --with-ensurepip=yes
(lfs chroot) root:/sources/Python-3.8.1 # make
(lfs chroot) root:/sources/Python-3.8.1 # make install
(lfs chroot) root:/sources/Python-3.8.1 # chmod -v 755 /usr/lib/libpython3.8.so
(lfs chroot) root:/sources/Python-3.8.1 # chmod -v 755 /usr/lib/libpython3.so
(lfs chroot) root:/sources/Python-3.8.1 # ln -sfv pip3.8 /usr/bin/pip3
(lfs chroot) root:/sources/Python-3.8.1 # install -v -dm755 /usr/share/doc/python-3.8.1/html 
(lfs chroot) root:/sources/Python-3.8.1 # tar --strip-components=1  \
  --no-same-owner       \
  --no-same-permissions \
  -C /usr/share/doc/python-3.8.1/html \
  -xvf ../python-3.8.1-docs-html.tar.bz2
```


### ninja

```bash
(lfs chroot) root:/sources # tar xf ninja-1.10.0.tar.gz 
(lfs chroot) root:/sources # cd ninja-1.10.0
(lfs chroot) root:/sources/ninja-1.10.0 # export NINJAJOBS=4
(lfs chroot) root:/sources/ninja-1.10.0 # sed -i '/int Guess/a \
  int   j = 0;\
  char* jobs = getenv( "NINJAJOBS" );\
  if ( jobs != NULL ) j = atoi( jobs );\
  if ( j > 0 ) return j;\
' src/ninja.cc
(lfs chroot) root:/sources/ninja-1.10.0 # python3 configure.py --bootstrap
(lfs chroot) root:/sources/ninja-1.10.0 # ./ninja ninja_test
(lfs chroot) root:/sources/ninja-1.10.0 # ./ninja_test --gtest_filter=-SubprocessTest.SetWithLots
(lfs chroot) root:/sources/ninja-1.10.0 # install -vm755 ninja /usr/bin/
(lfs chroot) root:/sources/ninja-1.10.0 # install -vDm644 misc/bash-completion /usr/share/bash-completion/completions/ninja
(lfs chroot) root:/sources/ninja-1.10.0 # install -vDm644 misc/zsh-completion  /usr/share/zsh/site-functions/_ninja
```


### meson

```bash
(lfs chroot) root:/sources # tar xf meson-0.53.1.tar.gz 
(lfs chroot) root:/sources # cd meson-0.53.1
(lfs chroot) root:/sources/meson-0.53.1 # python3 setup.py build
(lfs chroot) root:/sources/meson-0.53.1 # python3 setup.py install --root=dest
(lfs chroot) root:/sources/meson-0.53.1 # cp -rv dest/* /
```


### coreutils

```bash
(lfs chroot) root:/sources # tar xf coreutils-8.31.tar.xz
(lfs chroot) root:/sources # cd coreutils-8.31
(lfs chroot) root:/sources/coreutils-8.31 # patch -Np1 -i ../coreutils-8.31-i18n-1.patch
(lfs chroot) root:/sources/coreutils-8.31 # sed -i '/test.lock/s/^/#/' gnulib-tests/gnulib.mk
(lfs chroot) root:/sources/coreutils-8.31 # autoreconf -fiv
(lfs chroot) root:/sources/coreutils-8.31 # FORCE_UNSAFE_CONFIGURE=1 ./configure \
  --prefix=/usr            \
  --enable-no-install-program=kill,uptime
(lfs chroot) root:/sources/coreutils-8.31 # make
(lfs chroot) root:/sources/coreutils-8.31 # make NON_ROOT_USERNAME=nobody check-root
(lfs chroot) root:/sources/coreutils-8.31 # echo "dummy:x:1000:nobody" >> /etc/group
(lfs chroot) root:/sources/coreutils-8.31 # chown -Rv nobody . 
(lfs chroot) root:/sources/coreutils-8.31 # su nobody -s /bin/bash -c "PATH=$PATH make RUN_EXPENSIVE_TESTS=yes check"
(lfs chroot) root:/sources/coreutils-8.31 # sed -i '/dummy/d' /etc/group
(lfs chroot) root:/sources/coreutils-8.31 # make install
(lfs chroot) root:/sources/coreutils-8.31 # mv -v /usr/bin/{cat,chgrp,chmod,chown,cp,date,dd,df,echo} /bin
(lfs chroot) root:/sources/coreutils-8.31 # mv -v /usr/bin/{false,ln,ls,mkdir,mknod,mv,pwd,rm} /bin
(lfs chroot) root:/sources/coreutils-8.31 # mv -v /usr/bin/{rmdir,stty,sync,true,uname} /bin
(lfs chroot) root:/sources/coreutils-8.31 # mv -v /usr/bin/chroot /usr/sbin
(lfs chroot) root:/sources/coreutils-8.31 # mv -v /usr/share/man/man1/chroot.1 /usr/share/man/man8/chroot.8
(lfs chroot) root:/sources/coreutils-8.31 # sed -i s/\"1\"/\"8\"/1 /usr/share/man/man8/chroot.8
(lfs chroot) root:/sources/coreutils-8.31 # mv -v /usr/bin/{head,nice,sleep,touch} /bin
```


### check

```bash
(lfs chroot) root:/sources # tar xf check-0.14.0.tar.gz 
(lfs chroot) root:/sources # cd check-0.14.0
(lfs chroot) root:/sources/check-0.14.0 # ./configure --prefix=/usr
(lfs chroot) root:/sources/check-0.14.0 # make
(lfs chroot) root:/sources/check-0.14.0 # make check
(lfs chroot) root:/sources/check-0.14.0 # make docdir=/usr/share/doc/check-0.14.0 install
(lfs chroot) root:/sources/check-0.14.0 # sed -i '1 s/tools/usr/' /usr/bin/checkmk
```


### diffutils

```bash
(lfs chroot) root:/sources # tar xf diffutils-3.7.tar.xz 
(lfs chroot) root:/sources # cd diffutils-3.7
(lfs chroot) root:/sources/diffutils-3.7 # ./configure --prefix=/usr
(lfs chroot) root:/sources/diffutils-3.7 # make
(lfs chroot) root:/sources/diffutils-3.7 # make check
(lfs chroot) root:/sources/diffutils-3.7 # make install
```


### gawk

```bash
(lfs chroot) root:/sources # tar xf gawk-5.0.1.tar.xz 
(lfs chroot) root:/sources # cd gawk-5.0.1
(lfs chroot) root:/sources/gawk-5.0.1 # sed -i 's/extras//' Makefile.in
(lfs chroot) root:/sources/gawk-5.0.1 # ./configure --prefix=/usr
(lfs chroot) root:/sources/gawk-5.0.1 # make
(lfs chroot) root:/sources/gawk-5.0.1 # make check
(lfs chroot) root:/sources/gawk-5.0.1 # make install
(lfs chroot) root:/sources/gawk-5.0.1 # mkdir -v /usr/share/doc/gawk-5.0.1
(lfs chroot) root:/sources/gawk-5.0.1 # cp    -v doc/{awkforai.txt,*.{eps,pdf,jpg}} /usr/share/doc/gawk-5.0.1
```


### findutils

```bash
(lfs chroot) root:/sources # tar xf findutils-4.7.0.tar.xz  
(lfs chroot) root:/sources # cd findutils-4.7.0
(lfs chroot) root:/sources/findutils-4.7.0 # ./configure --prefix=/usr --localstatedir=/var/lib/locate
(lfs chroot) root:/sources/findutils-4.7.0 # make
(lfs chroot) root:/sources/findutils-4.7.0 # make check
(lfs chroot) root:/sources/findutils-4.7.0 # make install
(lfs chroot) root:/sources/findutils-4.7.0 # mv -v /usr/bin/find /bin
(lfs chroot) root:/sources/findutils-4.7.0 # sed -i 's|find:=${BINDIR}|find:=/bin|' /usr/bin/updatedb
```


### groff

```bash
(lfs chroot) root:/sources # tar zxf groff-1.22.4.tar.gz 
(lfs chroot) root:/sources # cd groff-1.22.4
(lfs chroot) root:/sources/groff-1.22.4 # PAGE=A4 ./configure --prefix=/usr
(lfs chroot) root:/sources/groff-1.22.4 # make -j1
(lfs chroot) root:/sources/groff-1.22.4 # make install
```


### grub

```bash
(lfs chroot) root:/sources # tar xf grub-2.04.tar.xz 
(lfs chroot) root:/sources # cd grub-2.04
(lfs chroot) root:/sources/grub-2.04 # ./configure --prefix=/usr          \
  --sbindir=/sbin        \
  --sysconfdir=/etc      \
  --disable-efiemu       \
  --disable-werror
(lfs chroot) root:/sources/grub-2.04 # make
(lfs chroot) root:/sources/grub-2.04 # make install
(lfs chroot) root:/sources/grub-2.04 # mv -v /etc/bash_completion.d/grub /usr/share/bash-completion/completions
```


### less

```bash
(lfs chroot) root:/sources # tar xf less-551.tar.gz 
(lfs chroot) root:/sources # cd less-551
(lfs chroot) root:/sources/less-551 # ./configure --prefix=/usr --sysconfdir=/etc
(lfs chroot) root:/sources/less-551 # make
(lfs chroot) root:/sources/less-551 # make install
```


### gzip

```bash
(lfs chroot) root:/sources # tar xf gzip-1.10.tar.xz 
(lfs chroot) root:/sources # cd gzip-1.10
(lfs chroot) root:/sources/gzip-1.10 # ./configure --prefix=/usr
(lfs chroot) root:/sources/gzip-1.10 # make
(lfs chroot) root:/sources/gzip-1.10 # make check
(lfs chroot) root:/sources/gzip-1.10 # make install
(lfs chroot) root:/sources/gzip-1.10 # mv -v /usr/bin/gzip /bin
```


### zstd

```bash
(lfs chroot) root:/sources # tar xf zstd-1.4.4.tar.gz 
(lfs chroot) root:/sources # cd zstd-1.4.4
(lfs chroot) root:/sources/zstd-1.4.4 # make
(lfs chroot) root:/sources/zstd-1.4.4 # make prefix=/usr install
(lfs chroot) root:/sources/zstd-1.4.4 # rm -v /usr/lib/libzstd.a
(lfs chroot) root:/sources/zstd-1.4.4 # mv -v /usr/lib/libzstd.so.* /lib
(lfs chroot) root:/sources/zstd-1.4.4 # ln -sfv ../../lib/$(readlink /usr/lib/libzstd.so) /usr/lib/libzstd.so
```


### iproute2

```bash
(lfs chroot) root:/sources # tar xf iproute2-5.5.0.tar.xz 
(lfs chroot) root:/sources # cd iproute2-5.5.0
(lfs chroot) root:/sources/iproute2-5.5.0 # sed -i /ARPD/d Makefile
(lfs chroot) root:/sources/iproute2-5.5.0 # rm -fv man/man8/arpd.8
(lfs chroot) root:/sources/iproute2-5.5.0 # sed -i 's/.m_ipt.o//' tc/Makefile
(lfs chroot) root:/sources/iproute2-5.5.0 # make
(lfs chroot) root:/sources/iproute2-5.5.0 # make DOCDIR=/usr/share/doc/iproute2-5.5.0 install
```


### kbd

```bash
(lfs chroot) root:/sources # tar xf kbd-2.2.0.tar.xz 
(lfs chroot) root:/sources # cd kbd-2.2.0
(lfs chroot) root:/sources/kbd-2.2.0 # patch -Np1 -i ../kbd-2.2.0-backspace-1.patch
(lfs chroot) root:/sources/kbd-2.2.0 # sed -i 's/\(RESIZECONS_PROGS=\)yes/\1no/g' configure
(lfs chroot) root:/sources/kbd-2.2.0 # sed -i 's/resizecons.8 //' docs/man/man8/Makefile.in
(lfs chroot) root:/sources/kbd-2.2.0 # PKG_CONFIG_PATH=/tools/lib/pkgconfig ./configure --prefix=/usr --disable-vlock
(lfs chroot) root:/sources/kbd-2.2.0 # make
(lfs chroot) root:/sources/kbd-2.2.0 # make check
(lfs chroot) root:/sources/kbd-2.2.0 # make install
(lfs chroot) root:/sources/kbd-2.2.0 # mkdir -v       /usr/share/doc/kbd-2.2.0
(lfs chroot) root:/sources/kbd-2.2.0 # cp -R -v docs/doc/* /usr/share/doc/kbd-2.2.0
```


### libpipeline

```bash
(lfs chroot) root:/sources # tar xf libpipeline-1.5.2.tar.gz 
(lfs chroot) root:/sources # cd libpipeline-1.5.2
(lfs chroot) root:/sources/libpipeline-1.5.2 # ./configure --prefix=/usr
(lfs chroot) root:/sources/libpipeline-1.5.2 # make
(lfs chroot) root:/sources/libpipeline-1.5.2 # make check
(lfs chroot) root:/sources/libpipeline-1.5.2 # make install
```


### make

```bash
(lfs chroot) root:/sources # tar xf make-4.3.tar.gz 
(lfs chroot) root:/sources # cd make-4.3
(lfs chroot) root:/sources/make-4.3 # ./configure --prefix=/usr
(lfs chroot) root:/sources/make-4.3 # make
(lfs chroot) root:/sources/make-4.3 # make PERL5LIB=$PWD/tests/ check
(lfs chroot) root:/sources/make-4.3 # make install
```


### patch

```bash
(lfs chroot) root:/sources # tar xf patch-2.7.6.tar.xz 
(lfs chroot) root:/sources # cd patch-2.7.6
(lfs chroot) root:/sources/patch-2.7.6 # ./configure --prefix=/usr
(lfs chroot) root:/sources/patch-2.7.6 # make
(lfs chroot) root:/sources/patch-2.7.6 # make check
(lfs chroot) root:/sources/patch-2.7.6 # make install
```


### man-db

```bash
(lfs chroot) root:/sources # tar xf man-db-2.9.0.tar.xz 
(lfs chroot) root:/sources # cd man-db-2.9.0
(lfs chroot) root:/sources/man-db-2.9.0 # ./configure --prefix=/usr                        \
  --docdir=/usr/share/doc/man-db-2.9.0 \
  --sysconfdir=/etc                    \
  --disable-setuid                     \
  --enable-cache-owner=bin             \
  --with-browser=/usr/bin/lynx         \
  --with-vgrind=/usr/bin/vgrind        \
  --with-grap=/usr/bin/grap            \
  --with-systemdtmpfilesdir=           \
  --with-systemdsystemunitdir=
(lfs chroot) root:/sources/man-db-2.9.0 # make
(lfs chroot) root:/sources/man-db-2.9.0 # make check
(lfs chroot) root:/sources/man-db-2.9.0 # make install
```


### tar

```bash
(lfs chroot) root:/sources # tar xf tar-1.32.tar.xz 
(lfs chroot) root:/sources # cd tar-1.32
(lfs chroot) root:/sources/tar-1.32 # FORCE_UNSAFE_CONFIGURE=1  \
  ./configure --prefix=/usr \
  --bindir=/bin
(lfs chroot) root:/sources/tar-1.32 # make
(lfs chroot) root:/sources/tar-1.32 # make check
(lfs chroot) root:/sources/tar-1.32 # make install
(lfs chroot) root:/sources/tar-1.32 # make -C doc install-html docdir=/usr/share/doc/tar-1.32
```


