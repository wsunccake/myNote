# expect

## run

expect [ pattern-string {action} ]

```bash
linux:~ # cat hello.exp
#!/usr/bin/expect

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


---

## var

```bash
set word1 "hello"
set word2 world
set words "$word1 ${word2}"

send "$word1 ${word2}\n"
send "$words\n"
send "[lindex $words 0]\n"
send "[lindex $words 1]\n"

# shell environment variable
send "$env(HOME)\n"
send "[lindex $env(HOME) 0]\n"
```


---

## loop

```bash
set words "hello world"

for {set i 0} {$i < 3} {incr i} {
  puts "$i: hello"
}

for {set i 0} {$i < 2} {incr i} {
  send "[lindex $words $i]\n"
}
```


---

## expect

```bash
linux:~ $ sh
sh-4.2$ ls
```

-->

```bash
#!/usr/bin/expect -f

set ver 4.2
spawn sh

### expect "sh-4.2$"
### $, dollar 被視為變數, 不是字元

# expect "sh-4.2"
# expect "sh-"
# 部分對比即可
expect "sh-$ver\\\$"
send "ls\n"

expect "sh-$ver"
exit
```


```bash
#!/usr/bin/expect -f

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
#!/usr/bin/expect -f
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
