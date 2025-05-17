import numpy as np
import pygame
from opensimplex import OpenSimplex


def generate_asteroid_texture(radius, seed=None):
    """Generate a smooth, natural-looking asteroid texture using noise"""
    size = int(radius * 2)
    surface = pygame.Surface((size, size), pygame.SRCALPHA)

    # Create noise generator with random or specified seed
    noise_gen = OpenSimplex(seed=seed)

    # Create base circular mask
    center = radius
    for x in range(size):
        for y in range(size):
            dx = x - center
            dy = y - center
            distance = np.sqrt(dx * dx + dy * dy)

            if distance < radius:
                # Generate multiple layers of noise for more detail
                noise_val = 0
                amplitude = 1.0
                frequency = 1.0

                for _ in range(4):  # Use 4 octaves of noise
                    noise_val += amplitude * noise_gen.noise2(
                        x * frequency * 0.1, y * frequency * 0.1
                    )
                    amplitude *= 0.5
                    frequency *= 2

                # Normalize noise to 0-1 range
                noise_val = (noise_val + 1) * 0.5

                # Create color gradient from dark to light gray
                color_val = int(noise_val * 128 + 64)

                # Smooth edge falloff
                edge_falloff = 1.0 - (distance / radius) ** 0.5
                alpha = int(255 * edge_falloff)

                surface.set_at((x, y), (color_val, color_val, color_val, alpha))

    return surface
