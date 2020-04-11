import pygame
import os
from game_data import *
from game import Game
from ship import Ship

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'  # make game window appears in the middle of the screen

GAME_WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rocket Bastien")

game = Game(GAME_WINDOW)


def redraw_window(screen: pygame.Surface, players: pygame.sprite.Group):
    screen.blit(images["bg"], (0, 0))
    players.draw(screen)
    pygame.display.flip()


def main():
    run = True
    clock = pygame.time.Clock()
    player_ID = 0
    players = pygame.sprite.Group()
    players.add(Ship(game))

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
