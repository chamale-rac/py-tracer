from figures import Intercept
import pmath as pm


def calculate_reflect_vector(vector: tuple[float, float, float], normal: tuple[float, float, float]) -> tuple[float, float, float]:
    reflect = 2 * pm.dot(vector, normal)
    reflect = pm.multiply(reflect, normal)
    reflect = pm.subtract(reflect, vector)
    reflect = pm.norm(reflect)
    return reflect


class Light:
    '''
    Light Class

    This class represents a light.

    Attributes:
        intensity (float): The intensity of the light.
        color (tuple[float, float, float]): The color of the light.
    '''

    def __init__(self, intensity: float = 1,  color: tuple[float, float, float] = (1, 1, 1), light_type: str = None) -> None:
        self.intensity = intensity
        self.color = color
        self.light_type = light_type

    def get_light_color(self) -> tuple[float, float, float]:
        return tuple([self.intensity * c for c in self.color])

    def get_diffuse_color(self, intercept: Intercept) -> tuple[float, float, float]:
        return None

    def get_specular_color(self, intercept: Intercept, view_position) -> tuple[float, float, float]:
        return None


class AmbientLight(Light):
    '''
    AmbientLight Class

    This class represents an ambient light.

    Attributes:
        intensity (float): The intensity of the light.
        color (tuple[float, float, float]): The color of the light.
    '''

    def __init__(self, intensity: float = 1, color: tuple[float, float, float] = (1, 1, 1)) -> None:
        super().__init__(intensity, color, "ambient")


class DirectionalLight(Light):
    '''
    DirectionalLight Class

    This class represents a directional light.

    Attributes:
        intensity (float): The intensity of the light.
        color (tuple[float, float, float]): The color of the light.
        direction (tuple[float, float, float]): The direction of the light.
    '''

    def __init__(self, intensity: float = 1, color: tuple[float, float, float] = (1, 1, 1), direction: tuple[float, float, float] = (0, -1, 0)) -> None:
        super().__init__(intensity, color, "directional")
        self.direction = pm.norm(direction)

    def get_diffuse_color(self, intercept: Intercept) -> tuple[float, float, float]:
        direction = [i*-1 for i in self.direction]

        intensity = pm.dot(intercept.normal, direction) * self.intensity
        intensity = max(0, min(1, intensity))
        intensity *= 1 - intercept.obj.material.ks

        diffuse_color = tuple([intensity * c for c in self.color])

        return diffuse_color

    def get_specular_color(self, intercept: Intercept, view_position: tuple[float, float, float]) -> tuple[float, float, float]:
        direction = [i*-1 for i in self.direction]

        reflect_vector = calculate_reflect_vector(direction, intercept.normal)

        view_direction = pm.subtract(view_position, intercept.point)
        view_direction = pm.norm(view_direction)

        specular_intensity = max(
            0, pm.dot(view_direction, reflect_vector)) ** intercept.obj.material.specular

        specular_intensity *= intercept.obj.material.ks
        specular_intensity *= self.intensity

        specular_color = tuple([specular_intensity * c for c in self.color])

        return specular_color


class PointLight(Light):
    '''
    PointLight Class

    This class represents a point light.

    Attributes:
        point (tuple[float, float, float]): The position of the light.
        intensity (float): The intensity of the light.
        color (tuple[float, float, float]): The color of the light.
    '''

    def __init__(self, point: tuple[float, float, float] = (0, 0, 0), intensity: float = 1, color: tuple[float, float, float] = (1, 1, 1)) -> None:
        super().__init__(intensity, color, "point")
        self.point = point

    def get_diffuse_color(self, intercept: Intercept) -> tuple[float, float, float]:
        direction = pm.subtract(self.point, intercept.point)
        R = pm.norm_magnitude(direction)
        direction = tuple([i/R for i in direction])

        intensity = pm.dot(intercept.normal, direction) * self.intensity
        intensity *= 1 - intercept.obj.material.ks

        # inverse squares law
        if R != 0:
            intensity /= R**2
        intensity = max(0, min(1, intensity))

        diffuse_color = tuple([intensity * c for c in self.color])

        return diffuse_color

    def get_specular_color(self, intercept: Intercept, view_position: tuple[float, float, float]) -> tuple[float, float, float]:
        direction = pm.subtract(self.point, intercept.point)
        R = pm.norm_magnitude(direction)
        direction = tuple([i/R for i in direction])

        reflect_vector = calculate_reflect_vector(direction, intercept.normal)

        view_direction = pm.subtract(view_position, intercept.point)
        view_direction = tuple(
            [i/pm.norm_magnitude(view_direction) for i in view_direction])

        specular_intensity = max(
            0, pm.dot(view_direction, reflect_vector)) ** intercept.obj.material.specular

        specular_intensity *= intercept.obj.material.ks
        specular_intensity *= self.intensity

        # inverse squares law
        if R != 0:
            specular_intensity /= R**2
        specular_intensity = max(0, min(1, specular_intensity))

        specular_color = tuple([specular_intensity * c for c in self.color])

        return specular_color

# TODO: Add SpotLight class
