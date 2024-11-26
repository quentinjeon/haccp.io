from flask import Blueprint, render_template
import sqlite3
from datetime import datetime
import re

DB_PATH = "db.sqlite3"

inventory_bp = Blueprint("inventory", __name__)

def extract_number(quantity_str):
    """수량 문자열에서 숫자를 추출합니다."""
    match = re.search(r'\d+', quantity_str)
    return int(match.group()) if match else 0

@inventory_bp.route("/")
def inventory():
    today = datetime.now().strftime("%Y-%m-%d")

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        # 현재 날짜 기준으로 유통기한 이전인 데이터 필터링
        cursor.execute("""
        SELECT item, quantity
        FROM parsed_data
        WHERE expiration_date > ?
        """, (today,))
        rows = cursor.fetchall()

    # 항목별로 재고 수량 계산
    inventory_data = {}
    for item, quantity in rows:
        quantity_number = extract_number(quantity)  # "500개" → 500
        if item in inventory_data:
            inventory_data[item] += quantity_number
        else:
            inventory_data[item] = quantity_number

    # 리스트 형태로 변환 (템플릿에 전달)
    inventory_data = [(item, total_quantity) for item, total_quantity in inventory_data.items()]

    return render_template("inventory.html", inventory_data=inventory_data)
