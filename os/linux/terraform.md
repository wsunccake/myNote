# terraform

## install

```bash
linux:~ # curl -LO https://releases.hashicorp.com/terraform/1.12.2/terraform_1.12.2_linux_amd64.zip
linux:~ # unzip terraform_1.12.2_linux_amd64.zip
linux:~ # mv terraform /usr/local/bin
```

## comamnd

```bash
linux:~/tf $ terraform init
linux:~/tf $ terraform plan
linux:~/tf $ terraform apply -auto-approve [-destroy]
linux:~/tf $ terraform destroy -auto-approve

linux:~/tf $ terraform show
linux:~/tf $ terraform state list
linux:~/tf $ terraform state show <resource>

linux:~/tf $ terraform fmt
linux:~/tf $ terraform validate
```

---

## content

- provider

  使用哪個平台

```conf
provider "docker" {}
```

- resource

  建立實體資源

```conf
resource "資源類型" "資源名稱" {
  參數 = 值
}
```

- data

  查詢現有的資源，不會建立新資源

```conf
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
}
```

- variable

  變數

```conf
variable "region" {
  type    = string
  default = "ap-northeast-1"
}

provider "aws" {
  region = var.region
}
```

- output

  輸出

```conf
output "instance_ip" {
  value = aws_instance.web.public_ip
}
```

- locals

  區域變數

```conf
locals {
  default_name = "demo-app"
}

name = local.default_name
```

- 條件運算與迴圈

```conf
instance_type = var.env == "prod" ? "t3.medium" : "t2.micro"

resource "aws_instance" "app" {
  for_each = toset(["a", "b", "c"])
  ami           = "ami-abc123"
  instance_type = "t2.micro"
  tags = {
    Name = "app-${each.key}"
  }
}
```

---

## provider

### docker

```bash
linux:~ # dnf install docker-ce   # rhel / fedora
linux:~ # apt install docker-ce   # debian / ubuntu
linux:~ # zypper in docker        # sle / opensuse
```

```conf
# main.tf
terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.2"
    }
  }
}

provider "docker" {}

resource "docker_image" "nginx" {
  name = "nginx:latest"
}

resource "docker_container" "nginx" {
  name  = "nginx_container"
  image = docker_image.nginx.name

  ports {
    internal = 80
    external = 8080
  }
}
```

---

### kvm

```bash
linux:~ # dnf install qemu-kvm libvirt
linux:~ # apt install libvirt-daemon libvirt-daemon-system libvirt-clients

linux:~ # curl -LO https://download.cirros-cloud.net/0.6.3/cirros-0.6.3-x86_64-disk.img
linux:~ # mv cirros-0.6.3-x86_64-disk.img cirros.img
```

```conf
# main.tf
terraform {
  required_providers {
    libvirt = {
      source  = "dmacvicar/libvirt"
      version = "0.7.1"
    }
  }
}

provider "libvirt" {
  uri = "qemu:///system"
}

resource "libvirt_volume" "cirros" {
  name   = "cirros.qcow2"
  pool   = "default"
  source = "${path.module}/cirros.img"
  format = "qcow2"
#  provisioner "local-exec" {
#    command = "sudo chown libvirt-qemu:libvirt-qemu ${libvirt_volume.cirros.id}"
#  }
}

resource "libvirt_domain" "cirros_vm" {
  name   = "cirros-vm"
  memory = 128
  vcpu   = 1

  disk {
    volume_id = libvirt_volume.cirros.id
  }

  network_interface {
    network_name = "default"
#    bridge = "mybrdige"
  }

  console {
    type        = "pty"
    target_type = "serial"
    target_port = "0"
  }

  graphics {
    type        = "vnc"
    listen_type = "address"
    autoport    = true
  }

  boot_device {
    dev = ["hd"]
  }
}

output "vm_ip_address" {
  value = libvirt_domain.cirros_vm.network_interface[0].addresses[0]
}
```

### esxi

download [Open Virtualization Format (OVF) Tool](https://developer.broadcom.com/tools/open-virtualization-format-ovf-tool/latest)

```bash
linux:~ # unzip -d /usr/local VMware-ovftool-xxx-lin.x86_64.zip
linux:~ # ln -s /usr/local/ovftool/ovftool /usr/local/bin/
```

```conf
# main.tf
terraform {
  required_providers {
    esxi = {
      source  = "josenk/esxi"
      version = "~> 1.10.3"
    }
  }
}

provider "esxi" {
  esxi_hostname = "192.168.100.1"
  esxi_username = "root"
  esxi_password = "password"
}

resource "esxi_guest" "test_vm" {
  guest_name = "testvm"
  ovf_source = "test.ova"

  disk_store = "datastore1"
  numvcpus   = 1
  memsize    = 2048
  power      = "off"

  network_interfaces {
    virtual_network = "VM Network"
  }
}
```

### vsphere

### openstack

---

## variable

```bash
linux:~/docker_hello $ tree
.
├── main.tf
├── outputs.tf
└── variables.tf

linux:~/docker_hello $ terraform apply -auto-approve -var 'container_name=web' -var 'host_port=8888'
```

```conf
# variables.tf
variable "container_name" {
  description = "Name of the container"
  type        = string
}

variable "host_port" {
  description = "Port to expose container"
  type        = number
}

variable "image_name" {
  description = "Docker image to use"
  type        = string
  default     = "nginx:alpine"
}
```

```conf
# main.tf
terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "3.6.2"
    }
  }
}

resource "docker_image" "nginx" {
  name         = var.image_name
  keep_locally = false
}

resource "docker_container" "web" {
  name  = var.container_name
  image = docker_image.nginx.name
  ports {
    internal = 80
    external = var.host_port
  }

  provisioner "local-exec" {
    command = <<EOT
echo '<h1>Hello from ${var.container_name}</h1>' > ./index.html
docker cp ./index.html ${self.name}:/usr/share/nginx/html/index.html
rm ./index.html
EOT
  }
}
```

```conf
# outputs.tf
output "web_container_name" {
  value = docker_container.web.name
}
```

---

## module

```bash
linux:~/ex_mod $ cp -r ~/docker_hello modules/.

linux:~/ex_mod $ tree
.
├── main.tf
└── modules
    └── docker_hello
        ├── main.tf
        ├── outputs.tf
        └── variables.tf

linux:~/ex_mod $ terraform apply -auto-approve
```

```conf
# main.tf
module "hello_web_1" {
  source         = "./modules/docker_hello"
  container_name = "hello-1"
  host_port      = 8080
}

module "hello_web_2" {
  source         = "./modules/docker_hello"
  container_name = "hello-2"
  host_port      = 8081
}

output "web1_container_name" {
  value = module.hello_web_1.web_container_name
}

output "web2_container_name" {
  value = module.hello_web_2.web_container_name
}
```
