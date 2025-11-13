# mdutil.F

`mdutil.F`

## MDCach

```f90
*Deck MDCach
      Integer Function MDCach(IType)
      Implicit Integer(A-Z)
C
C     Return a value related to the cache size of the machine to be
C     used in "pseudo" blocking scheme in Direct Methods. Used in
C     in determining the size of MaxCom.  This routine should return
C     the optimal amount of data to be used in blocking intermediate
C     information, which is typically half the total cache size.
C     The compile-time parameter DEFCACHE is in units of K real*8's;
C     this routine returns the size in units of real*8's.
C
C     If IType = 0 return the standard cachesize regardless
C     If IType = 1 then return -1 (no limit) if called on a thread
C     which has a GPU; otherwise, return the standard cachesize.
C
      Integer MaxIOp
      Parameter (MaxIOp=DEFMAXIOP)
      Common /IOp/ IOp(MaxIOp)
C
      If(IOp(4).ne.0) then
        MDCach = IOp(4)
      else
#ifdef DEFCACHE
        MDCach = DEFCACHE * 1024
#else
        MDCach = -1
#ifdef _IA64_
        MDCach = CacheSize(3)*1024/(2*8) + 1
#endif
#endif
        If(IType.eq.1.and.MDUsGPU(0).ge.0) MDCach = -1
        endIf
      Return
      End
```

用來推估 CPU/GPU 的快取 (cache) 大小, 以便在「direct method (直接方法)」計算時決定資料 blocking 大小.

| IType 值 | 回傳值意義                                                                   |
| -------- | ---------------------------------------------------------------------------- |
| 0        | 回傳標準快取大小（預設值或 IOp(4) 中的設定）                                 |
| 1        | 若該執行緒綁定 GPU → 回傳 -1 (代表不限制 blocking 大小) 否則回傳標準快取大小 |

```
DEFCACHE= Cache Size (bytes, per core) / (8 x 1024 x 2)
```

其中 8 是 real\*8 的 Byte, 1024 是將 Byte 轉成 KiB, 2 是因為 blocking 大小通常設為快取大小的一半.
以 Intel Skylake-X 架構為例 (如上面 lscpu 輸出所示):
在高性能計算中，數據分塊通常針對 L2 快取或 L3 快取進行優化，因為它們比 L1 快取（通常很小且專用於指令或數據）大得多.

- L1d cache (每個核心):
  32 KiB (數據快取)
- L2 cache (每個核心):
  1024 KiB 或 1 MiB (這是 Skylake-X 的實際 L2 大小, lscpu 顯示的 6 MiB 實際上是總 L2 快取，在某些架構上是共享的，但更常見於每個核心一個)
  L2 快取是獨享的，每核心的 L2 快取約為 6 MiB / 6 = 1 MiB 或 1024 KiB。這是最常見的優化目標。
- L3 cache (共享):
  8.3 MiB (由所有核心共享)
  所有核心共享的。如果程式在多執緒環境下運行，針對共享 L3 快取進行優化會很複雜。

```bash
linux:~ # lscpu
Architecture:                    x86_64
CPU op-mode(s):                  32-bit, 64-bit
Byte Order:                      Little Endian
Address sizes:                   46 bits physical, 48 bits virtual
CPU(s):                          12
On-line CPU(s) list:             0-11
Thread(s) per core:              2
Core(s) per socket:              6
Socket(s):                       1
NUMA node(s):                    1
Vendor ID:                       GenuineIntel
CPU family:                      6
Model:                           85
Model name:                      Intel(R) Core(TM) i7-7800X CPU @ 3.50GHz
Stepping:                        4
CPU MHz:                         1200.179
CPU max MHz:                     4000.0000
CPU min MHz:                     1200.0000
BogoMIPS:                        6999.82
Virtualization:                  VT-x
L1d cache:                       192 KiB
L1i cache:                       192 KiB
L2 cache:                        6 MiB
L3 cache:                        8.3 MiB
NUMA node0 CPU(s):               0-11
Vulnerability Itlb multihit:     KVM: Mitigation: Split huge pages
Vulnerability L1tf:              Mitigation; PTE Inversion; VMX conditional cache flushes, SMT vulnerable
Vulnerability Mds:               Vulnerable: Clear CPU buffers attempted, no microcode; SMT vulnerable
Vulnerability Meltdown:          Mitigation; PTI
Vulnerability Spec store bypass: Vulnerable
Vulnerability Spectre v1:        Mitigation; usercopy/swapgs barriers and __user pointer sanitization
Vulnerability Spectre v2:        Mitigation; Full generic retpoline, STIBP disabled, RSB filling
Vulnerability Srbds:             Not affected
Vulnerability Tsx async abort:   Vulnerable: Clear CPU buffers attempted, no microcode; SMT vulnerable
Flags:                           fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc art arch_perfm
                                 on pebs bts rep_good nopl xtopology nonstop_tsc cpuid aperfmperf pni pclmulqdq dtes64 monitor ds_cpl vmx est tm2 ssse3 sdbg fma cx16 xtpr pdcm pcid dca sse4_1 sse4_2 x2apic mov
                                 be popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm 3dnowprefetch cpuid_fault epb cat_l3 cdp_l3 invpcid_single pti mba tpr_shadow vnmi flexpriority ept vpid ept_
                                 ad fsgsbase tsc_adjust bmi1 hle avx2 smep bmi2 erms invpcid rtm cqm mpx rdt_a avx512f avx512dq rdseed adx smap clflushopt clwb intel_pt avx512cd avx512bw avx512vl xsaveopt xsav
                                 ec xgetbv1 xsaves cqm_llc cqm_occup_llc cqm_mbm_total cqm_mbm_local dtherm ida arat pln pts hwp hwp_act_window hwp_epp hwp_pkg_req
```

```
L2:
6 MiB = 6 × 1,048,576 bytes = 6,291,456 bytes (total for 6 cores)
  = 6,291,456 / 6 = 1,048,576 bytes (per core)
DEFCACHE = 1,048,576 / (8 × 1024 × 2) = 64

L3:
8.3 MiB = 8.3 × 1,048,576 bytes = 8,707,968 bytes (total for 6 cores)
  = 8,707,968 / 6  = 1,451,328 bytes (per core)
DEFCACHE = 1,451,328 / (8 × 1024 × 2) = 88.5 ≈ 89
```

---

## GSetMP

```f90
*Deck GSetMP
      Subroutine GSetMP(Init,MaxCur)
      Implicit Integer(A-Z)
C
C     Do whatever is necessary to set the number of threads used by
C     parallel library code to MaxCur.  Init indicates whether this is
C     the initial call.
C
      Logical Init
      Character*12 Str
#ifdef OMP_I4
      Logical*4 LFalse
      Integer*4 MaxCu4, IOut4
#else
      Logical LFalse
#endif
      Parameter (LFalse=.False.)
      Common /IO/ In, IOut, IPunch
C
      Call IntStr(MaxCur,Str)
      LenStr = LinEnd(Str)
C
C     Set up thread control if necessary when using shared memory.
C
      IOut4 = IOut
      If(Init) then
#ifdef _OPENMP_
        Call FixEnv('MPC_GANG','OFF')
        Call OMP_Set_Dynamic(LFalse)
        Call OMP_Set_Nested(LFalse)
#endif
        endIf
      MaxCu4 = MaxCur
#ifdef _OPENMP_
      Call OMP_Set_Num_Threads(MaxCu4)
#endif
#ifdef _SUN_
      Call SetEnv('PARALLEL',Str(1:LenStr))
#endif
C
C     Now set the Gaussian environment variable for number of
C     processors, plus any required machine-specific variables.
C
      Call FixEnv('GAUSS_NPROC',Str(1:LenStr))
      Call FixEnv('OMP_NUM_THREADS',Str(1:LenStr))
      Call FixEnv('NCPUS',Str(1:LenStr))
      Return
      End
```

```f90
#ifdef OMP_I4
    Logical*4 LFalse
#else
    Logical LFalse
#endif
    Parameter (LFalse=.False.)  <--- Compile-Time Constant, #define LFalse 0 或 const bool LFalse = false;
```

```f90
#ifdef _OPENMP_
        Call FixEnv('MPC_GANG','OFF')
        Call OMP_Set_Dynamic(LFalse)
        Call OMP_Set_Nested(LFalse)
#endif
->
#ifdef _OPENMP_
        Call FixEnv('MPC_GANG','OFF')
        Call OMP_Set_Dynamic(LFalse)
        Call OMP_Set_Max_Active_Levels(1)
#endif
```
