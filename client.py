from NetworkClient import NetworkClient
from game import Game
from game_data import *
from network_constants import MessageType


def main(username: str):
    pygame.init()
    # os.environ['SDL_VIDEO_CENTERED'] = '1'  # make game window appears in the middle of the screen
    #
    # GAME_WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # pygame.display.set_caption("Rocket Bastien")
    # pygame.display.set_icon(pygame.image.load("assets/images/rocket.png"))

    client = NetworkClient(username)
    my_game = Game()
    place_boats(my_game)
    print(client.send((MessageType.SEND_MY_GRID, my_game.my_grid))[1])

    startGame = False
    while not startGame:
        if client.receive_from_server()[0] == MessageType.START_PLAY:
            startGame = True

    print("Start game")

    client.send((MessageType.DISCONNECT,))
    pygame.quit()
    quit()


def place_boats(game: Game):
    game.place_one_boat(BoatType.aircraft_carrier, (1, 1), Orientation.vertical)
    game.place_one_boat(BoatType.cruiser, (1, 9), Orientation.horizontal)
    game.place_one_boat(BoatType.torpedo_boat, (4, 4), Orientation.vertical)
    game.place_one_boat(BoatType.destroyer, (6, 1), Orientation.horizontal)
    game.place_one_boat(BoatType.destroyer, (6, 8), Orientation.vertical)
    game.place_one_boat(BoatType.destroyer, (8, 6), Orientation.vertical)


if __name__ == "__main__":
    while True:
        name = input("Please enter your name: ")
        if 0 < len(name) < 20:
            break
        else:
            print("Error, this name is not allowed (must be between 1 and 19 characters [inclusive])")

    main(username=name)
