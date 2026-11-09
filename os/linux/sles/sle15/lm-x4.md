# LM-X 4.x

## introduction

1. 創立與起源（2000年代中葉）

- **誕生背景**：隨著 FlexNet (FLEXlm) 的市場壟斷以及結構漸趨龐大複雜，許多中小型獨立軟體商（ISV）希望尋求更輕量、易於整合、費用更合理且維護成本更低的授權管理解決方案。
- **研發公司**：位於丹麥哥本哈根的 **X-Formation** 公司於 2004 年創立，並推出了 **LM-X License Manager**。

2. 發展脈絡與市場定位

- **針對痛點改革**：X-Formation 的創辦團隊針對 FLEXlm 的痛點（如複雜的 Vendor Daemon 配置、繁瑣的除錯程序、高昂的授權許可費用）進行全新設計。
- **軟體即服務與雲端轉型**：LM-X 率先推動從傳統「純本地授權伺服器」向「雲端授權（Cloud Licensing）」與「混合授權」的過渡，協助軟體開發商更容易實現訂閱制（Subscription）與按量計費（Pay-per-use）模式。

3. 技術特徵與現代優勢

- **單一進程與簡化部署**：LM-X 簡化了伺服器架構，通常只需單一伺服器進程即可運作，設定檔（XML/JSON 導向）與部署難度遠低於 FLEXlm。
- **廣泛的語言與平台支援**：原生提供對 C/C++、Java、.NET (C#)、Python、Go 等多種現代程式語言的 API 封裝，適合跨平台與 Web/Cloud 整合。
- **高強度安全防護**：LM-X 在設計初期就導入了現代密碼學（如 ECC 橢圓曲線加密與 AES），並針對二進位檔防篡改與逆向工程做了更強的防護設計。
- **Web UI 與監控**：LM-X 早期就整合了基於 Web 的直覺管理介面與統計分析工具，方便系統管理員即時查看授權使用率。

---

## install

```bash
sle15:~ # unzip LMXTools481_Linux64.zip -d /opt

# manual
sle15:~ # /opt/LMXTools481_Linux64/lmx-serv \
  -b \
  -l /opt/demo.lic \
  -c /opt/LMXTools481_Linux64/lmx-serv.cfg \
  -lf /var/log/lmx-serv.log
# -b: 背景執行（daemon 模式，依工具文件為準）
# -l: 指定 license 檔路徑（亦可改在 cfg 內設定）
# -c: 設定檔路徑
# -lf 日誌檔路徑
```

---

## config

`lmx-serv.cfg`

```conf
# lmx-serv.cfg
# 單一授權檔
LICENSE_FILE = /opt/lmx/licenses/demo.lic

# 或載入目錄內所有 .lic
# LICENSE_FILE = /opt/lmx/licenses/*.lic
```

---

## service

```bash
sle15:~ # vi /etc/systemd/system/lmx-serv.service

sle15:~ # systemctl daemon-reload
sle15:~ # systemctl enable lmx-serv
sle15:~ # systemctl start lmx-serv
sle15:~ # systemctl status lmx-serv
```

```ini
[Unit]
Description=LM-X License Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/LMXTools481_Linux64
ExecStart=/opt/LMXTools481_Linux64/lmx-serv -c /opt/LMXTools481_Linux64/lmx-serv.cfg -lf /var/log/lmx-serv.log
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
sle15:~ # firewall-cmd --permanent --add-port=6200/tcp
sle15:~ # firewall-cmd --reload
```

---

## other

```bash
sle15:~ # /opt/LMXTools481_Linux64/lmxendutil -hostid
sle15:~ # /opt/LMXTools481_Linux64/lmxendutil -licstat -host 127.0.0.1 -port 6200
```