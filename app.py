import pygame

from pygame.locals import *

from rt import Raytracer

width = 512
height = 512

pygame.init()

screen = pygame.display.set_mode(
    (width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
screen.set_alpha(None)

raytracer = Raytracer(screen)
raytracer.set_clear_color(0.25, 0.25, 0.25)

is_running = True

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_running = False

    raytracer.clear()

    raytracer.point(100, 100)
    raytracer.point(101, 100)
    raytracer.point(102, 100)

    raytracer.render()
    pygame.display.flip()

pygame.quit()
