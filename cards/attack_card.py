# sample action
import sys

# Add the ptdraft folder path to the sys.path list
sys.path.append('../interface/')
from card import Card


class AttackCard(Card):
    def play(self, game_entity, owner, sources, targets):
        self.owner = owner
        self.game_entity = game_entity
        self.sources = sources
        self.targets = targets

        return True
