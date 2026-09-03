#!/bin/bash
# ==============================================================================
# File Name: idrac_functions.sh
# Description: Helper functions for iDRAC administration via RACADM / ipmitool
# ==============================================================================

# ----------------- 基本設定 -----------------
IDRAC_USER="root"
IDRAC_PASS="calvin"
IP_LIST="idrac_ip.txt"
LOG_FILE="idrac_setup.log"
ISO_URL="http://10.206.17.100/exsi.iso"

# DEBUG 開關 (true = 顯示實際執行的完整指令 ; false = 隱藏指令細節)
DEBUG_MODE=true

# 顏色定義
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# ----------------- Log 模組 -----------------

log_msg() {
    local level="$1"
    local msg="$2"
    local timestamp=$(date "+%Y-%m-%d %H:%M:%S")
    local formatted_msg=""

    case "$level" in
        "INFO")    formatted_msg="[${timestamp}] ${BLUE}[INFO]${NC}    ${msg}" ;;
        "SUCCESS") formatted_msg="[${timestamp}] ${GREEN}[SUCCESS]${NC} ${msg}" ;;
        "WARN")    formatted_msg="[${timestamp}] ${YELLOW}[WARN]${NC}    ${msg}" ;;
        "ERROR")   formatted_msg="[${timestamp}] ${RED}[ERROR]${NC}   ${msg}" ;;
        "DEBUG")   formatted_msg="[${timestamp}] ${PURPLE}[DEBUG]${NC}   ${msg}" ;;
        *)         formatted_msg="[${timestamp}] ${msg}" ;;
    esac

    echo -e "${formatted_msg}"
    echo -e "${formatted_msg}" | sed -r 's/\x1B\[[0-9;]*[a-zA-Z]//g' >> "$LOG_FILE"
}

log_cmd() {
    if [ "$DEBUG_MODE" = true ]; then
        log_msg "DEBUG" "Executing Command: ${PURPLE}$1${NC}"
    fi
}

# ----------------- 基礎功能模組 -----------------

get_service_tag() {
    local ip="$1"
    local cmd="racadm -r $ip -u $IDRAC_USER -p $IDRAC_PASS getsvctag"

    log_cmd "$cmd"
    local tag=$($cmd 2>/dev/null | tr -d '\r\n' | xargs)

    if [ -n "$tag" ]; then
        log_msg "SUCCESS" "Service Tag: [${tag}]"
        return 0
    else
        log_msg "ERROR"   "Failed to fetch Service Tag (Connection timeout or bad auth)"
        return 1
    fi
}

get_system_versions() {
    local ip="$1"
    local base_cmd="racadm -r $ip -u $IDRAC_USER -p $IDRAC_PASS"

    log_msg "INFO" "Fetching BIOS & Lifecycle Controller Version..."

    log_cmd "$base_cmd getsysinfo"
    local sysinfo=$($base_cmd getsysinfo 2>/dev/null)

    local bios_ver=$(echo "$sysinfo" | grep -i "BIOS Version" | awk -F'=' '{print $2}' | xargs)
    local lc_ver=$(echo "$sysinfo" | grep -i "Firmware Version" | head -n 1 | awk -F'=' '{print $2}' | xargs)

    if [ -n "$bios_ver" ] || [ -n "$lc_ver" ]; then
        log_msg "SUCCESS" "BIOS Version: [${bios_ver:-N/A}] | iDRAC/LC Version: [${lc_ver:-N/A}]"
        return 0
    else
        log_msg "WARN" "Failed to retrieve firmware version details."
        return 1
    fi
}

enable_ipmi_lan() {
    local ip="$1"
    local base_cmd="racadm -r $ip -u $IDRAC_USER -p $IDRAC_PASS"

    log_msg "INFO" "Enabling IPMI Over LAN & Privileges..."

    local cmd_set_new="$base_cmd set iDRAC.IPMILan.Enable 1"
    local cmd_set_old="$base_cmd config -g cfgIpmiLan -o cfgIpmiLanEnable 1"

    log_cmd "$cmd_set_new"
    $cmd_set_new &>/dev/null

    if [ $? -ne 0 ]; then
        log_msg "WARN" "New syntax failed, falling back to legacy config syntax..."
        log_cmd "$cmd_set_old"
        $cmd_set_old &>/dev/null
    fi

    if [ $? -ne 0 ]; then
        log_msg "ERROR" "Failed to enable IPMI Over LAN via RACADM"
        return 1
    fi

    local cmd_priv_new="$base_cmd set iDRAC.IPMILan.Privilege 4"
    local cmd_priv_old="$base_cmd config -g cfgIpmiLan -o cfgIpmiLanPrivilege 4"

    log_cmd "$cmd_priv_new"
    $cmd_priv_new &>/dev/null || { log_cmd "$cmd_priv_old"; $cmd_priv_old &>/dev/null; }

    log_msg "SUCCESS" "IPMI Over LAN enabled successfully"
    return 0
}

verify_ipmi_connection() {
    local ip="$1"
    local ipmi_cmd="ipmitool -I lanplus -H $ip -U $IDRAC_USER -P $IDRAC_PASS -R 1 -N 2 chassis power status"

    log_msg "INFO" "Testing IPMI connection with ipmitool..."
    log_cmd "$ipmi_cmd"

    local power_status=$($ipmi_cmd 2>/dev/null)

    if [ $? -eq 0 ]; then
        log_msg "SUCCESS" "ipmitool verified successfully -> (${power_status})"
        return 0
    else
        log_msg "WARN"    "ipmitool verification failed (Check Firewall UDP/623 or Credentials)"
        return 1
    fi
}

# ----------------- 高級作業模組 -----------------

idrac_info() {
    local ip="$1"
    if ! get_service_tag "$ip"; then
        log_msg "WARN" "Skipping remaining steps for ${ip} due to connection failure."
        return 1
    fi
    get_system_versions "$ip"

    if enable_ipmi_lan "$ip"; then
        verify_ipmi_connection "$ip"
    fi
}

clean_failed_jobs() {
    local ip="$1"
    local base_cmd="racadm -r $ip -u $IDRAC_USER -p $IDRAC_PASS"

    log_msg "INFO" "Cleaning failed jobs on $ip..."

    local failed_jobs=$($base_cmd jobqueue view 2>/dev/null | grep -B 2 "Status=Failed" | grep "Job ID" | awk -F'=' '{print $2}' | tr -d ']\r\n ' | xargs)

    if [ -n "$failed_jobs" ]; then
        for jid in $failed_jobs; do
            log_msg "WARN" "Deleting failed job: $jid"
            $base_cmd jobqueue delete -j "$jid" &>/dev/null
        done
        log_msg "SUCCESS" "Failed jobs cleaned successfully."
    else
        log_msg "INFO" "No failed jobs found."
    fi
}

check_and_mount_rfs() {
    local ip="$1"
    local base_cmd="racadm -r $ip -u $IDRAC_USER -p $IDRAC_PASS"
    local check_cmd="$base_cmd remoteimage -s"

    log_msg "INFO" "Checking Remote File Share (RFS) status..."
    log_cmd "$check_cmd"

    local rfs_status=$($check_cmd 2>/dev/null)
    local current_share=$(echo "$rfs_status" | grep -i "ShareName" | awk '{print $2}' | xargs)

    if [ -n "$current_share" ]; then
        log_msg "SUCCESS" "RFS already mounted -> [${current_share}]"
        return 0
    else
        log_msg "WARN" "No RFS ShareName found. Attempting to mount ISO: [${ISO_URL}]..."

        local mount_cmd="$base_cmd remoteimage -c -l ${ISO_URL}"
        log_cmd "$mount_cmd"
        $mount_cmd &>/dev/null

        local recheck_share=$($check_cmd 2>/dev/null | grep -i "ShareName" | awk '{print $2}' | xargs)
        if [ -n "$recheck_share" ]; then
            log_msg "SUCCESS" "RFS mounted successfully -> [${recheck_share}]"
            return 0
        else
            log_msg "ERROR" "Failed to mount RFS ISO on ${ip}"
            return 1
        fi
    fi
}

enable_html5_console() {
    local ip="$1"
    local base_cmd="racadm -r $ip -u $IDRAC_USER -p $IDRAC_PASS"

    log_msg "INFO" "Setting Virtual Console PluginType to HTML5 on $ip..."

    $base_cmd set iDRAC.VirtualConsole.Enable 1 &>/dev/null
    $base_cmd set iDRAC.VirtualConsole.PluginType HTML5 &>/dev/null
    if [ $? -ne 0 ]; then
        $base_cmd config -g cfgVirtualConsole -o cfgVirtualConsolePluginType 3 &>/dev/null
    fi

    local current_plugin=$($base_cmd get iDRAC.VirtualConsole.PluginType 2>/dev/null | grep -i "PluginType" | awk -F'=' '{print $2}' | xargs)
    log_msg "SUCCESS" "Virtual Console PluginType set to: [${current_plugin:-HTML5}]"
}

deploy_esxi() {
    local ip="$1"
    local base_cmd="racadm -r $ip -u $IDRAC_USER -p $IDRAC_PASS"

    log_msg "INFO" "Setting Boot Order to Virtual Optical / CD for $ip..."

    $base_cmd set iDRAC.ServerBoot.BootOnce 1 &>/dev/null
    $base_cmd set iDRAC.ServerBoot.FirstBootDevice VCD-DVD &>/dev/null

    if [ $? -eq 0 ]; then
        log_msg "SUCCESS" "Next boot device set to Virtual CD/DVD."
    else
        log_msg "ERROR" "Failed to set boot order."
        return 1
    fi

    log_msg "WARN" "Power cycling server [$ip] to begin ESXi Kickstart Installation..."
    $base_cmd serveraction powercycle &>/dev/null

    if [ $? -eq 0 ]; then
        log_msg "SUCCESS" "Server power cycle command sent successfully."
    else
        log_msg "ERROR" "Failed to send powercycle command."
        return 1
    fi
}
