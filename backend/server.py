# Main file to start with
from serving.communication import start_wsserver
from game_matching import game_creator,queue_manager
def main():
    # start login service
    start_wsserver()
    # start matching service
    queue_manager.QueueManager.start_matching_service()
    # start game manager
    game_creator.MatchedGameManager.start_creator_service()
    # start info logger / monitor
    pass


if __name__ == "__main__":
    main()
