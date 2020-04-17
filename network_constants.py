import pickle
import socket
from enum import Enum

SERVER_IP = "192.168.1.18"
PORT = 5050
HEADER = 128
FORMAT = 'utf-8'
ADDRESS_SERVER = (SERVER_IP, PORT)

MAX_PLAYERS_LOBBY = 2


class MessageType(Enum):
    DISCONNECT = "!DISCONNECT"
    GET = "GET"
    SEND_MY_GRID = "SEND_MY_GRID"
    SEND_MY_GUESSED = "SEND_MY_GUESSED"
    REPLY_ACK = "REPLY_ACK"
    REPLY_DISCONNECT = "REPLY_DISCONNECT"
    WHOSE_TURN = "WHOSE_TURN"
    START_PLAY = "START_PLAY"
    END_GAME = "END_GAME"


class LobbyStatus(Enum):
    WAIT_FOR_PLAYERS = "WAIT_FOR_PLAYERS"
    WAIT_FOR_GRIDS = "WAIT_FOR_GRIDS"
    START_PLAY = "START_PLAY"
    WAIT_FOR_GUESS_GRID = "WAIT_FOR_GUESS_GRID"


def make_header(message: bytes):
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)

    # complete header with ' ' to make the header the size of FORMAT
    send_length += b' ' * (HEADER - len(send_length))

    return send_length


def send_data_pickle(conn: socket, data):
    """
    Send data turned into pickle to conn
    :param conn: socket
    :param data: data to send
    :return: None
    """
    data_pickle = pickle.dumps(data)
    conn.send(make_header(data_pickle))
    conn.sendall(data_pickle)


def receive_data_pickle(conn: socket):
    """
    receive a data with header
    :param conn: socket
    :return: unpickle object
    """
    msg_length = conn.recv(HEADER).decode(FORMAT)  # get the length of the incoming msg
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length)  # adjust the buffer size
        message_object = pickle.loads(msg)
        return message_object
