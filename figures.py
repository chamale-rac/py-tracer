import pmath as pm
import math
from materials import Material


class Shape(object):
    '''
    Shape class

    This class represents a generic shape.

    Attributes:
        position (tuple[float, float, float]): The position of the shape.
        Material (Material): The material of the shape.
    '''

    def __init__(self, position: tuple[float, float, float], material: Material) -> None:
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

    def __init__(self, position: tuple[float, float, float], radius: float, material: Material) -> None:
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
    def __init__(self, position: tuple[float, float, float], normal: tuple[float, float, float], material: Material) -> None:
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
    def __init__(self, position: tuple[float, float, float], normal: tuple[float, float, float], radius: float, material: Material) -> None:
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


class AABB(Shape):
    '''
    Axis-Aligned Bounding Box class
    '''

    def __init__(self, position: tuple[float, float, float], size: tuple[float, float, float], material: Material) -> None:
        super().__init__(position, material)
        self.planes = []
        self.size = size

        right_plane = Plane(
            pm.add(position, (size[0] / 2,  0,  0)), (1,  0,  0), material)
        left_plane = Plane(
            pm.add(position, (-size[0] / 2,  0,  0)), (-1,  0,  0), material)
        top_plane = Plane(
            pm.add(position, (0,  size[1] / 2,  0)), (0,  1,  0), material)
        bottom_plane = Plane(
            pm.add(position, (0,  -size[1] / 2,  0)), (0,  -1,  0), material)
        front_plane = Plane(
            pm.add(position, (0,  0,  size[2] / 2)), (0,  0,  1), material)
        back_plane = Plane(
            pm.add(position, (0,  0,  -size[2] / 2)), (0,  0,  -1), material)

        self.planes = [right_plane, left_plane, top_plane,
                       bottom_plane, front_plane, back_plane]

        # Bounds
        self.min_bounds = [0, 0, 0]
        self.max_bounds = [0, 0, 0]

        bias = 0.0001

        for i, (pos, size) in enumerate(zip(position, size)):
            self.min_bounds[i] = pos - size / 2 - bias
            self.max_bounds[i] = pos + size / 2 + bias

    def ray_intersect(self, origin: tuple[float, float, float], direction: tuple[float, float, float]) -> bool:
        '''
        Ray intersect method, returns the intercept of the ray with the plane.

        Described as: distance = (position - origin) . normal / (direction . normal)
        '''
        intersect: Intercept = None
        t = float('inf')
        u, v = 0, 0

        for plane in self.planes:
            plane_intersect = plane.ray_intersect(origin, direction)

            if plane_intersect is not None:
                plane_point = plane_intersect.point

                if self.min_bounds[0] <= plane_point[0] <= self.max_bounds[0] and \
                        self.min_bounds[1] <= plane_point[1] <= self.max_bounds[1] and \
                        self.min_bounds[2] <= plane_point[2] <= self.max_bounds[2]:

                    if plane_intersect.distance < t:
                        t = plane_intersect.distance
                        intersect = plane_intersect

                        # Calculate texture coordinates
                        if abs(plane.normal[0]) > 0:
                            # Right or left plane
                            # Using the y and z coordinates
                            u = (plane_point[1] -
                                 self.min_bounds[1]) / (self.size[1] + 0.002)
                            v = (plane_point[2] -
                                 self.min_bounds[2]) / (self.size[2] + 0.002)
                        elif abs(plane.normal[1]) > 0:
                            # Top or bottom plane
                            # Using the x and z coordinates
                            u = (plane_point[0] -
                                 self.min_bounds[0]) / (self.size[0] + 0.002)
                            v = (plane_point[2] -
                                 self.min_bounds[2]) / (self.size[2] + 0.002)
                        elif abs(plane.normal[2]) > 0:
                            # Front or back plane
                            # Using the x and y coordinates
                            u = (plane_point[0] -
                                 self.min_bounds[0]) / (self.size[0] + 0.002)
                            v = (plane_point[1] -
                                 self.min_bounds[1]) / (self.size[1] + 0.002)

        if intersect is None:
            return None

        return Intercept(distance=intersect.distance,
                         point=intersect.point,
                         normal=intersect.normal,
                         obj=self,
                         texture_coords=(u, v))


class Triangle(Shape):
    '''
    Triangle class

    This class represents a triangle.

    Attributes:
        vertices (tuple[tuple[float, float, float], tuple[float, float, float], tuple[float, float, float]]): The vertices of the triangle.
    '''

    def __init__(self, vertices: tuple[tuple[float, float, float], tuple[float, float, float], tuple[float, float, float]], material: Material) -> None:
        super().__init__(self.calculate_triangle_center(vertices), material)
        self.vertices = vertices

    @staticmethod
    def calculate_triangle_center(vertices: tuple[tuple[float, float, float], tuple[float, float, float], tuple[float, float, float]]) -> tuple[float, float, float]:
        x = (vertices[0][0] + vertices[1][0] + vertices[2][0]) / 3
        y = (vertices[0][1] + vertices[1][1] + vertices[2][1]) / 3
        z = (vertices[0][2] + vertices[1][2] + vertices[2][2]) / 3
        return x, y, z

    def ray_intersect(self, origin: tuple[float, float, float], direction: tuple[float, float, float]) -> bool:
        '''
        Ray intersect method, returns the intercept of the ray with the triangle.

        Implementation of Möller-Trumbore intersection algorithm.
        '''
        epsilon = 0.0001

        vertex0, vertex1, vertex2 = self.vertices
        edge1 = pm.subtract(vertex1, vertex0)
        edge2 = pm.subtract(vertex2, vertex0)
        h = pm.cross(direction, edge2)
        a = pm.dot(edge1, h)

        if a > -epsilon and a < epsilon:
            return None

        f = 1.0 / a
        s = pm.subtract(origin, vertex0)
        u = f * pm.dot(s, h)

        if u < 0.0 or u > 1.0:
            return None

        q = pm.cross(s, edge1)
        v = f * pm.dot(direction, q)

        if v < 0.0 or u + v > 1.0:
            return None

        t = f * pm.dot(edge2, q)

        if t > epsilon:
            point = pm.add(origin, pm.multiply(t, direction))
            normal = pm.norm(pm.cross(edge1, edge2))
            u = 1 - u
            v = 1 - v
            return Intercept(distance=t, point=point, normal=normal, obj=self, texture_coords=(u, v))

        return None


class Obj(Shape):
    '''
    Obj class

    This class represents an OBJ (.obj) model.

    Attributes:
        filepath (str): The path to the OBJ file.
        translation (tuple[float, float, float]): The translation of the model.
        rotation (tuple[float, float, float]): The rotation of the model.
        scale (tuple[float, float, float]): The scale of the model.
    '''

    def __init__(self, position: tuple[float, float, float],
                 filepath: str,
                 material: Material,
                 rotate: tuple[float, float, float] = (0, 0, 0),
                 scale: tuple[float, float, float] = (1, 1, 1),
                 ) -> None:
        super().__init__(position, material)
        translate = position
        self.model_matrix = pm.model_matrix(translate, rotate, scale)
        self.vertices, self.faces = self.load(filepath)
        self.triangles = []

        # Create triangles applying transformations
        for face in self.faces:
            vertex_count = len(face)

            v0 = self.vertex_shader(
                self.vertices[face[0] - 1], self.model_matrix)
            v1 = self.vertex_shader(
                self.vertices[face[1] - 1], self.model_matrix)
            v2 = self.vertex_shader(
                self.vertices[face[2] - 1], self.model_matrix)

            if vertex_count == 3:
                self.triangles.append(Triangle((v0, v1, v2), self.material))

            elif vertex_count == 4:
                v3 = self.vertex_shader(
                    self.vertices[face[3] - 1], self.model_matrix)
                self.triangles.append(Triangle((v0, v1, v2), self.material))
                self.triangles.append(Triangle((v0, v2, v3), self.material))

    @staticmethod
    def vertex_shader(vertex: tuple[float, float, float], model_matrix: list[list[float]]):
        '''
        Vertex shader
        '''
        # Convert vertex to homogeneous coordinates
        vertex = list(vertex) + [1]

        # Apply model matrix
        vertex = pm.multiply_mv(model_matrix, vertex)
        vertex = (vertex[0] / vertex[3], vertex[1] /
                  vertex[3], vertex[2] / vertex[3])

        return vertex

    @staticmethod
    def load(path: str) -> object:
        '''
        Load object from path

        This function is used to load object from path. Read an OBJ file and return the vertex and face data.

        Attributes:
            path (str): The path to the OBJ file.
        '''
        import re

        print('Loading 3D model from: ' + path)

        # Initialize lists
        vertices = []
        faces = []

        # Open file
        with open(file=path, mode='r') as file:
            lines = file.read().splitlines()

        # Read file
        for line in lines:
            # Split line
            try:
                prefix, data = re.split(r'\s+', line, 1)
                prefix, data = prefix.strip(), data.strip()
            except:
                continue

            # Read vertex
            if prefix == 'v':
                vertex = tuple(map(float, data.split(' ')))
                vertices.append(vertex)
            # Read face
            elif prefix == 'f':
                face = tuple(int(vertex.split('/')[0])
                             for vertex in data.split(' '))
                faces.append(face)

        # Return data
        return vertices, faces

    def ray_intersect(self, origin: tuple[float, float, float], direction: tuple[float, float, float]) -> bool:
        '''
        Ray intersect method, returns the intercept of the ray with the triangle.

        Implementation of Möller-Trumbore intersection algorithm.
        '''
        intersect: Intercept = None
        t = float('inf')
        u, v = 0, 0

        for triangle in self.triangles:
            triangle_intersect = triangle.ray_intersect(origin, direction)

            if triangle_intersect is not None:
                if triangle_intersect.distance < t:
                    t = triangle_intersect.distance
                    intersect = triangle_intersect
                    u, v = triangle_intersect.texture_coords

        if intersect is None:
            return None

        return Intercept(distance=intersect.distance,
                         point=intersect.point,
                         normal=intersect.normal,
                         obj=self,
                         texture_coords=(u, v))


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
