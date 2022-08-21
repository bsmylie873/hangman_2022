import json
import sqlite3
import hangman
from flask import Flask, render_template, request, redirect, url_for, abort, jsonify
from hangman import Hangman
from random_functions import *

app = Flask(__name__)
hangman_game = Hangman(game_id=0, word="______", word_length=7, no_of_guesses=0, game_valid=True)


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
        cursor.execute("SELECT COUNT(*) FROM Games where Game_ID=?", (game_id,))
        result = cursor.fetchone()[0]

        if result == 0:
            cursor.execute("SELECT Word FROM Words where Word_ID=?", (word_id,))
            word_row = list(cursor.fetchone())
            starterStr = "_" * len(word_row[0])
            sqlite_insert_with_param = """INSERT INTO Games(Word_ID,Status,No_Of_Guesses) VALUES (?,?,?)"""
            data_tuple = (word_id, starterStr, 0)
            cursor.execute(sqlite_insert_with_param, data_tuple)
            conn.commit()
            conn.close()

            global hangman_game
            no_of_guesses = 0
            game_valid = True
            hangman_game = Hangman(game_id=game_id, word=starterStr, word_length=len(word_row[0]),
                                   no_of_guesses=no_of_guesses, game_valid=game_valid)
            game_details = json.dumps(hangman_game.__dict__)
            return redirect("/game/" + hangman_game.id)
        else:
            cursor.execute("SELECT * FROM Games where Game_ID=?", (game_id,))
            result_set = list(cursor.fetchone())
            game_valid = True
            hangman_game = Hangman(game_id=result_set[0], word=result_set[1], word_length=len(result_set[1]),
                                   no_of_guesses=result_set[3], game_valid=game_valid)
            game_details = json.dumps(hangman_game.__dict__)
            return redirect("/game/" + hangman_game.id)
    else:
        return abort(400)


@app.route("/game/<game_id>", methods=["GET"])
def get_game_status(game_id):
    return render_template("game.html")


@app.route("/game/<game_id>/<guess>", methods=["POST"])
def add_char(hangman_game):
    letter = request.form['letter']

    return hangman_game.process_guess(getattr(hangman_game, 'word'), letter)


def update_game_status(data):
    conn = sqlite3.connect('hangman.db')
    cursor = conn.cursor()
    game_db_data = None
    if data:
        game_id = data['game_id']
        game_status = data['game_status']
        cursor.execute('UPDATE Games SET Status = ? WHERE Game_ID = ?', (game_status, game_id))
        conn.commit()
        cursor.execute('"SELECT Game FROM Games where Game_ID=(%s)"', game_id)
        game_db_data = list(cursor.fetchone())
        return game_db_data
    else:
        return game_db_data


# def check_game_status():
#     if self.check_game_state():
#         return True
#     else:
#         return False


if __name__ == "__main__":
    app.run(port=40001, debug=True)
