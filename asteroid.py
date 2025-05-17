import random

import pygame

from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.velocity = pygame.Vector2(0, 0)

    def triangle(self):
        # Return points for circle approximation
        # Return points for drawing a polygon that looks like a circle
        points = []
        num_points = 20  # More points = smoother circle
        for i in range(num_points):
            angle = i * (360 / num_points)
            point = pygame.Vector2(0, -self.radius).rotate(angle) + self.position
            points.append(point)
        return points

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()

        # random splitting
        split_angle = random.uniform(20, 50)

        new_angle_a = self.velocity.rotate(split_angle)
        new_angle_b = self.velocity.rotate(-1 * split_angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS

        asteroid_a = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid_b = Asteroid(self.position.x, self.position.y, new_radius)

        asteroid_a.velocity = new_angle_a * 1.2
        asteroid_b.velocity = new_angle_b * 1.2
