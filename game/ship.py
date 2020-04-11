import pygame
from game.game_data import *


class Player(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface, x: int = 0, y: int = 0):

        super().__init__()

        # Display settings
        self.screen = screen
        self.screenWidth, self.screenHeight = self.screen.get_rect().size
        self.image = images["ship"]
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        # Position settings
        self.x = x
        self.y = y

        # Movement settings
        self.velocity = 5

    def mov_right(self):
        if self.x + self.width < self.screenWidth:
            self.rect.x += self.velocity

    def mov_left(self):
        if self.x > 0:
            self.rect.x -= self.velocity

    def mov_down(self):
        if self.y + self.height < self.screenHeight:
            self.rect.y += self.velocity

    def mov_up(self):
        if self.y > 0:
            self.rect.y -= self.velocity
