import linehelper
import consts
import math as Math
from pygame import *
from mapobjects.tile import Tile
from mapobjects.map import Map


def get_tile_corners(tile:Tile):
        yield tile.bounds.topleft
        yield tile.bounds.topright
        yield tile.bounds.bottomright
        yield tile.bounds.bottomleft


def get_edges(tile:Tile):
    yield (tile.bounds.topleft, tile.bounds.topright)
    yield (tile.bounds.topright, tile.bounds.bottomright)
    yield (tile.bounds.bottomright, tile.bounds.bottomleft)
    yield (tile.bounds.bottomleft, tile.bounds.topleft)


def get_tile_at(map:Map, x:float, y:float):
    x = Math.floor(x / consts.DEFAULT_TILE_SIZE)
    y = Math.floor(y / consts.DEFAULT_TILE_SIZE)

    if x < 0 or y < 0: return
    if x >= map.width or y >= map.height: return

    return map.map[y][x]


def enumarate_tile_row(map:Map, start:tuple[float, float], end:tuple[float, float]):
    STEP = 0.8
    MAXITR = 60
    
    dx, dy = linehelper.normalize_line(start, end)

    dx *= consts.DEFAULT_TILE_SIZE
    dy *= consts.DEFAULT_TILE_SIZE

    x, y = start

    checked = []
    maxdistance = linehelper.line_length_pow2(start, end)

    itr = 0
    while itr < MAXITR:
        nx, ny = x + STEP * dx, y + STEP * dy 

        rx, ry, rw, rh = linehelper.line_bounding_rect((x, y), (nx, ny))

        t1 = get_tile_at(map, rx, ry)
        t2 = get_tile_at(map, rx + rw, ry)
        t3 = get_tile_at(map, rx, ry + rh)
        t4 = get_tile_at(map, rx + rw, ry + rh)
        
        if (not t1) and (not t2) and (not t3) and (not t4):
            return
        
        if linehelper.line_length_pow2(start, (x, y)) > maxdistance:
            return

        if t1 not in checked:
            yield t1
            checked.append(t1)

        if t2 not in checked:
            yield t2
            checked.append(t2)

        if t3 not in checked:
            yield t3
            checked.append(t3)

        if t4 not in checked:
            yield t4
            checked.append(t4)

        x, y = nx, ny

        itr += 1