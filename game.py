import pygame
from ship import Ship


class Game:
    def __init__(self, screen):
        self.screen = screen

    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, dokill=False, collided=pygame.sprite.collide_mask)
