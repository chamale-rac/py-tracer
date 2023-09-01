import numpy as np


class Shape:
    '''
    Shape class

    This class represents a generic shape.

    Attributes:
        position (tuple[float, float, float]): The position of the shape.
    '''

    def __init__(self, position: tuple[float, float, float]) -> None:
        self.position = position

    def ray_intersect(self, origin: tuple[float, float, float], direction: tuple[float, float, float]) -> bool:
        return False


class Sphere(Shape):
    '''
    Sphere class

    This class represents a sphere.

    Attributes:
        position (tuple[float, float, float]): The position of the sphere.
        radius (float): The radius of the sphere.
    '''

    def __init__(self, position: tuple[float, float, float], radius: float) -> None:
        super().__init__(position)
        self.radius = radius

    def ray_intersect(self, origin: tuple[float, float, float], direction: tuple[float, float, float]) -> bool:
        L = np.subtract(self.position, origin)
        L_len = np.linalg.norm(L)
        tca = np.dot(L, direction)
        d = (L_len**2 - tca**2) ** 0.5

        if d > self.radius:
            return False

        thc = (self.radius**2 - d**2) ** 0.5
        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return False

        return True
