import pickle
import socket
from network_constants import HEADER, PORT, FORMAT, SERVER_IP, ADDRESS_SERVER, make_header, DISCONNECT_MESSAGE


class NetworkClient:
    def __init__(self, username: str):
        self.username = username
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = SERVER_IP
        self.port = PORT
        self.address_server = ADDRESS_SERVER
        self.id_client, self.id_lobby = self.connect()
        print(f"ID CLIENT:{self.id_client}, ID LOBBY:{self.id_lobby}")

    def connect(self):
        """
        Connect to server
        :return: server's answer to player's username, answer should be tuple (id_client, id_lobby)
        """
        try:
            self.client.connect(self.address_server)
            return self.send(self.username)

            # player_id = int(self.client.recv(8).decode(FORMAT))
            # print(f"Player ID {player_id}")
            # self.client.send(str.encode(self.username))
            # return player_id
        except OSError as msg:
            print(msg)
            self.client.close()
            self.client = None

    def disconnect(self):
        self.client.close()

    def send(self, data):
        """
        Send object to server. First it sends the size of object turned into pickle and then the pickled object
        WARNING size must be a number that can be coded with 64 bits
        :param data: object to send to server
        :return: response from server
        """
        try:
            message = pickle.dumps(data)
            self.client.send(make_header(message))
            self.client.send(message)

            answer_length = self.client.recv(HEADER).decode(FORMAT)
            if answer_length:
                answer = self.client.recv(int(answer_length))
                try:
                    answer = pickle.loads(answer)
                except Exception as e:
                    print(str(e))

                return answer

        except socket.error as e:
            print(e)

        if data == DISCONNECT_MESSAGE:
            self.disconnect()
