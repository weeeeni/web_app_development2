from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.note import Note

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
    search_query = request.args.get('q', '').strip()
    
    if search_query:
        notes = Note.search(search_query)
    else:
        notes = Note.get_all()
        
    return render_template('index.html', notes=notes, search_query=search_query)

@notes_bp.route('/notes/new', methods=['GET'])
def new_note():
    """
    顯示新增筆記的表單頁面。
    輸入: 無
    輸出: 渲染 add_note.html
    """
    return render_template('add_note.html')

@notes_bp.route('/notes/new', methods=['POST'])
def create_note():
    """
    處理新增筆記表單送出。
    輸入: 表單欄位 title, content, rating
    邏輯: 驗證 title 不可為空，呼叫 Note.create()
    輸出: 成功則重導向至 index，失敗則重新渲染 add_note.html 並顯示錯誤
    """
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()
    rating_str = request.form.get('rating', '0')
    
    # 驗證必填欄位
    if not title:
        flash('書名為必填欄位！', 'danger')
        # 帶著舊有資料回去，讓使用者不用重填
        return render_template('add_note.html', title=title, content=content, rating=rating_str)
        
    try:
        rating = int(rating_str)
    except ValueError:
        rating = 0
        
    note_id = Note.create(title, content, rating)
    
    if note_id:
        flash('筆記新增成功！', 'success')
        return redirect(url_for('notes.index'))
    else:
        flash('新增筆記失敗，請稍後再試。', 'danger')
        return render_template('add_note.html', title=title, content=content, rating=rating_str)

@notes_bp.route('/notes/<int:id>/edit', methods=['GET'])
def edit_note(id):
    """
    顯示編輯特定筆記的表單頁面。
    輸入: URL 參數 id
    邏輯: 呼叫 Note.get_by_id(id) 取得原始資料
    輸出: 若找不到回傳 404，否則渲染 edit_note.html，傳入 note 物件
    """
    note = Note.get_by_id(id)
    if not note:
        flash('找不到該筆記', 'danger')
        return redirect(url_for('notes.index'))
        
    return render_template('edit_note.html', note=note)

@notes_bp.route('/notes/<int:id>/edit', methods=['POST'])
def update_note(id):
    """
    處理更新筆記表單送出。
    輸入: URL 參數 id，表單欄位 title, content, rating
    邏輯: 驗證 title 不可為空，呼叫 Note.update()
    輸出: 成功則重導向至 index，失敗則重新渲染 edit_note.html 並顯示錯誤
    """
    # 確認筆記存在
    note = Note.get_by_id(id)
    if not note:
        flash('找不到該筆記', 'danger')
        return redirect(url_for('notes.index'))
        
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()
    rating_str = request.form.get('rating', '0')
    
    if not title:
        flash('書名為必填欄位！', 'danger')
        # 模擬一個 note 字典/物件來維持表單資料狀態
        current_data = {'id': id, 'title': title, 'content': content, 'rating': rating_str}
        return render_template('edit_note.html', note=current_data)
        
    try:
        rating = int(rating_str)
    except ValueError:
        rating = 0
        
    success = Note.update(id, title, content, rating)
    
    if success:
        flash('筆記更新成功！', 'success')
        return redirect(url_for('notes.index'))
    else:
        flash('更新筆記失敗，請稍後再試。', 'danger')
        current_data = {'id': id, 'title': title, 'content': content, 'rating': rating_str}
        return render_template('edit_note.html', note=current_data)

@notes_bp.route('/notes/<int:id>/delete', methods=['POST'])
def delete_note(id):
    """
    處理刪除特定筆記的請求。
    輸入: URL 參數 id
    邏輯: 呼叫 Note.delete(id)
    輸出: 重導向至 index
    """
    success = Note.delete(id)
    if success:
        flash('筆記已成功刪除！', 'success')
    else:
        flash('刪除筆記失敗。', 'danger')
        
    return redirect(url_for('notes.index'))
