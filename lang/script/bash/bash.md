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

```bash
i=0
until [ $i -eq 3 ]; do   
  i=`expr $i + 1`          
  echo "$i"                
done                                                                                                                                                

i=0
until false; do
i=`expr $i + 1`                                                                                                                                       echo "$i"
  [ $i -ge 3 ] && break
done
```


---

## case

```bash
case $SHELL in
  "/bin/bash")
    echo "BASH"
    ;;

  "/bin/tcsh")
    echo "TCSH"
    ;;
    
  *)
    echo "UNKNOWN"
    ;;
esac
```

---

## select

```bash
select V in a b q; do
  echo "select: $V"
  [ "$V" == "q" ] && break
done
```


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
ARR=(eth0 em1)
ARR+=(en0)
echo "ARR Length: ${#ARR[@]}"

for ITEM in ${ARR[*]}; do
  echo "ITEM: $ITEM"
done

for ((i=0; i < ${#ARR[@]}; i++)); do
  echo "Index: $i, ITEM: ${ARR[$i]}"
done

# Array Append
A1=(1 2 3 X)
A2=(a b c X)
A3=(${A1[@]} ${A2[*]})

# String to Array
S=1,2,3,4
A=(`echo $S | sed 's/,/ /g'`)

# Associated Array
declare -A MAP
MAP=( [eth0]=192.168.0.1 [em1]=172.16.0.1 )

echo "MAP Length: ${#MAP[@]}"

for KEY in ${!MAP[@]}; do
  echo "KEY: $KEY, VALUE: ${MAP[$KEY]}"
done
```


---

## arg

```bash
echo "#: $#, @: $@, *: $*, 1: $1"
shift
echo "#: $#, @: $@, *: $*, 1: $1"
```


---

## set

```bash
linux:~ # set
linux:~ # set -o
linux:~ # set -e
linux:~ # set +e
```


---

## grep


---

## sed

```bash
linux:~ # echo "Hello BASH script" | sed 's/.//6g'              # Hello
linux:~ # echo "Hello BASH script" | sed 's/.\{6\}//'           # BASH script
linux:~ # echo "Hello BASH script" | sed 's/.\{6\}//;s/.//5g'   # BASH

linux:~ # STR=/usr/lib64/man-db/libmandb-2.6.3.so
linux:~ # echo $STR

# /usr/lib64/man-db/libmandb-2.6.3
linux:~ # echo ${STR%.*}
linux:~ # echo /usr/lib64/man-db/libmandb-2.6.3.so | sed 's/\(.*\)\..*$/\1/'

# /usr/lib64/man-db/libmandb-2
linux:~ # echo ${STR%%.*}
linux:~ # sed 's/\..*$//'

# usr/lib64/man-db/libmandb-2.6.3.so
linux:~ # echo ${STR#*/}    
linux:~ # sed 's/\///'

# libmandb-2.6.3.so
linux:~ # echo ${STR##*/}
linux:~ # sed 's/.*\///'
```

---

## awk

```bash
linux:~ # seq 5 | awk ' { sum = sum + $1 } END { print sum }'

# awk access shell variable
linux:~ # awk -v today="`date`" 'BEGIN {print today}'

# awk access environment variable
linux:~ # awk 'BEGIN {print ENVIRON["HOME"]}'

# awk argument
linux:~ # awk 'BEGIN {print ARGV[0], ARGV[1]}' "`date`"

# awk script
linux:~ # cat avg.awk
#!/usr/bin/awk -f

BEGIN {
  sum = 0
  i = 0
}                                                                                                                                                   

{
  sum = sum + $1
  i += 1
}

END {
  "count:", i
  "sum: ", sum
  "average: %f\n", sum/i
}
```


---

## find

```bash
linux:~ # find . -maxdepth 1 -mindepth 1 -type d
linux:~ # find . -ctime +7 -type f
linux:~ # find . -ctime -7 -type f
linux:~ # find . -ctime  7 -type f
```


---

## expect

expect [ pattern-string {action} ]

```bash
linux:~ # cat hello.exp
#!/bin/expect

send_user "hello expect\n"
exit

# method 1
linux:~ # chmod +x hello.exp
linux:~ # ./hello.exp

# method 2
linux:~ # expect hello.exp

# method 3
linux:~ # expect
expect> send_user "hello expect\n"
expect> exit
```

```bash
#!/bin/expect -f

spawn sh

// regex, regular expression
expect -re "\\\$|#"
send "date\n"

// globbing, filename globbing
expect ".*" { send "hostname\n" }

send_user "\n"
exit
```

```bash
#!/bin/expect -f
set user <username>
set pw <password>
set ip <ssh_server>

spawn ssh -o PubkeyAuthentication=no -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null $user@$ip

expect "password:" {
    send "$pw\n"
    sleep 3
}

expect -re "\\\$|#" {
    interact
}

exit
```


---

## xargs

```bash
linux:~ # seq 5 | xargs echo
linux:~ # seq 5 | xargs -t echo
linux:~ # seq 5 | xargs -t -n1 echo
linux:~ # seq 5 | xargs -I {} echo {}
linux:~ # seq 5 | xargs -i date
linux:~ # seq 5 | xargs -i sh -c 'expr {} + 1'
linux:~ # find . -type d | xargs -n1 ls -l
```


---

## compgen

```bash
# command
linux:~ # compgen -a  # alias
linux:~ # compgen -b  # builtin command
linux:~ # compgen -c  # command

# variable
linux:~ # compgen -e  # shell variable
linux:~ # compgen -v  # all variable

# file, directory
linux:~ # compgen -f  # file
linux:~ # compgen -d  # directory

# user, group
linux:~ # compgen -u  # user
linux:~ # compgen -g  # group

# wild list
linux:~ # compgen -W "aa ab Aa xyz abc123" -- a
```


---

## complete

```bash
linux:~ # complete -p   # list bash completion
linux:~ # complete -r   # remove bash completion

linux:~ # echo -e '#!/bin/bash\n\necho "ARG: $@"' > foo
linux:~ # chmod +x foo
linux:~ # touch a.foo b.foo c.foo

# filter pattern
linux:~ # complete -f -X '!*.foo' foo
linux:~ # ./foo <TAB><TAB>

# word list
linux:~ # complete -W 'abc xyz 123' foo
linux:~ # ./foo <TAB><TAB>

# function
linux:~ # function _foo_complete_() {
    local cmd="${1##*/}"
    local word=${COMP_WORDS[COMP_CWORD]}
    local line=${COMP_LINE}
    local xpat='!*.foo'

    echo
    echo "cmd: $cmd"
    echo "cur: ${cur}"
    echo "comp_cword: $COMP_CWORD"
    echo "comp_words: ${COMP_WORDS[*]}"
    echo "comp_line: ${COMP_LINE}"

    COMPREPLY=($(compgen -f -X "$xpat" -- "${cur}"))

    echo "compreply: ${COMPREPLY[*]}"

}
linux:~ # complete -F _foo_complete_ foo
linux:~ # ./foo <TAB><TAB>
```
