import pygame

from circleshape import CircleShape


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        Asteroid.containers = None

    def draw(self, screen, position, radius, width=2):
        pygame.draw.circle(
            screen, color="white", center=position, radius=radius, width=width
        )

    def update(self, dt):
        self.position = self.velocity * dt
