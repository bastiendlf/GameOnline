import pickle
import socket
from network.network_constants import HEADER, PORT, FORMAT, SERVER, ADDRESS_SERVER, make_header, DISCONNECT_MESSAGE


class NetworkClient:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = SERVER
        self.port = PORT
        self.address_server = ADDRESS_SERVER
        self.player = self.connect()
        print(self.player)

    def connect(self):
        try:
            self.client.connect(self.address_server)
            return pickle.loads(self.client.recv(2048))
        except OSError as msg:
            print(msg)
            self.client.close()
            self.client = None

    def get_player(self):
        return self.player

    def disconnect(self):
        self.client.close()

    def send(self, data):
        """
        Send object to server. First it sends the size of object turned into pickle and then the pickled object
        WARNING size must be a number that can be coded with 64 bits
        :param data: python object to send to server
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
