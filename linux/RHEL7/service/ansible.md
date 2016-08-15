# Ansible

有分 Control Machine 和 Managed Node

----


## Install

method 1. yum

```
control:~ # yum localinstall http://dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-5.noarch.rpm
control:~ # yum update
control:~ # yum install ansible
```

method 2. pip

```
control: ~ # pip install --upgrade pip
control: ~ # pip install ansible
```


## Test

```
control:~ # cat playbooks/hosts
[test_node]
node1 ansible_connection=ssh ansible_ssh_host=192.168.0.11 ansible_ssh_port=22 ansible_ssh_user=root ansible_ssh_pass=password ansible_become_pass=password
node2 ansible_connection=ssh ansible_ssh_host=192.168.0.12 ansible_ssh_port=22 ansible_ssh_user=root ansible_ssh_private_key_file=private_file

control:~ # ansible test_node -i hosts -m ping  -vvv
control:~ # ansible node1 -i hosts -m command -s -a uptime
```
-i: host file
-m: moudle
-a: argument
-s: sudo root

----


## Config 

ansible 設定檔讀取順序

1. ANSIBLE_CONFIG 環境變數

2. ./ansible.cfg 當前路徑下檔案

3. ~/.ansible.cfg 個別使用者家目錄檔案

4. /etc/ansible/ansible.cfg 系統預設檔案

```
control:~ # cat /etc/ansible/ansible.cfg
[defaults]
ansible_python_interpreter = /usr/bin/python2
nocows = 1
```

----

## PlayBook

PlayBook 是 YAML 格式, yaml 其實可以轉成對應的 json, 範例如下

```
yml/yaml
---
- hosts: all
  tasks:
    - name: Hello World
      shell: echo "hello world"

    - name: Show Hostname
      shell: hostname


json
[
  {
     host: "all"
  },
  {
     tasks: [
              {
                 name: "Hello World",
                 shell: "echo \"hello world\""
              },
              {
                 name: "Show Hostname",
                 shell: "hostname"
              }
            ]
  }
]
```

---, 表示 yaml 檔案的開頭, 可以省略

-, 表示 list

:, 表示 dict

#, 表示註解

>, 換行


簡單的 ansible-playbook 測試如下

```
control:~ # cat playbooks/hello.yml
---
- hosts: all
  sudo: True
  tasks:
    - name: Hello World
      shell: echo "hello world"

control:~ # ansible-playbook hello.yml -i hosts
```

一個 playbook 內容需要有 host 和 task 組成






ansible-playbook site.yml -i hosts -e ENV_VARIABLE=env_value
ansible-playbook --list-tasks
ansible-playbook site.yml --start-at-task "my task"
