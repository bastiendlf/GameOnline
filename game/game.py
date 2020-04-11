import pygame
import os
from game.game_data import *

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'  # make game window appears in the middle of the screen

GAME_WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rocket Bastien")


