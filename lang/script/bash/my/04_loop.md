# loop

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

for f in /etc/*.conf; do
  echo $f
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

while read -r line; do
  username=`echo $line | awk -F: '{print $1}'`
  home=`echo $line | awk -F: '{print $6}'`
  echo "username: $username, home: $home"
done < /etc/passwd
```

---

## until

```bash
i=0
until [ $i -eq 3 ]; do   
  i=`expr $i + 1`          
  echo "$i"                
done

i=0
until false; do
  i=`expr $i + 1`
  echo "$i"
  [ $i -ge 3 ] && break
done
```


---

## select

```bash
select V in a b q; do
  echo "select: $V"
  [ "$V" == "q" ] && break
done
```
