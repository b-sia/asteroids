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
        self.timer = 0
        self.lives = 5
        self.score = 0

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
        self.timer -= dt
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
        if self.timer <= 0:
            projectile = Shot(self.position.copy(), self.angle)
            self.timer = PLAYER_SHOT_COOLDOWN

    def hit(self):
        self.lives -= 1
        return self.lives <= 0

    def draw_lives(self, screen):
        for i in range(self.lives):
            pos = Vector2(30 + i * 30, 30)

            forward = Vector2(0, -1).rotate(0) * 10  # Smaller radius
            right = Vector2(0, -1).rotate(90) * 10 / 1.5
            points = [pos + forward, pos - forward - right, pos - forward + right]
            pygame.draw.polygon(screen, "red", points, 2)

    def handle_collision(self, asteroid):
        collision_normal = self.position - asteroid.position
        collision_normal.normalize_ip()

        relative_velocity = self.velocity - asteroid.velocity

        restitution = 0.8  # 1 = perfect elasticity, 0 = inelastic (stick)
        impulse_scalar = -(1 + restitution) * relative_velocity * collision_normal

        # assume mass proportional to radius
        total_mass = self.radius + asteroid.radius
        self_mass_ratio = self.radius / total_mass
        asteroid_mass_ratio = asteroid.radius / total_mass

        # apply impulse to player and asteroid
        self.velocity += collision_normal * impulse_scalar * asteroid_mass_ratio
        asteroid.velocity -= collision_normal * impulse_scalar * self_mass_ratio

        # separate objects to prevent sticking
        overlap = (self.radius + asteroid.radius) - self.position.distance_to(
            asteroid.position
        )
        if overlap > 0:
            separation = collision_normal * overlap
            self.position -= separation * 0.5
            asteroid.position -= separation * 0.5

    def increase_score(self, asteroid_size):
        if asteroid_size <= 20:
            self.score += 25
        elif asteroid_size <= 40:
            self.score += 100
        else:
            self.score += 250

    def draw_score(self, screen):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, "white")
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(score_text, score_rect)
