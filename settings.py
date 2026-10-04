"""Settings module for Snake.

Defines the Settings class, which stores every configurable value used
by the game, including screen layout, colors, speed, scoring, and sounds.
"""

import pygame

class Settings:
    """Store all settings for Snake.

    Static settings are set once in __init__; settings that change during
    play (speed, level, scoring) are set in initialize_dynamic_settings().
    """

    def __init__(self):
        """Initialize game's static settings """
        # Screen settings.
        self.screen_width = 704
        self.screen_height = 704
        self.outline_size = 64
        self.tile_size = 32

        # Colors
        self.bg_color = (20, 20, 20)
        self.outline_colour = (40, 40, 40)

        # Fonts
        self.font_size_normal = 38

        # Playable area for snake to roam.
        self.snake_screen_width = 640
        self.snake_screen_height = 640

        # Snake settings.
        self.snake_color = (50, 205, 50)
        self.snake_size = self.tile_size
        self.snake_x = 304
        self.snake_y = 340

        # Apple settings.
        self.apple_size = self.tile_size
        self.apple_color = (255, 0, 0)

        # How quickly the game speeds up for each difficulty. Each value is
        # the factor the frame rate is multiplied by at every speed increase.
        self.speedup_scale_easy = 1.02
        self.speedup_scale_normal = 1.05
        self.speedup_scale_hard = 1.07

        # Game Level.
        self.snake_level = 1

        # Score multiplier.
        self.score_scale = 1.5

        # Snake speed (Frame Rate).
        self.FPS = 8

        # Sounds.
        self.apple_sound = pygame.mixer.Sound("assets/apple_sound.mp3")
        self.game_over = pygame.mixer.Sound("assets/game_over.mp3")
        self.startup = pygame.mixer.Sound("assets/startup.mp3")
        self.menu_music = "assets/menu_music.mp3"

        self.music_volume = 0.3

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        # Number of apples between speed increases, and the apple count at
        # which the next increase occurs.
        self.speed_step = 5
        self.next_speed_increase = 5

        # Reset the snake's speed (frame rate).
        self.FPS = 8

        # Base points awarded per apple.
        self.apple_points = 10

        # Reset the level.
        self.snake_level = 1

    def increase_speed(self, difficulty):
        """Increase the game speed according to the chosen difficulty.

        Args:
                difficulty: One of 'easy', 'normal', or 'hard'. Any other value
                        leaves the speed unchanged.
        """
        if difficulty == 'easy':
            self.FPS *= self.speedup_scale_easy
        if difficulty == 'normal':
            self.FPS *= self.speedup_scale_normal
        if difficulty == 'hard':
            self.FPS *= self.speedup_scale_hard
