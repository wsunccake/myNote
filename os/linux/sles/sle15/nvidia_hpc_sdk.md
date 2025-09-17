# NVIDIA HPC SDK

## install

download [NVIDIA HPC SDK](https://developer.nvidia.com/hpc-sdk)

```bash
sle:~ # tar zxf nvhpc_2025_257_Linux_x86_64_cuda_12.9.tar.gz
sle:~ # cd nvhpc_2025_257_Linux_x86_64_cuda_12.9
sle:~/nvhpc_2025_257_Linux_x86_64_cuda_12.9 # ./install
```

## usage

### bash, ksh, zsh

```bash
# compiler
sle:~ $ export NVARCH=`uname -s`_`uname -m`
sle:~ $ export NVCOMPILERS=/opt/nvidia/hpc_sdk
sle:~ $ export MANPATH=$MANPATH:$NVCOMPILERS/$NVARCH/25.7/compilers/man
sle:~ $ export PATH=$NVCOMPILERS/$NVARCH/25.7/compilers/bin:$PATH

# mpi
sle:~ $ export PATH=$NVCOMPILERS/$NVARCH/25.7/comm_libs/mpi/bin:$PATH
sle:~ $ export MANPATH=$MANPATH:$NVCOMPILERS/$NVARCH/25.7/comm_libs/mpi/man

# module
sle:~ $ export MODULEPATH=$NVCOMPILERS/modulefiles:$MODULEPATH
sle:~ $ module load nvhpc
```

### tcsh

```bash
# compiler
sle:~ > setenv NVARCH `uname -s`_`uname -m`
sle:~ > setenv NVCOMPILERS /opt/nvidia/hpc_sdk
sle:~ > setenv MANPATH "$MANPATH":$NVCOMPILERS/$NVARCH/25.7/compilers/man
sle:~ > set path = ($NVCOMPILERS/$NVARCH/25.7/compilers/bin $path)

# mpi
sle:~ > set path = ($NVCOMPILERS/$NVARCH/25.7/comm_libs/mpi/bin $path)
sle:~ > setenv MANPATH "$MANPATH":$NVCOMPILERS/$NVARCH/25.7/comm_libs/mpi/man

# module
sle:~ > setenv MODULEPATH $NVCOMPILERS/modulefiles:"$MODULEPATH"
sle:~ > module load nvhpc
```

---

## compiler

```bash
sle:~ $ echo $NVCOMPILERS

# c compiler
sle:~ $ which nvc
sle:~ $ nvc -o hello hello.c

# c++ compiler
sle:~ $ which nvc++
sle:~ $ nvc++ -o hello hello.cpp

# fortran compiler
sle:~ $ which nvfortran
sle:~ $ nvfortran -o hello -Mfixed hello.f     # fortran 77, fixed format
sle:~ $ nvfortran -o hello -Mfree hello.f90    # fortran 90, free format
```

```c
// hello.c
#include <stdio.h>

int main() {
    printf("Hello, C Compiler!\n");
    return 0;
}
```

```cpp
// hello.cpp
#include <iostream>

int main() {
    std::cout << "Hello, C++ Compiler" << std::endl;
    return 0;
}
```

```fortran
C hello.f
      PROGRAM HELLOW
      WRITE(UNIT=*, FMT=*) 'Hello, Fortran Compiler!'
      END
```

```fortran
! hello.f90
program hello
    implicit none
    print *, "Hello, Fortran Compiler!"
end program hello
```

---

## mpi

```bash
sle:~ $ mpicc   -o mpi_pi mpi_pi.c          # c
sle:~ $ mpicxx  -o mpi_pi mpi_pi.cpp        # c++
sle:~ $ mpif77  -o mpi_pi mpi_pi.f          # fortran 77
sle:~ $ mpifort -o mpi_pi mpi_pi.f90        # fortran 90

sle:~ $ mpirun -n <NPROC> ./mpi_pi
```

```c
// mpi_pi.c
#include <mpi.h>
#include <stdio.h>

int main(int argc, char* argv[]) {
    int rank, size;
    long long int n;
    double PI25DT = 3.141592653589793238462643;
    double local_sum, global_sum, h, x;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if (rank == 0) {
        printf("Enter the number of intervals: ");
        fflush(stdout);
        scanf("%lld", &n);
    }

    // Broadcast the number of intervals to all processes
    MPI_Bcast(&n, 1, MPI_LONG_LONG_INT, 0, MPI_COMM_WORLD);

    h = 1.0 / (double)n;
    local_sum = 0.0;

    // Each process calculates a partial sum
    for (int i = rank; i < n; i += size) {
        x = h * ((double)i + 0.5);
        local_sum += 4.0 / (1.0 + x * x);
    }

    // Reduce all local sums into a single global sum on process 0
    MPI_Reduce(&local_sum, &global_sum, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

    if (rank == 0) {
        double pi = global_sum * h;
        printf("Pi is approximately %.16f, Error is %.16f\n", pi, pi - PI25DT);
    }

    MPI_Finalize();
    return 0;
}
```

```cpp
// mpi_pi.cpp
#include <iostream>
#include <iomanip>
#include <mpi.h>

int main(int argc, char* argv[]) {
    int rank, size;
    long long int n;
    const double PI25DT = 3.141592653589793238462643;
    double local_sum, global_sum, h, x;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if (rank == 0) {
        std::cout << "Enter the number of intervals: ";
        std::cin >> n;
    }

    MPI_Bcast(&n, 1, MPI_LONG_LONG_INT, 0, MPI_COMM_WORLD);

    h = 1.0 / static_cast<double>(n);
    local_sum = 0.0;

    for (int i = rank; i < n; i += size) {
        x = h * (static_cast<double>(i) + 0.5);
        local_sum += 4.0 / (1.0 + x * x);
    }

    MPI_Reduce(&local_sum, &global_sum, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

    if (rank == 0) {
        double pi = global_sum * h;
        std::cout << std::setprecision(16) << "Pi is approximately " << pi
                  << ", Error is " << pi - PI25DT << std::endl;
    }

    MPI_Finalize();
    return 0;
}
```

```fortran
C mpi_pi.f
C     PROGRAM TO COMPUTE PI IN PARALLEL WITH FORTRAN 77
      PROGRAM PI_F77
      IMPLICIT NONE
      INCLUDE 'mpif.h'
      INTEGER IERROR, I, N, RANK, SIZE, I_START, I_END
      DOUBLE PRECISION H, X, LOCAL_SUM, GLOBAL_SUM, PI
      DOUBLE PRECISION PI25DT
      PARAMETER (PI25DT = 3.141592653589793238462643D0)

      CALL MPI_INIT(IERROR)
      CALL MPI_COMM_RANK(MPI_COMM_WORLD, RANK, IERROR)
      CALL MPI_COMM_SIZE(MPI_COMM_WORLD, SIZE, IERROR)

      IF (RANK .EQ. 0) THEN
         WRITE(*,*) 'Enter the number of intervals:'
         READ(*,*) N
      END IF

      CALL MPI_BCAST(N, 1, MPI_INTEGER, 0, MPI_COMM_WORLD, IERROR)

      H = 1.0D0 / DBLE(N)
      LOCAL_SUM = 0.0D0
      I_START = RANK + 1
      I_END = N

      DO 10 I = I_START, I_END, SIZE
         X = H * (DBLE(I) - 0.5D0)
         LOCAL_SUM = LOCAL_SUM + 4.0D0 / (1.0D0 + X*X)
10    CONTINUE

      CALL MPI_REDUCE(LOCAL_SUM, GLOBAL_SUM, 1, MPI_DOUBLE_PRECISION,
     &     MPI_SUM, 0, MPI_COMM_WORLD, IERROR)

      IF (RANK .EQ. 0) THEN
         PI = GLOBAL_SUM * H
         WRITE(*,*) 'Pi is approximately ', PI
         WRITE(*,*) 'Error is ', PI - PI25DT
      END IF

      CALL MPI_FINALIZE(IERROR)
      END
```

```fortran
! mpi_pi.f90
!     PROGRAM TO COMPUTE PI IN PARALLEL WITH FORTRAN 90
      PROGRAM pi_f90
      USE mpi
      IMPLICIT NONE
      INTEGER :: ierr, i, n, rank, size, i_start, i_end
      REAL(8) :: h, x, local_sum, global_sum, pi
      REAL(8), PARAMETER :: PI25DT = 3.141592653589793238462643D0

      CALL MPI_INIT(ierr)
      CALL MPI_COMM_RANK(MPI_COMM_WORLD, rank, ierr)
      CALL MPI_COMM_SIZE(MPI_COMM_WORLD, size, ierr)

      IF (rank == 0) THEN
         WRITE(*,*) 'Enter the number of intervals:'
         READ(*,*) n
      END IF

      CALL MPI_BCAST(n, 1, MPI_INTEGER, 0, MPI_COMM_WORLD, ierr)

      h = 1.0D0 / REAL(n, KIND=8)
      local_sum = 0.0D0
      i_start = rank + 1
      i_end = n

      DO i = i_start, i_end, size
         x = h * (REAL(i, KIND=8) - 0.5D0)
         local_sum = local_sum + 4.0D0 / (1.0D0 + x*x)
      END DO

      CALL MPI_REDUCE(local_sum, global_sum, 1, MPI_DOUBLE_PRECISION, &
     &     MPI_SUM, 0, MPI_COMM_WORLD, ierr)

      IF (rank == 0) THEN
         pi = global_sum * h
         WRITE(*,*) 'Pi is approximately ', pi
         WRITE(*,*) 'Error is ', pi - PI25DT
      END IF

      CALL MPI_FINALIZE(ierr)
      END PROGRAM pi_f90
```
