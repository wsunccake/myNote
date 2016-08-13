

## Config 

/etc/ansible/ansible.cfg

ansible_python_interpreter = /usr/bin/python2


```
ansible-playbook site.yml -i hosts -e ENV_VARIABLE=env_value

ansible-playbook --list-tasks
ansible-playbook site.yml --start-at-task "my task"
```

```
linux:~ # cat hosts
[group1]
192.168.0.1 ansible_connection=ssh ansible_user=root ansible_ssh_pass=passwd ansible_become_pass=passwd

linux:~ # cat hello.yml

- hosts: all
  tasks:
    - shell: echo "hello world"

linux:~ # ansible-playbook hello.yml -i hosts
```