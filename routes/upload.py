from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3
import os
import csv

DB_PATH = "db.sqlite3"
UPLOAD_FOLDER = "uploads"

upload_bp = Blueprint("upload", __name__)

@upload_bp.route("/", methods=["GET", "POST"])
def upload_csv():
    if request.method == "POST":
        file = request.files["file"]
        if file and file.filename.endswith(".csv"):
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                with open(file_path, "r", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    next(reader)  # Skip header
                    for row in reader:
                        cursor.execute("""
                        INSERT INTO item_list (item_name, shelf_life)
                        VALUES (?, ?)
                        """, (row[0], row[1]))
                conn.commit()
            os.remove(file_path)
            return redirect(url_for("items.manage_items"))
    return render_template("upload_csv.html")
