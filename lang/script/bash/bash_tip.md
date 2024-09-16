# bash tip

## console

### console garbage and gibberish

```bash
linux:~ $ reset
linux:~ $ tput reset

# if reset fail, do it
linux:~ $ stty sane

# type the following ANSI escape sequence
linux:~ $ echo -e "\033c"
```

---

## code convert

### utf

```bash
linux:~ $ echo -n '正' | xxd -p             # utf to hex
linux:~ $ echo -n "e6ada3" | xxd -r -p      # hex to utf
```

### ascii

```bash
linux:~ $ echo -n 'A' | xxd -ps     # ascii to hex
linux:~ $ echo -n 41 | xxd -r -p    # hex to ascii
```

### hex

```bash
# decimal to hex
linux:~ $ printf "%X\n" 26
linux:~ $ printf "%x\n" 26
linux:~ $ echo "obase=16; 26" | bc

# hex to decimal
linux:~ $ printf "%d\n" 0x1A
linux:~ $ printf "%d\n" 0x1a
linux:~ $ echo "ibase=16; 1A" | bc
linux:~ $ echo $((16#1A))
```

---

## calculate

## expr

```bash
echo $((1 + 2))
a=1
echo $(($a + 2))
```
