# compiler / debug tool

## ld

---

## ar

---

## nm

```bash
linux:~ $ nm <file>
```

---

## ldd

```bash
linux:~ $ ldd <file>
linux:~ $ LD_LIBRARY_PATH=<path>
```

---

## gdb

[gdb](./gdb.md)

---

## objdump

```bash
linux:~ $ objdump -S|-d|-D [-M intel] <file>        # disassemble
linux:~ $ objdump -x|-h|-p <file>                   # header
linux:~ $ objdump -p <file>                         # dynamic
```

---

## readelf

```bash
linux:~ $ readelf -a|-d|-D [-M intel] <file>        # disassemble
linux:~ $ readelf -h <file>                         # header
linux:~ $ readelf -d <file>                         # dynamic
```
