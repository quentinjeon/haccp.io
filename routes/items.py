from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3

DB_PATH = "db.sqlite3"

items_bp = Blueprint("items", __name__)

@items_bp.route("/", methods=["GET", "POST"])
def manage_items():
    error = None

    if request.method == "POST":
        item_name = request.form.get("item_name")
        shelf_life = request.form.get("shelf_life")
        storage_method = request.form.get("storage_method")

        if item_name and shelf_life:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()

                # 중복 검사
                cursor.execute("SELECT id FROM item_list WHERE item_name = ?", (item_name,))
                existing_item = cursor.fetchone()

                if existing_item:
                    error = f"'{item_name}'은(는) 이미 등록된 품목입니다."
                else:
                    # 품목 추가
                    cursor.execute("""
                    INSERT INTO item_list (item_name, shelf_life, storage_method)
                    VALUES (?, ?, ?)
                    """, (item_name, shelf_life, storage_method))
                    conn.commit()
                    return redirect(url_for("items.manage_items"))

    # 품목 리스트 가져오기
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, item_name, shelf_life, storage_method FROM item_list")
        items = cursor.fetchall()

    return render_template("items.html", items=items, error=error)

@items_bp.route("/delete/<int:item_id>")
def delete_item(item_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM item_list WHERE id = ?", (item_id,))
        conn.commit()
    return redirect(url_for("items.manage_items"))
