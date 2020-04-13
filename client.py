import os

from NetworkClient import NetworkClient
from game_data import *
from network_constants import DISCONNECT_MESSAGE, GET_PLAYERS


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

    run = True
    clock = pygame.time.Clock()
    all_players = client.send(GET_PLAYERS)

    current_ID = client.id_client

    while run:
        clock.tick(60)
        player = all_players[current_ID]

        player.move()
        all_players = client.send(player)

        for event in pygame.event.get():
            # if user hits red x button close window
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                # if user hits a escape key close program
                if event.key == pygame.K_ESCAPE:
                    run = False

        redraw_window(GAME_WINDOW, all_players)

    client.send(DISCONNECT_MESSAGE)
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
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # make game window appears in the middle of the screen

    GAME_WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Rocket Bastien")
    pygame.display.set_icon(pygame.image.load("assets/images/rocket.png"))

    main(username=name)
