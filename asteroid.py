import math
import random

import pygame

from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.velocity = pygame.Vector2(0, 0)

        # Create fewer control points for smoother interpolation
        self.num_control_points = 8
        self.control_points = [
            random.uniform(0.8, 1.2) for _ in range(self.num_control_points)
        ]

        # add first point to end to wrap the interpolation around
        self.control_points.append(self.control_points[0])

    def interpolate(self, t):
        """
        t: a value between 0 and 1 that represents progress around the asteroid's perimeter
        (e.g. t=0.25 = 25% around the shape)

        The segment maps the progress around the number of points.
        The segment is split into the integer part and fraction part.
        Integer part identifies which two control points to interpolate between.
        Fractional part represents the interpolation between the two points.

        Fractional part is replaced with a sigmoid-like curve interpolation,
        then adjacent controlled points are combined using a smooth f.
        """
        segment = t * self.num_control_points
        i = int(segment)
        f = segment - i
        f = f * f * (3 - 2 * f)

        return self.control_points[i] * (1 - f) + self.control_points[i + 1] * f

    def triangle(self):
        # Return points for circle approximation
        # Return points for drawing a polygon that looks like a circle
        points = []
        num_points = 32  # More points = smoother circle
        for i in range(num_points):
            t = i / num_points
            angle = t * 2 * math.pi

            # smoothly interpolated radius variation
            varied_radius = self.radius * self.interpolate(t)
            point = (
                pygame.Vector2(0, -varied_radius).rotate(math.degrees(angle))
                + self.position
            )
            points.append(point)
        return points

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        # prevents multiple splitting
        if self.radius <= ASTEROID_MIN_RADIUS:
            self.kill()
            return

        self.kill()

        # random splitting
        split_angle = random.uniform(20, 50)
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        asteroid_a = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid_b = Asteroid(self.position.x, self.position.y, new_radius)

        new_angle_a = self.velocity.rotate(split_angle)
        new_angle_b = self.velocity.rotate(-split_angle)

        asteroid_a.velocity = new_angle_a * 1.2
        asteroid_b.velocity = new_angle_b * 1.2
