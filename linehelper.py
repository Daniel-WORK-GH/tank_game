import math as Math
from pygame import *

def line_line_intersect(P0, P1, Q0, Q1):
    d = (P1[0]-P0[0]) * (Q1[1]-Q0[1]) + (P1[1]-P0[1]) * (Q0[0]-Q1[0]) 
    if d == 0:
        return None
    t = ((Q0[0]-P0[0]) * (Q1[1]-Q0[1]) + (Q0[1]-P0[1]) * (Q0[0]-Q1[0])) / d
    u = ((Q0[0]-P0[0]) * (P1[1]-P0[1]) + (Q0[1]-P0[1]) * (P0[0]-P1[0])) / d
    if 0 <= t <= 1 and 0 <= u <= 1:
        return (P1[0] * t + P0[0] * (1-t)), (P1[1] * t + P0[1] * (1-t))
    return None


def extend_point(center:Vector2, point:Vector2, newlen:float) -> Vector2:
    vec = point - center
    len = Math.sqrt((center[0] - point[0]) ** 2 + (center[1] - point[1]) ** 2)
    return center + Vector2(vec[0] / len, vec[1] / len) * newlen