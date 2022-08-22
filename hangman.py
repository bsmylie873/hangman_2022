class Hangman:
    def __init__(self, game_id, word, word_progress, word_length, no_of_guesses, game_valid):
        self.game_id = game_id
        self.word = word
        self.word_progress = word_progress
        self.word_length = word_length
        self.no_of_guesses = no_of_guesses
        self.game_valid = game_valid

    def increment_no_of_guesses(self):
        self.no_of_guesses += 1

    def process_guess(self, guess):
        guess = guess.upper()
        self.word = self.word.upper()
        list_of_changes = [None] * self.word_length
        for index, i in enumerate(self.word):
            if guess == i:
                list_of_changes[index] = guess
            else:
                list_of_changes[index] = self.word_progress[index]

        string = ''.join(str(x) for x in list_of_changes)
        print(string)
        if string == self.word_progress:
            self.increment_no_of_guesses()
        self.word_progress = string
        return self.word_progress

    def check_game_state(self):
        if self.no_of_guesses >= self.word_length - 1:
            self.game_valid = False
        return self.game_valid
