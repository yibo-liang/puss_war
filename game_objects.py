
class Agent:
    def __init__(self):
        self.agent_id = 0
        self.abilities = []
        self.cat_id = 0
        self.health = 0
        self.name = ""
        self.gender = 0  # 0 female , 1 male
        self.thumbnail = ""


class Cat:
    def __init__(self):
        self.cat_id = 0
        self.abilities = []
        self.health = 0
        self.name = ""
        self.gender = 0
        self.species = ""
        self.thumbnail = ""
