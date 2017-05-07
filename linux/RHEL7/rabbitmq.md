# RabbitMQ

![rabbitmq](https://www.rabbitmq.com/img/RabbitMQ-logo.svg)

## Install


```
# install package
centos:~ # yum install erlang
centos:~ # rpm --import http://www.rabbitmq.com/rabbitmq-signing-key-public.asc
centos:~ # yum install https://www.rabbitmq.com/releases/rabbitmq-server/v3.6.9/rabbitmq-server-3.6.9-1.el7.noarch.rpm

# start service
centos:~ # systemctl start rabbitmq-server
centos:~ # systemctl enable rabbitmq-server

# install plugin
centos:~ # rabbitmq-plugins enable rabbitmq_management
centos:~ # curl http://localhost:15672

# port
centos:~ # netstat -lutnp | grep -E '4369|5671|5672'
```


----

## Operation

```
# manage system
centos:~ # rabbitmqctl start
centos:~ # rabbitmqctl start_app
centos:~ # rabbitmqctl stop
centos:~ # rabbitmqctl stop_app
centos:~ # rabbitmqctl status
centos:~ # rabbitmqctl reset
centos:~ # rabbitmqctl force_reset

# manage user
centos:~ # rabbitmqctl list_users                              # show users
centos:~ # rabbitmqctl add_user <username> <password>          # create user
centos:~ # rabbitmqctl delete_user <username>                  # delete user
centos:~ # rabbitmqctl change_password <username> <password>   # change password
centos:~ # rabbitmqctl clear_password <username>               # clean password

# manage permission
centos:~ # rabbitmqctl list_permissions
centos:~ # rabbitmqctl list_user_permissions <username>
centos:~ # rabbitmqctl set_permissions [-p <vhostpath>] {user} {conf} {write} {read}
centos:~ # rabbitmqctl clear_permissions [-p <vhostpath>] <username>

centos:~ # rabbitmqctl set_user_tags <username> administrator

# manage vhost
centos:~ # rabbitmqctl list_vhosts
centos:~ # rabbitmqctl add_vhost <vhostpath>
centos:~ # rabbitmqctl delete_vhost <vhostpath>

# other
centos:~ # rabbitmqctl list_parameters
centos:~ # rabbitmqctl list_global_parameters
```


----

## Configure

```
centos:~ # vi /etc/rabbitmq/rabbitmq.config
[
 {rabbit,
  [
   {tcp_listeners, [5672]},
%%   {loopback_users, [<<"guest">>]}   %% 把 <<"guest">> 拿掉, guest 即可從外面登入 
   {loopback_users, []}
  ]
 }
].
```


----

## Hello

```
centos:~ # pip3 install virtualenv
centos:~ # virtualenv --python=python3 py3
centos:~ # cd py3
centos:~/py3 # source bin/active
centos:~/py3 # pip install pika
centos:~/py3 # mkdir hello
centos:~/py3 # cd hello
```


### Producer

```
# producer/sender
centos:~/py3/hello # vi send.py
#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()

centos:~/py3/hello # vi send.py
```


### Consumer

```
# consumer/receiver
centos:~/py3/hello # vi receive.py
#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()


channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

centos:~/py3/hello # python receive.py
```


### Queue

```
centos:~/py3/hello # rabbitmqctl [-p <vhostpath>] list_queues
```

