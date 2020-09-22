# bash util cmd

## generate mac, ip

```bash
convert_hex_to_dec() {
  local hex_num=$1

  dec_num=`printf "%d\n" "0x${hex_num}"`
  echo  $dec_num
}

convert_dec_to_hex() {
  local dec_num=$1
  local width=$2
  width=${width:-0}

  hex_num=`printf "%${width}x\n" "${dec_num}"`
  echo $hex_num
}

gen_mac() {
# 6576734208 -> 00:01:88:01:00:00
  local mac=$1
  local num=$2

  hex_num_first=`echo $mac | sed s/://g`
  dec_num_first=`convert_hex_to_dec $hex_num_first`
  dec_num_last=`expr $dec_num_first + $num - 1`

  for tmp_dec in `seq $dec_num_first $dec_num_last`; do
    tmp_hex=`convert_dec_to_hex $tmp_dec 012`
    tmp_mac=`printf "%02x:%02x:%02x:%02x:%02x:%02x" 0x${tmp_hex:0:2} 0x${tmp_hex:2:2} 0x${tmp_hex:4:2} 0x${tmp_hex:6:2} 0x${tmp_hex:8:2} 0x${tmp_hex:10:2}`
#    echo $tmp_dec, $tmp_hex, $tmp_mac
    echo $tmp_mac
  done
}

gen_ip() {
# 16843009 (dec) -> 01010101 (hex)
  local ip=$1
  local num=$2
 
  hex_num_first=""
  vals=(`echo $ip | sed 's/\./ /g'`)
  for v in ${vals[*]}; do
    hex_num_first="$hex_num_first`convert_dec_to_hex $v 02`"
  done
#  echo "$ip, ${vals[*]}, ${vals[0]}, ${vals[1]}, $hex_num_first"

  dec_num_first=`convert_hex_to_dec $hex_num_first`
  dec_num_last=`expr $dec_num_first + $num - 1`

  for tmp_dec in `seq $dec_num_first $dec_num_last`; do
    tmp_hex=`convert_dec_to_hex $tmp_dec 08`
    tmp_ip=`printf "%d.%d.%d.%d" 0x${tmp_hex:0:2} 0x${tmp_hex:2:2} 0x${tmp_hex:4:2} 0x${tmp_hex:6:2}`
#    echo $tmp_dec, $tmp_hex, $tmp_ip
    echo $tmp_ip
  done
}

gen_mac 00:11:22:33:44:FF 3
gen_ip 1.2.3.255 3
```


---

## curl to run api

```bash
curl_api_cmd() {
  local method=$1
  local url=$2
  local data=$3

  COOKIE=${COOKIE:=/tmp/curl_cmd.cookie}
  CURL_TIMEOUT=${CURL_TIMEOUT:=10}

  case ${method} in
  "GET"|"DELETE")
    curl --insecure \
         --silent \
         --max-time "${CURL_TIMEOUT}" \
         --cookie "${COOKIE}" \
         --write-out "\nResponse code: %{http_code}\nResponse time: %{time_total}\n" \
         --request "${method}"\
         --header "content-type: application/json" \
         "${url}"
    ;;
  "POST"|"PUT"|"PATCH")
    curl --insecure \
         --silent \
         --max-time "${CURL_TIMEOUT}" \
         --cookie "${COOKIE}" \
         --write-out "\nResponse code: %{http_code}\nResponse time: %{time_total}\n" \
         --request "${method}"\
         --header "content-type: application/json" \
         --data "${data}" \
         "${url}"
    ;;
  esac
}

curl_api_cmd GET https://api.github.com
```


### for bash 4.2-

```bash
restful_api() {
  eval "declare -A api_data="${1#*=}

  local method=${api_data['method']}
  local url=${api_data['url']}
  local data=${api_data['data']}
  local file=${api_data['file']}

  echo "Request method: ${method}"
  echo "Request URL: ${url}"

  if [ -z "$data" ]; then
    if [ -n "$file" ]; then
      data="@${file}"
      echo "Request body: `cat ${file}`"
    fi
  else
    echo "Request body: ${data}"
  fi

  echo -n 'Response body: '
  curl_api_cmd ${method} ${url} "${data}"
}

declare -A api_data=([url]=https://api.github.com [method]=GET)
restful_api "$(declare -p api_data)"
```


### for bash 4.3+

```bash
restful_api() {
  local -n api_data=$1

  echo $api_data

  local method=${api_data['method']}
  local url=${api_data['url']}
  local data=${api_data['data']}
  local file=${api_data['file']}

  echo "Request method: ${method}"
  echo "Request URL: ${url}"

  if [ -z "$data" ]; then
    if [ -n "$file" ]; then
      data="@${file}"
      echo "Request body: `cat ${file}`"
    fi
  else
    echo "Request body: ${data}"
  fi

  echo -n 'Response body: '
  curl_cmd ${method} ${url} "${data}"
}

declare -A API_DATA=([url]=https://api.github.com [method]=GET)
restful_api API_DATA
```

