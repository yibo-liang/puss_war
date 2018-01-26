# sample action
import sys

# Add the ptdraft folder path to the sys.path list
sys.path.append('../interface/')
from ability import Ability


class TheWorld(Ability):
    def __init__(self):
        Ability.__init__(self)
        self.id = 0
        self.description = "Spending 50% of your maximum action point in your next round" \
                           "and stop the time. Your opponent will skip next round"

    def operate(self, game_entity, owner):
        # make the opposite player skip next term
        return False
