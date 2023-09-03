import pygame
import math
import numpy as np

import materials
import figures
import lights


class Raytracer(object):
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
        self.lights = []

        self.camera = (0, 0, 0)

        self.viewport(0, 0, self.width, self.height)
        self.projection(60, 0.1)

        self.set_clear_color(0.25, 0.25, 0.25)
        self.set_current_color(1, 1, 1)

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
        y = self.height - y
        if 0 <= x < self.width and 0 <= y < self.height:
            if color:
                self.set_current_color(*color)
            self.screen.set_at((x, y), self.current_color)

    def cast_ray(self, origin: tuple[float, float, float], direction: tuple[float, float, float]) -> bool:
        intercept = None
        hit = None
        for obj in self.scene:
            intercept = obj.ray_intersect(origin, direction)
            if intercept:
                hit = intercept
        return hit

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

                    intercept = self.cast_ray(self.camera, direction)

                    if intercept:
                        material = intercept.obj.material

                        color_point = list(material.diffuse)

                        ambient_light = [0, 0, 0]
                        directional_light = [0, 0, 0]

                        for light in self.lights:
                            if light.light_type == "ambient":
                                ambient_light[0] += light.intensity * \
                                    light.color[0]
                                ambient_light[1] += light.intensity * \
                                    light.color[1]
                                ambient_light[2] += light.intensity * \
                                    light.color[2]

                            if light.light_type == "directional":
                                light_direction = np.array(
                                    light.direction) * -1
                                light_direction = light_direction / \
                                    np.linalg.norm(light_direction)

                                intensity = np.dot(
                                    intercept.normal, light_direction)

                                intensity = max(0, min(1, intensity))

                                directional_light[0] += intensity * \
                                    light.intensity * light.color[0]
                                directional_light[1] += intensity * \
                                    light.intensity * light.color[1]
                                directional_light[2] += intensity * \
                                    light.intensity * light.color[2]

                        color_point[0] *= ambient_light[0] + \
                            directional_light[0]
                        color_point[1] *= ambient_light[1] + \
                            directional_light[1]
                        color_point[2] *= ambient_light[2] + \
                            directional_light[2]

                        color_point[0] = min(1, color_point[0])
                        color_point[1] = min(1, color_point[1])
                        color_point[2] = min(1, color_point[2])

                        self.point(x, y, color_point)
