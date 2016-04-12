# Driver

lspci | grep -i nvidia


# Install CUDA

```
Linux:~ # sh cuda_<version>_linux.run
Linux:~ # nvidia-uninstall
```

## Diable Nouveau


```
Linux:~ # lsmod | grep nouveau
```


`RHEL/CentOS`

```
rhel:~ # cat /usr/lib/modprobe.d/blacklist-nouveau.conf
blacklist nouveau
options nouveau modeset=0

rhel:~ # dracut --force
```

`OpenSuSE`

```
opensuse:~ # cat /usr/lib/modprobe.d/blacklist-nouveau.conf
blacklist nouveau
options nouveau modeset=0

opensuse:~ # /sbin/mkinitrd
```


```
#!/bin/bash
/sbin/modprobe nvidia
if [ "$?" -eq 0 ]; then
  # Count the number of NVIDIA controllers found.
  NVDEVS=`lspci | grep -i NVIDIA`
  N3D=`echo "$NVDEVS" | grep "3D controller" | wc -l`
  NVGA=`echo "$NVDEVS" | grep "VGA compatible controller" | wc -l`
  N=`expr $N3D + $NVGA - 1`
  for i in `seq 0 $N`; do
  mknod -m 666 /dev/nvidia$i c 195 $i
  done
  mknod -m 666 /dev/nvidiactl c 195 255
else
  exit 1
fi

/sbin/modprobe nvidia-uvm
if [ "$?" -eq 0 ]; then
  # Find out the major device number used by the nvidia-uvm driver
  D=`grep nvidia-uvm /proc/devices | awk '{print $1}'`
  mknod -m 666 /dev/nvidia-uvm c $D 0
else
  exit 
```


/dev/nvidia*
nvidia-modprobe

usermod -a -G video <username>


# Environment

```
export PATH=/usr/local/cuda-7.5/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-7.5/lib64:$LD_LIBRARY_PATH

cuda-install-samples-7.5.sh

$ cat /proc/driver/nvidia/version
```


# Test

```
Linux:~ # cat hello.cu
// This is the REAL "hello world" for CUDA!
// It takes the string "Hello ", prints it, then passes it to CUDA with an array
// of offsets. Then the offsets are added in parallel to produce the string "World!"
// By Ingemar Ragnemalm 2010
 
#include <stdio.h>
 
const int N = 16; 
const int blocksize = 16; 
 
__global__ 
void hello(char *a, int *b) 
{
	a[threadIdx.x] += b[threadIdx.x];
}
 
int main()
{
	char a[N] = "Hello \0\0\0\0\0\0";
	int b[N] = {15, 10, 6, 0, -11, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
 
	char *ad;
	int *bd;
	const int csize = N*sizeof(char);
	const int isize = N*sizeof(int);
 
	printf("%s", a);
 
	cudaMalloc( (void**)&ad, csize ); 
	cudaMalloc( (void**)&bd, isize ); 
	cudaMemcpy( ad, a, csize, cudaMemcpyHostToDevice ); 
	cudaMemcpy( bd, b, isize, cudaMemcpyHostToDevice ); 
	
	dim3 dimBlock( blocksize, 1 );
	dim3 dimGrid( 1, 1 );
	hello<<<dimGrid, dimBlock>>>(ad, bd);
	cudaMemcpy( a, ad, csize, cudaMemcpyDeviceToHost ); 
	cudaFree( ad );
	cudaFree( bd );
	
	printf("%s\n", a);
	return EXIT_SUCCESS;
}

Linux:~ # nvcc hello.cu -o hello.exe
Linux:~ # ./hello.exe
```

# MPS


```
Linux:~ # nvidia-smi -c 3
```

set compute mode:

0: DEFAULT / SHARED_PROCESS

1: EXCLUSIVE_THREAD

2: PROHIBITED

3: EXCLUSIVE_PROCESS

```
# start MPS
Linux:~ # nvidia-smi -c EXCLUSIVE_PROCESS
Linux:~ # export CUDA_VISIBLE_DEVICES=0
Linux:~ # nvidia-cuda-mps-control -d

# stop MPS
Linux:~ # nvidia-smi -c 0
Linux:~ # echo quit | nvidia-cuda-mps-control

# show gpu info
Linux:~ # nvidia-smi -q -d CLOCK
Linux:~ # nvidia-smi -q -d SUPPORTED_CLOCKS
Linux:~ # nvidia-smi -q -d compute 

# monitor gpu
Linux:~ # nvidia-smi -l
```

# Reference

[driver](http://www.nvidia.com/Download/index.aspx)

[cuda](https://developer.nvidia.com/cuda-downloads)

[CUDA Installation Guide Linux](http://developer.download.nvidia.com/compute/cuda/7.5/Prod/docs/sidebar/CUDA_Installation_Guide_Linux.pdf)

[CUDA Quick Start Guide](http://developer.download.nvidia.com/compute/cuda/7.5/Prod/docs/sidebar/CUDA_Quick_Start_Guide.pdf)

[CUDA Toolkit Documentation v7.5](http://docs.nvidia.com/cuda/index.html#axzz41Zv5GNNs)

[Installing VASP](http://cms.mpi.univie.ac.at/wiki/index.php/Installing_VASP)
