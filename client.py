import numpy as np

from NetworkClient import NetworkClient
from game_data import *
from network_constants import NetworkRequests


def main(username: str):
    pygame.init()
    # os.environ['SDL_VIDEO_CENTERED'] = '1'  # make game window appears in the middle of the screen
    #
    # GAME_WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # pygame.display.set_caption("Rocket Bastien")
    # pygame.display.set_icon(pygame.image.load("assets/images/rocket.png"))
    client = NetworkClient(username)

    print(client.send("coucou1"))
    input()
    print(client.send(np.zeros((10, 10), dtype=int)))
    print(client.send(NetworkRequests.DISCONNECT))
    pygame.quit()
    quit()


if __name__ == "__main__":
    while True:
        name = input("Please enter your name: ")
        if 0 < len(name) < 20:
            break
        else:
            print("Error, this name is not allowed (must be between 1 and 19 characters [inclusive])")

    main(username=name)
