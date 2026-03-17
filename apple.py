import pygame
import random

from pygame.sprite import Sprite

class Apple(Sprite):
    """A class to manage the apple."""

    def __init__(self, snake_game):
        super().__init__()
        self.screen = snake_game.screen
        self.settings = snake_game.settings
        self.screen_rect = snake_game.screen.get_rect()
        self.color = self.settings.apple_color

        self.apple_x = 384
        self.apple_y = 340

        self.rect = pygame.Rect(self.apple_x, self.apple_y, 
                                self.settings.apple_size, 
                                self.settings.apple_size)
        
        self.apple_count = 0

    def spawn_apple(self, snake_positions, grid_positions):
        snake_set = set(tuple(pos) for pos in snake_positions)

        free_positions = [
            pos for pos in grid_positions if pos not in snake_set
        ]

        self.apple_x, self.apple_y = random.choice(free_positions)
    
    def draw_apple(self):
        """Draw the apple to the screen"""
        self.rect = pygame.Rect(self.apple_x, self.apple_y, 
                                self.settings.apple_size, 
                                self.settings.apple_size)
        pygame.draw.rect(self.screen, self.color, self.rect)
