'''
Custom vector math functions.
'''

import math


def subtract(v1: tuple[float, float, float], v2: tuple[float, float, float]) -> tuple[float, float, float]:
    '''
    Subtract two vectors
    '''
    return tuple(x - y for x, y in zip(v1, v2))


def norm(v: tuple[float, float, float]) -> tuple[float, float, float]:
    '''
    norm a vector
    '''
    magnitude = math.sqrt(sum(x ** 2 for x in v))
    if magnitude == 0:
        return v
    return tuple(x / magnitude for x in v)


def norm_magnitude(v: tuple[float, float, float]) -> tuple[float, float, float]:
    '''
    Norm a vector and return the magnitude
    '''
    return math.sqrt(sum(x ** 2 for x in v))


def dot(v1: tuple[float, float, float], v2: tuple[float, float, float]) -> float:
    '''
    Dot product of two vectors
    '''
    return sum(x * y for x, y in zip(v1, v2))


def multiply(scalar: float, vector: tuple[float, float, float]) -> tuple[float, float, float]:
    '''
    Multiply a scalar by a vector element-wise.
    '''
    return tuple(scalar * x for x in vector)


def add(v1: tuple[float, float, float], v2: tuple[float, float, float]) -> tuple[float, float, float]:
    '''
    Add two vectors
    '''
    return tuple(x + y for x, y in zip(v1, v2))
