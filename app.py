import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from hangman_game import *

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('hangman.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def home():
    conn = get_db_connection()
    words = conn.execute('SELECT * FROM words').fetchall()
    conn.close()
    return render_template('index.html')


if __name__ == "__main__":
    app.run(port=40001, debug=True)
