# bash adv

## optimization

### built-in command

```bash
# inefficient
if [ "$var" -eq 1 ]; then
    echo "Equal to 1"
fi

# efficient
if [[ "$var" -eq 1 ]]; then
    echo "Equal to 1"
fi
```

### minimize sub shell

```bash
# inefficient
output=$(cat file.txt)

# efficient
output=$(<file.txt)
```

### array for bulk data

```bash
# inefficient
item1="apple"
item2="banana"
item3="cherry"

# efficient
items=("apple" "banana" "cherry")
for item in "${items[@]}"; do
    echo "$item"
done
```

### enable noclobber

```bash
set -o noclobber
```

### use Function

```bash
function greet() {
    local name=$1
    echo "Hello, $name"
}

greet "Alice"
greet "Bob"
```

### efficient file operation

```bash
# inefficient
while read -r line; do
    echo "$line"
done < file.txt

# efficient
while IFS= read -r line; do
    echo "$line"
done < file.txt
```

### parallel processing

```bash
# using xargs for parallel processing
cat urls.txt | xargs -n 1 -P 4 curl -O
```

---

## error handling

### exit on error

```bash
set -e
```

### custom error message

```bash
command1 || { echo "command1 failed"; exit 1; }
```

### trap signal

```bash
trap 'echo "Error occurred"; cleanup; exit 1' ERR

function cleanup() {
    # cleanup code
}
```

### validate input

```bash
if [[ -z "$1" ]]; then
    echo "usage: $0 <argument>"
    exit 1
fi
```

### logging

```bash
logfile="script.log"
exec > >(tee -i $logfile)
exec 2>&1

echo "script started"
```

---

## automating complex system administration task

### automated backup

```bash
#!/bin/bash

set -e
trap 'echo "backup failed"; exit 1' ERR

backup_dir="/backup"
timestamp=$(date +%Y%m%d%H%M%S)
backup_file="${backup_dir}/backup_${timestamp}.tar.gz"

# Create a backup
tar -czf "$backup_file" /important_data

echo "backup completed: $backup_file"
```

### system monitoring

```bash
#!/bin/bash

threshold=80
partition="/dev/sda1"

usage=$(df -h | grep "$partition" | awk '{print $5}' | sed 's/%//')

if [[ "$usage" -gt "$threshold" ]]; then
    echo "disk usage on $partition is above $threshold%"
    # add code to handle high disk usage
fi
```

### user management

```bash
#!/bin/bash

function add_user() {
    local username=$1
    useradd "$username" && echo "User $username added successfully"
}

function remove_user() {
    local username=$1
    userdel "$username" && echo "User $username removed successfully"
}

case $1 in
    add)
        add_user "$2"
        ;;
    remove)
        remove_user "$2"
        ;;
    *)
        echo "Usage: $0 {add|remove} <username>"
        exit 1
        ;;
esac
```

### automated update

```bash
#!/bin/bash

set -e
trap 'echo "update failed"; exit 1' ERR

apt-get update && apt-get upgrade -y

echo "system updated successfully"
```

### network configuration

```bash
#!/bin/bash

function configure_network() {
    local interface=$1
    local ip_address=$2
    local gateway=$3

    cat <<EOF > /etc/network/interfaces
auto $interface
iface $interface inet static
    address $ip_address
    gateway $gateway
EOF

    systemctl restart networking
    echo "network configured on $interface"
}

configure_network "eth0" "192.168.1.100" "192.168.1.1"
```

---

## exec

```bash
linux:~ $ bash -c "exec -a my_sleep sleep 300" &
linux:~ $ ps aux | grep my_sleep
linux:~ $ pgrep -f my_sleep
linux:~ $ cat /proc/`pgrep -f my_sleep`/comm
linux:~ $ cat /proc/$(pgrep -f my_sleep)/cmdline
```

---

## ref

- [Advanced Shell Scripting Techniques: Automating Complex Tasks with Bash](https://omid.dev/2024/06/19/advanced-shell-scripting-techniques-automating-complex-tasks-with-bash/#enable-noclobber)
- [Advanced Bash-Scripting Guide](https://tldp.org/LDP/abs/html/)
- [Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html)
