# tcpreplay

## install

```bash
apt install tcpreplay
```

---

## example

```bash
tcpreplay -i eth0 demo.pcap
```

---

## speed control parameter

- 模擬真實情境 ➡️ 不加參數（1:1 還原當初錄製的速度）。
- 想快點看結果 ➡️ -x 2.0 或 -x 5.0（快轉）。
- 資安設備效能壓力測試 ➡️ -t（極限全速狂轟）。
- 固定流量上限（避免塞車） ➡️ -M 50（限制 50 Mbps）或 -p 1000（每秒 1000 封包）。
- 分析特定封包失敗原因 ➡️ -o（手動逐發確認）。

核心規則是：這寫控制速度的模式是互斥的，只能擇一使用，不能同時指定。

1. `-p`, `--pps`=`str`（每秒發送封包數）

限定每秒鐘只發送固定數量的封包（Packets Per Second）。

```bash
tcpreplay -i eth0 --pps=1000 input.pcap
```

2. `-M`, `--mbps`=`str`（限定頻寬 Mbps）

限定回放時的網路總頻寬。tcpreplay 會自動計算封包大小並調整間隔，讓流量維持在指定的 Mbps。

```bash
tcpreplay -i eth0 --mbps=10 input.pcap
```

3. `-t`, `--topspeed`（全速回放）

無視原封包的時間戳記，以目前網卡和 CPU 的硬體極限速度，將封包瘋狂轟炸出去。常用於壓力測試（Stress Testing）。

```bash
tcpreplay -i eth0 -t input.pcap
```

4. `-x`, `--multiplier`=`str`（倍速回放）

照原本側錄封包時的相對時間間隔，進行「等比例放大或縮小」的速度調整。

- 2.0：2 倍速快轉（時間減半）。
- 0.5：0.5 倍速慢動作播放（時間加倍）。

```bash
tcpreplay -i eth0 -x 2.0 input.pcap
```

5. `-o`, `--oneatatime`（單步手動回放）

按一下發一個封包。每當 tcpreplay 準備發送下一個封包時，它會暫停並等待使用者在終端機按下 Enter 鍵 才會打出去。

```bash
tcpreplay -i eth0 -o input.pcap
```

---

## other parameter

`-l` `number`, `--loop`=`number`

該 PCAP 檔要重複播放幾次。

```bash
tcpreplay -i eth0 -l 5 input.pcap
tcpreplay -i eth0 -l 0 input.pcap
```
