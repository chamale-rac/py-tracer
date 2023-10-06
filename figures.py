import pmath as pm
import math
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
        L_len = pm.norm_mag(L)
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

        # point = origin + t0 * direction
        point = pm.add(origin, pm.multiply(t0, direction))
        normal = pm.subtract(point, self.position)
        normal = pm.norm(normal)

        u = math.atan2(normal[2], normal[0]) / (2 * math.pi) + 0.5
        v = math.acos(normal[1]) / math.pi

        return Intercept(distance=t0,
                         point=point,
                         normal=normal,
                         obj=self,
                         texture_coords=(u, v))


class Plane(Shape):
    def __init__(self, position: tuple[float, float, float], normal: tuple[float, float, float], material: materials.Material) -> None:
        super().__init__(position, material)
        self.normal = pm.norm(normal)

    def ray_intersect(self, origin: tuple[float, float, float], direction: tuple[float, float, float]) -> bool:
        '''
        Ray intersect method, returns the intercept of the ray with the plane.

        Described as: distance = (position - origin) . normal / (direction . normal)
        '''
        denom = pm.dot(direction, self.normal)
        if abs(denom) <= 0.0001:
            # The ray is parallel to the plane
            return None

        num = pm.dot(pm.subtract(self.position, origin), self.normal)
        t = num / denom

        if t < 0:
            # The plane is behind the ray
            return None

        # point = origin + t0 * direction
        point = pm.add(origin, pm.multiply(t, direction))

        return Intercept(distance=t,
                         point=point,
                         normal=self.normal,
                         obj=self,
                         texture_coords=None)


class Disk(Plane):
    def __init__(self, position: tuple[float, float, float], normal: tuple[float, float, float], radius: float, material: materials.Material) -> None:
        super().__init__(position, normal, material)
        self.radius = radius

    def ray_intersect(self, origin: tuple[float, float, float], direction: tuple[float, float, float]) -> bool:
        plane_intersect = super().ray_intersect(origin, direction)

        if plane_intersect is None:
            return None

        contact_distance = pm.subtract(plane_intersect.point, self.position)
        contact_distance = pm.norm_mag(contact_distance)

        if contact_distance > self.radius:
            return None

        return Intercept(distance=plane_intersect.distance,
                         point=plane_intersect.point,
                         normal=self.normal,
                         obj=self,
                         texture_coords=None)


class Intercept(object):
    '''
    Intercept class

    This class represents an intercept.

    Attributes:
        distance (float): The distance of the intercept.
        point (tuple[float, float, float]): The point of the intercept.
        normal (tuple[float, float, float]): The normal of the intercept.
    '''

    def __init__(self, distance: float,  point: tuple[float, float, float], normal: tuple[float, float, float],  obj: Shape, texture_coords: tuple[float, float]) -> None:
        self.distance = distance
        self.point = point
        self.normal = normal
        self.obj = obj
        self.texture_coords = texture_coords
