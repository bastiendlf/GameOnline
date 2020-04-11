SERVER = "192.168.1.22"
PORT = 5050
HEADER = 128
FORMAT = 'utf-8'
ADDRESS_SERVER = (SERVER, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"


def make_header(message: bytes):
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)

    # complete header with ' ' to make the header the size of FORMAT
    send_length += b' ' * (HEADER - len(send_length))

    return send_length
