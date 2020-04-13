from network_constants import DISCONNECT_MESSAGE
from NetworkClient import NetworkClient


client = NetworkClient("Albert")

input()
print(client.send("Message 1"))
input()
print(client.send("Message 2"))
input()
print(client.send("message 3"))
input()
print(client.send(DISCONNECT_MESSAGE))

while True:
    i = 1