# robotframework 7.x - variables

### scalar variable `${}`

這是最基本的變數類型。它代表「單一物件」。儘管名字叫「標量」，但它不僅能存數字和字串，也能存儲清單、字典甚至複雜的 Python 物件實例。

特性：始終被視為一個整體的物件。

常用場景：存儲字串、整數、布林值，或將 List/Dict 作為一個完整的參數傳遞。

```robot
*** Variables ***
${NAME}         Gemini          # str
${AGE}          ${18}           # int
${IS_ACTIVE}    ${True}         # boolean
${FOLDER}       C:/Users/Temp

*** Test Cases ***
scalar variable demo
    Log    name: ${NAME}, age: ${${AGE} + 1}
    Should Be True    ${IS_ACTIVE}
```

---

## list variable `@{}`

List 變數用於存儲一系列按順序排列的值，類似 Python 的 list。

- ${list}：將清單當作「一個」參數（物件本身）。
- @{list}：將清單「打散」，裡面的每個元素都會變成一個獨立的參數。

```robot
*** Variables ***
@{FRUITS}       Apple    Banana    Cherry

*** Test Cases ***
list variable demo
    # 1. first element (index from 0)
    Log    ${FRUITS[0]}

    # 2. extend
    Log Many    @{FRUITS}

    # 3. for loop
    FOR    ${item}    IN    @{FRUITS}
        Log    fruit: ${item}
    END
```

---

## dictionary variable `&{}`

Dict 變數用於存儲鍵值對（Key-Value Pairs），類似 Python 的 dict。

- ${dict}：傳遞整個字典物件。
- &{dict}：將字典展開成「具名參數」（Named Arguments，例如 key=value）。

```robot
*** Variables ***
&{USER}         name=Vincent    email=vincent@example.com    role=Admin

*** Test Cases ***
dict variable demo
    # 1. access (recommend .)
    Log    name: ${USER.name}
    Log    email: ${USER['email']}

    # 2. extend
    Some Keyword With Arguments    &{USER}
```

| Symbol  | Type   | Python Type         | 主要用途         | 展開效果 (Expansion)                     |
| ------- | ------ | ------------------- | ---------------- | ---------------------------------------- |
| ${var}  | Scalar | any (str, int, obj) | 存儲單一值或物件 | 不展開，維持原樣                         |
| @{list} | List   | list                | 存儲多個有序資料 | 展開為多個獨立位置參數 (Positional Args) |
| &{dict} | Dict   | dict                | 存儲鍵值對       | 展開為多個具名參數 (Keyword/Named Args)  |

---

## advanced

1. List / Dict Assign Scalar：

將 List 或 Dict 賦值給 Scalar (${}) 是 Robot Framework 中非常重要的概念。不是在操作「一排變數」，而是操作「一個包含資料結構的 Python 物件」。把集合型態存入 ${} 時，它會保持其作為 Python list 或 dict 的原始特性，能夠使用點號（Dot notation）或內置方法來處理資料。

```robot
*** Test Cases ***
List to Scalar demo
    # Create List
    ${my_list}=    Create List    Apple    Banana    Cherry

    # 1. Access (Index)
    Log    Second Fruit: ${my_list[1]}

    # 2. Call Python List built-in
    ${count}=    Set Variable    ${{ len($my_list) }}
    Log    Len: ${count}

    # 3. Loop (Recommond)
    FOR    ${item}    IN    @{my_list}
        Log    Item: ${item}
    END

Dict to Scalar demo
    # Create Dict
    ${user_info}=    Create Dictionary    id=101    name=Vincent    role=Admin

    # 1. Access (Key, .)
    Log    Name: ${user_info.name}

    # 2. Access (Key, [])
    Log    Role: ${user_info['role']}

    # 3. Access (Key, .get)
    ${email}=    Set Variable    ${user_info.get('email', 'no mail')}
    Log    email: ${email}

    # 4. Loop (only key)
    FOR    ${key}    IN    @{$user_info}
        Log    key: ${key}
        Log    val: ${user_info['${key}']}
    END

    # 5. Loop (only value)
    FOR    ${val}    IN    @{$user_info.values()}
        Log    val: ${val}
    END

    # 6. Loop (both key & val)
    FOR    ${key}    ${value}    IN    @{user_info.items()}
        Log    key: ${key} -> val: ${value}
    END

    # 7. ${{ }}
    ${prices}=    Create Dictionary    apple=50    banana=20    cherry=100
    FOR    ${name}    ${price}    IN    @{ {k:v for k,v in $prices.items() if v > 30}.items() }
        Log    expansive: ${name} (price: ${price})
    END
```

| 優勢         | 說明                                                                                                             |
| ------------ | ---------------------------------------------------------------------------------------------------------------- |
| 結構化傳遞   | 你可以把一整組資料（例如用戶設定）封裝在一個 ${user} 變數裡，傳遞給各個關鍵字，而不是傳入一堆單獨的參數。        |
| 巢狀結構處理 | 當你的資料是「字典套清單」時（例如 {"users": ["A", "B"]}），使用 Scalar 才能輕易透過 ${data.users[0]} 存取內容。 |
| 效能與記憶體 | 在 Python 層面，這只是傳遞一個物件的參照（Reference），比展開成大量獨立變數更有效率。                            |

2. Object Mode (物件模式)：

在 `IF`、`WHILE`、`Evaluate` 語句中，直接使用 $ 開頭但不加 { }，RF 會將其視為一個完整的 Python 物件引用。

- traditional mode ${var}：RF 會先將變數「替換」成它的內容，再交給 Python 執行。這就像在 SQL 裡拼接字串，容易發生語法錯誤。
- object mode $var：直接把 Python 物件傳給判斷式。這就像在寫真正的 Python 代碼 if var:。

```
*** Test Cases ***
Boolean demo
    ${is_ready}=    Set Variable    ${True}

    # traditional mode
    IF    ${is_ready} == ${True}
        Log    system is ready
    END

    # object mode
    IF    $is_ready
        Log    system is ready
    END

None demo
    ${my_id}=       Set Variable    ${None}

    # traditional mode
    IF    "${my_id}" == "${None}"
        Log    ID is null
    END

    # object mode
    IF    not $my_id
        Log    ID is null
    END

Number compare
    ${count}=    Set Variable    ${10}

    # traditional mode
    IF    ${count} > 5 and ${count} <= 20
        Log    in range
    END

    # object mode
    IF    $count > 5 and $count <= 20
        Log    in range
    END

Object check
    ${user}=    Create Dictionary    name=Vincent    role=admin
    ${tags}=    Create List    smoke    regression

    # traditional mode
    ### 1. Dict check key
    IF    "${role}" == "admin"
        Log    Permission test
    END

    ### 2. List check len
    IF    "${user['role']}" == "admin"
        Log    Permission test
    END

    # object mode
    ### 1. Dict check key
    IF    $user.get('role') == 'admin'
        Log    Permission test
    END

    ### 2. List check len
    IF    len($tags) > 0 and 'smoke' in $tags
        Log    Smoking test
    END
```

| 需求       | 傳統模式 (容易報錯)              | 物件模式 (推薦)                   |
| ---------- | -------------------------------- | --------------------------------- |
| 判斷 None  | `IF "${var}" == "${None}"`       | `IF $var is None` (或 `not $var`) |
| 字串包含   | `IF "admin" in "${role}"`        | `IF "admin" in $role`             |
| 複雜運算   | `IF ${val} \* 2 > 10`            | `IF $val \* 2 > 10`               |
| 邏輯組合   | `IF "${a}"=="1" and "${b}"=="2"` | `IF $a == 1 and $b == 2`          |
| 底層處理   | 先把變數變成字串 "None"          | 直接傳遞 Python 的 None 物件      |
| 判斷式寫法 | `IF "${val}" == "None"`          | IF $val is None                   |
| 出錯率     | 高（常漏掉引號或型態出錯）       | 低（原生 Python 邏輯）            |
| 效能       | 略慢（多了字串轉換步驟）         | 快（直接操作記憶體物件）          |

3. Inline Python Evaluation `${{ }}`：

核心意義是在雙花括號內部的所有內容，都會被當作純 Python 程式碼執行。不需要呼叫 Evaluate 關鍵字，就能在變數賦值、參數傳遞甚至 IF 判斷中直接進行複雜的邏輯運算。

- 語法：`${{ python_expression }}`
- 運作：RF 會將括號內的表達式交給 Python 的 `eval()` 執行，並將結果回傳給 RF 變數。
- 變數引用：在 `${{ }}` 內部，建議直接使用 $var 來引用 RF 變數，這樣它會以 Python 物件的形式參與運算，避免字串轉義問題。

```robot
*** Variables ***
${WIDTH}    10
${HEIGHT}   20
${RAW_STR}    /user/bin/python/
@{NUMBERS}    ${1}    ${5}    ${12}    ${8}    ${20}


*** Test Cases ***
Calcuate and Type Convert
    # Calcuate
    ${area}=    Set Variable    ${{ $WIDTH * $HEIGHT }}

    # Type Convert
    ${average}=    Set Variable    ${{ round(($WIDTH + $HEIGHT) / 2, 1) }}
    Log    area: ${area}, avg: ${average}

String and Formatting
    # strip and upper
    ${clean_str}=    Set Variable    ${{ $RAW_STR.strip('/').upper() }}

    # f-string (Python 3.6+)
    ${info}=         Set Variable    ${{ f"Path is: {$clean_str}" }}
    Log    ${info}

List and Dict Comprehension
    ${large_nums}=    Set Variable    ${{ [n for n in $NUMBERS if n > 10] }}

    ${id_map}=        Set Variable    ${{ {f"id_{n}": n for n in $NUMBERS} }}
    Log    large number: ${large_nums}

Conditional Expression
    ${score}=    Set Variable    ${85}
    # Syntax：[true] if [condition] else [false]
    ${result}=    Set Variable    ${{ "Pass" if $score >= 60 else "Failed" }}
    Log    Result: ${result}
```

| 特性       | `${{ expression }}`      | `Evaluate`                          |
| ---------- | ------------------------ | ----------------------------------- |
| 語法簡潔度 | 極高，可嵌入任何地方     | 較長，需獨立一行                    |
| 適用場景   | 簡單運算、屬性存取、賦值 | 需要匯入複雜 Library 或執行多行代碼 |
| 變數引用   | 直接用 `$var`            | 常用 `${var}` (易出錯)              |

- 模組：如果要在內聯 Python 中使用 math 或 random，需要使用 `__import__`。
- 範例：`${random_int}=  Set Variable  ${{ __import__('random').randint(1, 10) }}`
- 效能：雖然方便，但在一個 Test Case 中過度使用極其複雜的內聯 Python 會降低可讀性。如果邏輯超過一行，建議寫成真正的 Python Library。
- 安全：不要在 `${{ }}` 中執行來自外部不可信的輸入，因為它具有執行任意 Python 代碼的能力。
