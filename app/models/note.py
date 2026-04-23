import sqlite3
from .database import get_db_connection

class Note:
    @staticmethod
    def get_all():
        """取得所有讀書筆記，依建立時間由新到舊排序"""
        try:
            with get_db_connection() as conn:
                notes = conn.execute('SELECT * FROM notes ORDER BY created_at DESC').fetchall()
                return notes
        except sqlite3.Error as e:
            print(f"Database error in get_all: {e}")
            return []

    @staticmethod
    def get_by_id(note_id):
        """依據 ID 取得單一讀書筆記"""
        try:
            with get_db_connection() as conn:
                note = conn.execute('SELECT * FROM notes WHERE id = ?', (note_id,)).fetchone()
                return note
        except sqlite3.Error as e:
            print(f"Database error in get_by_id: {e}")
            return None

    @staticmethod
    def create(title, content, rating):
        """新增一筆讀書筆記"""
        try:
            with get_db_connection() as conn:
                cursor = conn.execute(
                    'INSERT INTO notes (title, content, rating) VALUES (?, ?, ?)',
                    (title, content, rating)
                )
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error in create: {e}")
            return None

    @staticmethod
    def update(note_id, title, content, rating):
        """更新指定 ID 的讀書筆記內容"""
        try:
            with get_db_connection() as conn:
                conn.execute(
                    'UPDATE notes SET title = ?, content = ?, rating = ? WHERE id = ?',
                    (title, content, rating, note_id)
                )
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Database error in update: {e}")
            return False

    @staticmethod
    def delete(note_id):
        """刪除指定 ID 的讀書筆記"""
        try:
            with get_db_connection() as conn:
                conn.execute('DELETE FROM notes WHERE id = ?', (note_id,))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Database error in delete: {e}")
            return False
            
    @staticmethod
    def search(keyword):
        """根據書名或內容搜尋讀書筆記"""
        try:
            with get_db_connection() as conn:
                query = f"%{keyword}%"
                notes = conn.execute(
                    'SELECT * FROM notes WHERE title LIKE ? OR content LIKE ? ORDER BY created_at DESC',
                    (query, query)
                ).fetchall()
                return notes
        except sqlite3.Error as e:
            print(f"Database error in search: {e}")
            return []
