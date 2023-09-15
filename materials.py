class Material:
    '''
    Material Class

    This class represents a material.

    Attributes:
        diffuse (tuple[float, float, float]): The diffuse color of the material.
        albedo (tuple[float, float, float]): The albedo of the material.
        specular_exponent (float): The specular exponent of the material.
    '''

    def __init__(self, diffuse: tuple[float, float, float] = (1, 1, 1), specular: float = 1.0) -> None:
        self.diffuse = diffuse
        self.specular = specular
