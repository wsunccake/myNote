# Pipeline Architecture / 管道式架構

在軟體工程中，Pipeline Architecture（管道式架構），也常被稱為 Pipes and Filters（管道與過濾器） 模式。這種架構的核心思想是將一個複雜的處理過程分解為一系列離散、獨立的處理步驟（Filters），數據透過管道（Pipes）在這些步驟之間流動。

1. 核心組件 (Core Components)

管道式架構由兩個基本元素組成：

- 過濾器 (Filter)：
  - 負責具體的邏輯運算。
  - 無狀態性：理想情況下，過濾器不依賴其他過濾器的狀態。
  - 單一職責：每個過濾器只做一件事（如：數據清洗、格式轉換、加密）。

- 管道 (Pipe)：
  - 連通過濾器的通道。
  - 負責將上一個過濾器的 輸出 (Output) 傳遞給下一個過濾器的 輸入 (Input)。
  - 它可以是簡單的內存緩衝區，也可以是複雜的訊息隊列（Message Queue）。

2. 管道式架構的優缺點

| 優點                                                       | 缺點                                                            |
| ---------------------------------------------------------- | --------------------------------------------------------------- |
| 高解耦性：過濾器之間互相獨立，可以輕易替換或移除某個步驟。 | 效能開銷：數據在管道間傳遞（序列化/反序列化）可能產生額外負擔。 |
| 可重用性：同一個過濾器可以放在不同的管道中重複使用。       | 複雜度限制：不適合需要頻繁「回頭」或複雜狀態共享的邏輯。        |
| 支持併行：不同的過濾器可以在不同的執行緒或機器上運行。     | 錯誤處理困難：若管道中間發生異常，清理狀態或回滾相對複雜。      |
| 易於測試：每個過濾器都可以針對輸入輸出進行獨立單元測試。   | 數據格式限制：所有過濾器必須對傳輸的數據協議達成共識。          |

3. 在 Python 中的實作方式

在 Python 中，我們通常結合 函數式編程 與 生成器 (Generator) 來實現高效的管道架構，這樣可以避免一次性加載大量數據到內存中。

假設我們要從大量日誌中篩選出 ERROR 級別的訊息並加上時間戳記。

```python
def read_logs(file_path):
    """Filter 1: 讀取文件"""
    with open(file_path, 'r') as f:
        for line in f:
            yield line.strip()

def filter_errors(lines):
    """Filter 2: 篩選錯誤"""
    for line in lines:
        if "ERROR" in line:
            yield line

def add_timestamp(lines):
    """Filter 3: 增加處理標記"""
    import datetime
    for line in lines:
        yield f"[{datetime.datetime.now()}] {line}"

# 建立管道 (The Pipe)
log_pipeline = add_timestamp(filter_errors(read_logs("test_report.log")))

# 執行管道
for entry in log_pipeline:
    print(entry)
```