import math


def subtract(v1: tuple[float, float, float], v2: tuple[float, float, float]) -> tuple[float, float, float]:
    '''
    Subtract two vectors
    '''
    return tuple(x - y for x, y in zip(v1, v2))


def normalize(v: tuple[float, float, float]) -> tuple[float, float, float]:
    '''
    Normalize a vector
    '''
    magnitude = math.sqrt(sum(x ** 2 for x in v))
    if magnitude == 0:
        return v
    return tuple(x / magnitude for x in v)
