# eBPF

kprobe

uprobe

tracepoint

perf_event

## bcc

```bash
debian:~ # apt install linux-headers-`uname -r` linux-source-`uname -r`
debian:~ # apt install bpfcc-tools python3-bpfcc libbpfcc libbpfcc-dev bpftrace

centos:~ # yum install bcc-tools
centos:~ # yum install bcc-tools kernel-devel-`uname -r`
```

```bash
debian:~ # python3.9 /usr/share/doc/bpfcc-tools/examples/hello_world.py
debian:~ # python3.9 /usr/share/doc/bpfcc-tools/examples/tracing/bitehist.py
```

if show "warning: '**HAVE_BUILTIN_BSWAP32**' macro redefined [-Wmacro-redefined]", add it below

```python
prog = """
...
"""

b = BPF(text=prog)
```

->

```python
prog = """
...
"""

b = BPF(text=prog, cflags=["-Wno-macro-redefined"])
```

---

## kernel

```bash
linux:~ # grep CONFIG_BPF_SYSCALL=y /boot/config-`uname -r`

linux:~ # echo 1 > /proc/sys/net/core/bpf_jit_enable
```

---

## example

```python
# hello.py
from bcc import BPF

# bpf program in restricted C language.
prog = """
int hello_world(void *ctx) {
  bpf_trace_printk("Hello, World!\\n");
  return 0;
}
"""

b = BPF(text=prog, cflags=["-Wno-macro-redefined"])

# attaching hello_world function to sys_clone system call.
b.attach_kprobe(event=b.get_syscall_fnname("clone"), fn_name="hello_world")

# reading from /sys/kernel/debug/tracing/trace_pipe
b.trace_print(fmt="Program:{0} Message:{5}")
```

```python
# count.py
from bcc import BPF

prog = """
BPF_TABLE("array", u32, u32, stats, 1);
int hello_world(void *ctx) {
  u32 key = 0, value = 0, *val;
  val = stats.lookup_or_init(&key, &value);
  (*val)++;
  bpf_trace_printk("total fork syscall:%d\\n", *val);
  return 0;
}
"""

b = BPF(text=prog, debug=4, cflags=["-Wno-macro-redefined"])
b.attach_kprobe(event=b.get_syscall_fnname("clone"), fn_name="hello_world")
b.trace_print()
```

```python
# freq.py
from bcc import BPF
from time import sleep

prog = """
BPF_TABLE("array", u32, u32, stats, 1);
int hello_world(void *ctx) {
  u32 key = 0, value = 0, *val;
  val = stats.lookup_or_init(&key, &value);
  lock_xadd(val, 1);
  return 0;
}
"""

b = BPF(text=prog, cflags=["-Wno-macro-redefined"])

# getting shared kernel map
stats_map = b.get_table("stats")
b.attach_kprobe(event="sys_clone", fn_name="hello_world")

for x in range(0, 20):
    stats_map[ stats_map.Key(0) ] = stats_map.Leaf(0)
    sleep(1)
    print "Total sys_clone per second =", stats_map[ stats_map.Key(0) ].value;
```

---

## bpftrace

```bash
debian:~ # bpftrace -l
debian:~ # bpftrace -lv 'tracepoint:*'
debian:~ # bpftrace -l 'uprobe:/bin/bash:*'
```

---

## ref

[bcc Python Developer Tutorial](https://android.googlesource.com/platform/external/bcc/+/HEAD/docs/tutorial_bcc_python_developer.md)
