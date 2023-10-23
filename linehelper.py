import math

coordinate = tuple[float, float]

def line_line_intersect(P0:coordinate, P1:coordinate, Q0:coordinate, Q1:coordinate):
    d = (P1[0]-P0[0]) * (Q1[1]-Q0[1]) + (P1[1]-P0[1]) * (Q0[0]-Q1[0]) 
    if d == 0:
        return None
    t = ((Q0[0]-P0[0]) * (Q1[1]-Q0[1]) + (Q0[1]-P0[1]) * (Q0[0]-Q1[0])) / d
    u = ((Q0[0]-P0[0]) * (P1[1]-P0[1]) + (Q0[1]-P0[1]) * (P0[0]-P1[0])) / d
    if 0 <= t <= 1 and 0 <= u <= 1:
        return (P1[0] * t + P0[0] * (1-t)), (P1[1] * t + P0[1] * (1-t))
    return None


def line_length_pow2(start:coordinate, end:coordinate):
    return (end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2


def line_length(start:coordinate, end:coordinate):
    return math.sqrt(line_length_pow2(start, end))


def normalize_line(start:coordinate, end:coordinate):
    direction = ((end[0] - start[0]), (end[1] - start[1]))
    len = line_length(start, end)
    return (direction[0] / len, direction[1] / len)


def extend_point(center:coordinate, point:coordinate, newlen:coordinate):
    vec = point - center
    len = math.sqrt((center[0] - point[0]) ** 2 + (center[1] - point[1]) ** 2)
    return (center[0] + vec[0] / len * newlen, center[1] + vec[1] / len * newlen)