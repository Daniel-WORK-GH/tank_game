from pygame import *
from .. import consts
from consts import colors


class Tile:
    nothing = 0
    wall = 1

    def __init__(self, id, x=0, y=0,
            width=consts.DEFAULT_TILE_SIZE,
            height=consts.DEFAULT_TILE_SIZE,
            color=colors.white):
        self.id = id
        self.color = color
        self.position = Vector2(x, y)
        self.bounds = Rect(round(x), round(y), width, height)
        self.velocity = Vector2(0, 0)

    
    def draw(self, surface):
        draw.rect(surface, colors.red, self.bounds)