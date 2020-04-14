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
        self.all_players = dict()
        self.lobbyID = _lobbyID
        self.start = False

    def add_player(self, user_id: int, username: str):
        """
        Add new ship object to all_players (pygame.sprite.Group)
        :param user_id: int
        :param username: str
        :return: None
        """

        new_player = self.create_ship(user_id, username)
        self.all_players_grp.add(new_player)
        self.all_players[str(user_id)] = new_player

        if len(self.all_players_grp.sprites()) == 2:
            self.start = True

    def create_ship(self, user_id, username: str):
        """
        Picks a random start location for a player based on other player locations.
        It will ensure it does not spawn inside another player.
        :return: ship object
        """
        new_player = Ship(user_id, username)

        while True:
            new_player.rect.x = random.randrange(0, SCREEN_WIDTH)
            new_player.rect.y = random.randrange(0, SCREEN_HEIGHT)

            if not check_collision(new_player, self.all_players_grp):
                break

        return new_player

    def delete_player(self, user_id):
        self.all_players[str(user_id)].kill()  # remove from all groups
        del (self.all_players[str(user_id)])  # del element in players' list
