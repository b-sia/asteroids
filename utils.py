import numpy as np
import pygame
from opensimplex import OpenSimplex


def generate_asteroid_texture(radius, seed=None):
    """
    Generate a smooth, natural-looking asteroid texture using noise

    1.) Creates a noise generator with seed.
    2.) Create fractal noise patterns with noise gen.
    3.) Normalize noise, enhance contrast, create gray variation.
    4.) Edge smoothing.
    """
    size = int(radius * 2)
    surface = pygame.Surface((size, size), pygame.SRCALPHA)

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

                # Normalize noise to 0-1 range and enhance contrast
                noise_val = (noise_val + 1) * 0.5
                noise_val = noise_val * 0.8 + 0.2

                # Create more varied color gradient
                base_color = 64
                color_range = 160
                color_val = int(base_color + noise_val * color_range)

                # Smoother edge falloff that preserves texture
                edge_distance = distance / radius
                if edge_distance < 0.8:  # sharp opacity
                    alpha = 255
                else:
                    alpha = int(
                        255 * (1.0 - (edge_distance - 0.8) / 0.2)
                    )  # gradual transparency fade

                surface.set_at((x, y), (color_val, color_val, color_val, alpha))

    return surface
