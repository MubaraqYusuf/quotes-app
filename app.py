from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os
import random
import time

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def wait_for_db():
    while True:
        try:
            conn = get_db_connection()
            conn.close()
            print("PostgreSQL is ready!")
            break
        except Exception:
            print("Waiting for PostgreSQL...")
            time.sleep(2)

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS quotes (
            id SERIAL PRIMARY KEY,
            text TEXT NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.route("/")
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT text FROM quotes")
    quotes = cur.fetchall()
    cur.close()
    conn.close()

    quote = random.choice(quotes)[0] if quotes else "No quotes yet"
    return render_template("index.html", quote=quote)

@app.route("/add", methods=["GET", "POST"])
def add_quote():
    if request.method == "POST":
        new_quote = request.form.get("quote")
        if new_quote:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO quotes (text) VALUES (%s)", (new_quote,))
            conn.commit()
            cur.close()
            conn.close()
        return redirect(url_for("index"))

    return render_template("add.html")

if __name__ == "__main__":
    wait_for_db()
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
