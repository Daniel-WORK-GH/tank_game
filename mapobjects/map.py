from .tile import *
import consts

class Map:
    def __init__(self,
            tilewidth=consts.DEFAULT_TILE_SIZE,
            tileheight=consts.DEFAULT_TILE_SIZE):
        self.map:list[list[Tile]] = []
        self.tilewidth = tilewidth
        self.tileheight = tileheight
        self.width = 0
        self.height = 0
        self.availablespawns = []


    def get_tiles_in_range(self, center:Vector2, viewrange:tuple[int, int]):
        vx, vy = viewrange
        x, y = center

        x = round(x / consts.DEFAULT_TILE_SIZE)
        y = round(y / consts.DEFAULT_TILE_SIZE)

        startx = x - vx
        starty = y - vy

        diffx, diffy = 0, 0

        if startx < 0: 
            diffx = -startx
            startx = 0
        if starty < 0:
            diffy = -starty
            starty = 0

        endx = x + vx + diffx
        endy = y + vy + diffy

        diffx, diffy = 0, 0

        if endx > self.width: 
            diffx = endx - self.width
            endx = self.width
        if endy > self.height: 
            diffy = endy - self.height
            endy = self.height

        startx -= diffx
        starty -= diffy

        if startx < 0: startx = 0
        if starty < 0: starty = 0

        for y in range(starty, endy):
            for x in range(startx, endx):
                yield self.map[y][x]


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
                    
                    if id == Tile.spawn_id:
                        self.availablespawns.append(tile.bounds.center)

                    row.append(tile)  
                    x = x + 1
                    self.width = x

                self.map.append(row)
                y, x = y + 1, 0
                self.height = y


    def draw(self, surface, center, transform:transform.Transform):
        for tile in self.get_tiles_in_range(center, consts.VIEW_RANGE):
            tile.draw(surface, transform)

    