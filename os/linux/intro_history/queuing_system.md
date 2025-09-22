# queuing system

## history

佇列系統 (Queuing System) 在高效能運算 (HPC, High Performance Computing) 領域扮演著至關重要的角色, 負責管理和排程計算資源, 確保多個使用者提交的任務能夠有條不紊地執行.
從早期簡單的批次系統到現代功能豐富的資源管理器, 佇列系統的演進反映 HPC 需求的增長和技術的進步.

- IBM LoadLeveler
  時間: 可追溯至 1986 年
  說明: IBM 在 HPC 領域的作業排程器, LoadLeveler 的技術起源相當早. 根據其早期版本的文件版權資訊, 其開發可追溯至 1986 年. 主要在管理 IBM 大型機和叢集環境中的批次作業, 提供資源分配和作業排程功能.

- DQS (Distributed Queuing System)
  時間: 1990 年代初期 (具體年份較難精確考證, 但普遍認為是早期分散式佇列系統的代表)
  說明: 早期廣泛使用的分散式佇列系統之一, 為研究機構和大學提供了一種管理多個計算節點上任務的方式. 它實現了任務的分散式提交和執行, 為後來的更複雜系統奠定了基礎.

- PBS (Portable Batch System)
  時間: 1990 年代初期 (由 NASA Ames Research Center 開發)
  說明: PBS 是在 DQS 之後出現的一個里程碑式系統, 主要提供更強大的功能和更好的可移植性. 引入了作業腳本, 多個佇列和資源管理器等概念, 成為 HPC 領域的標準之一, 並衍生出多個版本, 如 OpenPBS 和 PBS Pro.

  - 作業腳本 (Job Scripts):允許使用者定義作業的資源需求（如 CPU 時間, 記憶體, 節點數量）和執行指令.
  - 佇列 (Queues):支援多個佇列, 每個佇列可以有不同的優先級和資源限制, 以滿足不同類型的作業需求.
  - 資源管理器 (Resource Manager):負責監控節點狀態和資源利用率, 以便更有效地調度作業.

- CODINE / GRD (Sun Grid Engine 的前身)
  時間: 1993 年 (由德國 Gridware 公司開發)
  說明: CODINE (Computing in Distributed Networked Environments) 和 GRD (Global Resource Director) 是 Sun Grid Engine 的核心技術來源. 它們在 1990 年代中期開始發展, 旨在提供網格計算環境下的資源管理和作業排程功能.

- OpenPBS
  時間: 1998 年
  說明: OpenPBS 是從 NASA 的 PBS 專案中衍生出來的開源版本. 它的發布使得 PBS 的技術能夠更廣泛地被社群使用和改進, 為後續的 TORQUE 等系統鋪平了道路.

- Sun Grid Engine (SGE)
  時間: 2000 年 (Sun Microsystems 收購 Gridware 後, 將 CODINE/GRD 重新命名並推廣)
  說明: 雖然其技術根源可追溯至 1993 年, 作為一個廣為人知的產品, Sun Grid Engine (SGE) 是在 Sun Microsystems 於 2000 年收購 Gridware 後才正式推出並開源 (2001 年). 它在當時的網格計算和叢集管理領域佔有重要地位.

- TORQUE (Terascale Open-source Resource and QUEue Manager)
  時間: 2000 年代初期 (從 OpenPBS 分支出來)
  說明: TORQUE 是從 OpenPBS 專案中分支出來的, 旨在提供一個更活躍維護和功能更豐富的開源解決方案. 它繼承了 PBS 的基本架構, 並在效能, 穩定性和可擴展性方面進行了改進.

- Slurm (Simple Linux Utility for Resource Management)
  時間: 2002-2003 年 (開始開發)
  說明: Slurm 是目前 HPC 領域最流行和廣泛使用的開源佇列系統之一. 它從零開始設計, 旨在提供高度可擴展, 容錯且功能豐富的資源管理和作業排程系統. Slurm 以其靈活的排程策略和強大的功能, 成為許多頂級超級電腦和 HPC 中心的標準配置.
  - 高度可擴展性:能夠管理從小型叢集到數十萬個核心的大型超級電腦.
  - 靈活的排程策略:支援多種排程演算法, 如優先級排程, 公平分享排程, 回填排程等, 以最大化資源利用率和滿足使用者需求.
  - 豐富的功能:提供精細的資源分配（如 CPU, 記憶體, GPU）, 作業依賴性, 陣列作業, 互動式作業等.
  - 模組化設計:易於擴展和整合第三方工具.
  - 強大的社群支援:擁有活躍的開發者社群和大量的使用者.
