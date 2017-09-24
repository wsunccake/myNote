# RabbitMQ

![rabbitmq](https://www.rabbitmq.com/img/RabbitMQ-logo.svg)

## Install

`method 1`

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


`method 2`

```
centos:~ # docker pull rabbitmq
centos:~ # docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq
centos:~ # docker exec -it rabbitmq rabbitmq-plugins enable rabbitmq_management
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

## Simple


![hello world](https://www.rabbitmq.com/img/tutorials/python-one-overall.png)

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

rabbitmq_server = 'localhost'
queue = 'hello'
message = 'Hello RabbitMQ!'

connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_server))
channel = connection.channel()

channel.queue_declare(queue=queue)

channel.basic_publish(exchange='',
                      routing_key=queue,
                      body=message)
print(" [x] Sent '{}'".format(message))
connection.close()

centos:~/py3/hello # vi send.py
```


### Consumer

```
# consumer/receiver
centos:~/py3/hello # vi receive.py
#!/usr/bin/env python
import pika

rabbitmq_server='localhost'
queue='hello'

connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_server))
channel = connection.channel()

channel.queue_declare(queue=queue)

def callback(ch, method, properties, body):
    print(" [x] Received {}".format(body))

channel.basic_consume(callback, queue=queue, no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

centos:~/py3/hello # python receive.py


centos:~/py3/hello # vi receive_one.py
#!/usr/bin/env python
import pika

rabbitmq_server='localhost'
queue='hello'

connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_server))
channel = connection.channel()

channel.queue_declare(queue=queue)

method_frame, header_frame, body = channel.basic_get(queue=queue)
if method_frame.NAME == 'Basic.GetEmpty':
    connection.close()
else:
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)
    connection.close()
    print(" [x] Received {}".format(body))

centos:~/py3/hello # vi receive_one.py
```


### Queue

```
centos:~/py3/hello # rabbitmqctl [-p <vhostpath>] list_queues
```


----

## Publish/Subscribe


![publish subscribe](https://www.rabbitmq.com/img/tutorials/bindings.png)



### Direct

```
centos:~/py3/direct # vi producer.py
import pika
import sys

user = 'guest'
password = 'guest'
host = 'localhost'
exchage = 'hello-exchage'
routing_key = 'hola'

credentials = pika.PlainCredentials(user, password)
connect_parameters = pika.ConnectionParameters(host,
                                               credentials=credentials)
connect_broker = pika.BlockingConnection(connect_parameters)

channel = connect_broker.channel()
channel.exchange_declare(exchange=exchage,
                         exchange_type='direct',
                         passive=False,
                         durable=True,
                         auto_delete=False)

message = sys.argv[1]
message_properties = pika.BasicProperties()
message_properties.content_type = 'text/plain'

channel.basic_publish(body=message,
                      exchange=exchage,
                      properties=message_properties,
                      routing_key=routing_key)

centos:~/py3/hello # vi consumer.py
import pika

user = 'guest'
password = 'guest'
host = 'localhost'
exchage = 'hello-exchage'
queue = 'hello-queue'
routing_key = 'hola'

credentials = pika.PlainCredentials(user, password)
connect_parameters = pika.ConnectionParameters(host,
                                               credentials=credentials)
connect_broker = pika.BlockingConnection(connect_parameters)

channel = connect_broker.channel()
channel.exchange_declare(exchange=exchage,
                         exchange_type='direct',
                         passive=False,
                         durable=True,
                         auto_delete=False)
channel.queue_declare(queue=queue)
channel.queue_bind(queue=queue,
                   exchange=exchage,
                   routing_key=routing_key)


def message_consumer(channel, method, header, body):
    channel.basic_ack(delivery_tag=method.delivery_tag)
    if body.decode('utf-8') == 'quit':
        channel.basic_cancel(consumer_tag='hello-consumer')
        channel.stop_consuming()
    else:
        print(body)

    return

channel.basic_consume(message_consumer, queue=queue, consumer_tag='hello-consumer')
channel.start_consuming()

centos:~/py3/hello # rabbitmqctl [-p <vhostpath>] list_exchages
centos:~/py3/hello # rabbitmqctl [-p <vhostpath>] list_queues
```


