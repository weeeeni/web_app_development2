from flask import Blueprint, render_template, request, redirect, url_for

# 建立 Blueprint 物件，方便在 app.py 進行註冊與管理
notes_bp = Blueprint('notes', __name__)

@notes_bp.route('/')
def index():
    """
    顯示所有讀書筆記，或處理搜尋請求。
    輸入: query string (例如 ?q=keyword) (選填)
    邏輯: 根據有無 q 參數，呼叫 Note.search() 或 Note.get_all()
    輸出: 渲染 index.html，傳入 notes 列表與 search_query
    """
    pass

@notes_bp.route('/notes/new', methods=['GET'])
def new_note():
    """
    顯示新增筆記的表單頁面。
    輸入: 無
    輸出: 渲染 add_note.html
    """
    pass

@notes_bp.route('/notes/new', methods=['POST'])
def create_note():
    """
    處理新增筆記表單送出。
    輸入: 表單欄位 title, content, rating
    邏輯: 驗證 title 不可為空，呼叫 Note.create()
    輸出: 成功則重導向至 index，失敗則重新渲染 add_note.html 並顯示錯誤
    """
    pass

@notes_bp.route('/notes/<int:id>/edit', methods=['GET'])
def edit_note(id):
    """
    顯示編輯特定筆記的表單頁面。
    輸入: URL 參數 id
    邏輯: 呼叫 Note.get_by_id(id) 取得原始資料
    輸出: 若找不到回傳 404，否則渲染 edit_note.html，傳入 note 物件
    """
    pass

@notes_bp.route('/notes/<int:id>/edit', methods=['POST'])
def update_note(id):
    """
    處理更新筆記表單送出。
    輸入: URL 參數 id，表單欄位 title, content, rating
    邏輯: 驗證 title 不可為空，呼叫 Note.update()
    輸出: 成功則重導向至 index，失敗則重新渲染 edit_note.html 並顯示錯誤
    """
    pass

@notes_bp.route('/notes/<int:id>/delete', methods=['POST'])
def delete_note(id):
    """
    處理刪除特定筆記的請求。
    輸入: URL 參數 id
    邏輯: 呼叫 Note.delete(id)
    輸出: 重導向至 index
    """
    pass
