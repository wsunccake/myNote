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

## compile - Intel oneAPI HPC Toolkit - method 1

`bsd/bldg16`

```bash
set zzz = `which ifort`
->
set zzz = `which ifx`
```

`bsd/mdutil.c`

```c
  f77_int wait_(ist) f77_int *ist; {pid_t wait(); return(wait((int) *ist));
->
  f77_int wait_(ist) f77_int *ist; {pid_t wait(); return(wait((int *) ist)); }
```

`bsd/mdutil.F`

```f
#ifdef _IA64_
        MDCach = CacheSize(3)*1024/(2*8) + 1
#endif
->
C#ifdef _IA64_
C        MDCach = CacheSize(3)*1024/(2*8) + 1
C#endif
```

`bsd/ia64.make`

```makefile
INTELDIR = /opt/intel/Compiler/11.1/072
MKLLIB = $(INTELDIR)/mkl/lib/64
COMPDIR = $(INTELDIR)/lib/ia64
BLAS = $(MKLLIB)/libmkl_intel_ilp64.a $(MKLLIB)/libmkl_intel_thread.a $(MKLLIB)/libmkl_core.a
...
PARSWITCHC = -openmp
PARSWITCH = -openmp -fpp2 -auto
...
RUNCC = icc -static-intel -L$(COMPDIR)
...
RUNF77 = ifort -L$(COMPDIR) -L$(MKLLIB)
->
INTELDIR = /opt/intel/oneapi
MKLLIB = $(INTELDIR)/mkl/2025.2/lib
COMPDIR = $(INTELDIR)/compiler/2025.2/lib
BLAS = ${MKLROOT}/lib/libmkl_blas95_ilp64.a ${MKLROOT}/lib/libmkl_lapack95_ilp64.a -Wl,--start-group ${MKLROOT}/lib/libmkl_intel_ilp64.a ${MKLROOT}/lib/libmkl_intel_thread.a ${MKLROOT}/lib/libmkl_core.a -Wl,--end-group -liomp5 -lpthread -lm -ldl
...
PARSWITCHC = -qopenmp
PARSWITCH = -qopenmp -fpp2 -auto
...
RUNCC = icx -static-intel -L$(COMPDIR)
...
RUNF77 = ifx -L$(COMPDIR) -L$(MKLLIB)
```

```bash
sle15sp7:~ # icx
sle15sp7:~ # ifx
sle15sp7:~ # echo $MKLROOT

# modify
sle15sp7:/usr/local/g16 # cp bsd/bldg16 bsd/bldg16.org
sle15sp7:/usr/local/g16 # cp bsd/mdutil.c bsd/mdutil.c.org
sle15sp7:/usr/local/g16 # cp bsd/mdutil.F bsd/mdutil.F.org
sle15sp7:/usr/local/g16 # cp bsd/ia64.make bsd/ia64.make.org
sle15sp7:/usr/local/g16 # cp bsd/i386.make bsd/i386.make.org

sle15sp7:/usr/local/g16 # vi bsd/bldg16
sle15sp7:/usr/local/g16 # vi bsd/mdutil.c
sle15sp7:/usr/local/g16 # vi bsd/mdutil.F
sle15sp7:/usr/local/g16 # vi bsd/ia64.make
sle15sp7:/usr/local/g16 # mv bsd/ia64.make bsd/i386.make

# build
sle15sp7:/usr/local/g16 # bsd/bldg16
```

---

## compile - Intel oneAPI HPC Toolkit - method 2

`bsd/bldg16`

```bash
set zzz = `which ifort`
->
set zzz = `which ifx`
```

`bsd/i386.make`

```makefile
FPARFLAG = -mp=nonuma
...
RUNCC = cc -g
...
TIME = -Mreentrant -Mrecursive -Mnosave -Minfo -Mneginfo -time
...
VECTOR = -Mvect=assoc,recog,noaltcode,cachesize:$(CSIZE)$(VECTOR4)
MACHTY = p7-32
MACH = -tp $(MACHTY) $(TIME)
OPTOI = -m32 -march=i486 -malign-double
GCCOPTS = -ffast-math -funroll-loops -fexpensive-optimizations
OPTFLAGO = $(OPTOI) -O3 $(GCCOPTS)
...
I8FLAG =
R8FLAG =
MMODEL =
PGISTATIC = -Bstatic_pgi
PGNAME = pgf77
...
#SYSLIBS = -lpthread -lm -lc $(GPULIB2)
...
NUMALIB =
...
UNROLL        = -Munroll
...
PC64 = -pc 64 -Kieee
...
OPTFLAG = -fast -O2 $(UNROLL) $(VECTOR)
->
FPARFLAG =
...
RUNCC = icx
...
#TIME = -Mreentrant -Mrecursive -Mnosave -Minfo -Mneginfo -time
...
#VECTOR = -Mvect=assoc,recog,noaltcode,cachesize:$(CSIZE)$(VECTOR4)
#MACHTY = p7-32
#MACH = -tp $(MACHTY) $(TIME)
#OPTOI = -m32 -march=i486 -malign-double
#GCCOPTS = -ffast-math -funroll-loops -fexpensive-optimizations
OPTFLAGO = -O2 -unroll
...
I8FLAG = -i8
R8FLAG = -r8
MMODEL = -mcmodel=medium
#PGISTATIC = -Bstatic_pgi
PGNAME = ifx -qopenmp
SPECFLAG = -auto -axCORE-AVX2 -shared-intel -static-libgcc -no-prec-div -ftz -pad -fpp -qmkl
...
#SYSLIBS = -lpthread -lm -lc $(GPULIB2)
...
NUMALIB = ${MKLROOT}/lib/libmkl_blas95_ilp64.a ${MKLROOT}/lib/libmkl_lapack95_ilp64.a -Wl,--start-group ${MKLROOT}/lib/libmkl_intel_ilp64.a ${MKLROOT}/lib/libmkl_intel_thread.a ${MKLROOT}/lib/libmkl_core.a -Wl,--end-group -liomp5 -lpthread -lm -ldl
...
UNROLL        = -unroll
...
PC64 = -pc64
...
OPTFLAG = -O2 $(UNROLL) $(VECTOR)
```

`mdutil.c`

```c
#include <sys/times.h>
#define NEED_AND
#define NEED_ISHFT
#define NEED_GSR48
#define NEED_PUTENV   // add this line
#include <unistd.h>
#include <errno.h>
#include <time.h>
#endif
```

```bash
sle15sp7:~ # icx
sle15sp7:~ # ifx
sle15sp7:~ # echo $MKLROOT

# modify
sle15sp7:/usr/local/g16 # cp bsd/bldg16 bsd/bldg16.org
sle15sp7:/usr/local/g16 # cp bsd/mdutil.c bsd/mdutil.c.org
sle15sp7:/usr/local/g16 # cp bsd/i386.make bsd/i386.make.org

sle15sp7:/usr/local/g16 # vi bsd/bldg16
sle15sp7:/usr/local/g16 # vi bsd/mdutil.c
sle15sp7:/usr/local/g16 # vi bsd/i386.make

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
