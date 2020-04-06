# LFS


## host os

download kali linux livecd to boot

```bash
kali@kail:~ $ sudo su -

kali:~ # rm /bin/sh
kali:~ # ln -s /bin/sh /bin/bash
kali:~ # apt install bison
kali:~ # apt install texinfo


kali:~ # cat > version-check.sh << "EOF"
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

kali:~ # bash version-check.sh
```


---

## partition

```bash
kali:~ # lsblk

# fdisk
kali:~ # fdisk /dev/<disk>

# parted
kali:~ # parted /dev/<disk>
(parted) help
(parted) unit
(parted) mklable [msdos]
(parted) mkpart [primary linux-swap 512B 2GiB]
(parted) mkpart [primary ext4 2GiB -1]
(parted) print

kali:~ # parted -s /dev/sda mklabel msdos
kali:~ # parted -s /dev/sda mkpart primary linux-swap 512B 2GiB
kali:~ # parted -s /dev/sda mkpart primary ext4 2GiB 100%


# make filesystem
kali:~ # mkswap /dev/sda1 
kali:~ # mkfs.ext4 /dev/sda2

# mount disk
kali:~ # export LFS=/mnt/lfs
kali:~ # mkdir -pv $LFS
kali:~ # mount -v -t ext4 /dev/<disk> $LFS

kali:~ # swapon /dev/sda1
```


---

## package

```bash
kali:~ # mkdir -v $LFS/sources
kali:~ # chmod -v a+wt $LFS/sources
kali:~ # wget http://linuxfromscratch.org/lfs/view/stable-systemd/wget-list
kali:~ # wget --input-file=wget-list --continue --directory-prefix=$LFS/sources

kali:~ # wget http://linuxfromscratch.org/lfs/view/stable-systemd/md5sums --directory-prefix=$LFS/sources
kali:~ # pushd $LFS/sources
kali:sources # md5sum -c md5sums
kali:~ # popd
```


---

## lfs user

```bash
kali:~ # mkdir -v $LFS/tools
kali:~ # ln -sv $LFS/tools /

kali:~ # groupadd lfs
kali:~ # useradd -s /bin/bash -g lfs -m -k /dev/null lfs
kali:~ # passwd lfs
kali:~ # chown -v lfs $LFS/tools
kali:~ # chown -v lfs $LFS/sources
kali:~ # su - lfs

lfs@kail:~ $ cat > ~/.bash_profile << "EOF"
exec env -i HOME=$HOME TERM=$TERM PS1='\u:\w\$ ' /bin/bash
EOF

lfs@kail:~ $ cat > ~/.bashrc << "EOF"
set +h
umask 022
LFS=/mnt/lfs
LC_ALL=POSIX
LFS_TGT=$(uname -m)-lfs-linux-gnu
PATH=/tools/bin:/bin:/usr/bin
export LFS LC_ALL LFS_TGT PATH
EOF

lfs@kail:~ $ source ~/.bash_profile
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


## temporary system

### binutils pass1

```bash
lfs@kali:/mnt/lfs/sources $ mkdir -v -p binutils-2.34-pass1/build
lfs@kali:/mnt/lfs/sources $ tar xvf binutils-2.34.tar.xz -C binutils-2.34-pass1/

lfs@kali:/mnt/lfs/sources $ cd binutils-2.34-pass1/build
lfs@kali:/mnt/lfs/sources/binutils-2.34-pass1/build $ ../binutils-2.34/configure \
 --prefix=/tools            \
 --with-sysroot=$LFS        \
 --with-lib-path=/tools/lib \
 --target=$LFS_TGT          \
 --disable-nls              \
 --disable-werror
lfs@kali:/mnt/lfs/sources/binutils-2.34-pass1/build $ make
lfs@kali:/mnt/lfs/sources/binutils-2.34-pass1/build $ case $(uname -m) in
  x86_64) mkdir -v /tools/lib && ln -sv lib /tools/lib64 ;;
esac
lfs@kali:/mnt/lfs/sources/binutils-2.34-pass1/build $ make install
```

### gcc pass1

```bash
lfs@kali:/mnt/lfs/sources $ mkdir -v -p gcc-9.2.0-pass1/build
lfs@kali:/mnt/lfs/sources $ tar xvf gcc-9.2.0.tar.xz -C gcc-9.2.0-pass1/
lfs@kali:/mnt/lfs/sources $ tar xvf mpfr-4.0.2.tar.xz
lfs@kali:/mnt/lfs/sources $ mv -v mpfr-4.0.2 gcc-9.2.0-pass1/gcc-9.2.0/mpfr
lfs@kali:/mnt/lfs/sources $ tar xvf gmp-6.2.0.tar.xz
lfs@kali:/mnt/lfs/sources $ mv -v gmp-6.2.0 gcc-9.2.0-pass1/gcc-9.2.0/gmp
lfs@kali:/mnt/lfs/sources $ tar xvf mpc-1.1.0.tar.gz
lfs@kali:/mnt/lfs/sources $ mv -v mpc-1.1.0 gcc-9.2.0-pass1/gcc-9.2.0/mpc

lfs@kali:/mnt/lfs/sources $ cd gcc-9.2.0-pass1/gcc-9.2.0/
lfs@kali:/mnt/lfs/sources/gcc-9.2.0-pass1/gcc-9.2.0 $ for file in gcc/config/{linux,i386/linux{,64}}.h
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

lfs@kali:/mnt/lfs/sources/gcc-9.2.0-pass1/gcc-9.2.0 $ case $(uname -m) in
  x86_64)
    sed -e '/m64=/s/lib64/lib/' \
        -i.orig gcc/config/i386/t-linux64
 ;;
esac

lfs@kali:/mnt/lfs/sources $ cd gcc-9.2.0-pass1/build
lfs@kali:/mnt/lfs/sources/gcc-9.2.0-pass1/build $ ../gcc-9.2.0/configure \
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
lfs@kali:/mnt/lfs/sources/gcc-9.2.0-pass1/build $ make
lfs@kali:/mnt/lfs/sources/gcc-9.2.0-pass1/build $ make install
```

### linux header api

```bash
lfs@kali:/mnt/lfs/sources $ tar xvf linux-5.5.3.tar.xz

lfs@kali:/mnt/lfs/sources $ cd linux-5.5.3
lfs@kali:/mnt/lfs/sources/linux-5.5.3 $ make mrproper
lfs@kali:/mnt/lfs/sources/linux-5.5.3 $ make headers
lfs@kali:/mnt/lfs/sources/linux-5.5.3 $ cp -rv usr/include/* /tools/include
```

### glibc

```bash
lfs@kali:/mnt/lfs/sources $ tar xf glibc-2.31.tar.xz
lfs@kali:/mnt/lfs/sources $ cd glibc-2.31
lfs@kali:/mnt/lfs/sources/glibc-2.31 $ mkdir build

lfs@kali:/mnt/lfs/sources/glibc-2.31 $ cd build
lfs@kali:/mnt/lfs/sources/glibc-2.31/build $ ../configure \
    --prefix=/tools                    \
    --host=$LFS_TGT                    \
    --build=$(../scripts/config.guess) \
    --enable-kernel=3.2                \
    --with-headers=/tools/include
lfs@kali:/mnt/lfs/sources/glibc-2.31/build $ make
lfs@kali:/mnt/lfs/sources/glibc-2.31/build $ make install

lfs@kali:/mnt/lfs/sources/glibc-2.31/build $ echo 'int main(){}' > dummy.c
lfs@kali:/mnt/lfs/sources/glibc-2.31/build $ $LFS_TGT-gcc dummy.c
lfs@kali:/mnt/lfs/sources/glibc-2.31/build $ ldd a.out | grep /tools
lfs@kali:/mnt/lfs/sources/glibc-2.31/build $ readelf -l a.out | grep ': /tools'
```

### libstdc++

```bash
lfs@kali:/mnt/lfs/sources/gcc-9.2.0-pass1/gcc-9.2.0 $ mkdir build

lfs@kali:/mnt/lfs/sources/gcc-9.2.0-pass1/gcc-9.2.0 $ cd build/
lfs@kali:/mnt/lfs/sources/gcc-9.2.0-pass1/gcc-9.2.0/build $ ../libstdc++-v3/configure \
    --host=$LFS_TGT                 \
    --prefix=/tools                 \
    --disable-multilib              \
    --disable-nls                   \
    --disable-libstdcxx-threads     \
    --disable-libstdcxx-pch         \
    --with-gxx-include-dir=/tools/$LFS_TGT/include/c++/9.2.0
lfs@kali:/mnt/lfs/sources/gcc-9.2.0-pass1/gcc-9.2.0/build $ make
lfs@kali:/mnt/lfs/sources/gcc-9.2.0-pass1/gcc-9.2.0/build $ make install
```

### binutils pass2

```bash
lfs@kali:/mnt/lfs/sources $ mkdir -v -p binutils-2.34-pass2/build
lfs@kali:/mnt/lfs/sources $ tar xvf binutils-2.34.tar.xz -C binutils-2.34-pass2/

lfs@kali:/mnt/lfs/sources $ cd binutils-2.34-pass2/build
lfs@kali:/mnt/lfs/sources/binutils-2.34-pass2/build $ CC=$LFS_TGT-gcc
AR=$LFS_TGT-ar                 \
RANLIB=$LFS_TGT-ranlib         \
../binutils-2.34/configure     \
  --prefix=/tools              \
  --disable-nls                \
  --disable-werror             \
  --with-lib-path=/tools/lib   \
  --with-sysroot
lfs@kali:/mnt/lfs/sources/binutils-2.34-pass2/build $ make
lfs@kali:/mnt/lfs/sources/binutils-2.34-pass2/build $ make install
lfs@kali:/mnt/lfs/sources/binutils-2.34-pass2/build $ make -C ld clean
lfs@kali:/mnt/lfs/sources/binutils-2.34-pass2/build $ make -C ld LIB_PATH=/usr/lib:/lib
lfs@kali:/mnt/lfs/sources/binutils-2.34-pass2/build $ cp -v ld/ld-new /tools/bin
```

### gcc pass2

```bash
lfs@kali:/mnt/lfs/sources $ mkdir -v -p gcc-9.2.0-pass2/build
lfs@kali:/mnt/lfs/sources $ tar xvf gcc-9.2.0.tar.xz -C gcc-9.2.0-pass2/

lfs@kali:/mnt/lfs/sources $ cd gcc-9.2.0-pass2/gcc-9.2.0/
lfs@kali:/mnt/lfs/sources/gcc-9.2.0-pass2/gcc-9.2.0 $ cat gcc/limitx.h gcc/glimits.h gcc/limity.h > `dirname $($LFS_TGT-gcc -print-libgcc-file-name)`/include-fixed/limits.h
lfs@kali:/mnt/lfs/sources/gcc-9.2.0-pass2/gcc-9.2.0 $ for file in gcc/config/{linux,i386/linux{,64}}.h
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
lfs@kali:/mnt/lfs/sources/gcc-9.2.0-pass2/gcc-9.2.0 $ case $(uname -m) in
  x86_64)
    sed -e '/m64=/s/lib64/lib/' \
        -i.orig gcc/config/i386/t-linux64
  ;;
esac
lfs@kali:/mnt/lfs/sources/gcc-9.2.0-pass2/gcc-9.2.0 $ tar xvf ../../mpfr-4.0.2.tar.xz 
lfs@kali:/mnt/lfs/sources/gcc-9.2.0-pass2/gcc-9.2.0 $ mv mpfr-4.0.2/ mpfr
lfs@kali:/mnt/lfs/sources/gcc-9.2.0-pass2/gcc-9.2.0 $ tar xvf ../../gmp-6.2.0.tar.xz 
lfs@kali:/mnt/lfs/sources/gcc-9.2.0-pass2/gcc-9.2.0 $ mv gmp-6.2.0 gmp 
lfs@kali:/mnt/lfs/sources/gcc-9.2.0-pass2/gcc-9.2.0 $ tar xvf ../../mpc-1.1.0.tar.gz 
lfs@kali:/mnt/lfs/sources/gcc-9.2.0-pass2/gcc-9.2.0 $ mv mpc-1.1.0 mpc 
lfs@kali:/mnt/lfs/sources/gcc-9.2.0-pass2/gcc-9.2.0 $ sed -e '1161 s|^|//|' -i libsanitizer/sanitizer_common/sanitizer_platform_limits_posix.cc

lfs@kali:/mnt/lfs/sources/gcc-9.2.0-pass2 $ cd build
lfs@kali:/mnt/lfs/sources/gcc-9.2.0-pass2/build $ CC=$LFS_TGT-gcc \
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
lfs@kali:/mnt/lfs/sources/gcc-9.2.0-pass2/build $ make
lfs@kali:/mnt/lfs/sources/gcc-9.2.0-pass2/build $ make install

lfs@kali:/mnt/lfs/sources/gcc-9.2.0-pass2/build $ ln -sv gcc /tools/bin/cc
lfs@kali:/mnt/lfs/sources/gcc-9.2.0-pass2/build $ echo 'int main(){}' > dummy.c
lfs@kali:/mnt/lfs/sources/gcc-9.2.0-pass2/build $ cc dummy.c
lfs@kali:/mnt/lfs/sources/gcc-9.2.0-pass2/build $ ldd a.out | grep /tools
lfs@kali:/mnt/lfs/sources/gcc-9.2.0-pass2/build $ readelf -l a.out | grep ': /tools'
```

### tcl

```bash
lfs@kali:/mnt/lfs/sources $ tar xvf tcl8.6.10-src.tar.gz 
lfs@kali:/mnt/lfs/sources $ cd tcl8.6.10
lfs@kali:/mnt/lfs/sources/tcl8.6.10 $ cd unix/
lfs@kali:/mnt/lfs/sources/tcl8.6.10/unix $ ./configure --prefix=/tools
lfs@kali:/mnt/lfs/sources/tcl8.6.10/unix $ make
lfs@kali:/mnt/lfs/sources/tcl8.6.10/unix $ TZ=UTC make test
lfs@kali:/mnt/lfs/sources/tcl8.6.10/unix $ make install
lfs@kali:/mnt/lfs/sources/tcl8.6.10/unix $ chmod -v u+w /tools/lib/libtcl8.6.so
lfs@kali:/mnt/lfs/sources/tcl8.6.10/unix $ make install-private-headers
lfs@kali:/mnt/lfs/sources/tcl8.6.10/unix $ ln -sv tclsh8.6 /tools/bin/tclsh
```

### expect

```bash
lfs@kali:/mnt/lfs/sources $ tar xvf expect5.45.4.tar.gz 
lfs@kali:/mnt/lfs/sources $ cd expect5.45.4
lfs@kali:/mnt/lfs/sources/expect5.45.4 $ cp -v configure{,.orig}
lfs@kali:/mnt/lfs/sources/expect5.45.4 $ sed 's:/usr/local/bin:/bin:' configure.orig > configure
lfs@kali:/mnt/lfs/sources/expect5.45.4 $ ./configure --prefix=/tools \
  --with-tcl=/tools/lib \
  --with-tclinclude=/tools/include
lfs@kali:/mnt/lfs/sources/expect5.45.4 $ make
lfs@kali:/mnt/lfs/sources/expect5.45.4 $ make test
lfs@kali:/mnt/lfs/sources/expect5.45.4 $ make SCRIPTS="" install
```

### deja gnu

```bash
lfs@kali:/mnt/lfs/sources $ tar xvf dejagnu-1.6.2.tar.gz 
lfs@kali:/mnt/lfs/sources $ cd dejagnu-1.6.2
lfs@kali:/mnt/lfs/sources/dejagnu-1.6.2 $ ./configure --prefix=/tools
lfs@kali:/mnt/lfs/sources/dejagnu-1.6.2 $ make
lfs@kali:/mnt/lfs/sources/dejagnu-1.6.2 $ make install
```

### m4

```bash
lfs@kali:/mnt/lfs/sources $ tar xvf m4-1.4.18.tar.xz 
lfs@kali:/mnt/lfs/sources $ cd m4-1.4.18
lfs@kali:/mnt/lfs/sources/m4-1.4.18 $ sed -i 's/IO_ftrylockfile/IO_EOF_SEEN/' lib/*.c
lfs@kali:/mnt/lfs/sources/m4-1.4.18 $ echo "#define _IO_IN_BACKUP 0x100" >> lib/stdio-impl.h
lfs@kali:/mnt/lfs/sources/m4-1.4.18 $ ./configure --prefix=/tools
lfs@kali:/mnt/lfs/sources/m4-1.4.18 $ make
lfs@kali:/mnt/lfs/sources/m4-1.4.18 $ make check
lfs@kali:/mnt/lfs/sources/m4-1.4.18 $ make install
```

### ncurses

```bash
lfs@kali:/mnt/lfs/sources $ tar xvf ncurses-6.2.tar.gz 
lfs@kali:/mnt/lfs/sources $ cd ncurses-6.2
lfs@kali:/mnt/lfs/sources/ncurses-6.2 $ sed -i s/mawk// configure
lfs@kali:/mnt/lfs/sources/ncurses-6.2 $ ./configure --prefix=/tools \
  --with-shared   \
  --without-debug \
  --without-ada   \
  --enable-widec  \
  --enable-overwrite
lfs@kali:/mnt/lfs/sources/ncurses-6.2 $ make
lfs@kali:/mnt/lfs/sources/ncurses-6.2 $ make install
lfs@kali:/mnt/lfs/sources/ncurses-6.2 $ ln -s libncursesw.so /tools/lib/libncurses.so
```

### bash

```bash
lfs@kali:/mnt/lfs/sources $ tar xvf bash-5.0.tar.gz 
lfs@kali:/mnt/lfs/sources $ cd bash-5.0
lfs@kali:/mnt/lfs/sources/bash-5.0 $ ./configure --prefix=/tools --without-bash-malloc
lfs@kali:/mnt/lfs/sources/bash-5.0 $ make
lfs@kali:/mnt/lfs/sources/bash-5.0 $ make tests
lfs@kali:/mnt/lfs/sources/bash-5.0 $ make install
lfs@kali:/mnt/lfs/sources/bash-5.0 $ ln -sv bash /tools/bin/sh
```

### bison

```bash
lfs@kali:/mnt/lfs/sources $ tar xvf bison-3.5.2.tar.xz 
lfs@kali:/mnt/lfs/sources $ cd bison-3.5.2
lfs@kali:/mnt/lfs/sources/bison-3.5.2 $ ./configure --prefix=/tools
lfs@kali:/mnt/lfs/sources/bison-3.5.2$ make
lfs@kali:/mnt/lfs/sources/bison-3.5.2$ make check
lfs@kali:/mnt/lfs/sources/bison-3.5.2$ make install
```

### bzip

```bash
lfs@kali:/mnt/lfs/sources $ tar xvf bzip2-1.0.8.tar.gz 
lfs@kali:/mnt/lfs/sources $ cd bzip2-1.0.8
lfs@kali:/mnt/lfs/sources/bzip2-1.0.8 $ make -f Makefile-libbz2_so
lfs@kali:/mnt/lfs/sources/bzip2-1.0.8 $ make clean
lfs@kali:/mnt/lfs/sources/bzip2-1.0.8 $ make
lfs@kali:/mnt/lfs/sources/bzip2-1.0.8 $ make PREFIX=/tools install
lfs@kali:/mnt/lfs/sources/bzip2-1.0.8 $ cp -v bzip2-shared /tools/bin/bzip2
lfs@kali:/mnt/lfs/sources/bzip2-1.0.8 $ cp -av libbz2.so* /tools/lib
lfs@kali:/mnt/lfs/sources/bzip2-1.0.8 $ ln -sv libbz2.so.1.0 /tools/lib/libbz2.so
```

### coreutils

```bash
lfs@kali:/mnt/lfs/sources $ tar xvf coreutils-8.31.tar.xz 
lfs@kali:/mnt/lfs/sources $ cd coreutils-8.31
lfs@kali:/mnt/lfs/sources/coreutils-8.31 $ ./configure --prefix=/tools --enable-install-program=hostname
lfs@kali:/mnt/lfs/sources/coreutils-8.31 $ make
lfs@kali:/mnt/lfs/sources/coreutils-8.31 $ make RUN_EXPENSIVE_TESTS=yes check
lfs@kali:/mnt/lfs/sources/coreutils-8.31 $ make install
```

### diffutils

```bash
lfs@kali:/mnt/lfs/sources $ tar xvf diffutils-3.7.tar.xz 
lfs@kali:/mnt/lfs/sources $ cd diffutils-3.7
lfs@kali:/mnt/lfs/sources/diffutils-3.7 $ ./configure --prefix=/tools
lfs@kali:/mnt/lfs/sources/diffutils-3.7 $ make
lfs@kali:/mnt/lfs/sources/diffutils-3.7 $ make check
lfs@kali:/mnt/lfs/sources/diffutils-3.7 $ make install
```

### file

```bash
lfs@kali:/mnt/lfs/sources $ tar xvf file-5.38.tar.gz 
lfs@kali:/mnt/lfs/sources $ cd file-5.38
lfs@kali:/mnt/lfs/sources/file-5.38 $ ./configure --prefix=/tools
lfs@kali:/mnt/lfs/sources/file-5.38 $ make
lfs@kali:/mnt/lfs/sources/file-5.38 $ make check
lfs@kali:/mnt/lfs/sources/file-5.38 $ make install
```

### findutils

```bash
lfs@kali:/mnt/lfs/sources $ tar xvf findutils-4.7.0.tar.xz 
lfs@kali:/mnt/lfs/sources $ cd findutils-4.7.0
lfs@kali:/mnt/lfs/sources/findutils-4.7.0 $ ./configure --prefix=/tools
lfs@kali:/mnt/lfs/sources/findutils-4.7.0 $ make
lfs@kali:/mnt/lfs/sources/findutils-4.7.0 $ make check
lfs@kali:/mnt/lfs/sources/findutils-4.7.0 $ make install
```

### gawk

```bash
lfs@kali:/mnt/lfs/sources $ tar xvf gawk-5.0.1.tar.xz 
lfs@kali:/mnt/lfs/sources $ cd gawk-5.0.1
lfs@kali:/mnt/lfs/sources/gawk-5.0.1 $ ./configure --prefix=/tools
lfs@kali:/mnt/lfs/sources/gawk-5.0.1 $ make
lfs@kali:/mnt/lfs/sources/gawk-5.0.1 $ make check
lfs@kali:/mnt/lfs/sources/gawk-5.0.1 $ make install
```

### gettext

```bash
lfs@kali:/mnt/lfs/sources $ tar xvf gettext-0.20.1.tar.xz 
lfs@kali:/mnt/lfs/sources $ cd gettext-0.20.1
lfs@kali:/mnt/lfs/sources/gettext-0.20.1 $ ./configure --disable-shared
lfs@kali:/mnt/lfs/sources/gettext-0.20.1 $ make
lfs@kali:/mnt/lfs/sources/gettext-0.20.1 $ cp -v gettext-tools/src/{msgfmt,msgmerge,xgettext} /tools/bin
```

### grep

```bash
lfs@kali:/mnt/lfs/sources $ tar xvf grep-3.4.tar.xz 
lfs@kali:/mnt/lfs/sources $ cd grep-3.4
lfs@kali:/mnt/lfs/sources/grep-3.4 $ ./configure --prefix=/tools
lfs@kali:/mnt/lfs/sources/grep-3.4 $ make
lfs@kali:/mnt/lfs/sources/grep-3.4 $ make check
lfs@kali:/mnt/lfs/sources/grep-3.4 $ make install
```

### gzip

```bash
lfs@kali:/mnt/lfs/sources $ tar xvf gzip-1.10.tar.xz 
lfs@kali:/mnt/lfs/sources $ cd gzip-1.10
lfs@kali:/mnt/lfs/sources/gzip-1.10 $ ./configure --prefix=/tools
lfs@kali:/mnt/lfs/sources/gzip-1.10 $ make
lfs@kali:/mnt/lfs/sources/gzip-1.10 $ make check
lfs@kali:/mnt/lfs/sources/gzip-1.10 $ make install
```

### make

```bash
lfs@kali:/mnt/lfs/sources$ tar xvf make-4.3.tar.gz 
lfs@kali:/mnt/lfs/sources$ cd make-4.3 
lfs@kali:/mnt/lfs/sources/make-4.3 $ ./configure --prefix=/tools --without-guile
lfs@kali:/mnt/lfs/sources/make-4.3 $ make
lfs@kali:/mnt/lfs/sources/make-4.3 $ make check
lfs@kali:/mnt/lfs/sources/make-4.3 $ make install
```

### patch

```bash
lfs@kali:/mnt/lfs/sources $ tar xvf patch-2.7.6.tar.xz 
lfs@kali:/mnt/lfs/sources $ cd patch-2.7.6
lfs@kali:/mnt/lfs/sources/patch-2.7.6 $ ./configure --prefix=/tools
lfs@kali:/mnt/lfs/sources/patch-2.7.6 $ make
lfs@kali:/mnt/lfs/sources/patch-2.7.6 $ make check
lfs@kali:/mnt/lfs/sources/patch-2.7.6 $ make install
```

### perl

```bash
lfs@kali:/mnt/lfs/sources $ tar xvf perl-5.30.1.tar.xz 
lfs@kali:/mnt/lfs/sources $ cd perl-5.30.1
lfs@kali:/mnt/lfs/sources/perl-5.30.1 $ sh Configure -des -Dprefix=/tools -Dlibs=-lm -Uloclibpth -Ulocincpth
lfs@kali:/mnt/lfs/sources/perl-5.30.1 $ make
lfs@kali:/mnt/lfs/sources/perl-5.30.1 $ cp -v perl cpan/podlators/scripts/pod2man /tools/bin
lfs@kali:/mnt/lfs/sources/perl-5.30.1 $ mkdir -pv /tools/lib/perl5/5.30.1
lfs@kali:/mnt/lfs/sources/perl-5.30.1 $ cp -Rv lib/* /tools/lib/perl5/5.30.1
```

### python

```bash
lfs@kali:/mnt/lfs/sources $ tar xf Python-3.8.1.tar.xz 
lfs@kali:/mnt/lfs/sources $ cd Python-3.8.1
lfs@kali:/mnt/lfs/sources/Python-3.8.1 $ sed -i '/def add_multiarch_paths/a \        return' setup.py
lfs@kali:/mnt/lfs/sources/Python-3.8.1 $ ./configure --prefix=/tools --without-ensurepip
lfs@kali:/mnt/lfs/sources/Python-3.8.1 $ make
lfs@kali:/mnt/lfs/sources/Python-3.8.1 $ make install
```

### sed

```bash
lfs@kali:/mnt/lfs/sources $ tar xf sed-4.8.tar.xz 
lfs@kali:/mnt/lfs/sources $ cd sed-4.8
lfs@kali:/mnt/lfs/sources/sed-4.8 $ ./configure --prefix=/tools
lfs@kali:/mnt/lfs/sources/sed-4.8 $ make
lfs@kali:/mnt/lfs/sources/sed-4.8 $ make check
lfs@kali:/mnt/lfs/sources/sed-4.8 $ make install
```

### tar

```bash
lfs@kali:/mnt/lfs/sources $ tar xf tar-1.32.tar.xz 
lfs@kali:/mnt/lfs/sources $ cd tar-1.32
lfs@kali:/mnt/lfs/sources/tar-1.32 $ ./configure --prefix=/tools
lfs@kali:/mnt/lfs/sources/tar-1.32 $ make
lfs@kali:/mnt/lfs/sources/tar-1.32 $ make check
lfs@kali:/mnt/lfs/sources/tar-1.32 $ make install
```

### texinfo

```bash
lfs@kali:/mnt/lfs/sources $ tar xf texinfo-6.7.tar.xz 
lfs@kali:/mnt/lfs/sources $ cd texinfo-6.7
lfs@kali:/mnt/lfs/sources/texinfo-6.7 $ ./configure --prefix=/tools
lfs@kali:/mnt/lfs/sources/texinfo-6.7 $ make
lfs@kali:/mnt/lfs/sources/texinfo-6.7 $ make check
lfs@kali:/mnt/lfs/sources/texinfo-6.7 $ make install
```

### util-linux

```bash
lfs@kali:/mnt/lfs/sources $ tar xf util-linux-2.35.1.tar.xz 
lfs@kali:/mnt/lfs/sources $ cd util-linux-2.35.1
lfs@kali:/mnt/lfs/sources/util-linux-2.35.1 $ ./configure --prefix=/tools \
  --without-python               \
  --disable-makeinstall-chown    \
  --without-systemdsystemunitdir \
  --without-ncurses              \
  PKG_CONFIG=""
lfs@kali:/mnt/lfs/sources/util-linux-2.35.1 $ make
lfs@kali:/mnt/lfs/sources/util-linux-2.35.1 $ make install
```

### xz

```bash
lfs@kali:/mnt/lfs/sources $ tar xf xz-5.2.4.tar.xz 
lfs@kali:/mnt/lfs/sources $ cd xz-5.2.4
lfs@kali:/mnt/lfs/sources/xz-5.2.4 $ ./configure --prefix=/tools
lfs@kali:/mnt/lfs/sources/xz-5.2.4 $ make
lfs@kali:/mnt/lfs/sources/xz-5.2.4 $ make check
lfs@kali:/mnt/lfs/sources/xz-5.2.4 $ make install
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
root@kali:~# chown -R root:root /mnt/lfs/tools
```


---
