import sqlite3
import time

from flask import Flask, render_template, request, redirect, url_for, abort, flash
from hangman import Hangman
from random_functions import *

# Assign Flask app and load config file.
app = Flask(__name__)
app.config.from_pyfile('config.py')

# Initialise Hangman object.
hangman_game = Hangman(game_id=0, word="", word_progress="_", word_length=0, no_of_guesses=0,
                       game_valid=True)


# Render home page.
@app.route('/')
def index():
    return render_template('base.html')


# Start either a new game or an existing game.
@app.route("/game/", methods=["POST"])
def start_game():
    # Create connection to database and create cursor.
    conn = sqlite3.connect('hangman.db')
    cursor = conn.cursor()

    # Check if request method is of POST type.
    if request.method == "POST":
        # Retrieve form data.
        form_data = request.form
        game_id = form_data.get("game_id")

        # Execute query to database to see if game already exists.
        cursor.execute("SELECT COUNT(*) FROM Games WHERE Game_ID=?", (game_id,))
        result = cursor.fetchone()[0]

        # If no rows are fetched, then game must be new.
        if result == 0:
            # Generate random word id, and query database to find the corresponding word.
            word_id = random_word_id()
            cursor.execute("SELECT Word FROM Words WHERE Word_ID=?", (word_id,))
            word_row = list(cursor.fetchone())

            # Generate starting string for game using length of word.
            starterStr = "_" * len(word_row[0])

            # Prepare SQL query and data array.
            sqlite_insert_with_param = """INSERT INTO Games(Game_ID,Word_ID,Status,No_Of_Guesses) VALUES (?,?,?,?)"""
            data_tuple = (game_id, word_id, starterStr, 0)

            # Cursor executes prepare query with prepared array as parameter.
            cursor.execute(sqlite_insert_with_param, data_tuple)

            # Commit changes and close connection.
            conn.commit()
    else:
        # Minor error handling.
        return abort(400)

    # Cursor will execute query to get game details using game_id.
    cursor.execute("SELECT * FROM Games WHERE Game_ID=?", (game_id,))
    game_result_set = list(cursor.fetchone())

    # Cursor will execute query to get word details using the word_id gained from fetching the game details.
    cursor.execute("SELECT * FROM Words WHERE Word_ID=?", (game_result_set[1],))
    word_result_set = list(cursor.fetchone())

    # Initialise game_valid boolean to true.
    game_valid = True

    # Refer to outer scope and assign values fetched to global hangman object.
    global hangman_game
    hangman_game = Hangman(game_id=game_result_set[0], word=word_result_set[1], word_length=word_result_set[2],
                           word_progress=game_result_set[2], no_of_guesses=game_result_set[3], game_valid=game_valid)

    # Check that game fetched is valid and hasn't already been lost. If not redirect to game with game_id parameter.
    if hangman_game.check_game_state():
        return redirect(url_for('game', game_id=game_id))
    else:
        time.sleep(2)
        return redirect(url_for('loss'))


# Redirect to game screen, which renders game page.
@app.route("/game/<game_id>/", methods=["GET", "POST"])
def game(game_id):
    return render_template("game.html", game_id=game_id, game_details=hangman_game)


# Handles adding guess to the game, taking in a game_id and guess parameter.
@app.route("/game/<game_id>/guess", methods=["POST"])
def add_char(game_id):
    # Retrieve guess from POST request.
    letter = request.form['letter']

    # Process guess to check if it is valid or not. This will return an altered object.
    hangman_game.process_guess(letter)

    # Check if game is still valid, parameter game_valid will be updated.
    hangman_game.game_valid = hangman_game.check_game_state()

    # If game is valid, check if game has been won. If not, redirect to game page, otherwise redirect to loss screen.
    # TODO: This prevents the user from viewing the hangman image as they lose, and so will need to be changed.
    if hangman_game.game_valid:
        if hangman_game.check_game_won():
            return redirect(url_for('win', game_id=game_id, hangman_game=hangman_game))
        return redirect(url_for('game', game_id=game_id, hangman_game=hangman_game))
    else:
        time.sleep(2)
        return redirect(url_for('loss'))


# Render loss page.
@app.route('/loss/')
def loss():
    return render_template('loss.html')


# Render win page.
@app.route('/win/<game_id>')
def win(game_id):
    return render_template('win.html', game_id=game_id, game_details=hangman_game)


# Run app.
if __name__ == "__main__":
    app.run(port=40001, debug=True)
