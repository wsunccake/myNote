# terraform

## Provisioning & Configuration

### `Provisioning` (佈建)

Provisioning 指的是創建和管理基礎設施的生命週期，從無到有地建立資源。這就像是你在蓋房子，先要準備好土地、打地基、建構主體結構、拉好水電管線。

- 核心概念

  - 目標：從零開始建立所需的硬體和軟體環境。
  - 範例：創建一台雲端虛擬機（EC2）、設定虛擬網路（VPC）、建立一個資料庫實例（RDS）、或是配置一個負載平衡器。
  - 工具類型：通常被稱為 Infrastructure as Code (IaC) 工具。它們使用宣告式 (Declarative) 的方式，讓你描述你想要的最終狀態，工具會自動計算出要執行的步驟來達到這個狀態。

- 主要工具

  - `Terraform`: 最廣泛使用的 IaC 工具之一，支援多種雲端服務商（AWS, GCP, Azure 等）。
  - `CloudFormation`: 亞馬遜 AWS 官方的佈建工具。
  - `Pulumi`: 類似 Terraform，但允許你使用主流程式語言（如 Python, JavaScript, Go）來定義基礎設施。

- 使用情境

  - 新專案啟動: 當你需要為一個新專案從頭建立完整的雲端環境時。
  - 環境複製: 快速複製一個現有的生產環境到測試或開發環境。
  - 自動化 CI/CD: 在持續整合/持續部署（CI/CD）流程中，自動創建測試環境。
  - 資源管理: 追蹤、更新和銷毀不再需要的基礎設施資源。

### `Configuration` (配置)

Configuration 指的是在已存在的基礎設施上進行設定和調整。這就像是房子蓋好之後，你要進行內部裝潢，安裝電器、擺放家具、設定網路和安全系統。

- 核心概念

  - 目標：在已佈建好的伺服器上，安裝軟體、設定服務、部署應用程式、管理用戶權限等。
  - 範例：在一台虛擬機上安裝 Nginx 伺服器、設定防火牆規則、部署一個 Web 應用程式的程式碼，或是確保所有服務都在正確啟動。
  - 工具類型：通常被稱為 配置管理 (Configuration Management) 工具。它們可以支援程序式 (Procedural) 或宣告式的方式，定義一系列要執行的動作。

- 主要工具

  - `Ansible`: 無代理程式（agentless）的配置管理工具，透過 SSH 連接，語法簡單易學。
  - `Chef`: 採用主從式架構（client-server），需在目標機器上安裝代理程式。
  - `Puppet`: 也是主從式架構，擅長處理大規模的配置任務。

- 使用情境

  - 應用程式部署: 將最新的應用程式版本部署到多台伺服器上。
  - 伺服器環境初始化: 在新佈建的伺服器上，進行基礎環境的設定，例如安裝 Docker、設定系統參數。
  - 環境一致性管理: 確保所有伺服器的配置都符合預期，避免配置漂移（Configuration Drift）。
  - 服務啟動與管理: 啟動、停止或重啟伺服器上的特定服務。

| 特性     | Provisioning (佈建)                | Configuration (配置)                     |
| -------- | ---------------------------------- | ---------------------------------------- |
| 工作階段 | 前置：在資源不存在時執行           | 後置：在資源已存在時執行                 |
| 主要對象 | 基礎設施：虛擬機、網路、資料庫     | 作業系統與應用程式                       |
| 處理方式 | 宣告式，關注最終狀態               | 程序式或宣告式，關注執行的步驟           |
| 優勢     | 創建、更新、銷毀資源精準、多雲支援 | 靈活、擅長處理應用層面的設定、無代理程式 |
| 常見工具 | Terraform, CloudFormation          | Ansible, Chef, Puppet                    |

---

## Terraform vs Ansible

Terraform 和 Ansible 雖然都屬於自動化工具，但它們在核心目的、運作方式和擅長領域上有著根本性的差異。簡單來說，你可以把它們想像成建築工程中的兩種不同角色：

- Terraform 就像是建築師：負責規劃和建造房子的「基礎建設」，例如地基、樑柱、牆壁、電力系統等。它專注於 基礎設施的佈建 (Infrastructure Provisioning)。

- Ansible 則像是裝潢師：負責在房子蓋好後，進行內部的「配置」，例如安裝電器、擺放家具、佈置燈光。它專注於 配置管理 (Configuration Management)。

### `Terraform` State 概念

在 `Provisioning` 工具（如 Terraform）的世界裡，State 是其核心功能。

- 什麼是 State？
  - Terraform 會在執行後產生一個 terraform.tfstate 檔案。
  - 這檔案記錄 Terraform 實際在雲端上所創建的所有資源（例如 EC2 ID、VPC 名稱、S3 Bucket URL 等）及其當前的配置狀態。
  - 將它視為一個真實世界的資源地圖。
- 為什麼 State 很重要？
  - 精準追蹤：Terraform 透過比較你當前的程式碼（.tf 檔案）與 State 檔案中的記錄，來精確判斷「實際環境」和「期望環境」之間的差異。
  - 計畫性變更：當執行 terraform plan 時，它會告訴「要達到你程式碼所描述的狀態，我需要新增、修改或刪除哪些資源」。這個能力是基於 State 檔案的。
  - 防止重複創建：有了 State，Terraform 知道哪些資源已經存在，避免了重複創建同樣的資源。

### `Ansible` State 概念

在 `Configuration` 工具（如 Ansible）的世界裡，原生並沒有類似 Terraform 這樣集中的 State 管理機制。

- Ansible 如何工作？
  - Ansible 的 Playbook（YAML 檔案）是一系列要執行的指令。
  - 當執行 Playbook 時，它會按照你定義的步驟依序在目標機器上執行。
  - 它會執行一個操作，然後檢查該操作是否成功。它沒有一個集中的檔案來記錄「已經設定了什麼，現在的配置是什麼樣子」。
- 為什麼沒有 State？
  - Ansible 的主要目的是確保目標機器上的配置符合預期。雖然它有冪等性 (Idempotence) 的特性（重複執行 Playbook 會確保結果一致，但不會重複執行不必要的動作），但它並沒有一個外部的檔案來追蹤整個基礎設施的狀態。
  - Ansible 更像是一個無狀態的執行引擎，它執行任務，然後就完成了，不會留下一個全局的狀態檔案。

| 特性       | Terraform (Provisioning)                       | Ansible (Configuration)                  |
| ---------- | ---------------------------------------------- | ---------------------------------------- |
| State 記錄 | 有，透過 terraform.tfstate 檔案管理。          | 無，沒有內建的集中式狀態管理。           |
| 工作方式   | 透過 State 檔案來比較並同步程式碼與實際資源。  | 執行一系列指令來達到預期狀態。           |
| 核心優勢   | 精確管理資源的生命週期，追蹤創建、更新與刪除。 | 靈活地配置已存在的資源，且無需代理程式。 |
| 關注點     | 資源的「存在」與「不存在」。                   | 資源上的「設定」與「配置」。             |

---

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

## step

1. Initialization: `terraform init`

1.1 下載 Provider:

Terraform 讀取配置檔案 (.tf)，確定所需 Provider (例如 aws, azurerm, google) 及其版本限制。從 Terraform Registry 下載這些 Provider 的二進制執行檔。快取檢查： 如果設定了快取目錄 (透過 `TF_PLUGIN_CACHE_DIR` 或 `plugin_cache_dir`)，Terraform 會先檢查本地快取。如果存在且版本匹配，則直接從快取中複製；否則才從網路下載。

`TF_PLUGIN_CACHE_DIR`

```bash
linux:~ $ export TF_PLUGIN_CACHE_DIR="$HOME/.terraform.d/plugin-cache"
```

```bash
linux:~ $ vi .terraformrc
plugin_cache_dir="$HOME/.terraform.d/plugin-cache"
```

1.2 安裝 Provider

下載的 Provider 執行檔會被放置在當前工作目錄的 .terraform/providers 子目錄中。 Terraform 執行時會尋找 Provider 的位置。

1.3 後端 Backend

如果定義了後端 (例如 S3, Azure Blob)，Terraform 會初始化後端並檢查 State 檔案。

2. Configuration: `Provider {} Block`

2.1 讀取配置

Terraform 讀取 provider "name" { ... } 區塊中的參數 (例如 AWS 的 region, access_key 或 Google 的 project 等)。

2.2 Provider 啟動

Terraform 執行安裝的 Provider 二進制檔案，並將這些配置參數傳遞給 Provider。

2.3 建立連線

Provider 使用這些參數建立與目標雲端平台 (例如 AWS API) 的連線、驗證身分並準備好接收後續的操作指令。

3. Execution: `terraform plan/apply`

3.1 資源發現 (Plan)

Terraform 讀取配置檔案中的資源定義 (resource "type" "name" { ... })。對於每個資源，Terraform 會呼叫對應的 Provider 的方法 (例如 Read, Create)
Plan： 呼叫 Read 方法獲取目標平台目前狀態，並與 State 檔案進行比較，以決定要執行哪些操作。
Apply： 呼叫 Create, Update, 或 Delete 方法。

3.2 API 互動

Provider 接收到 Terraform 的指令後，將其轉換為對應雲端平台的 API 呼叫，執行實際的資源操作。

3.3 狀態管理 (State Update)

資源操作完成後，Provider 將資源的最新狀態資訊 (如 ID, 屬性值) 傳回給 Terraform。Terraform 將這些最新資訊寫入 State 檔案 (terraform.tfstate)，完成一個閉環操作。

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

linux:~/docker_hello $ terraform init
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

linux:~/ex_mod $ terraform init
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

---

## workspaces

```bash
linux:~/ex_ws $ cp -r ~/docker_hello/* .

linux:~/ex_ws $ tree
.
├── main.tf
├── outputs.tf
└── variables.tf

linux:~/ex_ws $ vi main.tf

linux:~/ex_ws $ terraform init

linux:~/ex_ws $ terraform workspace list
linux:~/ex_ws $ terraform workspace new stage
linux:~/ex_ws $ terraform apply -var 'container_name=web' -var 'host_port=8080' -auto-approve
linux:~/ex_ws $ terraform workspace new prod
linux:~/ex_ws $ terraform apply -var 'container_name=web' -var 'host_port=80' -auto-approve
linux:~/ex_ws $ terraform workspace select stage
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
  name  = "${var.container_name}-${terraform.workspace}"
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

---

## environment-based folder

```bash
linux:~/ex_env $ cp -r ~/docker_hello modules/.

linux:~/ex_env $ tree
.
├── modules
│   └── docker_hello
│       ├── main.tf
│       ├── outputs.tf
│       └── variables.tf
├── prod
│   └── main.tf
└── stage
    └── main.tf

linux:~/ex_mod/prod $ terraform init
linux:~/ex_mod/prod $ terraform apply -auto-approve

linux:~/ex_mod/stage $ terraform init
linux:~/ex_mod/stage $ terraform apply -auto-approve
```

```conf
# prod/main.tf
module "hello_web" {
  source         = "../modules/docker_hello"
  container_name = "prod hello"
  host_port      = 80
}

output "web_container_name" {
  value = module.hello_web.web_container_name
}
```

```conf
# stage/main.tf
module "hello_web" {
  source         = "../modules/docker_hello"
  container_name = "stage hello"
  host_port      = 8080
}

output "web_container_name" {
  value = module.hello_web.web_container_name
}
```

---

## loop

```conf
# for - list
variable "vm_names" {
  type    = list(string)
  default = ["my-app-logs", "my-app-backups", "my-app-assets"]
}

output "vm_with_prefix" {
  value = [for name in var.vm_names : "project-x-${name}"]
}

# for - map
variable "instance_types" {
  type = map(string)
  default = {
    "web"  = "t2.micro"
    "db"   = "t2.small"
    "cache" = "t2.nano"
  }
}

output "instance_details" {
  value = { for app, type in var.instance_types : "${app}_instance" => "Type: ${type}" }
}

# for - range
variable "vm_count" {
  type    = number
  default = 3
}

output "vm_names_and_ids" {
  value = { for i in range(var.vm_count) : "vm_${i}" => "id_${i}" }
}
```

- 字串內插 (docker.${each.key})
- 函數計算 (docker[element(keys(...))])
- 條件表達式 (count.index == 0 ? docker.host_0 : docker.host_1)

---

## condition
