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


def reflect_vector(vector: tuple[float, float, float], normal: tuple[float, float, float]) -> tuple[float, float, float]:
    '''
    Calculate the reflected vector.

    Attributes:
        vector (tuple[float, float, float]): The incident vector.
        normal (tuple[float, float, float]): The normal vector.
    '''
    reflect = 2 * dot(vector, normal)
    reflect = multiply(reflect, normal)
    reflect = subtract(reflect, vector)
    reflect = norm(reflect)
    return reflect


def refract_vector(vector: tuple[float, float, float], normal: tuple[float, float, float], n1: float, n2: float) -> tuple[float, float, float]:
    '''
    Calculate the refracted vector using Snell's law.

    Attributes:
        vector (tuple[float, float, float]): The incident vector.
        normal (tuple[float, float, float]): The normal vector.
        n1 (float): The index of refraction of the external medium.
        n2 (float): The index of refraction of the internal medium.
    '''
    c1 = dot(normal, vector)

    if c1 < 0:
        c1 = -c1
    else:
        normal = multiply(-1, normal)
        n1, n2 = n2, n1

    n = n1 / n2

    part1 = multiply(n, add(vector, multiply(c1, normal)))
    part2 = multiply(math.sqrt(1 - math.pow(n, 2) *
                     (1 - math.pow(c1, 2))), normal)

    T = subtract(part1, part2)
    T = norm(T)

    return T


def total_internal_reflection(vector: tuple[float, float, float], normal: tuple[float, float, float], n1: float, n2: float) -> tuple[float, float, float]:
    '''
    Check if total internal reflection occurs.

    Attributes:
        vector (tuple[float, float, float]): The incident vector.
        normal (tuple[float, float, float]): The normal vector.
        n1 (float): The index of refraction of the external medium.
        n2 (float): The index of refraction of the internal medium.
    '''
    c1 = dot(normal, vector)

    if c1 < 0:
        c1 = -c1
    else:
        normal = multiply(-1, normal)
        n1, n2 = n2, n1

    if n1 < n2:
        return False

    theta1 = math.acos(c1)
    thetaC = math.asin(n2/n1)

    return theta1 >= thetaC


def fresnel(vector: tuple[float, float, float], normal: tuple[float, float, float], n1: float, n2: float) -> tuple[float, float]:
    '''
    Calculate the Fresnel coefficients.

    Attributes:
        n1 (float): The index of refraction of the external medium.
        n2 (float): The index of refraction of the internal medium.
    '''
    c1 = dot(normal, vector)

    if c1 < 0:
        c1 = -c1
    else:
        normal = multiply(-1, normal)
        n1, n2 = n2, n1

    s2 = (n1 * math.sqrt(1 - math.pow(c1, 2))) / n2
    c2 = math.sqrt(1 - math.pow(s2, 2))

    F1 = (n2*c1 - n1*c2) / (n2*c1 + n1*c2)
    F1 = math.pow(F1, 2)

    F2 = (n1*c2 - n2*c1) / (n1*c2 + n2*c1)
    F2 = math.pow(F2, 2)

    Kr = (F1 + F2) / 2
    Kt = 1 - Kr

    return (Kr, Kt)
