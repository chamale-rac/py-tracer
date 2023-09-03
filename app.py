import pygame
from rt import Raytracer
from figures import *
from lights import *
from materials import *

width = 512
height = 512

pygame.init()

screen = pygame.display.set_mode(
    (width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
screen.set_alpha(None)

raytracer = Raytracer(screen)

brick = Material(diffuse=(1, 0.4, 0.4))

raytracer.scene.append(Sphere(position=(0, 0, -5), radius=1, material=brick))

raytracer.lights.append(AmbientLight(intensity=0.1))
raytracer.lights.append(DirectionalLight(direction=(0, -1, -1), intensity=0.7))

is_running = True

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            is_running = False

    raytracer.clear()
    raytracer.render()

    pygame.display.flip()

pygame.quit()
