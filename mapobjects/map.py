from .tile import *
import consts

class Map:
    def __init__(self,
            tilewidth=consts.DEFAULT_TILE_SIZE,
            tileheight=consts.DEFAULT_TILE_SIZE):
        self.map:list[Tile] = []
        self.tilewidth = tilewidth
        self.tileheight = tileheight


    def load(self, mapname):      
        with open(mapname) as file:
            x, y = 0, 0

            for line in file.readlines():
                idstr = line.split(',')

                for i in idstr:
                    id = int(i)

                    tile = create_tile(id,
                        x * self.tilewidth, y * self.tileheight,
                        self.tilewidth, self.tileheight)
                    self.map.append(tile)
                    
                    x = x + 1
                y, x = y + 1, 0


    def draw(self, surface):
        for tile in self.map:
            tile.draw(surface)

    