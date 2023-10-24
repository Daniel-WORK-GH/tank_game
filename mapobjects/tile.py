from pygame import *
import consts
from consts import colors
from mapobjects import transform


class Tile:
    nothing_id = 0
    wall_id = 1
    spawn_id = 2

    def __init__(self, id, x=0, y=0,
            width=consts.DEFAULT_TILE_SIZE,
            height=consts.DEFAULT_TILE_SIZE,
            color=colors.white):
        self.id = id
        self.color = color
        self.position = Vector2(x, y)
        self.bounds = Rect(round(x), round(y), width, height)


    def set_data(self, x, y, width, height):
        self.set_location(x, y)
        self.set_size(width, height)


    def set_location(self, x, y):
        self.position.x = x
        self.position.y = y
        self.bounds.x = round(x)
        self.bounds.y = round(y)


    def set_size(self, width, height):
        self.bounds.width = width
        self.bounds.height = height


    def clone(self) -> "Tile":
        return Tile(self.id,
                self.position.x, self.position.y,
                self.bounds.w, self.bounds.h,
                self.color)

    
    def draw(self, surface, trans:transform.Transform):
        if self.id == Tile.wall_id:
            if trans:
                newpos = transform.transformPoint(self.position, trans.position, 0)
                newbounds = Rect(*newpos, *self.bounds.size)
                draw.rect(surface, self.color, newbounds)
            else:
                draw.rect(surface, self.color, self.bounds)


tile_ids = {
    Tile.nothing_id : Tile(Tile.nothing_id),
    Tile.wall_id : Tile(Tile.wall_id, color=consts.colors.black),
    Tile.spawn_id : Tile(Tile.spawn_id, color=consts.colors.grass_light)
}


def create_tile(id, x, y, width, height):
    tile = tile_ids[id].clone()
    tile.set_data(x, y, width, height)
    return tile