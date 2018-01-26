# sample action
import sys

# Add the ptdraft folder path to the sys.path list
sys.path.append('../interface/')
from action import *


class Attack_Action(Action):
    def __init__(self, game_entity):
        Action.__init__(self, game_entity)
        self.id = 1
        self.name = "Attack"
        self.description = ""
        self.game_entity = game_entity
        self.targets = []
        self.sources = []
        self.damage = 0
        self.cancelled = False

    def act(self):
        if self.cancelled:
            return True
        for target in self.targets:
            target["hp"] -= self.damage
        return True
