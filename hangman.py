import sqlite3


class Hangman:
    def __init__(self, game_id, word, word_length, no_of_guesses, game_valid):
        self.id = game_id
        self.word = word
        self.word_length = word_length
        self.no_of_guesses = no_of_guesses
        self.game_valid = game_valid

    # @property
    # def id(self):
    #     return self.id
    #
    # @id.setter
    # def id(self, value):
    #     self.id = value
    #
    # @id.deleter
    # def id(self):
    #     del self.id
    #
    # @property
    # def word(self):
    #     return self.word_id
    #
    # @word.setter
    # def word(self, value):
    #     self.word_id = value
    #
    # @word.deleter
    # def word(self):
    #     del self.word
    #
    # @property
    # def word_length(self):
    #     return self.word_id
    #
    # @word_length.setter
    # def word_length(self, value):
    #     self.word_length = value
    #
    # @word_length.deleter
    # def word_length(self):
    #     del self.word_length
    #
    # @property
    # def no_of_guesses(self):
    #     return self.no_of_guesses
    #
    # @no_of_guesses.setter
    # def no_of_guesses(self, value):
    #     self.no_of_guesses = value
    #
    # @no_of_guesses.deleter
    # def no_of_guesses(self):
    #     del self.no_of_guesses

    def increment_no_of_guesses(self):
        self.no_of_guesses += 1

    def process_guess(self, guess, to_display):
        guess = guess.lower()
        conn = sqlite3.connect('hangman.db')
        cursor = conn.cursor()

        cursor.execute("SELECT Word FROM Words where Word_ID=(%s)", self.word_id)
        result_set = list(cursor.fetchall())
        result_set[0] = result_set[0].lower()
        for index, result in enumerate(result_set[0]):
            if guess == result:
                to_display[index] = guess

        self.increment_no_of_guesses()

        return to_display

    # @property
    # def game_valid(self):
    #     return self.no_of_guesses
    #
    # @game_valid.setter
    # def game_valid(self, value):
    #     self.game_valid = value
    #
    # @game_valid.deleter
    # def game_valid(self):
    #     del self.game_valid

    def check_game_state(self):
        if self.no_of_guesses >= self.word_length - 1:
            self.game_valid = False
        return self.game_valid
