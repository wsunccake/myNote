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


## Ad-Hoc

```
control:~ # cat playbooks/hosts
[test_node]
node1 ansible_connection=ssh ansible_ssh_host=192.168.0.11 ansible_ssh_port=22 ansible_ssh_user=root ansible_ssh_pass=password ansible_become_pass=password
node2 ansible_connection=ssh ansible_ssh_host=192.168.0.12 ansible_ssh_port=22 ansible_ssh_user=root ansible_ssh_private_key_file=private_file

# 已指令模式執行 ansible 稱為 Ad-Hoc
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

\#, 表示註解

\>, 換行


簡單的 ansible-playbook 測試如下

```
control:~/playbooks # cat ansible.cfg
[defaults]
hostfile = hosts
host_key_checking = False

control:~/playbooks # cat hello.yml
---
- hosts: all
  gather_facts: False
  tasks:
    - name: Hello World
      shell: echo "hello world"

control:~/playbooks # ansible-playbook hello.yml  # 執行 playbook

# ansible module help
control:~ # ansible-doc -l      # 顯示所有 action module
control:~ # ansible-doc shell

# playbook task
control:~/playbooks # ansible-playbook --list-tasks
control:~/playbooks # ansible-playbook site.yml --start-at-task "Hello World"
```

一個 playbook 內容需要有 host 和 task 組成. task 內除了 name 之外, 皆由 action module 組成.

```
# 使用變數的方式
control:~/playbooks # cat say_hello.yml
---
- hosts: all
  gather_facts: False
  vars_files:
    - user_vars.yml
  vars:
    user: abc
  tasks:
    - name: Hello World
      shell: echo "hello {{ user }}"

control:~/playbooks # cat user_vars.yml
---
user: zzz

control:~/playbooks/ # ansible-playbook -e 'user=xyz' say_hello.yml

control:~/playbooks # cat ext_vars.yml
user: ijk

control:~/playbooks/ # ansible-playbook -e '@ext_vars.yml' say_hello.yml
```

範例 [docker_install.yml](./docker_install.yml)

```
control:~/project # tree
.
├── ansible.cfg
├── roles
│   └── docker
│       ├── files
│       │   └── ca.crt
│       ├── handlers
│       │   └── main.yml
│       ├── tasks
│       │   └── main.yml
│       └── vars
│           └── main.yml
├── site.yml
└── staging

control:~/project # cat ansible.cfg 
[defaults]
hostfile = staging
host_key_checking = False

control:~/project # staging 
192.168.0.10 ansible_ssh_user=root ansible_ssh_pass=password ansible_become_pass=password

control:~/project # cat site.yml 
---
- hosts: all
  become: yes
  become_method: su
  roles:
    - docker

control:~/project # cat roles/docker/vars/main.yml 
---
os_distro: CentOS
os_version: 7
docker_bip: 10.253.0.1/24
private_registry: registry
private_dns: 192.168.0.1

control:~/project # cat roles/docker/tasks/main.yml 
---
- fail: 
    msg: OS don't support
  when:
    - ansible_distribution != '{{ os_distro }}'
    - ansible_distribution_major_version != '{{ os_version }}'

- yum:
    name: epel-release
    state: installed

- yum:
    name: docker
    state: installed

- replace: 
    dest: /etc/sysconfig/docker
    regexp: OPTIONS=.*
    replace: OPTIONS="--selinux-enabled --log-driver=journald --signature-verification=false --bip={{ docker_bip }}"
    backup: yes
  notify:
    - restart service

- yum:
    name: python2-pip
    state: installed

- pip:
    name: docker-compose
    state: present

- file:
    path: /etc/docker/certs.d/{{ private_registry }}:5000
    state: directory
    backup: no

- copy:
    src: ca.crt
    dest: /etc/docker/certs.d/{{ private_registry }}:5000
    owner: root
    group: root
    mode: 0644
    backup: yes

- lineinfile:
    dest: /etc/resolv.conf
    state: absent
    regexp: '^nameserver\s+{{ private_dns }}$'

- shell: sed -i 1a'nameserver {{ private_dns }}' /etc/resolv.conf

control:~/project # cat roles/docker/handlers/main.yml 
---
- name: restart service
  service: 
    name: docker
    state: restarted
    enabled: yes
```
----

## Inventory
