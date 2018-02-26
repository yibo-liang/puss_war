# Main file to start with
from serving.communication import start_wsserver
def main():
    # start login service
    start_wsserver()
    # start matching service
    # start game manager
    # start info logger / monitor
    pass


if __name__ == "__main__":
    main()
