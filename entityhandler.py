import json
from mapobjects.player import Player
from network.client import Client
from network import converter
   
idableEntities:dict[str, Player] = {}
thisPlayer = Player("tempname")

idableEntities[thisPlayer.name] = thisPlayer


def update_players(playerJsonList:str):
    players = converter.json_to_players_list(playerJsonList)

    idableEntities.clear()
    idableEntities[thisPlayer.name] = thisPlayer

    for player in players:
        # Update all other players on server, 
        # stored in [idableEntities]
        idableEntities[player.name] = player


def update(clock, events):
    thisPlayer.update(clock, events)


def draw(surface):
    for name, player in idableEntities.items():
        player.draw(surface)
    