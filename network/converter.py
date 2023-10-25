import json
import copy
from mapobjects.player import Player, Rocket


def player_to_json(player:Player) -> str:
    x, y = player.position
    _, _, w, h = player.bounds
    hw, hh = player.headsize
    angle = player.bodyangle
    headangle = player.headangle
    playershot = player.shot
    elptime = player.elapsedcooldown   

    shotdict = None
    if playershot:
        shotsource = playershot.player
        start = (playershot.start[0], playershot.start[1])
        direction =(playershot.direction[0], playershot.direction[1])
        end = playershot.end
        shotdict = {'player':shotsource, 'start':start, 'direction':direction, 'end':end}

    ret = {
        "name":player.name,
        "position":(x, y),
        "size":(w, h),
        "headsize":(hw, hh),
        "angle":angle,
        "headangle":headangle,
        "elapsedtime":elptime,
        "shot":shotdict
    }

    return json.dumps(ret)


def set_player_data(player:Player, playerJsonData:str):
    dic = json.loads(playerJsonData)
    name = dic['name']
    position = dic['position']
    size = dic['size']
    headsize = dic['headsize']
    angle = dic['angle']
    headangle = dic['headangle']
    elptime = dic['elapsedtime']
    shot = dic['shot']

    rocket = None

    if shot:
        rocket = Rocket(shot['player'], shot['start'], shot['direction'], shot['end'])            

    player.set_data(name, position[0], position[1], size[0], size[1], headsize[0], headsize[1], angle, headangle, rocket, elptime)


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
