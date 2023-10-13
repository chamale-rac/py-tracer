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


def norm_mag(v: tuple[float, float, float]) -> tuple[float, float, float]:
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


def cross(v1: tuple[float, float, float], v2: tuple[float, float, float]) -> tuple[float, float, float]:
    '''
    Cross product of two vectors
    '''
    return (v1[1] * v2[2] - v1[2] * v2[1],
            v1[2] * v2[0] - v1[0] * v2[2],
            v1[0] * v2[1] - v1[1] * v2[0])


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


def transpose(matrix: list[list[float]]) -> list[list[float]]:
    '''
    Transpose a matrix.
    '''
    return [list(row) for row in zip(*matrix)]


def multiply_mv(matrix: list[list[float]], vector: tuple[float]) -> tuple[float]:
    '''
    Multiply a matrix by a vector
    '''
    # Check matrix column length and vector length match
    assert len(matrix[0]) == len(vector)
    _len = len(vector)

    result = [sum(matrix[i][j] * vector[j] for j in range(_len))
              for i in range(_len)]

    return tuple(result)


def rotation_matrix(rotation: tuple[float, float, float]) -> list[list[float]]:
    '''
    Create a rotation matrix from rotation tuple

    Using the rotation tuple (x, y, z), create a rotation matrix. Based on the theory from https://en.wikipedia.org/wiki/Rotation_matrix#In_three_dimensions
    '''

    # represents an extrinsic rotation whose (improper) Euler angles are α, β, γ, about axes x, y, z.
    x, y, z = rotation

    cx = math.cos(x)
    sx = math.sin(x)

    cy = math.cos(y)
    sy = math.sin(y)

    cz = math.cos(z)
    sz = math.sin(z)

    matrix = [
        [cy*cz, sx*sy*cz - cx*sz, cx*sy*cz + sx*sz],
        [cy*sz, sx*sy*sz + cx*cz, cx*sy*sz - sx*cz],
        [-sy, sx*cy, cx*cy]
    ]

    # Return a 4x4 matrix
    return [row + [0] for row in matrix] + [[0, 0, 0, 1]]


def translation_matrix(translation: tuple[float, float, float]) -> list[list[float]]:
    '''
    Create a translation matrix from translation tuple

    Using the translation tuple (x, y, z), create a translation matrix. Based on the theory from https://en.wikipedia.org/wiki/Translation_matrix

    '''
    x, y, z = translation

    return [
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ]


def scale_matrix(scale: tuple[float, float, float]) -> list[list[float]]:
    '''
    Create a scale matrix from scale tuple

    Using the scale tuple (x, y, z), create a scale matrix. Based on the theory from https://en.wikipedia.org/wiki/Scaling_(geometry)

    '''
    x, y, z = scale

    return [
        [x, 0, 0, 0],
        [0, y, 0, 0],
        [0, 0, z, 0],
        [0, 0, 0, 1]
    ]


def multiply_mm(matrix1: list[list[float]], matrix2: list[list[float]]) -> list[list[float]]:
    '''
    Multiply two matrices
    '''
    return [[sum(a * b for a, b in zip(x_row, y_col)) for y_col in zip(*matrix2)] for x_row in matrix1]


def multiply_matrices(*matrices: list[list[float]]) -> list[list[float]]:
    '''
    Multiply multiple matrices
    '''
    result = matrices[0]
    for matrix in matrices[1:]:
        result = multiply_mm(result, matrix)
    return result


def model_matrix(translate: tuple[float, float, float],
                 rotate: tuple[float, float, float],
                 scale: tuple[float, float, float]) -> tuple[tuple[float, float, float], tuple[float, float, float], tuple[float, float, float]]:
    '''
    Model matrix

    This function is used to create a model matrix.

    Attributes:
        translate (tuple[float, float, float]): The translation of the model.
        rotate (tuple[float, float, float]): The rotation of the model.
        scale (tuple[float, float, float]): The scale of the model.
    '''
    # Translation matrix
    T = translation_matrix(translate)

    # Rotation matrix
    R = rotation_matrix(rotate)

    # Scale matrix
    S = scale_matrix(scale)

    # Model matrix := T * R * S
    model_matrix = multiply_matrices(T, R, S)

    return model_matrix


def rotate(vector: tuple[float, float, float], rotation_matrix: list[list[float]]) -> tuple[float, float, float]:
    '''
    Rotate a vector by a rotation tuple
    '''
    return tuple(sum(rotation_matrix[i][j] * vector[j] for j in range(3)) for i in range(3))
