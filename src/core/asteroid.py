import math
import random

import numpy as np
import pygame

from src.core.circleshape import CircleShape
from src.utils.constants import ASTEROID_MIN_RADIUS
from src.utils.utils import generate_asteroid_texture


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

        # Generate unique texture with surface caching
        self.cached_surface = None
        self.last_points = None
        self._setup_texture()

        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-30, 30)  # degrees per second

    def _setup_texture(self):
        self.original_texture = generate_asteroid_texture(
            self.radius, seed=random.randint(1, 1000)
        )
        self.cached_surface = None

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
        self.rotation += self.rotation_speed * dt
        self.rotation %= 360

    def draw(self, surface, points=None):
        if points is None:
            points = self.triangle()

        if self.cached_surface is None or self.last_points != points:
            # Create a surface for the deformed asteroid
            # important to make asteroid slightly bigger, else
            # surface interpolation cannot be done, and you will
            # have square asteroids :(
            size = int(self.radius * 2.4)

            deformed = pygame.Surface((size, size), pygame.SRCALPHA)

            # Calculate center of the surface
            center = pygame.Vector2(size / 2, size / 2)

            # precalculate angles and radiuses for the shape
            angles = []
            radiuses = []

            for i in range(360):  # One degree steps
                angle = math.radians(i)
                t = angle / (2 * math.pi)
                varied_radius = self.radius * self.interpolate(t)
                angles.append(angle)
                radiuses.append(varied_radius)

            # Use numpy for faster array operations
            x_coords = np.arange(size)
            y_coords = np.arange(size)
            xx, yy = np.meshgrid(x_coords, y_coords)

            # Calculate positions relative to center
            pos_x = xx - center.x
            pos_y = yy - center.y
            distances = np.sqrt(pos_x**2 + pos_y**2)
            angles = np.arctan2(pos_y, pos_x) % (2 * np.pi)

            # Map angles to pre-calculated radiuses
            angle_indices = (angles * 180 / np.pi).astype(int)
            varied_radiuses = np.array(radiuses)[angle_indices]

            # Create mask for valid pixels
            mask = distances <= varied_radiuses

            # Apply texture only where mask is True
            for x, y in np.argwhere(mask):
                ratio = distances[y][x] / varied_radiuses[y][x]
                normalized_x = int(pos_x[y][x] * ratio + self.radius)
                normalized_y = int(pos_y[y][x] * ratio + self.radius)

                if (
                    0 <= normalized_x < self.original_texture.get_width()
                    and 0 <= normalized_y < self.original_texture.get_height()
                ):
                    color = self.original_texture.get_at((normalized_x, normalized_y))
                    deformed.set_at((x, y), color)

            self.cached_surface = deformed
            self.last_points = points.copy()

        # Rotate the deformed texture
        rotated = pygame.transform.rotate(deformed, self.rotation)
        rect = rotated.get_rect(center=self.position)
        surface.blit(rotated, rect)

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
