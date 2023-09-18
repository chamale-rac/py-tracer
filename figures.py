import pmath as pm
import materials


class Shape(object):
    '''
    Shape class

    This class represents a generic shape.

    Attributes:
        position (tuple[float, float, float]): The position of the shape.
        Material (Material): The material of the shape.
    '''

    def __init__(self, position: tuple[float, float, float], material: materials.Material) -> None:
        self.position = position
        self.material = material

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

    def __init__(self, position: tuple[float, float, float], radius: float, material: materials.Material) -> None:
        super().__init__(position, material)
        self.radius = radius

    def ray_intersect(self, origin: tuple[float, float, float], direction: tuple[float, float, float]):
        L = pm.subtract(self.position, origin)
        L_len = pm.norm_magnitude(L)
        tca = pm.dot(L, direction)
        d = (L_len**2 - tca**2) ** 0.5

        if d > self.radius:
            return None

        thc = (self.radius**2 - d**2) ** 0.5
        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return None

        point = pm.add(origin, pm.multiply(t0, direction))
        normal = pm.subtract(point, self.position)
        normal = pm.norm(normal)

        return Intercept(distance=t0,
                         point=point,
                         normal=normal,
                         obj=self)


class Intercept(object):
    '''
    Intercept class

    This class represents an intercept.

    Attributes:
        distance (float): The distance of the intercept.
        point (tuple[float, float, float]): The point of the intercept.
        normal (tuple[float, float, float]): The normal of the intercept.
    '''

    def __init__(self, distance: float,  point: tuple[float, float, float], normal: tuple[float, float, float],  obj: Shape) -> None:
        self.distance = distance
        self.point = point
        self.normal = normal
        self.obj = obj
