import contextlib
with contextlib.redirect_stdout(None):
    import pygame

import random
from ship import Ship
from game_data import SCREEN_HEIGHT, SCREEN_WIDTH


def check_collision(sprite: pygame.sprite.Sprite, group: pygame.sprite.Group):
    return pygame.sprite.spritecollide(sprite, group, dokill=False, collided=pygame.sprite.collide_mask)


class Lobby:
    def __init__(self, _lobbyID):
        """
        Creates a lobby to play a game
        :param _lobbyID: int
        """
        self.all_players_grp = pygame.sprite.Group()
        self.all_players = {}
        self.lobbyID = _lobbyID
        self.start = False

    def add_player(self, username: str):
        """
        Add new ship object to all_players (pygame.sprite.Group)
        :param username: str
        :return: None
        """
        self.all_players_grp.add(self.create_ship(username))
        if len(self.all_players_grp.sprites()) == 2:
            self.start = True

    def create_ship(self, username: str):
        """
        Picks a start location for a player based on other player locations.
        It will ensure it does not spawn inside another player.
        :return: ship object
        """
        new_player = Ship(username)

        while True:
            new_player.rect.x = random.randrange(0, SCREEN_WIDTH)
            new_player.rect.y = random.randrange(0, SCREEN_HEIGHT)

            if not check_collision(new_player, self.all_players):
                break

        return new_player

    def get_game_objects(self):
        return {"players": self.all_players}
