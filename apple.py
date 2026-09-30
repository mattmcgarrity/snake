"""Apple module for Snake.

Defines the Apple class, which represents the food item the snake chases.
"""

import pygame
import random

from pygame.sprite import Sprite

class Apple(Sprite):
    """Manage the apple: its position, spawning, and drawing.

    Attributes:
        screen: The pygame display surface the apple is drawn on.
        settings: The shared Settings instance.
        screen_rect: Rect describing the full display surface.
        color: RGB tuple used to draw the apple.
        apple_x: Current x pixel coordinate of the apple's top-left corner.
        apple_y: Current y pixel coordinate of the apple's top-left corner.
        rect: pygame.Rect used for drawing and collision detection.
        apple_count: Number of apples eaten in the current game.
    """

    def __init__(self, snake_game):
        """Initialize the apple at its default starting position.

        Args:
            snake_game: The running SnakeGame instance, used to access the
                screen and settings.
        """
        super().__init__()
        self.screen = snake_game.screen
        self.settings = snake_game.settings
        self.screen_rect = snake_game.screen.get_rect()
        self.color = self.settings.apple_color

        # Default starting position, used until the first spawn_apple() call.
        self.apple_x = 384
        self.apple_y = 340

        self.rect = pygame.Rect(self.apple_x, self.apple_y,
                                self.settings.apple_size,
                                self.settings.apple_size)

        self.apple_count = 0

    def spawn_apple(self, snake_positions, grid_positions):
        """Move the apple to a random grid tile not occupied by the snake.

        Args:
            snake_positions: List of [x, y] coordinates occupied by the
                snake's body.
            grid_positions: List of (x, y) tuples for every tile in the
                playable area.
        """
        # Convert to a set of tuples for fast membership checks.
        snake_set = set(tuple(pos) for pos in snake_positions)

        free_positions = [
            pos for pos in grid_positions if pos not in snake_set
        ]

        self.apple_x, self.apple_y = random.choice(free_positions)

        self.rect.topleft = (self.apple_x, self.apple_y)

    def draw_apple(self):
        """Draw the apple to the screen"""
        # Rebuild the rect each frame so it tracks the latest spawn position.
        self.rect = pygame.Rect(self.apple_x, self.apple_y,
                                self.settings.apple_size,
                                self.settings.apple_size)
        pygame.draw.rect(self.screen, self.color, self.rect)
