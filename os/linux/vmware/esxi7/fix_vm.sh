#!/bin/sh




###
### env var
###

MAX_CPU=24
MAX_RAM=49152
MAX_DISK_SIZE=600G
CPU=${CPU:=$MAX_CPU}
RAM=${RAM:=$MAX_RAM}
DISK_SIZE=${DISK_SIZE:=$MAX_DISK_SIZE}

NET0=${NET0:=Br192}
MAC0=${MAC0:=00:50:56:01:00:01}
NET1=${NET1:=BrCluster}
MAC1=${MAC1:=00:50:56:02:00:01}
NET2=${NET2:=VM Network}
MAC2=${MAC2:=00:50:56:03:00:01}

###
### func
###

get_vm_info() {
    local vm_name=$1
    local vm_info=$(vim-cmd vmsvc/getallvms | awk -v vm=$vm_name '($2 == vm){print $_}')
    if [ -z "$vm_info" ]; then
        echo "no found VM: $vm_name"
        exit 1
    fi

    export VM_ID=$(echo "$vm_info" | awk '{print $1}')
    export DS_NAME=$(echo "$vm_info" | awk '{print $3}' | sed -e 's/\[//' -e 's/\]//')
    local vmx_rel=$(echo "$vm_info" | awk '{print $4}')
    export VMX_FILE="/vmfs/volumes/$DS_NAME/$vmx_rel"

    echo "VM_ID: $VM_ID"
    echo "VMX_FILE: $VMX_FILE"
    echo "DS_NAME: $DS_NAME"
}

power_off_vm() {
    local vm_id=$1    

    echo "power off: $vm_id"
    local state=$(vim-cmd vmsvc/power.getstate $vm_id | tail -1)
    if [ "$state" != "Powered off" ]; then
        vim-cmd vmsvc/power.off $vm_id > /dev/null
        sleep 2
    fi
}

adjust_max_resource() {
    cp $VMX_FILE $VMX_FILE.org

    adjust_cpu_ram $VMX_FILE
    adjust_disk
}

adjust_cpu_ram() {
    local vmx_file=$1
    local keys="numvcpus memsize"

    echo "adjust cpu & ram"
    for key in $keys; do
        awk -v key=$key 'tolower($0) !~ /key/ && tolower($0) !~ /key/' "$vmx_file" > "$vmx_file.tmp" && mv "$vmx_file.tmp" "$vmx_file"
        sed -i "/$key/d" "$vmx_file"
    done

    sed -i "1i memsize = \"$RAM\"" "$vmx_file"
    sed -i "1i numvcpus = \"$CPU\"" "$vmx_file"
}

adjust_nic() {
    local vmx_file=$1
    local keys="ethernet0.addressType ethernet0.address ethernet0.networkName
ethernet1.addressType ethernet1.address ethernet1.networkName
ethernet2.addressType ethernet2.address ethernet2.networkName"

    echo "adjust nic"
    for key in $keys; do
        awk -v key=$key 'tolower($0) !~ /key/ && tolower($0) !~ /key/' "$vmx_file" > "$vmx_file.tmp" && mv "$vmx_file.tmp" "$vmx_file"
        sed -i "/$key/d" "$vmx_file"
    done

    sed -i "1i ethernet2.networkName = \"$NET2\"" "$vmx_file"
    sed -i "1i ethernet2.address = \"$MAC2\"" "$vmx_file"
    sed -i "1i ethernet2.addressType = \"static\"" "$vmx_file"
    sed -i "1i ethernet1.networkName = \"$NET1\"" "$vmx_file"
    sed -i "1i ethernet1.address = \"$MAC1\"" "$vmx_file"
    sed -i "1i ethernet1.addressType = \"static\"" "$vmx_file"
    sed -i "1i ethernet0.networkName = \"$NET0\"" "$vmx_file"
    sed -i "1i ethernet0.address = \"$MAC0\"" "$vmx_file"
    sed -i "1i ethernet0.addressType = \"static\"" "$vmx_file"
}

adjust_disk() {
    local vmx_file=$1
    local vmdk_dir=$(dirname $vmx_file)
    local vmdk_name=$(awk -F\" '/scsi0:0.fileName/{print $2}' $vmx_file)
    local vmdk_path="${vmdk_dir}/${vmdk_name}$"

    echo "adjust disk"
    vmkfstools -X $DISK_SIZE $vmdk_file
}

reload_config() {
    local vm_id=$1
    local vmx_file=$2

    echo "reload config"
    vim-cmd vmsvc/reload $vm_id

    echo "unregister vm: $vm_id"
    vim-cmd vmsvc/unregister $vm_id

    echo "register vm: $vmx_file"
    vm_id=$(vim-cmd solo/registervm $vmx_file)
}

power_on_vm() {
    echo "power on: $vm_id"
    vim-cmd vmsvc/power.on $vm_id
}

help() {
    echo "Usage: $0 <VM_NAME>"
    echo
    echo "export CPU=$CPU"
    echo "export RAM=$RAM"
    echo "export DISK_SIZE=$DISK_SIZE"
    echo "env MAX_FLAG=1 $0 <VM_NAME>"
    echo
    echo "export NET0=$NET0"
    echo "export MAC0=$MAC0"
    echo "export NET1=$NET1"
    echo "export MAC1=$MAC1"
    echo "export NET2=$NET2"
    echo "export MAC2=$MAC2"
    echo "env NIC_FLAG=1 $0 <VM_NAME>"
}

###
### main
###

if [ "$#" == "0" ]; then
    help
    exit 1
fi

VM_NAME=$1
get_vm_info $VM_NAME
power_off_vm $VM_ID

if [ "x$MAX_FLAG" == "x1"];
    adjust_max_resource
fi

if [ "x$NIC_FLAG" == "x1"];
    adjust_nic $VMX_FILE
fi

reload_config $VM_ID $VMX_FILE
