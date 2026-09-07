from flask import Flask, render_template, request, redirect
import mysql.connector
import os

app = Flask(__name__)


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "mysql"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "root"),
        database=os.getenv("MYSQL_DATABASE", "guestbook")
    )


@app.route("/")
def home():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM messages ORDER BY id DESC")
    messages = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("index.html", messages=messages)


@app.route("/add", methods=["POST"])
def add_message():
    name = request.form["name"]
    message = request.form["message"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO messages (name, message) VALUES (%s, %s)",
        (name, message)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)