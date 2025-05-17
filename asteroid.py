import pygame

from circleshape import CircleShape


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.velocity = pygame.Vector2(0, 0)

    def triangle(self):
        # Return points for circle approximation
        # Return points for drawing a polygon that looks like a circle
        points = []
        num_points = 8  # More points = smoother circle
        for i in range(num_points):
            angle = i * (360 / num_points)
            point = pygame.Vector2(0, -self.radius).rotate(angle) + self.position
            points.append(point)
        return points

    def update(self, dt):
        self.position += self.velocity * dt
