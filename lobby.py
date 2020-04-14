import contextlib

with contextlib.redirect_stdout(None):
    pass


class Lobby:
    def __init__(self, _lobbyID: int, max_players: int = 2):
        """
        Creates a lobby to play a game
        :param _lobbyID: int
        :param max_players: int
        """
        self.lobbyID = _lobbyID
        self.max_players = max_players
        self.all_players = dict()
        self.start = False

    def add_player(self, player_id: int, username: str):
        """
        Add a new player in the lobby if lobby not full
        :param player_id: int
        :param username: str
        :return: None
        """
        if len(self.all_players) < self.max_players:
            self.all_players[str(player_id)] = username
            print(f"[LOBBY] {username} is connected in lobby number {self.lobbyID}")

    def is_full(self):
        return self.max_players == len(self.all_players)

    def get_number_players_connected(self):
        return len(self.all_players)

    def remove_player(self, playerID: int):
        """
        Remove player from all_players dict
        :param playerID: int
        :return: None
        """
        del (self.all_players[str(playerID)])
