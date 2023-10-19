from pygame import *
import consts
from consts import colors


class Tile:
    nothing_id = 0
    wall_id = 1

    def __init__(self, id, x=0, y=0,
            width=consts.DEFAULT_TILE_SIZE,
            height=consts.DEFAULT_TILE_SIZE,
            color=colors.white):
        self.id = id
        self.color = color
        self.position = Vector2(x, y)
        self.bounds = Rect(round(x), round(y), width, height)
        self.velocity = Vector2(0, 0)


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

    
    def draw(self, surface):
        if self.id != Tile.nothing_id:
            draw.rect(surface, self.color, self.bounds)


tiles = {
    Tile.nothing_id : Tile(Tile.nothing_id),
    Tile.wall_id : Tile(Tile.wall_id, color=consts.colors.black)
}


def create_tile(id, x, y, width, height):
    tile = tiles[id].clone()
    tile.set_data(x, y, width, height)
    return tile