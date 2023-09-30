import pygame
from pygame import Surface
import math

from lights import *
from figures import Shape, Intercept
from materials import *

import threading
import time

MAX_RECURSION_DEPTH = 3


class Raytracer(object):
    '''
    Raytracer class

    This class is responsible for the main loop of the raytracer.

    Attributes:
        screen (pygame.display): The screen to render to.
    '''

    def __init__(self, screen: Surface) -> None:
        self.screen = screen
        self.width, self.height = screen.get_size()

        self.scene: list[Shape] = []
        self.lights: list[Light] = []

        self.camera_position = (0, 0, 0)

        self.viewport(0, 0, self.width, self.height)
        self.projection(60, 0.1)

        self.set_clear_color(0.25, 0.25, 0.25)
        self.set_current_color(1, 1, 1)

        self.batch_size = 64
        self.threads = False
        self.render_using = 'normal'

        self.environment_map: Surface = None

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
        # # invert y
        y = self.height - y
        if 0 <= x < self.width and 0 <= y < self.height:
            if color:
                self.set_current_color(*color)
            self.screen.set_at((x, y), self.current_color)

    def cast_ray(self, origin: tuple[float, float, float], direction: tuple[float, float, float], scene_obj: Shape = None, recursion: int = 0) -> Intercept | None:
        if recursion >= MAX_RECURSION_DEPTH:
            return None

        depth = float('inf')
        intercept = None
        hit = None

        for obj in self.scene:
            if obj != scene_obj:
                intercept = obj.ray_intersect(origin, direction)
                if intercept and intercept.distance < depth:
                    hit = intercept
                    depth = intercept.distance
        return hit

    def ray_color(self, intercept: Intercept, ray_direction: tuple[float, float, float], recursion: int = 0):
        if intercept is None:
            if self.environment_map:
                x = (math.atan2(ray_direction[2],
                                ray_direction[0]) / (2 * math.pi) + 0.5) * self.environment_map.get_width()
                y = math.acos(ray_direction[1]) / math.pi * \
                    self.environment_map.get_height()

                environment_color = self.environment_map.get_at(
                    (int(x), int(y)))

                return [i/255 for i in environment_color[:3]]
            else:
                return None

        material = intercept.obj.material
        surface_color = material.diffuse

        if material.texture and intercept.texture_coords:
            texture_x = intercept.texture_coords[0] * \
                material.texture.get_width()
            texture_y = intercept.texture_coords[1] * \
                material.texture.get_height()

            texture_color = material.texture.get_at(
                (int(texture_x), int(texture_y)))

            texture_color = [i/255 for i in texture_color[:3]]
            surface_color = [i*j for i, j in zip(
                surface_color, texture_color)]

        reflect_color = [0, 0, 0]
        ambient_color = [0, 0, 0]
        diffuse_color = [0, 0, 0]
        specular_color = [0, 0, 0]
        final_color = [0, 0, 0]

        if material.material_type == OPAQUE:
            for light in self.lights:
                if light.light_type == "ambient":
                    r, g, b = light.get_light_color()
                    ambient_color = [
                        ambient_color[0] + r,
                        ambient_color[1] + g,
                        ambient_color[2] + b
                    ]
                else:
                    shadow_intersect = None
                    direction = None

                    if light.light_type == "directional":
                        direction = [i*-1 for i in light.direction]
                    elif light.light_type == "point":
                        direction = pm.subtract(
                            light.point, intercept.point)
                        direction = pm.norm(direction)

                    shadow_intersect = self.cast_ray(
                        intercept.point,  direction, intercept.obj)

                    if shadow_intersect is None:
                        r, g, b = light.get_diffuse_color(
                            intercept)

                        diffuse_color = [
                            diffuse_color[0] + r,
                            diffuse_color[1] + g,
                            diffuse_color[2] + b
                        ]

                        r, g, b = light.get_specular_color(
                            intercept, self.camera_position)

                        specular_color = [
                            specular_color[0] + r,
                            specular_color[1] + g,
                            specular_color[2] + b
                        ]

        elif material.material_type == REFLECTIVE:
            reflect = pm.reflect_vector([i*-1 for i in ray_direction],
                                        intercept.normal)

            reflect_intercept = self.cast_ray(
                intercept.point, reflect, intercept.obj, recursion + 1)

            reflect_color = self.ray_color(
                reflect_intercept, reflect, recursion + 1)

            for light in self.lights:
                if light.light_type != "ambient":
                    shadow_intersect = None
                    direction = None

                    if light.light_type == "directional":
                        direction = [i*-1 for i in light.direction]
                    elif light.light_type == "point":
                        direction = pm.subtract(
                            light.point, intercept.point)
                        direction = pm.norm(direction)

                    shadow_intersect = self.cast_ray(
                        intercept.point,  direction, intercept.obj)

                    if shadow_intersect is None:
                        r, g, b = light.get_specular_color(
                            intercept, self.camera_position)

                        specular_color = [
                            specular_color[0] + r,
                            specular_color[1] + g,
                            specular_color[2] + b
                        ]

        light_color = [
            ambient_color[0] +
            diffuse_color[0] + specular_color[0] + reflect_color[0],
            ambient_color[1] +
            diffuse_color[1] + specular_color[1] + reflect_color[1],
            ambient_color[2] +
            diffuse_color[2] + specular_color[2] + reflect_color[2]
        ]

        final_color = [
            min(1, surface_color[0] * light_color[0]),
            min(1, surface_color[1] * light_color[1]),
            min(1, surface_color[2] * light_color[2])
        ]

        return final_color

    def pixel_render(self, x: int, y: int) -> None:
        # from window coordinates to norm device coordinates (NDC)
        position_x = ((x + 0.5 - self.viewport_x) /
                      self.viewport_width) * 2 - 1
        position_y = ((y + 0.5 - self.viewport_y) /
                      self.viewport_height) * 2 - 1

        position_x *= self.right_edge
        position_y *= self.top_edge

        # create ray
        direction = pm.norm(
            (position_x, position_y, -self.near_plane))

        intercept = self.cast_ray(self.camera_position, direction)
        ray_color = self.ray_color(intercept, direction)

        if ray_color:
            self.point(x, y, ray_color)
            pygame.display.flip()

    def render(self) -> None:
        start_time = time.time()
        if self.render_using == 'threads':
            print("Rendering with threads...")
            tasks = []
            for x in range(self.viewport_x, self.viewport_x + self.viewport_width, self.batch_size):
                for y in range(self.viewport_y, self.viewport_y + self.viewport_height, self.batch_size):
                    x_end = min(x + self.batch_size, self.width)
                    y_end = min(y + self.batch_size, self.height)
                    tasks.append(threading.Thread(
                        target=self.batch_render, args=(x, x_end, y, y_end)))
            for task in tasks:
                task.start()
            for task in tasks:
                task.join()
        else:
            print("Rendering without threads...")
            for x in range(self.viewport_x, self.viewport_x + self.viewport_width):
                for y in range(self.viewport_y, self.viewport_y + self.viewport_height):
                    self.pixel_render(x, y)

        end_time = time.time()
        print("Rendering took {} seconds".format(end_time - start_time))

    def batch_render(self, x_start, x_end, y_start, y_end) -> None:
        for x in range(x_start, x_end):
            for y in range(y_start, y_end):
                if 0 <= x < self.width and 0 <= y < self.height:
                    self.pixel_render(x, y)
