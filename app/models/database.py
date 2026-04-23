import sqlite3
import os

# 將資料庫放在專案根目錄的 instance 資料夾下
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db_connection():
    """建立並回傳一個資料庫連線"""
    try:
        # 確保 instance 目錄存在
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        
        conn = sqlite3.connect(DB_PATH)
        # 讓查詢結果可以用字典的方式存取欄位，方便在 Jinja2 中使用
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        raise

def init_db():
    """初始化資料庫，執行 schema.sql 來建表"""
    schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'schema.sql')
    
    try:
        with get_db_connection() as conn:
            with open(schema_path, 'r', encoding='utf-8') as f:
                conn.executescript(f.read())
            conn.commit()
            print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")
