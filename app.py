from flask import Flask
from app.routes.notes import notes_bp
from app.models.database import init_db
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
    app.secret_key = os.environ.get('SECRET_KEY', 'default_dev_key')

    # 註冊 Blueprint
    app.register_blueprint(notes_bp)

    return app

app = create_app()

if __name__ == '__main__':
    # 初始化資料庫
    init_db()
    app.run(debug=True)
