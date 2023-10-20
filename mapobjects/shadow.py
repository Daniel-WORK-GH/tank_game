import consts
import math as Math
from pygame import *
from mapobjects.tile import Tile

class Shadow:
    def __init__(self, surface:Surface, tiles:list[Tile]):
        self.tiles = tiles
        self.mappoints = self.create_map_points()
        self.surface = Surface(surface.get_size(), SRCALPHA)


    def lineLineIntersect(self, P0, P1, Q0, Q1):
        d = (P1[0]-P0[0]) * (Q1[1]-Q0[1]) + (P1[1]-P0[1]) * (Q0[0]-Q1[0]) 
        if d == 0:
            return None
        t = ((Q0[0]-P0[0]) * (Q1[1]-Q0[1]) + (Q0[1]-P0[1]) * (Q0[0]-Q1[0])) / d
        u = ((Q0[0]-P0[0]) * (P1[1]-P0[1]) + (Q0[1]-P0[1]) * (P0[0]-P1[0])) / d
        if 0 <= t <= 1 and 0 <= u <= 1:
            return round(P1[0] * t + P0[0] * (1-t)), round(P1[1] * t + P0[1] * (1-t))
        return None


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


    def create_map_points(self) -> list[Vector2]:
        points:list[Vector2] = []
        count:list[int] = []
        
        for tile in self.tiles:
            for corner in self.get_corners(tile):
                if tile.id != Tile.nothing_id:
                    if corner in points:
                        count[points.index(corner)] += 1
                    else:
                        points.append(corner)
                        count.append(1)

        return [points[i] for i in range(0, len(points)) if count[i] != 4 and count[i] != 2]


    def project_vectors(self, center:Vector2) -> list[Vector2, Vector2]:
        vectors:list[tuple[Vector2, Vector2]] = []
        
        for point in self.mappoints:
            vectors.append((center, point))

        return vectors


    def create_shadow(self, center:Vector2) -> list[Vector2]:
        BIGNUM = 10_000

        vectors = self.project_vectors(center)

        shadowpoly:list[Vector2] = []

        for vector in vectors:
            temp = (vector[0], (vector[1][0] * BIGNUM, vector[1][1] * BIGNUM))
            mindistance = BIGNUM
            minintersection = None
            for tile in self.tiles:
                if tile.id != Tile.nothing_id: 
                    for edge in self.get_edges(tile):
                        intersection = self.lineLineIntersect(temp[0], temp[1], edge[0], edge[1])
                        if intersection:
                            distance = (intersection[0] - center[0]) ** 2 + (intersection[1] - center[1])
                            if distance < mindistance: 
                                mindistance = distance
                                minintersection = intersection

            if minintersection != None:
                shadowpoly.append(minintersection)

        shadowpoly.sort(key=lambda p: Math.atan2(p[1] - center[1], p[0] - center[0]))
        return shadowpoly


    def draw(self, surface:Surface, center:Vector2):
        shadow = self.create_shadow(center)
        #draw.polygon(surface, consts.colors.smitranparent_gray, shadow)

        if consts.DEBUG_MAP:
            for line in self.project_vectors(center):
                draw.line(surface, consts.colors.blue, *line)
            
            for p in self.mappoints:
                draw.circle(surface, consts.colors.blue, p, 4)

            for s in shadow:
                draw.circle(surface, consts.colors.black, s, 4)