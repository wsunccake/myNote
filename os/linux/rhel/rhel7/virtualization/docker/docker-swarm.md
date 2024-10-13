# Docker Swarm


## Config

```bash
# init manager
manager:~ # docker swarm init --advertise-addr <manage_node_ip>
manager:~ # docker swarm join-token worker    # show token for worker
manager:~ # docker swarm join-token manager   # show token for manager

# init worker
worker:~ # docker swarm join --token <token> <manage_node_ip>:2377
```

---

## Usage

```bash
# node/service status
manager:~ # docker node ls
manager:~ # docker service ls

# create service
manager:~ # docker service create --name cluster --constraint "node.role == worker" -p 80:80 russmckendrick/cluster
manager:~ # docker service scale cluster=4

# show detail service
manager:~ # docker service inspect cluster

# remove service
manager:~ # docker service rm cluster

# GUI
manager:~ # docker run -it -d -p 8080:8080 -e HOST=<manage_node_ip> -v /var/run/docker.sock:/var/run/docker.sock dockersamples/visualizer
```

