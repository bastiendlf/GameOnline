from NetworkClient import NetworkClient
from game_data import *
from network_constants import DISCONNECT_MESSAGE


def redraw_window(screen: pygame.Surface, players: pygame.sprite.Group):
    """
    redraw all objects on screen window
    :param screen: pygame.Surface
    :param players: pygame.sprite.Group
    :return: None
    """
    screen.blit(BACKGROUND, (0, 0))
    players.draw(screen)
    pygame.display.flip()


def check_collision(sprite: pygame.sprite.Sprite, group: pygame.sprite.Group):
    return pygame.sprite.spritecollide(sprite, group, dokill=False, collided=pygame.sprite.collide_mask)


def main(username: str):
    client = NetworkClient(username)

    print(client.send("coucou1"))
    input()
    print(client.send("je suis trop content lol"))
    input()
    print(client.send("dernier message"))
    input()
    print(client.send(DISCONNECT_MESSAGE))
    pygame.quit()
    quit()


if __name__ == "__main__":
    while True:
        name = input("Please enter your name: ")
        if 0 < len(name) < 20:
            break
        else:
            print("Error, this name is not allowed (must be between 1 and 19 characters [inclusive])")

    pygame.init()
    # os.environ['SDL_VIDEO_CENTERED'] = '1'  # make game window appears in the middle of the screen
    #
    # GAME_WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # pygame.display.set_caption("Rocket Bastien")
    # pygame.display.set_icon(pygame.image.load("assets/images/rocket.png"))

    main(username=name)
