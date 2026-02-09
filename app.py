from flask import Flask, render_template, request, redirect
import psycopg2
import time

app = Flask(__name__)

DB_CONFIG = {
    "host": "db",
    "database": "quotes_db",
    "user": "postgres",
    "password": "postgres",
    "port": 5432
}


def wait_for_db():
    while True:
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            conn.close()
            print("PostgreSQL is ready!")
            break
        except psycopg2.OperationalError:
            print("Waiting for PostgreSQL...")
            time.sleep(2)


wait_for_db()


def get_db():
    return psycopg2.connect(**DB_CONFIG)


def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS quotes (
            id SERIAL PRIMARY KEY,
            quote TEXT NOT NULL,
            author TEXT NOT NULL
        );
    """)

    conn.commit()
    cur.close()
    conn.close()


init_db()


@app.route("/")
def index():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT quote, author FROM quotes ORDER BY id DESC;")
    quotes = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("index.html", quotes=quotes)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        quote = request.form["quote"]
        author = request.form["author"]

        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO quotes (quote, author) VALUES (%s, %s);",
            (quote, author)
        )

        conn.commit()
        cur.close()
        conn.close()

        return redirect("/")

    return render_template("add.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
