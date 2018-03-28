from game_handler.game_thread import GameThread
from game_handler.game_settlement_handler import SettlementHandler
import uuid


class Event:
    def __init__(self, function):
        self.id = uuid.uuid4()
        self.function = function


def trigger(self, e):
    self.function(e)


class GameEventsHandler:
    def __init__(self, game_thread):
        self.game_thread = game_thread
        self.events = {
            "gamestart": [],
            "playerstart": [],
            "playershuffle": [],
            "playerdrawcard": [],
            "playerusecard": [],
            "playerdiscard": [],
            "playerendterm": [],
            "dealdamage": [],
            "receivedamage": [],
            "cardtargeted": [],
            "abilityargeted": [],

        }

    def init(self):
        self.settlement_handler = self.game_thread.settlement_handler

    def trigger(self, event_name, data):
        handlers = self.events[event_name]
        for handler in handlers:
            handler.trigger(data)

    def add_event_listener(self, name, func):
        event = Event(func)
        self.events[name].append(event)
        return event.id

    def remove_event_listener(self, name, id):
        handlers = self.events[name]
        for i in range(len(handlers)):
            if handlers[i].id == id:
                handlers.pop(i)
                break
