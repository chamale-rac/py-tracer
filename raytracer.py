import pygame
from rt import Raytracer
from figures import *
from lights import *
from materials import *

width = 256
height = 256

pygame.init()

screen = pygame.display.set_mode(
    (width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
screen.set_alpha(None)

raytracer = Raytracer(screen)

brick = Material(diffuse=(1, 0.4, 0.4), specular=8, ks=0.01)
grass = Material(diffuse=(0.4, 1, 0.4), specular=32, ks=0.1)
water = Material(diffuse=(0.4, 0.4, 1), specular=256, ks=0.2)

raytracer.scene.append(
    Sphere(position=(1, 1, -5), radius=0.5, material=grass))
raytracer.scene.append(
    Sphere(position=(0, 0, -7), radius=2, material=brick))
raytracer.scene.append(
    Sphere(position=(0.5, -1, -5), radius=0.3, material=water))

raytracer.lights.append(AmbientLight(intensity=0.1))
raytracer.lights.append(DirectionalLight(
    direction=(-1, -1, -1), intensity=0.7))
raytracer.lights.append(PointLight(point=(2.5, 0, -5),
                        intensity=0.5, color=(1, 0, 1)))
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
