import random


def random_word_id():
    return random.randint(1, 1000)


def random_word():
    words = [line.strip() for line in open('words.txt') if len(line) == 7]
    return random.choice(words).upper()
