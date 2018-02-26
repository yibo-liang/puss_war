
import queue
from game_handler.game_thread import GameThread

class MatchedGameManager:
    matched_players = queue.Queue()
    active_games = []

    @staticmethod
    def add_matched_player(players):
        MatchedGameManager.matched_players.put(players)

    @staticmethod
    def start_creator_service():
        def s():
            while True:
                cookies = MatchedGameManager.matched_players.get()
                new_game = GameThread(cookies)
                new_game.start()
                print("New Game created.")