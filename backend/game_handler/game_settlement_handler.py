from game_handler.game_operator import GameOperator
from game_handler.game_thread import GameThread
from queue import PriorityQueue
import queue


class PriorityQueueNative(PriorityQueue):
    def __init__(self):
        PriorityQueue.__init__(self)
        self.counter = 0

    def put(self, item, priority):
        PriorityQueue.put(self, (priority, self.counter, item))
        self.counter += 1

    def get(self, *args, **kwargs):
        _, _, item = PriorityQueue.get(self, *args, **kwargs)
        return item


class SettlementHandler:
    def __init__(self, game_thread):
        self.game_thread = game_thread
        self.game_operator = None
        self.settlement_queue = PriorityQueueNative()
        self.settlement_count = 0

    def init(self):
        self.game_operator = self.game_thread.game_operator

    def new_settlement(self, settlement_args, priority):
        self.settlement_queue.put(settlement_args, priority)

    def do_next_settlement(self):
        try:
            next_settlement = self.settlement_queue.get(block=False)
            settlement_result = self.do_settlement(next_settlement)
            return settlement_result
        except queue.Empty:
            return None

    def do_settlement(self, settlement_args):
        name = settlement_args["SETTLEMENT"]

        def draw_card(settlement):
            player_i = settlement["PLAYER_I"]
            unit_type = settlement["UNIT_TYPE"]
            success, card_drawn = self.game_operator.draw_from_deck(unit_type=unit_type, player_i=player_i)
            if success:
                return {
                    "SETTLEMENT_RESULT": "UPDATE_CARD",
                    "CARD_UUID": card_drawn["uuid"],
                    "UPDATE": {
                        "position": "hand"
                    }
                }
            else:
                raise Exception("Unexpected error when drawing card")

        settlements = {
            "DRAW_CARD": draw_card,
            "PLAYER_ACTION": None
        }

        return settlements[name](settlement_args)
