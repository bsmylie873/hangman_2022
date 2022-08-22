import json
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, abort
from hangman import Hangman
from random_functions import *

app = Flask(__name__)
hangman_game = Hangman(game_id=0, word="______", word_progress="______", word_length=7, no_of_guesses=0,
                       game_valid=True)


@app.route('/')
def index():
    return render_template('base.html')


@app.route("/game/", methods=["POST"])
def start_game():
    word_id = random_word_id()
    conn = sqlite3.connect('hangman.db')
    cursor = conn.cursor()

    if request.method == "POST":
        form_data = request.form
        game_id = form_data.get("game_id")
        print("Game ID is " + game_id)
        cursor.execute("SELECT COUNT(*) FROM Games WHERE Game_ID=?", (game_id,))
        result = cursor.fetchone()[0]

        if result == 0:
            cursor.execute("SELECT Word FROM Words WHERE Word_ID=?", (word_id,))
            word_row = list(cursor.fetchone())
            starterStr = "_" * len(word_row[0])
            sqlite_insert_with_param = """INSERT INTO Games(Game_ID,Word_ID,Status,No_Of_Guesses) VALUES (?,?,?,?)"""
            data_tuple = (game_id, word_id, starterStr, 0)
            cursor.execute(sqlite_insert_with_param, data_tuple)
            conn.commit()
            conn.close()
    else:
        return abort(400)
    conn = sqlite3.connect('hangman.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Games WHERE Game_ID=?", (game_id,))
    result_set = list(cursor.fetchone())
    cursor.execute("SELECT * FROM Words WHERE Word_ID=?", (result_set[1],))
    word_result_set = list(cursor.fetchone())
    game_valid = True
    global hangman_game
    hangman_game = Hangman(game_id=result_set[0], word=word_result_set[1], word_length=word_result_set[2],
                           word_progress=result_set[2], no_of_guesses=result_set[3], game_valid=game_valid)
    if hangman_game.check_game_state():
        return redirect(url_for('game', game_id=game_id))
    else:
        return render_template("loss.html")


@app.route("/game/<game_id>/", methods=["GET", "POST"])
def game(game_id):
    return render_template("game.html", game_id=game_id, game_details=hangman_game)


@app.route("/game/<game_id>/guess", methods=["POST"])
def add_char(game_id):
    letter = request.form['letter']
    hangman_game.process_guess(letter)
    hangman_game.game_valid = hangman_game.check_game_state()

    if hangman_game.game_valid:
        return redirect(url_for('game', game_id=game_id, hangman_game=hangman_game))
    else:
        return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(port=40001, debug=True)
