import csv
from flask import Blueprint, render_template, request, redirect, url_for, Response
import sqlite3
from datetime import datetime, timedelta

DB_PATH = "db.sqlite3"

production_bp = Blueprint("production", __name__)

def parse_text(input_text):
    parts = input_text.split()
    if len(parts) != 3:
        raise ValueError("입력 형식은 '항목 수량 동작'이어야 합니다.")
    return parts[0], parts[1], parts[2]

def save_to_db(text_input, item, quantity, action):
    created_date = datetime.now().strftime("%Y-%m-%d")
    production_date = datetime.now().strftime("%Y-%m-%d")
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT shelf_life FROM item_list WHERE item_name = ?", (item,))
        result = cursor.fetchone()
        expiration_date = (datetime.now() + timedelta(days=int(result[0]))).strftime("%Y-%m-%d") if result else None
        cursor.execute("""
        INSERT INTO parsed_data (text_input, item, quantity, action, created_date, production_date, expiration_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (text_input, item, quantity, action, created_date, production_date, expiration_date))
        conn.commit()

@production_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text_input = request.form.get("text_input")
        try:
            item, quantity, action = parse_text(text_input)
            save_to_db(text_input, item, quantity, action)
            return redirect(url_for("production.index"))
        except ValueError as e:
            return render_template("index.html", error=str(e))

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT id, item, quantity, action, created_date, production_date, expiration_date
        FROM parsed_data
        """)
        data = cursor.fetchall()

    return render_template("index.html", data=data, error=None)

@production_bp.route("/delete/<int:record_id>")
def delete_record(record_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM parsed_data WHERE id = ?", (record_id,))
        conn.commit()
    return redirect(url_for("production.index"))

@production_bp.route("/export_csv")
def export_csv():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT id, item, quantity, action, created_date, production_date, expiration_date
        FROM parsed_data
        """)
        data = cursor.fetchall()

    # CSV 생성
    output = []
    header = ["ID", "Item", "Quantity", "Action", "Created Date", "Production Date", "Expiration Date"]
    output.append(header)
    output.extend(data)

    # UTF-8로 응답
    def generate():
        for row in output:
            yield ",".join(map(str, row)) + "\n"

    return Response(
        generate(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=production_data.csv"}
    )
