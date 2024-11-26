from flask import Flask
from routes.production import production_bp
from routes.items import items_bp
from routes.upload import upload_bp
from routes.inventory import inventory_bp
import sqlite3
import os

DB_PATH = "db.sqlite3"
SCHEMA_PATH = "schema.sql"

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


# DB 초기화 함수
def init_db():
    """Initialize the database with tables from the schema.sql file."""
    if not os.path.exists(SCHEMA_PATH):
        raise FileNotFoundError("schema.sql 파일을 찾을 수 없습니다.")
    with sqlite3.connect(DB_PATH) as conn:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as schema_file:
            conn.executescript(schema_file.read())
    print("데이터베이스 초기화 완료!")


# Blueprints 등록
app.register_blueprint(production_bp, url_prefix="/")
app.register_blueprint(items_bp, url_prefix="/items")
app.register_blueprint(upload_bp, url_prefix="/upload")

app.register_blueprint(inventory_bp, url_prefix="/inventory")

# 앱 실행
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
