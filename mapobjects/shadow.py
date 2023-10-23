import consts
import math as Math
import linehelper
from pygame import *
from mapobjects.tile import Tile
from mapobjects.map import Map

class Shadow:
    def __init__(self, surface:Surface, map:Map):
        self.map = map
        self.surface = Surface(surface.get_size(), SRCALPHA)
        self.mappoints = self.create_map_points()
 

    def get_corners(self, tile:Tile):
        yield tile.bounds.topleft
        yield tile.bounds.topright
        yield tile.bounds.bottomright
        yield tile.bounds.bottomleft


    def get_edges(self, tile:Tile):
        yield (tile.bounds.topleft, tile.bounds.topright)
        yield (tile.bounds.topright, tile.bounds.bottomright)
        yield (tile.bounds.bottomright, tile.bounds.bottomleft)
        yield (tile.bounds.bottomleft, tile.bounds.topleft)


    def get_tile_at(self, x:float, y:float):
        x = Math.floor(x / consts.DEFAULT_TILE_SIZE)
        y = Math.floor(y / consts.DEFAULT_TILE_SIZE)

        if x < 0 or y < 0: return
        if x >= self.map.width or y >= self.map.height: return

        return self.map.map[y][x]
    

    def enumarate_tile_row(self, start:tuple[float, float], end:tuple[float, float]):
        STEP = 0.8
        MAXITR = 40
        
        dx, dy = linehelper.normalize_line(start, end)

        dx *= consts.DEFAULT_TILE_SIZE
        dy *= consts.DEFAULT_TILE_SIZE

        x, y = start

        itr = 0
        while itr < MAXITR:
            nx, ny = x + STEP * dx, y + STEP * dy 

            rx, ry, rw, rh = linehelper.line_bounding_rect((x, y), (nx, ny))

            yield self.get_tile_at(rx, ry)
            yield self.get_tile_at(rx + rw, ry)
            yield self.get_tile_at(rx, ry + rh)
            yield self.get_tile_at(rx + rw, ry + rh)

            x, y = nx, ny
            itr += 1

    
    def create_map_points(self) -> list[Vector2]:
        points:list[Vector2] = []
        count:list[int] = []
        
        for row in self.map.map:
            for tile in row:
                for corner in self.get_corners(tile):
                    if tile.id != Tile.nothing_id:
                        if corner in points:
                            count[points.index(corner)] += 1
                        else:
                            points.append(corner)
                            count.append(1)

        w, h = self.surface.get_size()
        points.append((0, 0))
        points.append((w, 0))
        points.append((w, h))
        points.append((0, h))
        count.extend((1, 1, 1, 1))

        return [points[i] for i in range(0, len(points)) if count[i] != 4 and count[i] != 2]


    def project_vectors(self, center:Vector2) -> list[Vector2, Vector2]:
        vectors:list[tuple[Vector2, Vector2]] = []
        
        for point in self.mappoints:
            offset = point - center
            vectors.append((center, center + offset.rotate(-0.01)))
            vectors.append((center, point))
            vectors.append((center, center + offset.rotate(0.01)))

        return vectors


    def create_shadow(self, center:Vector2) -> list[Vector2]:
        BIGNUM = 10_000

        vectors = self.project_vectors(center)

        shadowpoly:list[Vector2] = []

        for vector in vectors:
            temp = (vector[0], linehelper.extend_point(center, vector[1], BIGNUM))
            minintersection = temp[1]
            mindistance = (minintersection[0] - center[0]) ** 2 + (minintersection[1] - center[1]) ** 2

            for tile in self.enumarate_tile_row(temp[0], temp[1]):
                if tile and tile.id != Tile.nothing_id:
                    foundintersection = False

                    for edge in self.get_edges(tile):
                        intersection = linehelper.line_line_intersect(*temp, *edge)
                        
                        if intersection:
                            distance = linehelper.line_length_pow2(temp[0], intersection)

                            if distance < mindistance:
                                mindistance = distance
                                minintersection = intersection
                                foundintersection = True

                    if foundintersection:
                        break

            if minintersection != None:
                shadowpoly.append(minintersection)

        shadowpoly.sort(key=lambda p: Math.atan2(p[1] - center[1], p[0] - center[0]))
        return shadowpoly


    def draw(self, surface:Surface, center:Vector2):
        shadow = self.create_shadow(center)

        self.surface.fill(consts.colors.transparent_dark_gray)
        draw.polygon(self.surface, consts.colors.black_rgba,
            [(round(p[0]), round(p[1])) for p in shadow])
        #shadowmask = mask.from_threshold(self.surface, consts.colors.white, (1, 1, 1))

        if not consts.DEBUG_MAP:    
            sur = Surface(surface.get_size(), SRCALPHA)
            sur.fill((*consts.colors.grass, 255))
            sur.blit(self.surface, (0, 0), None, BLEND_RGBA_SUB)
            #surface.fill(consts.colors.white)
            surface.blit(sur, (0, 0))
            #draw.polygon(surface, consts.colors.smitranparent_gray, shadowmask.outline())

        if consts.DEBUG_MAP:
            #draw.polygon(surface, consts.colors.smitranparent_gray,
            #    [(round(p[0]), round(p[1])) for p in shadow])

            #for s in shadowmask.outline():
            #    draw.circle(surface, consts.colors.red, s, 4)
            
            #surface.blit(self.surface, (0, 0))
            #surface.blit(shadowmask.to_surface(), (0, 0))

            for line in self.project_vectors(center):
                draw.line(surface, consts.colors.blue, *line)
            
            for p in self.mappoints:
                draw.circle(surface, consts.colors.blue, p, 4)

            for s in shadow:
                draw.circle(surface, consts.colors.red, s, 4)