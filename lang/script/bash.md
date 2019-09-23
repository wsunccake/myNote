# BASH

## run

```bash
# method 1
linux:~ # chmod +x script.sh
linux:~ # ./script.sh

# method 2
linux:~ # sh script.sh

# method 3
linux:~ # export VAR=value
linux:~ # ./script.sh

# method 4s
linux:~ # env VAR=value ./script.sh
```

---

## stdout, stderr

```bash
| Function                              | CSH             |  SH
| ------------------------------------- | --------------- | -----------------
| Send stdout to file                   | prog > file     |  prog > file
| Send stderr to file                   |                 |  prog 2> file
| Send stdout and stderr to file        | prog >& file    |  prog > file 2>&1
| Take stdin from file                  | prog < file     |  prog < file
| Send stdout to end of file            | prog >> file    |  prog >> file
| Send stderr to end of file            |                 |  prog 2>> file
| Send stdout and stderr to end of file | prog >>& file   |  prog >> file 2>&1
|                                       |                 |  prog &> file
|                                       |                 |  prog >& file
| Read stdin from keyboard until c      | prog <          |  prog <
| Pipe stdout to prog2                  | prog | prog2    |  prog | prog2
| Pipe stdout and stderr to prog2       | prog |& prog2   |  prog 2>&1 | prog2
```


---

## pipe example

```bash
linux:~ # tar cf - *.log | gzip > file.tar.gz
linux:~ # gzip -dc file.tar.gz | tar xf -
linux:~ # tar cf - *.log | tar xf - -C backup_dir

linux:~ # curl http://download/file.tar.gz -o file.tar.gz && tar zxf file.tar.gz
linux:~ # curl http://download/file.tar.gz | tar zx
```


---

## prefix and suffix

```bash
FILE_PATH=/usr/lib/python/site-package/xxx-1.0/yyy.zz
echo "raw:"
echo ${FILE_PATH}

echo "prefix:"
echo ${FILE_PATH%.*}
echo ${FILE_PATH%%.*}

echo "suffix:"
echo ${FILE_PATH#*/}
echo ${FILE_PATH##*/}

# For bash 4.x
SENTENCE="That is a test."
echo "sentence:"
echo "${SENTENCE}"

echo "reverse:"
echo "${SENTENCE~~}"

echo "upper:"
echo "${SENTENCE^^}"

echo "lower:"
echo "${SENTENCE,,}"

# define var operation
VAR="Hello Bash"
echo "define VAR: ${VAR}"
echo "\${VAR:=value}: ${VAR:=value}"
echo "VAR: ${VAR}"
echo

VAR="Hello Bash"
echo "define VAR: ${VAR}"
echo "\${VAR:-value}: ${VAR:-value}"
echo "VAR: ${VAR}"
echo

VAR="Hello Bash"
echo "define VAR: ${VAR}"
echo "VAR:+value ${VAR:+value}"
echo "VAR: ${VAR}"
echo

VAR="Hello Bash"
echo "define VAR: ${VAR}"
echo "\${VAR:?value}: ${VAR:?value}"
echo "VAR: ${VAR}"
echo

# undefine var operation
unset VAR
echo "undefine VAR: ${VAR}"
echo "\${VAR:=value}: ${VAR:=value}"
echo "VAR: ${VAR}"
echo

unset VAR
echo "undefine VAR: ${VAR}"
echo "\${VAR:-value}: ${VAR:-value}"
echo "VAR: ${VAR}"
echo

unset VAR
echo "undefine VAR: ${VAR}"
echo "\${VAR:+value}: ${VAR:+value}"
echo "VAR: ${VAR}"
echo

unset VAR
echo "undefine VAR: ${VAR}"
#echo "VAR:?value ${VAR:?value}"  # show err
echo "VAR: ${VAR}"
echo
```


---

## if

```bash
if [ "x$SEX" == "xmale" ]; then
  echo "Hi male"
else
  echo "Hi Female"
fi

[ "x$SEX" == "xmale" ] && echo "Hi male" || echo "Hi Female"
```


---

## for

```bash
for ((i=1; i<=3; i++)); do
  echo $i
done

for E in "1 2 3"; do
  echo "index: $E"
done

for E in 1 2 3; do
  echo "index: $E"
done

for E in `echo -e "1\n2\n3"`; do
  echo "index: $E"
done

for E in `seq 3`; do
  echo "index: $E"
done

seq 3 | xargs -i echo "{}"
```


---

## while

```bash
i=0
while [ $i -lt 3 ]; do
  i=`expr $i + 1`
  echo "$i"
done

i=0
while true; do
  i=`expr $i + 1`
  echo "$i"
  if [ $i -ge 3 ]; then
    break
  fi
done
```

---

## until


---

## case


---

## select


---

## heredoc

```bash
cat > tmp.txt << EOF
echo "hello bash"
EOF

mysql -u root << EOF
  USE nova;
  SELECT id hypervisor_hostname FROM compute_nodes WHERE hypervisor_hostname = "$HOST";
  DELETE FROM compute_nodes WHERE hypervisor_hostname = "$HOST";
EOF

mongo << EOF
use $DB
print("$COLLECTION")
db.getCollection("$COLLECTION").findOne()
EOF
```


---

## array

```bash
# Array
declare -a ARR
ARR=( eth0 em1 )

echo "ARR Length: ${#ARR[@]}"

for ITEM in ${ARR[*]}; do
  echo "ITEM: $ITEM"
done

for ((i=0; i < ${#ARR[@]}; i++)); do
  echo "Index: $i, ITEM: ${ARR[$i]}"
done

# Associated Array
declare -A MAP
MAP=( [eth0]=192.168.0.1 [em1]=172.16.0.1 )

echo "MAP Length: ${#MAP[@]}"

for KEY in ${!MAP[@]}; do
  echo "KEY: $KEY, VALUE: ${MAP[$KEY]}"
done
```
