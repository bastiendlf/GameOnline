import os

from game_data import *
from ship import Ship

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'  # make game window appears in the middle of the screen

GAME_WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rocket Bastien")
pygame.display.set_icon(pygame.image.load("assets/images/rocket.png"))


def redraw_window(screen: pygame.Surface, players: pygame.sprite.Group):
    screen.blit(BACKGROUND, (0, 0))
    players.draw(screen)
    pygame.display.flip()


def check_collision(sprite: pygame.sprite.Sprite, group: pygame.sprite.Group):
    return pygame.sprite.spritecollide(sprite, group, dokill=False, collided=pygame.sprite.collide_mask)


def main():
    run = True
    clock = pygame.time.Clock()
    players = pygame.sprite.Group()
    players.add(Ship("bastien", x=50, y=300))

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        for player in players:
            player.move()
        redraw_window(GAME_WINDOW, players)


if __name__ == "__main__":
    main()
