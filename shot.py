import math

import pygame
from pygame import Vector2

from circleshape import CircleShape
from constants import BULLET_RADIUS, PLAYER_SHOT_SPEED, SCREEN_HEIGHT, SCREEN_WIDTH


class Shot(CircleShape):
    def __init__(self, position: Vector2, angle: float):
        super().__init__(position.x, position.y, BULLET_RADIUS)
        self.velocity = pygame.Vector2(0, 1)

        angle_rad = math.radians(angle - 90)  # -90 to align with player direction
        self.velocity = Vector2(
            math.cos(angle_rad) * PLAYER_SHOT_SPEED,
            math.sin(angle_rad) * PLAYER_SHOT_SPEED,
        )

    def update(self, dt):
        self.position += self.velocity * dt

        # Optional: Remove shot if it goes off screen
        if (
            self.position.x < 0
            or self.position.x > SCREEN_WIDTH
            or self.position.y < 0
            or self.position.y > SCREEN_HEIGHT
        ):
            self.kill()

    def triangle(self):
        forward = pygame.Vector2(0, -1).rotate(0)
        right = pygame.Vector2(0, -1).rotate(90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
