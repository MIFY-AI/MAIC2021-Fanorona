
from faronona.faronona_player import FarononaPlayer
from faronona.faronona_rules import FarononaRules
import random


class AI(FarononaPlayer):

    name = "War of Hearts"

    def __init__(self, color):
        super(AI, self).__init__(self.name, color)
        self.position = color.value

    def play(self, state, remain_time):

        return FarononaRules.random_play(state, self.position)
