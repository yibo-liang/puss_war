# An action is a result from using a card or an ability
# Actions will be added to queues of actions
# Action will make direct change of current game data
class Action:
    def __init__(self, game_entity):
        self.id = 0
        self.name = ""
        self.description = ""
        self.game_entity = game_entity

    def act(self):
        return True


