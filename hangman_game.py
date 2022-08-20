# from app import app
# from random_functions import *
#
#
# class Game(db.Model):
#     id = db.Column(db.Integer, primary_key=True, default=random_word_id())
#     word = db.Column(db.String(7), default=random_word)
#     tried = db.Column(db.String(50), default='')
#     player = db.Column(db.String(50))
#
#     def __init__(self, player):
#         self.player = player
#
#     @property
#     def errors(self):
#         return ''.join(set(self.tried) - set(self.word))
#
#     @property
#     def current(self):
#         return ''.join([c if c in self.tried else '_' for c in self.word])
#
#     @property
#     def points(self):
#         return 100 + 2 * len(set(self.word)) + len(self.word) - 10 * len(self.errors)
#
#     # Play
#
#     def try_letter(self, letter):
#         if not self.finished and letter not in self.tried:
#             self.tried += letter
#             db.session.commit()
#
#     # Game status
#
#     @property
#     def won(self):
#         return self.current == self.word
#
#     @property
#     def lost(self):
#         return len(self.errors) == 6
#
#     @property
#     def finished(self):
#         return self.won or self.lost
