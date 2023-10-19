from .tile import *
import consts

class Map:
    def __init__(self,
            tilewidth=consts.DEFAULT_TILE_SIZE,
            tileheight=consts.DEFAULT_TILE_SIZE):
        self.map:list[list[Tile]] = []
        self.tilewidth = tilewidth
        self.tileheight = tileheight

    def load(self, mapname):      
        with open(mapname) as file:
            x, y = 0, 0

            for line in file.readlines():
                idstr = line.split(',')

                row = []
                for i in idstr:
                    id = int(i)

                    tile = create_tile(id,
                        x * self.tilewidth, y * self.tileheight,
                        self.tilewidth, self.tileheight)
                    
                    row.append(tile)
                    x = x + 1

                self.map.append(row)
                y, x = y + 1, 0

    def draw(self, surface):
        for row in self.map:
            for tile in row:
                tile.draw(surface)

    