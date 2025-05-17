import math

import pygame
from pygame import Vector2

from circleshape import CircleShape
from constants import *
from shot import Shot


class Player(CircleShape):
    def __init__(self, pos: Vector2, radius=20):
        # Initialize parent CircleShape with position and radius
        super().__init__(pos, 15, radius=radius)

        self.velocity = Vector2(0, 0)
        self.acceleration = 200.0  # pixels per second squared
        self.rotation_speed = 180  # degrees/s
        self.friction = 0.99  # dampens velocity
        self.angle = 0

    def rotate(self, direction: float, dt):
        """Rotate the player (direction: 1 for right, -1 for left)"""
        self.angle += self.rotation_speed * direction * dt
        # self.angle = PLAYER_TURNED_SPEED * dt
        self.angle %= 360  # keep angle between 0 and 360

    def thrust(self, dt: float):
        """Apply thrust in the direction the player is facing"""
        # convert angle to radians for math calculations
        angle_rad = math.radians(self.angle - 90)

        # calculate the thrust direction vector
        thrust_dir = Vector2(math.cos(angle_rad), math.sin(angle_rad))

        # accelerate
        self.velocity += thrust_dir * self.acceleration * dt

    def update(self, dt: float):
        """Update player position based on velocity"""
        self.move(dt)
        self.screen_wrap()

    def move(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-1, dt)
        if keys[pygame.K_d]:
            self.rotate(1, dt)
        if keys[pygame.K_w]:
            self.thrust(dt)
        if keys[pygame.K_s]:
            self.thrust(-dt)

        self.velocity *= self.friction
        self.position += self.velocity * dt

    def screen_wrap(self):
        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x = 0

        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y = 0

    def triangle(self):
        forward = Vector2(0, -1).rotate(self.angle)
        right = Vector2(0, -1).rotate(self.angle + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def shoot(self):
        projectile = Shot(self.position, self.angle)
        projectile.velocity = Vector2(0, 1)
        projectile.velocity *= PLAYER_SHOT_SPEED
