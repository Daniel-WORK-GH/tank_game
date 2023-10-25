import consts
import math as Math
import linehelper
import mapobjects.transform as Transform
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
        MAXITR = 60
        
        dx, dy = linehelper.normalize_line(start, end)

        dx *= consts.DEFAULT_TILE_SIZE
        dy *= consts.DEFAULT_TILE_SIZE

        x, y = start

        checked = []
        maxdistance = linehelper.line_length_pow2(start, end)

        itr = 0
        while itr < MAXITR:
            nx, ny = x + STEP * dx, y + STEP * dy 

            rx, ry, rw, rh = linehelper.line_bounding_rect((x, y), (nx, ny))

            t1 = self.get_tile_at(rx, ry)
            t2 = self.get_tile_at(rx + rw, ry)
            t3 = self.get_tile_at(rx, ry + rh)
            t4 = self.get_tile_at(rx + rw, ry + rh)
            
            if (not t1) and (not t2) and (not t3) and (not t4):
                return
            
            if linehelper.line_length_pow2(start, (x, y)) > maxdistance:
                return

            if t1 not in checked:
                yield t1
                checked.append(t1)

            if t2 not in checked:
                yield t2
                checked.append(t2)

            if t3 not in checked:
                yield t3
                checked.append(t3)

            if t4 not in checked:
                yield t4
                checked.append(t4)

            x, y = nx, ny

            itr += 1

    
    def create_map_points(self) -> list[Vector2]:
        points:list[Vector2] = []
        count:list[int] = []
        
        for row in self.map.map:
            for tile in row:
                if tile.id == Tile.wall_id:
                    for corner in self.get_corners(tile):
                        if corner in points:
                            count[points.index(corner)] += 1
                        else:
                            points.append(corner)
                            count.append(1)

        w, h = self.surface.get_size()

        return [points[i] for i in range(0, len(points)) if count[i] != 4 and count[i] != 2]


    def project_vectors(self, center:Vector2) -> list[Vector2, Vector2]:
        BIGNUM = 10_000

        linelen = linehelper.line_length((0, 0), (
            consts.VIEW_RANGE[0] * consts.DEFAULT_TILE_SIZE,
            consts.VIEW_RANGE[1] * consts.DEFAULT_TILE_SIZE
        ))

        vectors:list[tuple[Vector2, Vector2]] = []
        
        distance = linehelper.line_length_pow2((0, 0), (
            consts.VIEW_RANGE[0] * consts.DEFAULT_TILE_SIZE,
            consts.VIEW_RANGE[1] * consts.DEFAULT_TILE_SIZE
        ))

        for point in self.mappoints:
            offset = point - center

            pointdistance = linehelper.line_length_pow2((0, 0), offset)

            if pointdistance > distance:
                continue

            v1 =  center + offset.rotate(-0.01)
            v2 = center + offset.rotate(0.01)

            v1 = linehelper.extend_point(center, v1, linelen)
            v2 = linehelper.extend_point(center, v2, linelen)

            vectors.append((center, v1))
            vectors.append((center, point))
            vectors.append((center, v2))

        return vectors


    def create_shadow(self, center:Vector2) -> list[Vector2]:
        vectors = self.project_vectors(center)

        shadowpoly:list[Vector2] = []

        for vector in vectors:
            minintersection = vector[1]
            mindistance = (minintersection[0] - center[0]) ** 2 + (minintersection[1] - center[1]) ** 2

            for tile in self.enumarate_tile_row(vector[0], vector[1]):
                if tile and tile.id == Tile.wall_id:
                    foundintersection = False

                    for edge in self.get_edges(tile):
                        intersection = linehelper.line_line_intersect(*vector, *edge)
                        
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
            
            for p in self.mappoints:
                draw.circle(surface, consts.colors.blue, p, 4)

            for s in shadow:
                draw.circle(surface, consts.colors.red, s, 4)