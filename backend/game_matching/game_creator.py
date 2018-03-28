import queue
from game_handler.game_thread import GameThread
import threading


class MatchedGameManager:
    matched_players = queue.Queue()
    active_games = []

    @staticmethod
    def add_matched_player(players):
        MatchedGameManager.matched_players.put(players)
        print("Added new match info {}".format(players))

    @staticmethod
    def start_creator_service():
        def s():
            while True:
                print("Trying to create game from matched_players")
                info = MatchedGameManager.matched_players.get()

                new_game = GameThread(info)

                print("New Game created.")
                new_game.start()

        threading.Thread(target=s).start()
