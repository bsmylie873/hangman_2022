class Hangman:

    # Constructor for object with appropriate attributes.
    def __init__(self, game_id, word, word_progress, word_length, no_of_guesses, game_valid):
        self.game_id = game_id
        self.word = word
        self.word_progress = word_progress
        self.word_length = word_length
        self.no_of_guesses = no_of_guesses
        self.game_valid = game_valid

    # Simple method to increment number of guesses by user.
    def increment_no_of_guesses(self):
        self.no_of_guesses += 1

    # Method to process guess input.
    def process_guess(self, guess):
        # Convert guess and word to uppercase if they aren't already.
        guess = guess.upper()
        self.word = self.word.upper()

        # Declare a temporary list which will be the same length as the word and will be filled with null values.
        list_of_changes = [None] * self.word_length

        # Loop through the word as a series of characters with an explicit index. If the guess matches the current
        # character, assign it to the same index in the temporary list. Otherwise, copy the character from the current
        # word to that same index.
        for index, i in enumerate(self.word):
            if guess == i:
                list_of_changes[index] = guess
            else:
                list_of_changes[index] = self.word_progress[index]

        # Construct new string from temporary list.
        string = ''.join(str(x) for x in list_of_changes)

        # Check if string and original word are the same. If so, this guess was wrong and we increment the hangman
        # counter.
        if string == self.word_progress:
            self.increment_no_of_guesses()

        # Assign the word to the new string and return it.
        self.word_progress = string
        return self.word_progress

    # Method to check if current game is valid or not by comparing the number of guesses to the word length minus one.
    def check_game_state(self):
        if self.no_of_guesses >= self.word_length - 1:
            self.game_valid = False
        return self.game_valid
