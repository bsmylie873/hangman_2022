import unittest
from unittest.mock import MagicMock
import hangman
from random_functions import *


class hangmanAssignmentTests(unittest.TestCase):
    def setUp(self):
        self.game_id = 1
        self.word = "test"
        self.word_progress = "____"
        self.word_length = 4
        self.no_of_guesses = 0
        self.game_valid = True

    def test_check_assignment(self):
        hangman_game = hangman.Hangman(0, "", "", 0, 0, False)
        hangman_game.game_id = self.game_id
        hangman_game.word = self.word
        hangman_game.word_progress = self.word_progress
        hangman_game.word_length = self.word_length
        hangman_game.no_of_guesses = self.no_of_guesses
        hangman_game.game_valid = self.game_valid
        self.assertEqual(hangman_game.game_id, 1)
        self.assertEqual(hangman_game.word, "test")
        self.assertEqual(hangman_game.word_progress, "____")
        self.assertEqual(hangman_game.word_length, 4)
        self.assertEqual(hangman_game.no_of_guesses, 0)
        self.assertEqual(hangman_game.game_valid, True)

    def test_correct_guess(self):
        hangman_game = hangman.Hangman(555, "test", "____", 4, 0, True)
        hangman_game.process_guess("t")
        self.assertEqual(hangman_game.game_id, 555)
        self.assertEqual(hangman_game.word, "TEST")
        self.assertEqual(hangman_game.word_progress, "T__T")
        self.assertEqual(hangman_game.word_length, 4)
        self.assertEqual(hangman_game.no_of_guesses, 0)
        self.assertEqual(hangman_game.game_valid, True)

    def test_incorrect_guess(self):
        hangman_game = hangman.Hangman(555, "test", "____", 4, 0, True)
        hangman_game.process_guess("g")
        self.assertEqual(hangman_game.game_id, 555)
        self.assertEqual(hangman_game.word, "TEST")
        self.assertEqual(hangman_game.word_progress, "____")
        self.assertEqual(hangman_game.word_length, 4)
        self.assertEqual(hangman_game.no_of_guesses, 1)
        self.assertEqual(hangman_game.game_valid, True)

    def test_invalid_guess(self):
        hangman_game = hangman.Hangman(555, "test", "____", 4, 0, True)
        hangman_game.process_guess("5")
        self.assertEqual(hangman_game.game_id, 555)
        self.assertEqual(hangman_game.word, "TEST")
        self.assertEqual(hangman_game.word_progress, "____")
        self.assertEqual(hangman_game.word_length, 4)
        self.assertEqual(hangman_game.no_of_guesses, 1)
        self.assertEqual(hangman_game.game_valid, True)

    def test_game_success(self):
        hangman_game = hangman.Hangman(555, "test", "TE_T", 4, 0, True)
        hangman_game.process_guess("s")
        self.assertEqual(hangman_game.game_id, 555)
        self.assertEqual(hangman_game.word, "TEST")
        self.assertEqual(hangman_game.word_progress, "TEST")
        self.assertEqual(hangman_game.word_length, 4)
        self.assertEqual(hangman_game.no_of_guesses, 0)
        self.assertEqual(hangman_game.game_valid, True)

    def test_game_failure(self):
        hangman_game = hangman.Hangman(555, "test", "TE_T", 4, 5, True)
        hangman_game.process_guess("t")
        self.assertEqual(hangman_game.game_id, 555)
        self.assertEqual(hangman_game.word, "TEST")
        self.assertEqual(hangman_game.word_progress, "TE_T")
        self.assertEqual(hangman_game.word_length, 4)
        self.assertEqual(hangman_game.no_of_guesses, 6)
        self.assertEqual(hangman_game.game_valid, True)

    def test_check_game_state_valid(self):
        hangman_game = hangman.Hangman(555, "test", "TE_T", 4, 2, True)
        hangman_game.check_game_state()
        self.assertEqual(hangman_game.game_valid, True)

    def test_check_game_state_invalid(self):
        hangman_game = hangman.Hangman(555, "test", "TE_T", 4, 4, True)
        hangman_game.check_game_state()
        self.assertEqual(hangman_game.game_valid, False)

    def test_check_game_won_valid(self):
        hangman_game = hangman.Hangman(555, "test", "TEST", 4, 2, True)
        bool = hangman_game.check_game_state()
        self.assertTrue(bool)

    def test_check_game_won_invalid(self):
        hangman_game = hangman.Hangman(555, "test", "T_ST", 4, 2, True)
        bool = hangman_game.check_game_state()
        self.assertTrue(bool)

    def test_process(self):
        hangman_game = hangman.Hangman(0, "", "", 0, 0, False)
        hangman_game.game_id = self.game_id
        hangman_game.word = self.word
        hangman_game.word_progress = self.word_progress
        hangman_game.word_length = self.word_length
        hangman_game.no_of_guesses = self.no_of_guesses
        hangman_game.game_valid = self.game_valid
        hangman_game.increment_no_of_guesses()
        self.assertEqual(hangman_game.game_id, 1)
        self.assertEqual(hangman_game.word, "test")
        self.assertEqual(hangman_game.word_progress, "____")
        self.assertEqual(hangman_game.word_length, 4)
        self.assertEqual(hangman_game.no_of_guesses, 1)
        self.assertEqual(hangman_game.game_valid, True)


class random_FunctionsAssignmentTests(unittest.TestCase):
    def setUp(self):
        self.number = random_word_id()

    def test_check_output_is_int(self):
        self.assertTrue(type(self.number) is int)

    def test_check_output_is_in_range(self):
        self.assertGreaterEqual(self.number, 1)
        self.assertLessEqual(self.number, 1000)


if __name__ == '__main__':
    unittest.main()
