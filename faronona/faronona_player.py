
from core import Player


class FarononaPlayer(Player):

    

    def __init__(self, name, color):

        Player.__init__(self, color)
        self.name = name
        self._reset_player_info()
        self.allow_combo = True  # true if the player decides to make a multiple move

    def _reset_player_info(self):
        self.pieces_on_board = 22

    def play(self, state):
        raise NotImplementedError