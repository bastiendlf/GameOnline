import pygame
from ship import Ship


class Lobby:
    def __init__(self, _lobbyID):
        """
        Creates a lobby to play a game
        :param _lobbyID: int
        """
        self.all_players = pygame.sprite.Group()
        self.lobbyID = _lobbyID
        self.start = False

    def add_player(self, player: Ship):
        self.all_players.add(player)
        if len(self.all_players.sprites()) == 2:
            self.start = True

