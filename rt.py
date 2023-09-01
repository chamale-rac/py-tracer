import pygame


class Raytracer:
    '''
    Raytracer class

    This class is responsible for the main loop of the raytracer.

    Attributes:
        screen (pygame.display): The screen to render to.
    '''

    def __init__(self, screen: pygame.display) -> None:
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        self.set_clear_color(0, 0, 0)
        self.set_current_color(1, 1, 1)
        self.viewport(0, 0, self.width, self.height)

    def viewport(self, x, y, width, height):
        self.viewport_x = x
        self.viewport_y = y
        self.viewport_width = width
        self.viewport_height = height

    def set_clear_color(self, r, g, b):
        self.clear_color = (r*255, g*255, b*255)

    def clear(self):
        self.screen.fill(self.clear_color)

    def set_current_color(self, r, g, b):
        self.current_color = (r*255, g*255, b*255)

    def point(self, x, y, color=None):
        # TODO: Consider flipping the y axis
        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            if color:
                self.set_current_color(*color)
        self.screen.set_at((x, y), self.current_color)

    def render(self):
        pass
