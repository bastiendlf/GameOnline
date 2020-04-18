import numpy as np


class Lobby:
    def __init__(self, _lobby_id: int, max_players: int = 2):
        """
        Creates a lobby to play a game
        :param _lobby_id: int
        :param max_players: int
        """
        self.lobbyID = _lobby_id
        self.max_players = max_players
        self.all_players = list()
        self.all_grids = dict()
        self.start = False
        self.end_turn = False
        self.current_turn = set()

    def add_player(self, player_id: int, username: str):
        """
        Add a new player in the lobby if lobby not full
        :param player_id: int
        :param username: str
        :return: None
        """
        if not self.is_full():
            self.all_players.append((player_id, username))
            print(f"[LOBBY {self.lobbyID}] {username} is connected in lobby.")
            if self.all_players.__len__() == 1:
                self.current_turn = username

    def change_turn(self):
        if self.current_turn == self.all_players[0][1]:
            self.current_turn = self.all_players[1][1]
        elif self.current_turn == self.all_players[1][1]:
            self.current_turn = self.all_players[0][1]
        print(f"[LOBBY {self.lobbyID}] Current turn:" + str(self.current_turn))

    def add_grid_player(self, player_id: int, grid: np.ndarray):
        self.all_grids[str(player_id)] = grid
        if self.all_players.__len__() == self.all_grids.__len__() == self.max_players:
            self.start = True

    def is_full(self):
        return self.max_players == len(self.all_players)

    def get_number_players_connected(self):
        return len(self.all_players)

    def remove_player(self, player_id: int, username: str):
        """
        Remove player from all_players dict
        :param username: str
        :param player_id: int
        :return: None
        """
        self.all_players.remove((player_id, username))
        del self.all_grids[str(player_id)]
