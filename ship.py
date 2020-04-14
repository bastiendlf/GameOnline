from game_data import *


class Ship(pygame.sprite.Sprite):
    def __init__(self, _client_ID: int, username: str, x: int = 0, y: int = 0):
        """
        Creates a ship for game. One ship = 1 player
        :param _client_ID: int
        :param username: string
        :param x: int
        :param y: int
        """

        super().__init__()

        self.client_ID = _client_ID
        self.username = username

        # Display settings
        self.screenWidth = SCREEN_WIDTH
        self.screenHeight = SCREEN_HEIGHT
        self.image = pygame.transform.scale(pygame.image.load("assets/images/rocket.png"), PLAYER_SIZE)
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        # Position settings
        self.rect.x = x if x < self.screenWidth + self.width else 0
        self.rect.y = y if y < self.screenHeight + self.height else 0

        # Movement settings
        self.velocity = 5

    def move(self):
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.x > 0:
            self.rect.x -= self.velocity

        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.x + self.width < self.screenWidth:
            self.rect.x += self.velocity

        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.y > 0:
            self.rect.y -= self.velocity

        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.y + self.height < self.screenHeight:
            self.rect.y += self.velocity
