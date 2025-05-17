import pygame
from pygame import Vector2

from asteroid import Asteroid
from asteroid_field import AsteroidField
from constants import *
from player import Player
from shot import Shot


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")

    # clock obj to control frame rate
    clock = pygame.time.Clock()

    running = True
    dt = 0

    # Player -> CircleShape -> pygame.sprite.Sprite
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroid_group = pygame.sprite.Group()
    shot_group = pygame.sprite.Group()

    # new Player instances add themselves to the groups
    Player.containers = [updatable, drawable]
    Shot.containers = [updatable, drawable, shot_group]
    Asteroid.containers = [updatable, drawable, asteroid_group]
    AsteroidField.containers = [updatable]

    # need to instantiate so that objects
    # are added to containers
    player = Player(Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    asteroid_field = AsteroidField()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    player.shoot()

        screen.fill((0, 0, 0))

        updatable.update(dt)

        for asteroid in asteroid_group:
            if player.collision(asteroid):
                print("Game Over!")
                running = False
                break

            for shot in shot_group:
                if shot.collision(asteroid):
                    asteroid.kill()

        for sprite in drawable:
            sprite.draw(screen, sprite.triangle())

        pygame.display.flip()

        # control the frame rate
        # doing clock caps the frame rate at 60FPS so
        # game loop doesn't hog all the CPU/GPU
        dt = clock.tick(60) / 1000

    pygame.quit()


if __name__ == "__main__":
    print("Starting asteroids")
    print("Screen width: ", SCREEN_WIDTH)
    print("Screen Height: ", SCREEN_HEIGHT)
    main()
