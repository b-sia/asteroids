import pygame
from circleshape import CircleShape

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        # if hasattr(self, "containers"):
        #     super().__init__(self.containers)
        # else:
        #     super().__init__()

        Asteroid.containers = None

    def draw(self, screen, position, radius, width=2):
        pygame.draw.circle(screen, color="white", center=position, radius=radius, width=width)

    def update(self, dt):
        self.position = self.velocity * dt
