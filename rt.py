import pygame
import math
import numpy as np


class Raytracer:
    '''
    Raytracer class

    This class is responsible for the main loop of the raytracer.

    Attributes:
        screen (pygame.display): The screen to render to.
    '''

    def __init__(self, screen: pygame.display) -> None:
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.scene = []
        self.camera = (0, 0, 0)

        self.viewport_x = 0
        self.viewport_y = 0
        self.viewport_width = self.width
        self.viewport_height = self.height

        self.projection(60, 0.1)

        self.clear_color = (0, 0, 0)
        self.current_color = (255, 255, 255)

    def viewport(self, x: int, y: int, width: int, height: int) -> None:
        self.viewport_x = x
        self.viewport_y = y
        self.viewport_width = width
        self.viewport_height = height

    def projection(self, fov: float = 60, n: float = 0.1) -> None:
        aspect_ratio = self.viewport_width / self.viewport_height
        self.near_plane = n
        self.top_edge = math.tan((fov*math.pi / 180) / 2) * n
        self.right_edge = self.top_edge * aspect_ratio

    def set_clear_color(self, r: float, g: float, b: float) -> None:
        self.clear_color = (int(r * 255), int(g * 255), int(b * 255))

    def clear(self) -> None:
        self.screen.fill(self.clear_color)

    def set_current_color(self, r: float, g: float, b: float) -> None:
        self.current_color = (int(r * 255), int(g * 255), int(b * 255))

    def point(self, x: int, y: int, color: tuple[float, float, float] = None) -> None:
        # invert y
        y = self.height - y - 1
        if 0 <= x < self.width and 0 <= y < self.height:
            if color:
                self.set_current_color(*color)
            self.screen.set_at((x, y), self.current_color)

    def cast_ray(self, origin: tuple[float, float, float], direction: tuple[float, float, float]) -> bool:
        for obj in self.scene:
            if obj.ray_intersect(origin, direction):
                return True
        return False

    def render(self) -> None:
        for x in range(self.viewport_x, self.viewport_x + self.viewport_width + 1):
            for y in range(self.viewport_y, self.viewport_y + self.viewport_height + 1):
                if 0 <= x < self.width and 0 <= y < self.height:
                    # from window coordinates to normalized device coordinates (NDC)
                    position_x = ((x + 0.5 - self.viewport_x) /
                                  self.viewport_width) * 2 - 1
                    position_y = ((y + 0.5 - self.viewport_y) /
                                  self.viewport_height) * 2 - 1

                    position_x *= self.right_edge
                    position_y *= self.top_edge

                    # create ray
                    direction = np.array(
                        [position_x, position_y, -self.near_plane])
                    direction /= np.linalg.norm(direction)

                    if self.cast_ray(self.camera, direction):
                        self.point(x, y)
