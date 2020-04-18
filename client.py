from NetworkClient import NetworkClient
from game import Game
from game_data import *
from network_constants import MessageType


def main(username: str):
    pygame.init()
    # os.environ['SDL_VIDEO_CENTERED'] = '1'  # make game window appears in the middle of the screen
    #
    # GAME_WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # pygame.display.set_caption("BattleShip Bastien")
    # pygame.display.set_icon(pygame.image.load("assets/images/warship.png"))

    client = NetworkClient(username)
    my_game = Game()
    print("This is your grid : ")
    print(my_game.my_grid)
    place_boats_old(my_game)

    print(client.send((MessageType.SEND_MY_GRID, my_game.my_grid))[1])
    print("Waiting for your opponent...")

    startGame = False
    while not startGame:
        if client.receive_from_server()[0] == MessageType.START_PLAY:
            startGame = True

    print("Start game")
    while startGame:
        turn = client.send((MessageType.WHOSE_TURN, ""))

        if turn[0] == MessageType.END_GAME:
            break
        elif turn[0] == MessageType.WHOSE_TURN:
            if turn[1] == username:  # my turn
                print("****YOUR TURN****")
                print_grids(my_game)
                while True:
                    x = int(input("Enter x guess (0-9):"))
                    if 0 <= x <= 9:
                        break
                while True:
                    y = int(input("Enter y guess (0-9):"))
                    if 0 <= y <= 9:
                        break
                my_game.attack_enemy((x, y))
                my_game.my_guessed = client.send((MessageType.SEND_MY_GUESSED, my_game.my_guessed))[1]

            else:  # opponent's turn
                print("****OPPONENT TURN****")
                print_grids(my_game)
                print("OPPONENT IS PLAYING, PLEASE WAIT...")
                answer = client.send((MessageType.UPDATED_GRID, ""))
                if answer[0] == MessageType.UPDATED_GRID:
                    my_game.my_grid = answer[1]
                print_grids(my_game)

    client.send((MessageType.DISCONNECT,))
    pygame.quit()
    quit()


def place_boats_old(game: Game):
    game.place_one_boat(BoatType.aircraft_carrier, (1, 1), Orientation.vertical)
    game.place_one_boat(BoatType.cruiser, (1, 9), Orientation.horizontal)
    game.place_one_boat(BoatType.torpedo_boat, (4, 4), Orientation.vertical)
    game.place_one_boat(BoatType.destroyer, (6, 1), Orientation.horizontal)
    game.place_one_boat(BoatType.destroyer, (6, 8), Orientation.vertical)
    game.place_one_boat(BoatType.destroyer, (8, 6), Orientation.vertical)


def place_boats(game: Game):
    boats_to_place = {"aircraft carrier": BoatType.aircraft_carrier,
                      "cruiser": BoatType.cruiser,
                      "destroyer 1": BoatType.destroyer,
                      "destroyer 2": BoatType.destroyer,
                      "torpedo_boat": BoatType.torpedo_boat}

    for item in boats_to_place.items():
        print(f"Please place your {item[0]} (length {item[1].value}):")
        while True:
            print("Press 1 for vertical, 2 for horizontal :")
            direction = int(input())
            if direction == 1 or direction == 2:
                break
        orientation = Orientation.vertical if direction == 1 else Orientation.horizontal
        x, y = -1, -1
        while not game.check_correct_boat_location(item[1], (x, y), orientation):
            print("Please enter correct location :")
            x = int(input("Choose x location of your boat (0 - 9)"))
            y = int(input("Choose y location of your boat (0 - 9)"))
        game.place_one_boat(item[1], (x, y), orientation)
        print("This is your grid : ")
        print(game.my_grid)


def print_grids(game: Game):
    print("Your guessed : ")
    print(game.my_guessed)
    print("Your grid :")
    print(game.my_grid)


if __name__ == "__main__":
    print("Welcome in BattleShip game")
    while True:
        name = input("Please enter your name: ")
        if 0 < len(name) < 20:
            break
        else:
            print("Error, this name is not allowed (must be between 1 and 19 characters [inclusive])")

    main(username=name)
