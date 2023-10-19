import json
from player import Player


def player_to_json(player:Player) -> str:
    x, y = player.position
    _, _, w, h = player.bounds
    return json.dumps({"name":player.name, "position":(x, y), "size":(w, h)})


def set_player_data(player:Player, playerJsonData:str):
    dic = json.loads(playerJsonData)
    name = dic['name']
    position = dic['position']
    size = dic['size']

    player.set_data(name, position[0], position[1], size[0], size[1])


def json_to_player(jsonData:str) -> Player:
    player = Player()
    set_player_data(player, jsonData)
    return player
    


def player_list_to_json(players:list[Player]) -> str:
    jsonlist = []

    for p in players:
        jsonlist.append(player_to_json(p))
        
    return json.dumps(jsonlist)


def json_to_players_list(jsonPlayerList:str) -> list[Player]:
    jsonlist = json.loads(jsonPlayerList)
    playerlist = []

    for j in jsonlist:
        playerlist.append(json_to_player(j))

    return playerlist
