from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def create_table():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE
    )
    """)

    conn.commit()
    conn.close()

create_table()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/add', methods=['POST'])
def add():

    name = request.form['name']
    email = request.form['email']

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=?",
        (email,)
    )

    user = cursor.fetchone()

    if user:
        conn.close()
        return "Duplicate Data Found!"

    cursor.execute(
        "INSERT INTO users(name,email) VALUES(?,?)",
        (name,email)
    )

    conn.commit()
    conn.close()

    return redirect('/view')

@app.route('/view')
def view():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")

    data = cursor.fetchall()

    conn.close()

    return render_template(
        "view.html",
        data=data
    )

if __name__ == "__main__":
    app.run(debug=True)
