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

send_user "$word1 ${word2}\n"
send_user "$words\n"
send_user "[lindex $words 0]\n"
send_user "[lindex $words 1]\n"

# shell environment variable
set h0 $env(HOME)
send_user "$env(HOME)\n"
send_user "[lindex $env(HOME) 0]\n"

# argument
set a0 [lindex $argv 0]
if { [string compare $a0 ""] == 0 } {
  set a0 192.168.0.1
}
send_user "argument: $a0\n"
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

```bash
#!/usr/bin/expect -f

set USERNAME super
set PASSWORDS "default !Admin"
set AP_IP  [lindex $argv 0]
if { [string compare $AP_IP ""] == 0 } {
  set AP_IP 192.168.10.10
}
set WAIT_TIME 3

spawn ssh $AP_IP

set i 0

# login
expect {
  "Please Login:" {
    send "$USERNAME\n"
    sleep $WAIT_TIME
    exp_continue
  }

  "Password :" {
    send "[lindex $PASSWORDS $i]\n"
    sleep $WAIT_TIME
    incr i
    exp_continue
  }

  eof {
    send_user "\n\n*** ERROR: server has closed the connection\n"
    exit $ERR_UNEXPECTED_OUTPUT
  }
}

# check login status
expect {
  "New Password:" {
    send "\n"
    exit
  }

  "apcli:" {
    send "\n"
    sleep $WAIT_TIME
  }
}

# set factory
set SET_FACTORY_CMD "set\\ factory reboot"
for {set i 0} {$i < 2} {incr i} {
  expect "rkscli:" {
    send "[lindex $SET_FACTORY_CMD $i]\n"
  }
}

expect "apcli:" {
  send "\n"
  sleep $WAIT_TIME
}

exit
```
