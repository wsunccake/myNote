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


## begin

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
