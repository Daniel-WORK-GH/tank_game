import consts
import linehelper
from pygame import *
from mapobjects.tile import Tile


def clamp(x, lower, upper):
    return max(lower, min(upper, x))

def getNearestPointInPerimeter(l, t, w, h, x, y):
    r, b = l + w, t + h

    x, y = clamp(x, l, r), clamp(y, t, b)

    dl, dr, dt, db = abs(x - l), abs(x - r), abs(y - t), abs(y  - b)
    m = min(dl, dr, dt, db)

    if m == dt: return x, t
    if m == db: return x, b
    if m == dl: return l, y
    return r, y

def collide_player_world(playerpos:Vector2, corners:list[Vector2]) -> Vector2:
    smallestdistlen = 0
    smallestdistvec = Vector2(0,0)

    for corner in corners:
        for row in consts.WORLD_MAP.map:
            for tile in row:
                bounds = tile.bounds.inflate(4, 4)
                if tile.id == Tile.wall_id and bounds.collidepoint(*corner):
                    currdist = linehelper.line_length_pow2(playerpos, corner)

                    dist = getNearestPointInPerimeter(
                        bounds.left,
                        bounds.top,
                        bounds.width,
                        bounds.height,
                        corner.x,
                        corner.y
                    )

                    vec = Vector2(dist[0] - corner.x, dist[1] - corner.y)

                    newdist = linehelper.line_length_pow2(playerpos, dist)

                    if currdist > newdist:
                        playerpos += vec


    #return smallestdistvec
