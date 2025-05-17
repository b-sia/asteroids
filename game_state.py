import pygame
from pygame import Vector2

from constants import *
from player import Player


class GameState:
    def __init__(self, sprite_groups):
        self.is_game_over = False
        self.is_paused = False
        self.sprite_groups = sprite_groups
        self.running = True
        self.player = None
        self.reset_game()

    def reset_game(self):
        """Reset the game state"""
        # remove existing players
        if self.player:
            self.player.kill()

        # Create new player at center of screen
        start_pos = Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.player = Player(start_pos)

        # Add player to sprite groups
        self.sprite_groups["updatable"].add(self.player)
        self.sprite_groups["drawable"].add(self.player)

        self.is_game_over = False
        self.is_paused = False

    def show_game_over_popup(self, screen):
        """Show game over popup with final score and options"""
        # Create semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))

        # Create popup rectangle
        popup_width, popup_height = 400, 300
        popup_x = SCREEN_WIDTH // 2 - popup_width // 2
        popup_y = SCREEN_HEIGHT // 2 - popup_height // 2
        popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
        pygame.draw.rect(screen, (50, 50, 50), popup_rect)
        pygame.draw.rect(screen, "white", popup_rect, 2)

        # Render text
        font = pygame.font.Font(None, 48)
        game_over_text = font.render("Game Over", True, "white")
        score_text = font.render(f"Final Score: {self.player.score}", True, "white")
        continue_text = font.render("Press SPACE to continue", True, "white")
        quit_text = font.render("Press ESC to quit", True, "white")

        # Position text
        screen.blit(
            game_over_text,
            game_over_text.get_rect(centerx=SCREEN_WIDTH // 2, y=popup_y + 50),
        )
        screen.blit(
            score_text, score_text.get_rect(centerx=SCREEN_WIDTH // 2, y=popup_y + 120)
        )
        screen.blit(
            continue_text,
            continue_text.get_rect(centerx=SCREEN_WIDTH // 2, y=popup_y + 190),
        )
        screen.blit(
            quit_text, quit_text.get_rect(centerx=SCREEN_WIDTH // 2, y=popup_y + 240)
        )

        pygame.display.flip()

    def handle_game_over(self, screen):
        """Handle game over state and user input"""
        self.is_game_over = True
        self.show_game_over_popup(screen)

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                        return
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        return
