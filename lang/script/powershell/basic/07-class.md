# class

## 1. PowerShell Class 的核心組成

一個標準的 Class 通常包含以下四個部分：

1. **Properties** (屬性)：定義物件存取的資料。
2. **Constructor** (建構子)：建立物件時執行的初始化動作。
3. **Methods** (方法)：物件可以執行的功能。
4. **Static** (靜態成員)：不需建立物件即可呼叫的功能。

---

2. 詳細範例

建立一個「員工」類別

```pwsh
class Employee {
    # 1. 屬性 (Properties)
    [string]$Name
    [string]$Role
    [datetime]$JoinDate
    hidden [int]$Salary  # 使用 hidden 關鍵字可以在預設顯示中隱藏

    # 2. 建構子 (Constructor) - 與類別同名
    Employee([string]$name, [string]$role, [int]$salary) {
        $this.Name = $name
        $this.Role = $role
        $this.Salary = $salary
        $this.JoinDate = Get-Date
    }

    # 3. 方法 (Methods)
    [string] GetSummary() {
        return "員工: $($this.Name), 職位: $($this.Role), 入職日期: $($this.JoinDate.ToShortDateString())"
    }

    # 4. 靜態方法 (Static Method) - 透過類別直接呼叫
    static [string] GetCompanyPolicy() {
        return "公司規定：準時上班，準時下班。"
    }
}

# 建立物件 (執行建構子)
$emp1 = [Employee]::new("Alice", "工程師", 80000)

# 呼叫實例方法
$emp1.GetSummary()

# 呼叫靜態方法
[Employee]::GetCompanyPolicy()
```

---

## 3. Class 的進階功能：繼承 (Inheritance)

PowerShell Class 支援單一繼承，子類別會繼承父類別的所有屬性與方法。

```pwsh
class Manager : Employee {
    [string[]]$TeamMembers

    # 子類別建構子，使用 base 呼叫父類別建構子
    Manager([string]$name, [int]$salary, [string[]]$team) : base($name, "經理", $salary) {
        $this.TeamMembers = $team
    }
}

$mgr = [Manager]::new("Bob", 120000, @("Alice", "Chris"))
$mgr.GetSummary() # 繼承自 Employee 的方法
```

---

## 4. Class vs. PSCustomObject

在 PowerShell 中，兩者都可以用來儲存結構化資料，但用途不同：

| Feature  | PSCustomObject                   | Class                    |
| -------- | -------------------------------- | ------------------------ |
| 結構     | 隨意定義（動態）                 | 嚴謹定義（靜態結構）     |
| 方法     | 較難定義 (需使用 ScriptProperty) | 直接定義，效能較佳       |
| 型別檢查 | 較弱                             | 強大，可作為參數型別限制 |
| 適用場景 | 快速產出資料、CSV 轉換           | 模組開發、大型腳本架構   |

| Keyword            | Explain                                                 |
| ------------------ | ------------------------------------------------------- |
| class              | 定義一個新的類別。                                      |
| $this              | 指向「當前物件實例」的自動變數。                        |
| [ClassName]::new() | 建立類別實例的標準方式。                                |
| static             | 定義屬於類別本身（而非物件）的方法或屬性。              |
| hidden             | 隱藏屬性，使其不顯示在 Get-Member 或預設輸出中。        |
| enum               | 定義「列舉」類型，常與 Class 搭配使用（例如定義狀態）。 |
