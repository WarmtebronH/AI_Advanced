import random

class RandomAI:
    def __init__(self, color):
        self.color = color

    def choose_move(self, game):
        board = game.board
        valid_moves = board.get_all_valid_moves(self.color)
        if valid_moves:
            return random.choice(valid_moves)
        else:
            return None
