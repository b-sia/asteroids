import pygame
from pygame import Vector2

from asteroid import Asteroid
from asteroid_field import AsteroidField
from constants import *
from game_state import GameState
from player import Player
from shot import Shot


def initialize_sprite_groups():
    """Initialize and return sprite groups used in the game"""
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroid_group = pygame.sprite.Group()
    shot_group = pygame.sprite.Group()

    # Set up sprite containers
    Player.containers = [updatable, drawable]
    Shot.containers = [updatable, drawable, shot_group]
    Asteroid.containers = [updatable, drawable, asteroid_group]
    AsteroidField.containers = [updatable]

    return updatable, drawable, asteroid_group, shot_group


def draw_state(game_state, screen, drawable):
    # Drawing
    screen.fill((0, 0, 0))

    # Draw all game objects
    for sprite in drawable:
        sprite.draw(screen, sprite.triangle())

    # Draw UI elements
    game_state.player.draw_score(screen)
    game_state.player.draw_lives(screen)
    pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")
    clock = pygame.time.Clock()

    updatable, drawable, asteroid_group, shot_group = initialize_sprite_groups()
    sprite_groups = {
        "updatable": updatable,
        "drawable": drawable,
        "asteroid_group": asteroid_group,
        "shot_group": shot_group,
    }

    # Initialize game state and sprite groups
    game_state = GameState(sprite_groups)

    dt = 0

    # need to instantiate so that objects
    # are added to containers
    asteroid_field = AsteroidField()

    while game_state.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state.running = False
                if event.key == pygame.K_SPACE:
                    game_state.player.shoot()

        # Skip updates if game is over or paused
        if not game_state.is_game_over and not game_state.is_paused:
            updatable.update(dt)

            for asteroid in asteroid_group:
                if game_state.player.collision(asteroid):
                    game_state.player.handle_collision(asteroid)
                    if game_state.player.hit():
                        draw_state(game_state, screen, drawable)
                        game_state.handle_game_over(screen)
                        break

                for shot in shot_group:
                    if shot.collision(asteroid):
                        game_state.player.increase_score(asteroid.radius)
                        asteroid.split()

        screen.fill((0, 0, 0))

        # Draw all game objects
        for sprite in drawable:
            sprite.draw(screen, sprite.triangle())

        updatable.update(dt)
        draw_state(game_state, screen, drawable)

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
