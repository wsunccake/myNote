# vasp6

## require

- OS: SLE 15 SP7
- Compiler: Intel oneAPI HPC Toolkit 2025.2
  - C / C++
  - Fortran
  - MKL
  - MPI
- VASP: 6.4.1

---

## compile - Intel oneAPI HPC Toolkit

```bash
sle15sp7:~ # icx
sle15sp7:~ # icpx
sle15sp7:~ # mpiifx

sle15sp7:~ # tar zxf vasp.6.4.1.tgz -C /usr/local
sle15sp7:~ # cd /usr/local/vasp.6.4.1

# config makefile
sle15sp7:/usr/local/vasp.6.4.1 # cp arch/makefile.include.intel ./makefile.include
sle15sp7:/usr/local/vasp.6.4.1 # vi makefile.include
sle15sp7:/usr/local/vasp.6.4.1 # vi parse/makefile

# build
sle15sp7:/usr/local/vasp.6.4.1 # make <target>
# target: std|gam|ncl|gpu|
sle15sp7:/usr/local/vasp.6.4.1 # make std
sle15sp7:/usr/local/vasp.6.4.1 # ls bin
```

```makefile
# arch/makefile.include.intel
FC         = mpiifort
FCL        = mpiifort
CC_LIB     = icc
CXX_PARS   = icpc
->
FC         = mpiifx [-static-intel|-Bstatic]
FCL        = mpiifx -qmkl=sequential [-static-intel|-Bstatic]
CC_LIB     = icx
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
sle15sp7:~ $ cp -r /usr/local/vasp.6.4.1/testsuite/tests/NaCl .
sle15sp7:~ $ cp /usr/local/vasp.6.4.1/testsuite/POTCARS/POTCAR.NaCl NaCl/POTCARS
sle15sp7:~ $ cp /usr/local/vasp.6.4.1/bin/vasp_std NaCl
sle15sp7:~ $ cd NaCl
sle15sp7:~/NaCl $ mpirun -np 2 ./vasp_std
```
