from pygame import Vector2
import math


class Transform:
    def __init__(self, position):
        self.position = position


def findPolygonCenter(points:list[Vector2]) -> Vector2:
    avgx, avgy = 0, 0
    count = len(points)
    for p in points:
        avgx += p[0]
        avgy += p[1]

    return Vector2(avgx / count, avgy / count)


def centerPolygon(points:list[Vector2]) -> list[Vector2]:
    center = findPolygonCenter(points)
    return [p - center for p in points]


def transformPoint(point:Vector2, position:Vector2, angle:float):
    # x' = xcos(a) - ysin(a)
    # y' = ycos(a) - xsin(a)

    a = math.radians(angle)
    x = point[0] * math.cos(a) - point[1] * math.sin(-a)
    y = point[1] * math.cos(-a) - point[0] * math.sin(a)

    return Vector2(position.x + x, position.y + y)


def transformPolygon(points:list[Vector2], position:Vector2, angle:float=0) -> list[Vector2]:
    return [transformPoint(p, position, angle) for p in points]