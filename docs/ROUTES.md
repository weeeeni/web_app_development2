# 讀書筆記本系統 - 路由與頁面設計 (Routes Design)

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 筆記列表 / 搜尋 | GET | `/` | `index.html` | 顯示所有讀書筆記，若有 `?q=` 參數則顯示搜尋結果 |
| 新增筆記頁面 | GET | `/notes/new` | `add_note.html` | 顯示供使用者填寫書籍資訊的表單 |
| 建立筆記 | POST | `/notes/new` | — | 接收表單資料，寫入資料庫後重導向至首頁 |
| 編輯筆記頁面 | GET | `/notes/<int:id>/edit` | `edit_note.html` | 根據 ID 查詢原筆記內容，並顯示於表單供編輯 |
| 更新筆記 | POST | `/notes/<int:id>/edit` | — | 接收更新後的表單資料，更新資料庫後重導向至首頁 |
| 刪除筆記 | POST | `/notes/<int:id>/delete` | — | 根據 ID 刪除該筆記，刪除後重導向至首頁 |

## 2. 每個路由的詳細說明

### 2.1 筆記列表與搜尋 (`GET /`)
- **輸入**：URL 參數 `q`（選填，作為搜尋關鍵字）。
- **處理邏輯**：
  - 如果有 `q` 參數，呼叫 `Note.search(q)`。
  - 如果沒有 `q` 參數，呼叫 `Note.get_all()`。
- **輸出**：渲染 `index.html`，傳入取得的 `notes` 列表與當前 `search_query` 狀態。

### 2.2 新增筆記頁面 (`GET /notes/new`)
- **輸入**：無。
- **處理邏輯**：單純準備顯示頁面。
- **輸出**：渲染 `add_note.html`。

### 2.3 建立筆記 (`POST /notes/new`)
- **輸入**：表單內的 `title`, `content`, `rating`。
- **處理邏輯**：
  - 驗證 `title` 是否為空。若空則回傳錯誤。
  - 呼叫 `Note.create(title, content, rating)` 存入 SQLite。
- **輸出**：成功後執行 `redirect(url_for('notes.index'))`。
- **錯誤處理**：驗證失敗時，帶著錯誤訊息與原輸入內容，重新渲染 `add_note.html`。

### 2.4 編輯筆記頁面 (`GET /notes/<int:id>/edit`)
- **輸入**：URL 變數 `id`。
- **處理邏輯**：呼叫 `Note.get_by_id(id)` 查詢該筆記。
- **輸出**：渲染 `edit_note.html`，將取得的 `note` 資料傳入模板中。
- **錯誤處理**：如果該 ID 在資料庫中不存在，回傳 404 Not Found 錯誤。

### 2.5 更新筆記 (`POST /notes/<int:id>/edit`)
- **輸入**：URL 變數 `id` 以及表單內的 `title`, `content`, `rating`。
- **處理邏輯**：
  - 驗證 `title` 是否為空。
  - 呼叫 `Note.update(id, title, content, rating)` 更新 SQLite。
- **輸出**：成功後執行 `redirect(url_for('notes.index'))`。
- **錯誤處理**：驗證失敗時，帶著錯誤訊息與原輸入內容，重新渲染 `edit_note.html`。

### 2.6 刪除筆記 (`POST /notes/<int:id>/delete`)
- **輸入**：URL 變數 `id`。
- **處理邏輯**：呼叫 `Note.delete(id)` 從 SQLite 移除資料。
- **輸出**：執行完畢後 `redirect(url_for('notes.index'))`。
- **注意**：使用 POST 方法而非 GET，以防爬蟲或瀏覽器預先載入觸發刪除操作。

## 3. Jinja2 模板清單

所有模板都將放在 `app/templates/` 目錄中。

| 模板檔案名稱 | 繼承自 | 說明 |
| --- | --- | --- |
| `base.html` | (無) | **共用基礎版型**：包含 `<html>` 標籤、載入 CSS/JS、網頁導覽列 (Navbar) 以及預留的 `{% block content %}` 區塊。 |
| `index.html` | `base.html` | **首頁**：包含搜尋列、筆記列表區塊，針對沒有資料的情況顯示提示。 |
| `add_note.html` | `base.html` | **新增頁面**：包含書名、心得文字框、評分下拉選單的 HTML 表單。 |
| `edit_note.html` | `base.html` | **編輯頁面**：結構與新增頁面相同，但欄位中會預先填入舊的資料。 |

## 4. 路由骨架程式碼

請參考 `app/routes/notes.py`。
