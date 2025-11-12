# gaussian 16

## require

- OS: SLE 15 SP7
- Compiler: NVIDIA HPC SDK 25.7
  - Fortran
- Gaussian 16

---

## package

```bash
sle15sp7:~ # zypper in -t pattern devel_basis
sle15sp7:~ # zypper in tcsh
sle15sp7:~ # zypper in glibc-devel-32bit

sle15sp7:~ # tar jxf wkssrc.tbz -C /usr/local
sle15sp7:~ # chown -R <user>:<group> /usr/local/g16

# set env
sle15sp7:~ # export g16root=/usr/local
sle15sp7:/usr/local/g16 # source bsd/g16.profile   # for sh / bash
sle15sp7:/usr/local/g16 # source bsd/g16.login     # for csh / tcsh
```

---

## compile - NVIDIA HPC SDK

```bash
sle15sp7:~ # pgf77
sle15sp7:~ # pgf77 -help -tp

# modify option
sle15sp7:/usr/local/g16 # sed -i s/p7-64/x86-64-v3/ bsd/set-mflags
sle15sp7:/usr/local/g16 # set -i s/p7-64/x86-64-v3/ bsd/setup-make

# build
sle15sp7:/usr/local/g16 # bsd/bldg16
```

---

## run

```bash
sle15sp7:~ # export g16root=/usr/local
sle15sp7:~ # export GAUSS_EXEDIR=$g16root/g16:$g16root/g16/bsd
sle15sp7:~ # export GAUSS_SCRDIR=/tmp
sle15sp7:~ # export LD_LIBRARY_PATH=$GAUSS_EXEDIR:$LD_LIBRARY_PATH
sle15sp7:~ # export PATH=$GAUSS_EXEDIR:$PATH

sle15sp7:~ # mkdir test
sle15sp7:~/test # cd testt
sle15sp7:~/test # cp $g16root/tests/com/test0000.com .
sle15sp7:~/test # g16 test0000.com
```
