# Prototype for ability
class Ability:
    def __init__(self):
        self.id = ""
        self.name = ""
        self.description = ""

        # ability type
        # 0 active ability
        # 1 passive ability
        self.type = 0

    # override this function
    def operate(self, game_entity, owner):
        # return False if ability fails to operate
        return False

        # test ability
