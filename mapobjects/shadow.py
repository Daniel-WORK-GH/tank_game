import consts
import math as Math
import linehelper
import mapobjects.transform as Transform
from pygame import *
from mapobjects.tile import Tile
from mapobjects.map import Map
from mapobjects.tilehelper import *


class Shadow:
    def __init__(self, surface:Surface, map:Map):
        self.map = map
        self.surface = Surface(surface.get_size(), SRCALPHA)
        self.corners = self.create_map_points()
    
    def create_map_points(self) -> list[tuple[Vector2, int]]: # points, num of tile near it
        points:list[Vector2] = []
        count:list[int] = []
        
        for row in self.map.map:
            for tile in row:
                if tile.id == Tile.wall_id:
                    for corner in get_tile_corners(tile):
                        if corner in points:
                            count[points.index(corner)] += 1
                        else:
                            points.append(corner)
                            count.append(1)

        #w = self.map.width * consts.DEFAULT_TILE_SIZE
        #h = self.map.height * consts.DEFAULT_TILE_SIZE

        #points.append((0, 0))
        #points.append((w, 0))
        #points.append((w, h))
        #points.append((0, h))
        #count.extend((1, 1, 1, 1))

        return [(points[i], count[i]) for i in range(0, len(points)) if count[i] != 4 and count[i] != 2]


    def project_vectors(self, center:Vector2) -> list[Vector2, Vector2]:
        viewvec = (
            consts.VIEW_RANGE[0] * consts.DEFAULT_TILE_SIZE,
            consts.VIEW_RANGE[1] * consts.DEFAULT_TILE_SIZE
        )

        linelen = linehelper.line_length((0, 0), viewvec)

        vectors:list[tuple[Vector2, Vector2]] = []
        
        distance = linehelper.line_length_pow2((0, 0), (
            consts.VIEW_RANGE[0] * consts.DEFAULT_TILE_SIZE,
            consts.VIEW_RANGE[1] * consts.DEFAULT_TILE_SIZE
        ))

        for point, cnt in self.corners:
            offset = point - center

            pointdistance = linehelper.line_length_pow2((0, 0), offset)

            if pointdistance > distance and cnt != 3:
                continue
            
            if cnt == 1:
                v1 =  center + offset.rotate(-0.01)
                v2 = center + offset.rotate(0.01)

                v1 = linehelper.extend_point(center, v1, linelen)
                v2 = linehelper.extend_point(center, v2, linelen)

                vectors.append((center, v1))
                vectors.append((center, point))
                vectors.append((center, v2))
            else:
                vectors.append((center, point))

        return vectors


    def create_shadow(self, center:Vector2) -> list[Vector2]:
        vectors = self.project_vectors(center)

        shadowpoly:list[Vector2] = []

        for vector in vectors:
            minintersection = vector[1]
            mindistance = (minintersection[0] - center[0]) ** 2 + (minintersection[1] - center[1]) ** 2

            for tile in enumarate_tile_row(self.map, vector[0], vector[1]):
                if tile and tile.id == Tile.wall_id:
                    foundintersection = False

                    for edge in get_edges(tile):
                        intersection = linehelper.line_line_intersect(vector[0], vector[1], edge[0], edge[1])
                        
                        if intersection:
                            distance = linehelper.line_length_pow2(vector[0], intersection)

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


    def draw(self, surface:Surface, center:Vector2, transfrom:Transform.Transform):
        shadow = self.create_shadow(center)

        if transfrom:
            for i in range(0, len(shadow)):
                shadow[i] = Transform.transformPoint(shadow[i], transfrom.position, 0)

        self.surface.fill(consts.colors.transparent_dark_gray)
        draw.polygon(self.surface, consts.colors.black_rgba,
            [(round(p[0]), round(p[1])) for p in shadow])

    
        sur = Surface(surface.get_size(), SRCALPHA)
        sur.fill((*consts.colors.grass, 255))
        sur.blit(self.surface, (0, 0), None, BLEND_RGBA_SUB)
        surface.blit(sur, (0, 0))

        if consts.DEBUG_MAP:
            for line in self.project_vectors(center):
                line = (
                    Transform.transformPoint(line[0], transfrom.position, 0), 
                    Transform.transformPoint(line[1], transfrom.position, 0)
                )
                draw.line(surface, consts.colors.blue, *line)
            
            for p, _ in self.corners:
                draw.circle(surface, consts.colors.blue,
                    Transform.transformPoint(p, transfrom.position, 0), 4)

            for s in shadow:
                draw.circle(surface, consts.colors.red, s, 4)