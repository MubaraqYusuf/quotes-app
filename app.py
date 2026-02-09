import os
import time
import logging
from flask import Flask, render_template, request, redirect, jsonify
import psycopg2
from psycopg2 import OperationalError
from psycopg2 import pool

app = Flask(__name__)

# -------------------- Logging --------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------- Database Config --------------------
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "db"),
    "database": os.getenv("POSTGRES_DB", "quotes_db"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
    "port": int(os.getenv("DB_PORT", 5432))
}

# -------------------- Connection Pool --------------------
connection_pool = None


def init_connection_pool():
    global connection_pool
    for i in range(10):
        try:
            connection_pool = pool.SimpleConnectionPool(1, 10, **DB_CONFIG)
            logger.info("PostgreSQL connection pool created")
            return
        except OperationalError:
            logger.warning("Waiting for PostgreSQL... retrying")
            time.sleep(3)
    raise Exception("Failed to connect to PostgreSQL")


def get_db():
    return connection_pool.getconn()


def release_db(conn):
    connection_pool.putconn(conn)


# -------------------- Database Setup --------------------

def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS quotes (
            id SERIAL PRIMARY KEY,
            quote TEXT NOT NULL,
            author VARCHAR(255) NOT NULL
        );
    ''')

    conn.commit()
    cur.close()
    release_db(conn)


# -------------------- Routes --------------------

@app.route("/")
def index():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT id, quote, author FROM quotes ORDER BY id DESC;")
    quotes = cur.fetchall()

    cur.close()
    release_db(conn)

    return render_template("index.html", quotes=quotes)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        quote = request.form.get("quote")
        author = request.form.get("author")

        if not quote or not author:
            return "Quote and author are required", 400

        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO quotes (quote, author) VALUES (%s, %s);",
            (quote, author)
        )

        conn.commit()
        cur.close()
        release_db(conn)

        return redirect("/")

    return render_template("add.html")


@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM quotes WHERE id=%s;", (id,))

    conn.commit()
    cur.close()
    release_db(conn)

    return redirect("/")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":
        quote = request.form.get("quote")
        author = request.form.get("author")

        cur.execute(
            "UPDATE quotes SET quote=%s, author=%s WHERE id=%s;",
            (quote, author, id)
        )

        conn.commit()
        cur.close()
        release_db(conn)

        return redirect("/")

    cur.execute("SELECT quote, author FROM quotes WHERE id=%s;", (id,))
    data = cur.fetchone()

    cur.close()
    release_db(conn)

    return render_template("edit.html", data=data, id=id)


@app.route("/search")
def search():
    q = request.args.get("q", "")

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, quote, author FROM quotes WHERE quote ILIKE %s ORDER BY id DESC;",
        (f"%{q}%",)
    )

    results = cur.fetchall()

    cur.close()
    release_db(conn)

    return render_template("index.html", quotes=results, search=q)


# -------------------- REST API --------------------

@app.route("/api/quotes")
def api_quotes():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT id, quote, author FROM quotes ORDER BY id DESC;")
    data = cur.fetchall()

    cur.close()
    release_db(conn)

    return jsonify([
        {"id": q[0], "quote": q[1], "author": q[2]}
        for q in data
    ])


# -------------------- Startup --------------------

if __name__ == "__main__":
    init_connection_pool()
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
