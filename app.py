from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# --- 初始化資料庫 ---
def init_db():
    conn = sqlite3.connect("records.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            amount INTEGER,
            balance INTEGER
        )
    """)
    conn.commit()
    conn.close()

init_db()


# --- 查看全部記帳紀錄 ---
@app.route("/")
def index():
    conn = sqlite3.connect("records.db")
    cursor = conn.cursor()
    cursor.execute("SELECT date, amount, balance FROM records ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return render_template("index.html", records=rows)


# --- 新增資料 ---
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        date = request.form.get("date")
        amount = int(request.form.get("amount"))
        balance = int(request.form.get("balance"))

        conn = sqlite3.connect("records.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO records (date, amount, balance) VALUES (?, ?, ?)",
            (date, amount, balance)
        )
        conn.commit()
        conn.close()

        return redirect("/")

    # 預設日期填今天
    today = datetime.now().strftime("%Y-%m-%d")
    return render_template("add.html", today=today)


if __name__ == "__main__":
    app.run(debug=True)
