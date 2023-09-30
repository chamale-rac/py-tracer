OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2

material_types = {
    'OPAQUE': OPAQUE,
    'REFLECTIVE': REFLECTIVE,
    'TRANSPARENT': TRANSPARENT
}


class Material:
    '''
    Material Class

    This class represents a material.

    Attributes:
        diffuse (tuple[float, float, float]): The diffuse color of the material.
        albedo (tuple[float, float, float]): The albedo of the material.
        specular_exponent (float): The specular exponent of the material.
    '''

    def __init__(self, diffuse: tuple[float, float, float] = (1, 1, 1), specular: float = 1.0, ks: float = 0.0, material_type: int = material_types['OPAQUE'], texture=None, ior: float = 1.0) -> None:
        self.diffuse = diffuse
        self.specular = specular
        self.ks = ks
        self.material_type = material_type
        self.texture = texture
        self.ior = ior
