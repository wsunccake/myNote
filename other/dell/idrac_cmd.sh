#!/bin/bash
# ==============================================================================
# Script Name: idrac_cmd.sh
# Description: Main Entrypoint for Batch iDRAC operations
# Usage:       ./idrac_cmd.sh {info|clean|mount|html5|deploy|all}
# ==============================================================================

# 定義 Function 檔路徑
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FUNC_FILE="${SCRIPT_DIR}/idrac_functions.sh"

# 檢查並載入 Functions 檔案
if [ -f "$FUNC_FILE" ]; then
    source "$FUNC_FILE"
else
    echo "Error: Function file '${FUNC_FILE}' not found!"
    exit 1
fi

act="$1"

if [ -z "$act" ]; then
    echo "Usage: $0 {info|clean|mount|html5|deploy|all}"
    echo "  info   : Query Service Tag, Firmware versions & Enable IPMI"
    echo "  clean  : Clean failed jobs in job queue"
    echo "  mount  : Check and mount RFS ISO"
    echo "  html5  : Enable HTML5 Virtual Console"
    echo "  deploy : Set Virtual Optical BootOnce and Powercycle server"
    echo "  all    : Execute all tasks sequentially"
    exit 1
fi

if [ ! -f "$IP_LIST" ]; then
    log_msg "ERROR" "IP list file '$IP_LIST' not found!"
    exit 1
fi

grep -Ev '^#|^$' "$IP_LIST" | while read -r IDRAC_IP; do
    echo "========================================================================"
    log_msg "INFO" "Target Host: [${IDRAC_IP}]"

    case "$act" in
        "info")
            idrac_info "$IDRAC_IP"
            ;;
        "clean")
            clean_failed_jobs "$IDRAC_IP"
            ;;
        "mount")
            check_and_mount_rfs "$IDRAC_IP"
            ;;
        "html5")
            enable_html5_console "$IDRAC_IP"
            ;;
        "deploy")
            deploy_esxi "$IDRAC_IP"
            ;;
        "all")
            idrac_info "$IDRAC_IP" || continue
            clean_failed_jobs "$IDRAC_IP"
            check_and_mount_rfs "$IDRAC_IP"
            enable_html5_console "$IDRAC_IP"
            deploy_esxi "$IDRAC_IP"
            ;;
        *)
            log_msg "ERROR" "Unknown action: '$act'. Valid options: info, clean, mount, html5, deploy, all."
            exit 1
            ;;
    esac
done
