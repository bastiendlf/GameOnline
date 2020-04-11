import pygame
from game_data import *


class Ship(pygame.sprite.Sprite):
    def __init__(self, Game, x: int = 0, y: int = 0):

        super().__init__()

        # Display settings
        self.game = Game
        self.screen = self.game.screen
        self.screenWidth, self.screenHeight = self.screen.get_rect().size
        self.image = images["ship"]
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        # Position settings
        self.rect.x = x
        self.rect.y = y

        # Movement settings
        self.velocity = 5

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.velocity

        if keys[pygame.K_RIGHT] and self.rect.x + self.width < self.screenWidth:
            self.rect.x += self.velocity

        if keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= self.velocity

        if keys[pygame.K_DOWN] and self.rect.y + self.height < self.screenHeight:
            self.rect.y += self.velocity
