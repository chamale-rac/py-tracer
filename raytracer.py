import os
import pygame
from rt import Raytracer
from figures import *
from lights import *
from materials import *
import matplotlib
import datetime


def app():
    # Constants
    file_path = './assets/scenes/triangles.txt'
    environment_map_path = './assets/textures/environment/brown_photostudio_05_8k.png'
    screen_shot_path = './assets/screenshots/'

    width = 1920
    height = 1080

    pygame.init()

    pygame.display.set_caption(f"RT - {file_path}")

    # pygame.FULLSCREEN
    screen = pygame.display.set_mode(
        (width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
    screen.set_alpha(None)

    raytracer = Raytracer(screen)
    raytracer.environment_map = pygame.image.load(environment_map_path)
    materials = {}
    textures = {
        'None': None,
    }

    def parseScene(filepath: str = "./default.txt"):
        use_hex = False
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
                elif keyword == "plane":
                    position = tuple(map(float, params[:3]))
                    normal = tuple(map(float, params[3:6]))
                    material_name = params[6]
                    raytracer.scene.append(Plane(
                        position=position, normal=normal, material=materials[material_name]))
                elif keyword == "disk":
                    position = tuple(map(float, params[:3]))
                    normal = tuple(map(float, params[3:6]))
                    radius = float(params[6])
                    material_name = params[7]
                    raytracer.scene.append(Disk(
                        position=position, normal=normal, radius=radius, material=materials[material_name]))
                elif keyword == "AABB":
                    position = tuple(map(float, params[:3]))
                    size = tuple(map(float, params[3:6]))
                    material_name = params[6]
                    raytracer.scene.append(AABB(
                        position=position, size=size, material=materials[material_name]))
                elif keyword == "triangle":
                    a = tuple(map(float, params[:3]))
                    b = tuple(map(float, params[3:6]))
                    c = tuple(map(float, params[6:9]))
                    vertices = [a, b, c]
                    material_name = params[9]
                    raytracer.scene.append(
                        Triangle(vertices=vertices, material=materials[material_name]))
                elif keyword == "texture":
                    if params[0] != 'None':
                        texture = pygame.image.load(params[1])
                        textures[params[0]] = texture
                elif keyword == "material":
                    name = params[0]
                    offset = 0
                    if use_hex:
                        diffuse = tuple(
                            matplotlib.colors.to_rgb(f'#{params[1]}'))
                    else:
                        diffuse = tuple(map(float, params[1:4]))
                        offset = 2
                    specular = float(params[2 + offset])
                    ks = float(params[3 + offset])
                    material_type = material_types[params[4 + offset]]
                    texture = textures[params[5 + offset]]
                    ior = float(params[6 + offset])
                    materials[name] = Material(
                        diffuse=diffuse, specular=specular, ks=ks, material_type=material_type, texture=texture, ior=ior)
                elif keyword == "clear_color":
                    color = tuple(map(float, params[:3]))
                    raytracer.set_clear_color(*color)
                elif keyword == "batch_size":
                    raytracer.batch_size = int(params[0])
                elif keyword == "render_using":
                    raytracer.render_using = params[0]
                elif keyword == "use_hex":
                    if params[0] == 'true':
                        use_hex = True

    parseScene(file_path)

    ss = 0
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
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                pygame.display.set_caption("Saving...")
                # Screenshot name unique using timestamp
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                screen_shot_name = f'screenshot{ss}_{timestamp}.png'
                pygame.image.save(screen, os.path.join(
                    os.path.dirname(screen_shot_path), screen_shot_name))
                ss += 1
                print(
                    f"Saved screenshot: {screen_shot_path}{screen_shot_name}")
                pygame.display.set_caption(f"RT - {file_path}")

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
