# terraform example

## docker

### alpine

```c
// main.tf
terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.2"
    }
  }
}

provider "docker" {
  host = "ssh://user@ip:port"
}

resource "docker_image" "alpine" {
  name = "alpine:latest"
}

resource "docker_container" "alpine" {
  name  = "alpine"
  image = docker_image.alpine.name

  // -t
  tty = true
}

  // -v
  volumes {
    host_path      = "/opt/workspace/app"
    container_path = "/workspace/app"
    read_only      = false
  }

  // -e
  env = [
    "APP_HOME=/workspace/app"
  ]

  // -w
  working_dir = "/workspace/app"
```

```bash
linux:~/tf $ terraform init
linux:~/tf $ terraform plan
linux:~/tf $ terraform apply -auto-approve
linux:~/tf $ terraform destroy -auto-approve
```

### alpine - variable

```c
// main.tf
terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.2"
    }
  }
}

variable "docker_host_address" {
  description = "The SSH address for the Docker provider, e.g., ssh://user@ip:port"
  type        = string
  default     = "ssh://user@localhost"
}

provider "docker" {
  host = var.docker_host_address
}

resource "docker_image" "alpine" {
  name = "alpine:latest"
}

resource "docker_container" "alpine" {
  name  = "alpine"
  image = docker_image.alpine.name

  // -t
  tty = true
}
```

```bash
# dev.tfvars
docker_host_address = "ssh://user@localhost"
```

```bash
linux:~/tf $ terraform init
linux:~/tf $ terraform plan
linux:~/tf $ terraform apply -auto-approve -var 'docker_host_address=ssh://user@localhost'      # 使用 var
linux:~/tf $ terraform apply -auto-approve -var-file=dev.tfvars                                 # 使用 var file
linux:~/tf $ terraform destroy -auto-approve [-target=docker_container.alpine]
```

### alpine - list

```c
// main.tf
terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.2"
    }
  }
}

variable "docker_host_list" {
  description = "The SSH address for the Docker provider, e.g., ssh://user@ip:port"
  type        = list(string)
  default     = ["ssh://user@localhost", "ssh://user@server"]
}

provider "docker" {
  alias = "host_0"
  host  = var.docker_host_list[0]
}

provider "docker" {
  alias = "host_1"
  host  = var.docker_host_list[1]
}

resource "docker_image" "alpine0" {
  provider = docker.host_0
  name = "alpine:latest"
}

resource "docker_image" "alpine1" {
  provider = docker.host_1
  name = "alpine:latest"
}

resource "docker_container" "alpine0" {
  provider = docker.host_0
  name = "alpine"
  image = docker_image.alpine0.name

  tty = true
}

resource "docker_container" "alpine1" {
  provider = docker.host_1
  name = "alpine"
  image = docker_image.alpine1.name

  tty = true
}
```

### alpine - map

```c
// main.tf
terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.2"
    }
  }
}

variable "docker_host_map" {
  description = "The SSH address for the Docker provider, e.g., ssh://user@ip:port"
  type        = map(string)
  default     = {
    host_0 = "ssh://user@localhost"
    host_1 = "ssh://user@server"
  }
}

provider "docker" {
  alias = "host_0"
  host  = var.docker_host_map["host_0"]
}

provider "docker" {
  alias = "host_1"
  host  = var.docker_host_map["host_1"]
}

resource "docker_image" "alpine0" {
  provider = docker.host_0
  name = "alpine:latest"
}

resource "docker_image" "alpine1" {
  provider = docker.host_1
  name = "alpine:latest"
}

resource "docker_container" "alpine0" {
  provider = docker.host_0
  name = "alpine"
  image = docker_image.alpine0.name

  tty = true
}

resource "docker_container" "alpine1" {
  provider = docker.host_1
  name = "alpine"
  image = docker_image.alpine1.name

  tty = true
}
```
