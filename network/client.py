from network.network_constants import DISCONNECT_MESSAGE
from network.NetworkClient import NetworkClient


client = NetworkClient()

print(client.send("hello from ME "))
input()
print(client.send("Lille very nice"))
input()
print(client.send(DISCONNECT_MESSAGE))
