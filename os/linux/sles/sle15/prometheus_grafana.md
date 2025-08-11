# prometheus & grafana

## concept

`Prometheus` 是一個開源的監控系統，專為可靠性而設計。它主要負責：

- 資料收集 (Scraping)：Prometheus 會定期從配置的目標（通常是運行在 HPC 節點上的 Exporter）中拉取 (pull) 指標資料。這些 Exporter 將系統的各項指標（例如 CPU 使用率、記憶體、網路 I/O、磁碟空間、GPU 使用率、Slurm 作業狀態等）轉換為 Prometheus 格式。
- 時間序列資料儲存 (TSDB)：收集到的資料以時間序列的形式儲存在其內建的時序資料庫中。
- 查詢語言 (PromQL)：Prometheus 提供強大的查詢語言 PromQL，可以用來對收集到的指標進行複雜的查詢、聚合和分析。
- 警報 (Alerting)：Prometheus 可以根據預定義的規則評估指標，並在達到閾值時觸發警報，例如發送到 Alertmanager。

在 HPC 環境中，Prometheus 通常部署在專用的監控節點上，並配置為從所有計算節點、登入節點、儲存系統甚至排程系統 (如 Slurm) 中的 Exporter 拉取資料。

`Grafana` 是一個開源的數據視覺化和儀表板工具，它與 Prometheus 完美結合，提供：

- 資料視覺化：Grafana 能夠連接多種數據源，包括 Prometheus，並將其查詢結果以豐富多樣的圖表、表格和統計數字的形式呈現。
- 儀表板 (Dashboards)：使用者可以建立高度可自訂的儀表板，將多個指標視覺化，以便一目瞭然地掌握 HPC 叢集的運行狀況。這對於快速識別瓶頸、異常或資源利用率低下等問題至關重要。
- 警報通知：雖然 Prometheus 可以觸發警報，但 Grafana 也可以配置警報規則，並透過各種通知通道（如 Slack、Email、PagerDuty 等）發送通知。
- 使用者介面：提供直觀的 Web 介面，方便使用者查詢資料、建立儀表板和管理設定。

在 HPC 環境中，Grafana 通常也部署在監控節點上，作為所有監控數據的統一視覺化入口。

`HPC` 監控架構

1. 監控節點 (Monitor Node)：

   - 運行 Prometheus Server：負責資料收集、儲存和查詢。
   - 運行 Grafana Server：提供視覺化儀表板和警報。
   - 可選：運行 Alertmanager 處理來自 Prometheus 的警報。

2. 計算節點 (Compute Nodes)：

   - 每個計算節點都運行一個或多個 Exporter，例如：
   - Node Exporter：收集基本的作業系統和硬體指標 (CPU、記憶體、磁碟 I/O、網路)。
   - NVIDIA DCGM Exporter：收集 GPU 相關指標 (GPU 利用率、記憶體使用率、溫度等)。
   - Slurm Exporter：收集 Slurm 排程系統的指標，如作業狀態、節點分配、隊列資訊等。
   - Lustre Exporter / BeeGFS Exporter：監控並行檔案系統的效能指標。
   - 自定義 Exporter：針對特定的應用或服務（如 MPI 進程、HPC 應用程式的內部指標）編寫自定義的 Exporter。

3. 儲存系統 (Storage System)：

   - 如果使用外部儲存，可能會在其上運行專門的 Exporter 來收集儲存效能指標。

4. 網路設備 (Network Devices)：

   - 可選：使用 SNMP Exporter 等來監控網路設備。

---

## prometheus

```bash
# install package
prometheus:~ # zypper in golang-github-prometheus-prometheus

# config file
prometheus:~ # vi /etc/prometheus/prometheus.yml
global:
  scrape_interval:     15s # By default, scrape targets every 15 seconds.
  evaluation_interval: 15s # By default, scrape targets every 15 seconds.
  external_labels:
      monitor: 'example'
rule_files:
scrape_configs:
  - job_name: 'prometheus'
    scrape_interval: 5s
    scrape_timeout: 5s
    static_configs:
      - targets: ['localhost:9090']
  - job_name: node
    static_configs:
      - targets: ['localhost:9100']

# service
prometheus:~ # systemctl enable prometheus --now

# data storage
prometheus:~ # ls /var/lib/prometheus

# parameter
prometheus:~ # prometheus \
  --config.file=/etc/prometheus/prometheus.yml \
  --storage.tsdb.path=/var/lib/prometheus
  [--storage.tsdb.retention.time=1y]
  [--storage.tsdb.retention.size=50GB]
# --config.file: 設定檔路徑
# --storage.tsdb.path: TSDB 的儲存目錄
# --storage.tsdb.retention.time: 保留資料的時間長度
# --storage.tsdb.retention.size: 資料庫的最大磁碟使用量
```

```bash
# test
prometheus:~ # curl <prometheus>:9090/config
```

---

## grafana

```bash
# install package
grafana:~ # zypper in grafana

# config
grafana:~ # ls /etc/grafana

# service
grafana:~ # systemctl enable grafana-server --now
```

```bash
# test
grafana:~ # curl <grafana>:3000/login
```

- 預設使用者帳號密碼
  default account and password: admin/admin

- 新增資料來源
  Connections -> Data Source -> +Add new data source
  選用 prometheus 並輸入 http://<prometheus>:9090

- 新增儀表板
  Import Dashboard ->
  ID: 1860 for node exporter
  ID: 4323 for slurm exporter
  ID: 19835 for slurm exporter

---

## exporter

### slurm exporter

```bash
# install package
exporter:~ # zypper in golang-github-vpenso-prometheus_slurm_exporter

# service
exporter:~ # systemctl enable prometheus-slurm_exporter --now

# test
exporter:~ # curl <exporter>:8080/metrics
```

```bash
prometheus:~ # vi /etc/prometheus/prometheus.yml
  - job_name: slurm-exporter
     scrape_interval: 30s
     scrape_timeout: 30s
     static_configs:
       - targets: ['MGMTSERVER:8080']
```

### node exporter

```bash
# install package
exporter:~ # zypper in golang-github-prometheus-node_exporter

# service
exporter:~ # systemctl enable prometheus-node_exporter --now

# test
exporter:~ # curl <exporter>:9100/metrics
```

```bash
prometheus:~ # vi /etc/prometheus/prometheus.yml
  - job_name: node-exporter
    static_configs:
      - targets: ['<EXPORTER NODE1>:9100']
      - targets: ['<EXPORTER NODE2>:9100']

prometheus:~ # systemctl restart prometheus
```
