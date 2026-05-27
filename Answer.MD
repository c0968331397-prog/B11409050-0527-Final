# 台科大資管 Python 考試作答區

---

## 基本資料

**學號：** B11409050  
**系級：** 資管系大一  
**姓名：** 李諺明  

---

## 一、 原始碼分析報告 (Static Analysis) (共8小題，每小題3分，總共24分)

### 1.1 變數與邏輯對照表

| 原始變數名稱 | 代表意義 (Business Logic) | 建議修正名稱 |
|---|---|---|
| Q1 l1 (in load_proc) | 從檔案讀取的所有原始文字行列表，每個元素代表一本書的資料字串 | `file_lines` |
| Q2 d2 (in main) | 全域的書籍資料清單（記憶體中的圖書館資料庫），每個元素是一本書的字典 | `book_list` |
| Q3 c_res (in check) | 檢查某個 ISBN 是否已存在於資料庫中的函式，回傳 True/False | `is_isbn_exists` |

### 1.2 壞味道 (Code Smells) 診斷

請列出原程式碼中至少 5 個嚴重的設計問題，並說明為什麼不好：

- **Q1：** 變數與字典鍵命名不具意義（`l1`, `d2`, `c_res`, `t`, `i`, `s`）——讀者無法從名稱理解其用途，維護時需要逐行追蹤才能推測意義，大幅增加理解成本。

- **Q2：** 使用自訂分隔符號 `@@` 和 `##` 儲存資料——若書名或 ISBN 本身包含這些字串，解析會直接出錯；且此格式非標準，無法使用現有工具（如 `json`、`csv`）讀取，未來難以整合或遷移。

- **Q3：** `d2` 是全域可變變數（Global Mutable State）——函式與主程式共用同一份資料，任何函式都能在不明確傳參的情況下修改它，導致程式難以測試、難以追蹤資料流，也無法支援多實例執行。

- **Q4：** 完全沒有錯誤處理（No Error Handling）——若 `lib_data.txt` 內容格式損毀（例如缺少 `@@` 或 `##`），`split` 後索引超出範圍會直接讓程式崩潰，且不會給出任何有意義的錯誤訊息。

- **Q5：** `borrow` 指令在找不到 ISBN 時靜默失敗（Silent Failure）——使用者輸入一個不存在的 ISBN，程式不回應任何錯誤，讓使用者誤以為操作成功，這會造成難以發現的資料問題。

- **Q6（加分）：** 使用裸露的 `open()` 而非 `with` 語法開啟檔案——若程式在寫入過程中異常中斷，檔案不會被正確關閉，可能導致資料遺失或檔案損毀。

---

## 二、 Vibe-Coding 協作紀錄 (共6小題，每小題3分，總共18分)

請記錄你如何引導 GitHub Copilot 進行重構。
重構的要求，請根據題目卷以及你發現的 Code Smells 來進行。

### 2.1 關鍵 Prompt 紀錄

請貼出你對 AI 下達過最有效的 3 個 Prompt：

```log
Prompt A：
請分析 legacy_lib.py 這段圖書館管理程式碼，找出所有變數的真實業務意義，
並列出至少 5 個 Code Smells，說明每個問題為何會造成維護困難。

Prompt B：
請依照 Clean Code 原則，將 legacy_lib.py 重構為 modern_library.py。
要求：(1) 使用 class LibraryManager 封裝所有邏輯，
(2) 以 JSON 格式取代原本的 @@ ## 分隔格式儲存資料，
(3) 所有檔案操作加上 try-except 錯誤處理，
(4) 程式結束時才一次寫入檔案，不要每次 add 都寫入磁碟，
(5) 所有變數與方法使用有意義的英文命名。

Prompt C：
borrow 指令在 ISBN 不存在時沒有回傳任何錯誤訊息，請修正這個 Silent Failure 問題，
並在 add 指令中加入對輸入格式的驗證（書名不可為空、ISBN 只能包含數字）。
```

### 2.2 AI 錯誤處理

1. AI 在撰寫過程中是否有出錯？（例如：漏寫了某個功能、語法錯誤）你是如何發現並請它修正的？

2. 發現的問題： AI 最初將 `save_to_file()` 放在每次 `add_book()` 內部呼叫，仍然重複了原本低效率寫入磁碟的問題，而不是只在程式結束時才儲存。

3. 修正的對話： 我告訴它「請移除 add_book 內的 save_to_file 呼叫，改成只在 run() 的 exit 分支與程式正常結束時呼叫一次，模擬 in-memory 操作直到退出才持久化」。

---

## 三、 成果驗證與測試  (共2小題，每小題10分，總共20分)

確保你的 `modern_library.py` 功能正確。

### 3.1 測試結果驗證 (Terminal)

請貼上執行程式並輸入 show 後，顯示資料清單。(請從呼叫執行程式到結束程式完整的把操作對話複製到下框)

```log
=== 圖書館管理系統 v1.0 ===
指令：add <書名>/<ISBN>/<狀態> | show | borrow <ISBN> | exit
> add 深入淺出Python/978001/available
[成功] 已新增書籍：深入淺出Python (ISBN: 978001)
> add 資料結構理論/978002/available
[成功] 已新增書籍：資料結構理論 (ISBN: 978002)
> add 演算法實作/978003/available
[成功] 已新增書籍：演算法實作 (ISBN: 978003)
> add 重複測試書/978001/available
[錯誤] ISBN 978001 已存在，無法重複新增。
> borrow 978002
[成功] 書籍 ISBN 978002 狀態已更新為「borrowed」。
> show
--- 書籍清單（共 3 筆）---
[1] 書名: 深入淺出Python       | ISBN: 978001 | 狀態: available
[2] 書名: 資料結構理論           | ISBN: 978002 | 狀態: borrowed
[3] 書名: 演算法實作            | ISBN: 978003 | 狀態: available
> exit
[系統] 資料已儲存，系統關閉。
```

### 3.2 產出的資料檔案格式

請貼上重構後生成的 `books.json` 前幾行內容：

```json
[
  {
    "title": "深入淺出Python",
    "isbn": "978001",
    "status": "available"
  },
  {
    "title": "資料結構理論",
    "isbn": "978002",
    "status": "borrowed"
  },
  {
    "title": "演算法實作",
    "isbn": "978003",
    "status": "available"
  }
]
```

---

## 四、 Git 提交紀錄 (Commit History)  (共2小題，總共13分)

### 4.1. 請執行 `git log --oneline` 並將 Commit 紀錄貼在此處，以證明你的開發流程(此小題6分)


```log
95df2fc test: add test output books.json and update Answer.MD with results
15a7e35 feat: implement modern_library.py with class-based JSON storage
355f82b docs: complete code audit report in Answer.MD
a61d385 init: add project base files and legacy library code
```

### 4.2. GitHub Repository 連結(此小題7分)

將專案推送到 GitHub (Public) 若提交到 Private 連結不給分。 請設定 Repository 名稱為 `學號-0527-Final` Ex: B11526748-0527-Final **請用 - 不是 _**

```log
https://github.com/c0968331397-prog/B11409050
```

希望這兩份 Markdown 格式能幫你省下不少排版時間！祝你的考試順利舉行！

最後請保留整份專案資料夾歐！
