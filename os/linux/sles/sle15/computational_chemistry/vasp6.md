# vasp6

## require

- OS: SLE 15 SP7
- Compiler: Intel oneAPI HPC Toolkit 2025.2
  - C / C++
  - Fortran
  - MKL
  - MPI
- VASP: 6.3.2

## website

- [VASP](https://www.vasp.at/)
- [VASPsol](https://github.com/henniggroup/VASPsol)
- [CP-VASP](https://github.com/yuanyue-liu-group/CP-VASP)
- [VTST](https://theory.cm.utexas.edu/vtsttools/index.html)

---

## compile - Intel oneAPI HPC Toolkit

```bash
sle15sp7:~ # zypper in -t pattern devel_basis
sle15sp7:~ # icx
sle15sp7:~ # icpx
sle15sp7:~ # mpiifx

sle15sp7:~ # tar zxf vasp.6.3.2.tgz -C /usr/local
sle15sp7:~ # cd /usr/local/vasp.6.3.2

# config makefile
sle15sp7:/usr/local/vasp.6.3.2 # cp arch/makefile.include.intel ./makefile.include
sle15sp7:/usr/local/vasp.6.3.2 # vi makefile.include
sle15sp7:/usr/local/vasp.6.3.2 # cp parse/makefile parse/makefile.org
sle15sp7:/usr/local/vasp.6.3.2 # vi parse/makefile

# build
sle15sp7:/usr/local/vasp.6.3.2 # make <target>
# target: std|gam|ncl|gpu|
sle15sp7:/usr/local/vasp.6.3.2 # make std
sle15sp7:/usr/local/vasp.6.3.2 # ls bin

# clean
sle15sp7:/usr/local/vasp.6.3.2 # make veryclean
```

```makefile
# arch/makefile.include.intel
FC         = mpiifort
FCL        = mpiifort
...
CC_LIB     = icc
...
CXX_PARS   = icpc
->
FC         = mpiifx [-static-intel|-Bstatic]
FCL        = mpiifx [-qmkl=sequential] [-static-intel|-Bstatic]
...
CC_LIB     = icx
...
CXX_PARS   = icpx
```

```makefile
# parse/makefile
%.o:    %.F90
        ifort -c $< -o $@
...
locproj_test:   call_from_fortran.o $(CPPOBJ_PARS) $(COBJ_PARS) locproj.tab.h
        ifort call_from_fortran.o $(CPPOBJ_PARS) $(COBJ_PARS)  -lstdc++ -o locproj_test
->
%.o:    %.F90
        ifx -c $< -o $@
...
locproj_test:   call_from_fortran.o $(CPPOBJ_PARS) $(COBJ_PARS) locproj.tab.h
        ifx call_from_fortran.o $(CPPOBJ_PARS) $(COBJ_PARS)  -lstdc++ -o locproj_test
```

| Make     | executable | kernel             | 適用情境                                                                                                                   | 優點                                                             |
| -------- | ---------- | ------------------ | -------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| make std | vasp_std   | Standard K-point   | 用於大多數常規計算，如塊體材料 (bulk system)、週期性結構的結構弛豫、電子結構計算等。                                       | 功能最全面，最常用。                                             |
| make gam | vasp_gam   | Gamma-point only   | 用於只需使用 單一 K 點（Gamma 點） 的體系，特別是大尺寸的超晶胞 (supercells) 或非週期性分子/團簇（如果使用很大的真空層）。 | 記憶體用量 (Memory usage) 最低，計算速度通常最快，數值穩定性高。 |
| make ncl | vasp_ncl   | Non-Collinear Spin | 用於需要處理非共線磁性結構 (non-collinear magnetism) 或需要包含自旋-軌道耦合 (Spin-Orbit Coupling, SOC) 效應的計算。       | 能夠處理更複雜的磁性或相對論效應。                               |

---

## run

```bash
sle15sp7:~ $ cp -r /usr/local/vasp.6.3.2/testsuite/tests/NaCl .
sle15sp7:~ $ cp /usr/local/vasp.6.3.2/testsuite/POTCARS/POTCAR.NaCl NaCl/POTCARS
sle15sp7:~ $ cp /usr/local/vasp.6.3.2/bin/vasp_std NaCl
sle15sp7:~ $ cd NaCl
sle15sp7:~/NaCl $ mpirun -np 2 ./vasp_std
```

---

## VASPsol

```bash
sle15sp7:~ $ git clone https://github.com/henniggroup/VASPsol.git
sle15sp7:~ $ cd /usr/local/vasp.6.3.2/src/

sle15sp7:/usr/local/vasp.6.3.2/src $ mv solvation.F solvation.F.org
sle15sp7:/usr/local/vasp.6.3.2/src $ cp ~/VASPsol/src/solvation.F .
sle15sp7:/usr/local/vasp.6.3.2/src $ patch -Np0 < ~/VASPsol/patches/pbz_patch_610

sle15sp7:/usr/local/vasp.6.3.2/src $ cd ..
sle15sp7:/usr/local/vasp.6.3.2 $ cp makefile.include makefile.include.org
sle15sp7:/usr/local/vasp.6.3.2 $ vi makefile.include
sle15sp7:/usr/local/vasp.6.3.2 $ make std
```

```makefile
# makefile.include
              -Dfock_dblbuf
->
              -Dfock_dblbuf \
              -Dsol_compat
```

---

## CP-VASP

```bash
sle15sp7:/usr/local/vasp.6.3.2/src $ patch -Np0 < ~/CP-VASP/version1/vasp6.4_6.3_cpm.patch
```

---

## VTST

```bash
sle15sp7:~ $ tar zxf vtstcode-213.tgz
sle15sp7:~ $ cd /usr/local/vasp.6.3.2/src/

sle15sp7:/usr/local/vasp.6.3.2/src $ cp -r ~/vtstcode-213/vtstcode6.3/* .
sle15sp7:/usr/local/vasp.6.3.2/src $ cp main.F main.F.org
sle15sp7:/usr/local/vasp.6.3.2/src $ cp .objects .objects.org
sle15sp7:/usr/local/vasp.6.3.2/src $ cp makefile makefile.org

sle15sp7:/usr/local/vasp.6.3.2/src $ vi main.F
sle15sp7:/usr/local/vasp.6.3.2/src $ vi .objects
sle15sp7:/usr/local/vasp.6.3.2/src $ vi makefile

sle15sp7:/usr/local/vasp.6.3.2/src $ cd ..
sle15sp7:/usr/local/vasp.6.3.2 $ make std
```

```F
! src/main.F
      CALL CHAIN_FORCE(T_INFO%NIONS,DYN%POSION,TOTEN,TIFOR, &
           LATT_CUR%A,LATT_CUR%B,IO%IU6)
...
      IF (LCHAIN) CALL chain_init( T_INFO, IO)
->
      CALL CHAIN_FORCE(T_INFO%NIONS,DYN%POSION,TOTEN,TIFOR, &
           TSIF,LATT_CUR%A,LATT_CUR%B,IO%IU6)
...
      CALL chain_init( T_INFO, IO)
```

```makefile
# src/.objects
        elf.o \
        hamil_rot.o \
        chain.o \
        dyna.o \
...
        elf.o \
        hamil_rot.o \
        bfgs.o dynmat.o instanton.o lbfgs.o sd.o cg.o dimer.o bbm.o \
        fire.o lanczos.o neb.o qm.o \
        pyamff_fortran/*.o ml_pyamff.o \
        opt.o \
        chain.o \
        dyna.o \
```

```makefile
# src/makefile
LIB=lib parser
...
dependencies: sources
->
LIB=lib parser pyamff_fortran
...
dependencies: sources libs
```
