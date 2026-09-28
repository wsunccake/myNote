# Pipeline - var

在 Jenkins Pipeline 中，params.VAR、env.VAR 和直接寫 VAR（區域/全域變數）代表了完全不同的變數來源與作用域 (Scope)。

## 核心差異

- **params.VAR**
  - 來源: 觸發 Build 時傳入的參數 (Parameters)
  - 讀寫權限: 唯讀 (Read-Only)
  - 作用域 (Scope): 全局 (Pipeline 任何地方)
  - 跨 Job 傳遞: 需透過 build job 顯式傳遞

- **env.VAR**
  - 來源: 系統/Node 環境變數
  - 讀寫權限: 可讀可寫 (寫入會影響子程序)
  - 作用域 (Scope): 全局，或特定 environment 區塊/Node
  - 跨 Job 傳遞: 會自動繼承給該 Node 執行的 Shell/Batch

- **VAR**
  - 來源: Groovy 程式碼變數 (Script Variable)
  - 讀寫權限: 可讀可寫
  - 作用域 (Scope): 依據宣告方式（def 為局部，未宣告為全局）
  - 跨 Job 傳遞: 無法自動傳給子 Job 或 Shell

---

## params.VAR (Build 參數)

- 時機： 當變數是由外部觸發時決定（例如：使用者手動點選下拉選單、GitLab Webhook 帶入的參數、或是父 Job 帶入的參數）。
- 特性：
  - 必須在 parameters { ... } 區塊中定義。
  - 在整個 Pipeline 執行期間無法被程式碼修改（唯讀）。
- 範例：
  ```groovy
  pipeline {
      agent any
      parameters {
          string(name: 'DEPLOY_ENV', defaultValue: 'staging', description: '部署環境')
      }
      stages {
          stage('Deploy') {
              steps {
                  // 讀取傳入的參數
                  echo "Deploying to: ${params.DEPLOY_ENV}"
              }
          }
      }
  }
  ```

---

## env.VAR (環境變數)

- 時機：
  1. 需要呼叫外部 Script（如 sh 'echo $VAR' 或 bat）時，希望這變數能直接注入到 Shell 環境裡。
  2. 使用 Jenkins 內建的環境資訊（如 env.BUILD_NUMBER、env.NODE_NAME、env.JOB_NAME）。
- 特性：
  - 可以動態覆寫與新增（例如 env.MY_VERSION = '1.0.0'）。
  - 寫入 env 後，後續執行的所有 sh 或 bat 步驟都能直接用 $VAR 取用，無需另外傳參。
- 範例：
  ```groovy
  pipeline {
      agent any
      environment {
          // 全局環境變數
          APP_NAME = 'my-app'
      }
      stages {
          stage('Build') {
              environment {
                  // 僅在這個 stage 生效的環境變數
                  STAGE_SECRET = 'xyz123'
              }
              steps {
                  script {
                      // 動態修改/新增 env 變數
                      env.BUILD_DATE = new Date().format('yyyyMMdd')
                  }
                  // Shell 腳本可以直接讀取 env 變數
                  sh 'echo "Building ${APP_NAME} on ${BUILD_DATE} with secret ${STAGE_SECRET}"'
              }
          }
      }
  }
  ```

---

## 3. 直接寫 VAR 或 def VAR (Groovy 程式碼變數)

- 時機： 純粹在 Pipeline 邏輯中做運算、字串處理、流程控制（如 if/else、迴圈），不需要傳給 Shell 或其他 Job 的邏輯變數。
- 特性與 Scope 陷阱：
  - def VAR = 'foo'（局部變數）： 作用域僅限於當前區塊（例如某個 script 區塊或某個函數內）。
  - VAR = 'foo'（無 def 的 Pipeline 全局變數）： 綁定在 Groovy Binding，會在整個 Pipeline 任何角落都讀得到（但不建議濫用，容易造成變數污染）。
- 範例：

  ```groovy
  pipeline {
      agent any
      stages {
          stage('Process Data') {
              steps {
                  script {
                      // 局部變數 (推薦使用 def)
                      def isSuccess = true
                      def userList = ['Alice', 'Bob']

                      if (isSuccess) {
                          for (user in userList) {
                              echo "Processing ${user}"
                          }
                      }
                  }
              }
          }
      }
  }
  ```

---

💡 實務常犯錯誤與取用順序

1. 變數覆蓋的優先順序（Shadowing）

在 Pipeline 中直接引用 ${VAR} 時，Jenkins 的尋找順序為：

    1. Groovy 本地變數 (def VAR)
    2. 環境變數 (env.VAR)
    3. 參數 (params.VAR)

最佳實踐： 為了避免名稱衝突與混淆，永遠顯式加上字首！- 讀取參數寫 params.MY_VAR - 讀取環境變數寫 env.MY_VAR

2. Shell 腳本中的單引號與雙引號陷阱

- 雙引號 "..."（Groovy 插值）： 由 Jenkins 引擎在送到 Shell 前先把變數替換掉。

```groovy
sh "echo ${env.BUILD_NUMBER}" // Groovy 替換成 "echo 12" 後送給 Shell
```

- 單引號 '...'（原生 Shell 變數）： Groovy 不處理，直接由 Shell 讀取環境變數（僅對 env.VAR 有效）。

```groovy
sh 'echo $BUILD_NUMBER' // Shell 執行時自己印出環境變數
```

3. 跨 Job 傳參的正確寫法

需要把當前的變數傳給下一個 Job 時：

```groovy
build job: 'child-job', parameters: [
    // 1. 把自己的 params 轉傳給子 Job
    string(name: 'ENV_TYPE', value: params.DEPLOY_ENV),

    // 2. 把自己的 env 傳給子 Job
    string(name: 'BUILD_NODE', value: env.NODE_NAME),

    // 3. 把 Groovy 算好的 def 變數傳給子 Job
    string(name: 'CUSTOM_TAG', value: myLocalCalculatedTag)
]
```

---

## environment

在 Jenkins Pipeline 中，你在 environment 區塊定義的變數，其作用範圍（Scope）是全域（Global）的，而且它會自動注入到系統環境變數中。這意味著不論是在 sh、script 還是 Pipeline 的其他地方，都可以直接存取它。

```groovy
pipeline {
    agent {
        node {
            // 使用 Elvis 運算子做 Safe Fallback
            // 如果 params.NODE_LABEL 還是 null，自動退回使用 'built-in'
            label "${params.NODE_LABEL ?: 'built-in'}"
        }
    }

    parameters {
        string(name: 'NODE_LABEL', defaultValue: 'built-in', description: '指定執行的 Node Label')
        string(name: 'APP_HOME', defaultValue: '/var/jenkins_home/workspace/app', description: 'app 主目錄')
        string(name: 'WORK_DIR', defaultValue: '.', description: '工作目錄')
    }

    // 解決路徑互參問題：在 environment 裡面做動態字串組合
    environment {
        APP_HOME = "${params.APP_HOME}"
    }

    stages {
        stage('Test') {
            steps {
                sh 'echo "Running on node: ${NODE_NAME}"'
                sh 'echo "App home is: ${APP_HOME}"'
            }
        }
    }
}
```

**各個使用場景的存取方式**

1. 在 sh 步驟中使用（Shell 腳本）

這是在 sh 中最常用、也最容易混淆的部分。主要分為兩種寫法：

    A. 單引號 sh '...'（推薦：由 Linux 原生 Shell 讀取）

    因為變數已經注入到系統環境中，Linux Shell 可以直接透過 $APP_HOME 讀取它。

    ```groovy
    sh 'echo "App path is: $APP_HOME"'
    sh 'cd $ACX_ANSIBLE_HOME && ansible-playbook site.yml'
    ```

    B. 雙引號 sh "..."（由 Jenkins Groovy 引擎先解析替換）

    Groovy 會先將 ${env.APP_HOME} 替換成字串，再把組好的命令丟給 Linux 執行。

    ```groovy
    sh "echo \"App path is: ${env.APP_HOME}\""
    ```

2. 在 script { ... } 區塊中（Groovy 程式碼）

在 Groovy 程式碼區塊內，必須透過 env.變數名 來明確讀取這個環境變數：

```groovy
stage('Script Stage') {
    steps {
        script {
            // 正確：透過 env 讀取
            def myAppPath = env.APP_HOME
            echo "Path in groovy: ${myAppPath}"

            // 也可以在 Groovy 內做判斷
            if (env.APP_HOME.contains('app')) {
                echo "Path is valid!"
            }
        }
    }
}
```

3. 跨 Stage / 跨 步驟 的作用域

定義在 pipeline 最頂層的 environment 區塊：

    - 範圍： 涵蓋整個 Pipeline 中的每一個 Stage、每一個 Step。
    - 修改權限： 在 script 區塊內可以隨時覆寫它（例如 env.ACX_ANSIBLE_HOME = '/new/path'），之後執行的 sh 都會吃修改後的新值。
    - 💡 補充說明：限定 Stage 的作用域
        只希望變數在「某個特定 Stage」生效，可以把 environment 移到該 Stage 內部：
        ```groovy
        stage('App Run') {
            environment {
                // 這個變數只在這個 Stage 裡有效，離開 Stage 就自動失效
                STAGE_ONLY_VAR = "hello"
            }
            steps {
                sh 'echo $STAGE_ONLY_VAR'
            }
        }
        ```
