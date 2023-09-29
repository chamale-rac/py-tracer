import os
import pygame
from rt import Raytracer
from figures import *
from lights import *
from materials import *


def app():
    # Constants
    file_path = './test_scene.txt'
    # width = 1080
    # height = 720
    width = 256
    height = 256

    pygame.init()

    pygame.display.set_caption(f"RT - {file_path}")
    screen = pygame.display.set_mode(
        (width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
    screen.set_alpha(None)

    raytracer = Raytracer(screen)
    materials = {}

    def parseScene(filepath: str = "./default.txt"):
        with open(filepath, "r") as f:
            for line in f:
                # Parse the line
                tokens = line.strip().split()
                if not tokens:
                    continue
                keyword = tokens[0]
                params = tokens[1:]

                # Create the object
                if keyword == "ambient":
                    raytracer.lights.append(
                        AmbientLight(intensity=float(params[0])))
                elif keyword == "directional":
                    direction = tuple(map(float, params[:3]))
                    intensity = float(params[3])
                    raytracer.lights.append(DirectionalLight(
                        direction=direction, intensity=intensity))
                elif keyword == "point":
                    point = tuple(map(float, params[:3]))
                    intensity = float(params[3])
                    color = tuple(map(float, params[4:]))
                    raytracer.lights.append(PointLight(
                        point=point, intensity=intensity, color=color))
                elif keyword == "sphere":
                    position = tuple(map(float, params[:3]))
                    radius = float(params[3])
                    material_name = params[4]
                    material = materials[material_name]
                    raytracer.scene.append(
                        Sphere(position=position, radius=radius, material=material))
                elif keyword == "material":
                    name = params[0]
                    diffuse = tuple(map(float, params[1:4]))
                    specular = float(params[4])
                    ks = float(params[5])
                    material_type = material_types[params[6]]
                    materials[name] = Material(
                        diffuse=diffuse, specular=specular, ks=ks, material_type=material_type)
                elif keyword == "clear_color":
                    color = tuple(map(float, params[:3]))
                    raytracer.set_clear_color(*color)
                elif keyword == "batch_size":
                    raytracer.batch_size = int(params[0])
                elif keyword == "render_using":
                    raytracer.render_using = params[0]

    parseScene(file_path)

    is_running = True
    once = True
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                is_running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r and pygame.key.get_mods() & pygame.KMOD_CTRL:
                # Reload the scene file
                pygame.display.set_caption("Reloading...")
                raytracer.scene.clear()
                raytracer.lights.clear()
                materials.clear()
                parseScene(file_path)
                once = True
        if once:
            pygame.display.set_caption("Rendering...")
            raytracer.clear()
            raytracer.render()
            pygame.display.set_caption("Done!")
            pygame.display.set_caption(f"RT - {file_path}")
            once = False

    pygame.quit()


if __name__ == "__main__":
    app()
