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
        self.direction = direction

# TODO: Add PointLight class
# TODO: Add SpotLight class
