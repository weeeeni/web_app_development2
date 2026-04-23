from .database import get_db_connection

class Note:
    @staticmethod
    def get_all():
        """取得所有筆記，依建立時間由新到舊排序"""
        with get_db_connection() as conn:
            notes = conn.execute('SELECT * FROM notes ORDER BY created_at DESC').fetchall()
            return notes

    @staticmethod
    def get_by_id(note_id):
        """依據 ID 取得單一筆記"""
        with get_db_connection() as conn:
            note = conn.execute('SELECT * FROM notes WHERE id = ?', (note_id,)).fetchone()
            return note

    @staticmethod
    def create(title, content, rating):
        """新增一筆筆記"""
        with get_db_connection() as conn:
            cursor = conn.execute(
                'INSERT INTO notes (title, content, rating) VALUES (?, ?, ?)',
                (title, content, rating)
            )
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def update(note_id, title, content, rating):
        """更新筆記內容"""
        with get_db_connection() as conn:
            conn.execute(
                'UPDATE notes SET title = ?, content = ?, rating = ? WHERE id = ?',
                (title, content, rating, note_id)
            )
            conn.commit()

    @staticmethod
    def delete(note_id):
        """刪除一筆筆記"""
        with get_db_connection() as conn:
            conn.execute('DELETE FROM notes WHERE id = ?', (note_id,))
            conn.commit()
            
    @staticmethod
    def search(keyword):
        """根據書名或內容搜尋筆記"""
        with get_db_connection() as conn:
            query = f"%{keyword}%"
            notes = conn.execute(
                'SELECT * FROM notes WHERE title LIKE ? OR content LIKE ? ORDER BY created_at DESC',
                (query, query)
            ).fetchall()
            return notes
