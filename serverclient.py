from server import ThreadServer
from client import Client

from player import Player
import converter

import time

server = ThreadServer("127.0.0.1", 20_001)
server.start()

p1 = Player("player1", 10, 10)
p2 = Player("player2", 10, 10)

# player 1
client = Client()
client.connect("127.0.0.1", 20_001)
client.send(converter.player_to_json(p1))
time.sleep(1)
print(client.recv())


# player 2
client.connect("127.0.0.1", 20_001)
client.send(converter.player_to_json(p2))
time.sleep(1)
print(client.recv())


server.stop()
