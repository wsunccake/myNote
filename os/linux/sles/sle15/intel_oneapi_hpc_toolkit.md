# Intel oneAPI HPC Toolkit

## require

```bash
sle:~ # zypper in gcc-c++ libnotify4 at-spi2-core
```

---

## install

download [Intel® oneAPI HPC Toolkit](https://www.intel.com/content/www/us/en/developer/tools/oneapi/hpc-toolkit-download.html)

```bash
sle:~ # sh intel-oneapi-hpc-toolkit-<yyyy>.<m>.<xxx>_offline.sh
```

## usage

```bash
sle:~ $ ls /opt/intel/oneapi
sle:~ $ source /opt/intel/oneapi/<yyyy>.<m>/oneapi-vars.sh
sle:~ $ echo $ONEAPI_ROOT
```

### compiler

```bash
sle:~ $ echo $CMPLR_ROOT

# c compiler
sle:~ $ which icx
sle:~ $ icx -o hello hello.c

# c++ compiler
sle:~ $ which icpx
sle:~ $ icpx -o hello hello.cpp

# fortran compiler
sle:~ $ which ifx
sle:~ $ ifx -o hello -fixed hello.f     # fortran 77
sle:~ $ ifx -o hello hello.f90          # fortran 90
```

```c
// hello.c
#include <stdio.h>

int main() {
    printf("Hello, World!\n");
    return 0;
}
```

```cpp
// hello.cpp
#include <iostream>

int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}
```

```fortran
C hello.f
      PROGRAM HELLOW
      WRITE(UNIT=*, FMT=*) 'Hello, World!'
      END
```

```fortran
! hello.f90
program hello
    implicit none
    print *, "Hello, World!"
end program hello
```

### mkl

```bash
sle:~ $ echo $MKLROOT

sle:~ $ icx -o matrix matrix.c -lmkl_rt -lpthread -lm           # c
sle:~ $ icpx -o matrix matrix.cpp -lmkl_rt -lpthread -lm        # c++
sle:~ $ ifx -o matrix matrix.f -lmkl_rt -lpthread -lm           # fortran 77
sle:~ $ ifx -o matrix matrix.f90 -lmkl_rt -lpthread -lm         # fortran 90
```

```c
// matrix.c
#include <stdio.h>
#include "mkl.h"

int main() {
    double A[4] = {1.0, 2.0, 3.0, 4.0}; // 2x2 matrix, column-major
    double B[4] = {1.0, 1.0, 1.0, 1.0}; // 2x2 matrix, column-major
    double C[4] = {0.0, 0.0, 0.0, 0.0}; // Result matrix, C = A*B

    int m = 2, n = 2, k = 2;
    double alpha = 1.0, beta = 0.0;

    cblas_dgemm(CblasColMajor, CblasNoTrans, CblasNoTrans,
                m, n, k, alpha, A, m, B, k, beta, C, m);

    printf("Result matrix C:\n");
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            printf("%f ", C[i + j*m]);
        }
        printf("\n");
    }

    return 0;
}
```

```cpp
// matrix.cpp
#include <iostream>
#include "mkl.h"

int main() {
    double A[4] = {1.0, 2.0, 3.0, 4.0};
    double B[4] = {1.0, 1.0, 1.0, 1.0};
    double C[4] = {0.0, 0.0, 0.0, 0.0};

    int m = 2, n = 2, k = 2;
    double alpha = 1.0, beta = 0.0;

    cblas_dgemm(CblasColMajor, CblasNoTrans, CblasNoTrans,
                m, n, k, alpha, A, m, B, k, beta, C, m);

    std::cout << "Result matrix C:" << std::endl;
    for (int i = 0; i < m; ++i) {
        for (int j = 0; j < n; ++j) {
            std::cout << C[i + j * m] << " ";
        }
        std::cout << std::endl;
    }

    return 0;
}
```

```fortran
C matrix.f
      PROGRAM DGEMMEX
C
C     Parameters: M, N, K - matrix dimensions
C                 ALPHA, BETA - scalar multipliers
C
      INTEGER M, N, K
      PARAMETER (M=2, N=2, K=2)
      DOUBLE PRECISION A(M,K), B(K,N), C(M,N)
      DOUBLE PRECISION ALPHA, BETA
C
C     Initialize matrices
C
      DATA A /1.0, 2.0, 3.0, 4.0/
      DATA B /1.0, 1.0, 1.0, 1.0/
      DATA C /4*0.0/
      DATA ALPHA /1.0/, BETA /0.0/
C
C     Call MKL's dgemm routine
C
      CALL DGEMM('N', 'N', M, N, K, ALPHA, A, M, B, K, BETA, C, M)
C
C     Print the result
C
      PRINT *, 'Result matrix C:'
      PRINT 100, ((C(I,J), J=1,N), I=1,M)
100   FORMAT(2F10.2)
C
      END
```

```fortran
! matrix.f90
PROGRAM dgemm_example
    USE mkl_dgemm_fortran_95, ONLY: dgemm
    IMPLICIT NONE
    INTEGER, PARAMETER :: m=2, n=2, k=2
    REAL(8) :: A(m, k), B(k, n), C(m, n)
    REAL(8) :: alpha, beta

    ! Initialize matrices
    A = RESHAPE((/1.0d0, 2.0d0, 3.0d0, 4.0d0/), (/m, k/))
    B = 1.0d0
    C = 0.0d0

    alpha = 1.0d0
    beta = 0.0d0

    ! Call MKL's dgemm routine
    CALL dgemm(A, B, C, transa='n', transb='n', alpha=alpha, beta=beta)

    ! Print the result
    WRITE(*,*) 'Result matrix C:'
    WRITE(*,*) C

END PROGRAM dgemm_example
```

### mpi

```bash
sle:~ $ echo $I_MPI_ROOT

sle:~ $ mpicc  -o mpi_pi [-cc=<c_compiler>]       mpi_pi.c          # c
sle:~ $ mpicxx -o mpi_pi [-cxx=<c++_compiler>]    mpi_pi.cpp        # c++
sle:~ $ mpif77 -o mpi_pi [-fc=<fortran_compiler>] mpi_pi.f          # fortran 77
sle:~ $ mpif90 -o mpi_pi [-fc=<fortran_compiler>] mpi_pi.f90        # fortran 90

sle:~ $ mpiicx  -o mpi_pi mpi_pi.c              # intel c
sle:~ $ mpiicpx -o mpi_pi mpi_pi.cpp            # intel c++
sle:~ $ mpiifx  -o mpi_pi mpi_pi.f              # intel fortran 77
sle:~ $ mpiifx  -o mpi_pi mpi_pi.f90            # intel fortran 90

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
