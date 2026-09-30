"""Snake module for Snake.

Defines the Snake class, which handles the snake's movement, body
tracking, drawing, and collision detection.
"""

import pygame
import random

from pygame.sprite import Sprite

class Snake(Sprite):
    """Manage the snake's position, movement, body, and collisions.

    The snake moves one tile at a time. Its body is stored as a list of
    [x, y] coordinates, with the head as the last element.

    Attributes:
        screen: The pygame display surface the snake is drawn on.
        settings: The shared Settings instance.
        screen_rect: Rect describing the full display surface.
        color: RGB tuple used to draw the snake.
        rect: pygame.Rect representing the snake's head.
        snake_len: Current length of the snake in segments.
        snake_list: List of [x, y] coordinates of every body segment.
        x: Head x position, stored as a float.
        y: Head y position, stored as a float.
        moving_right: True while the snake is heading right.
        moving_left: True while the snake is heading left.
        moving_up: True while the snake is heading up.
        moving_down: True while the snake is heading down.
    """

    def __init__(self, snake_game):
        """Initialize the snake and set its starting position.

        Args:
            snake_game: The running SnakeGame instance, used to access the
                screen and settings.
        """
        super().__init__()
        self.screen = snake_game.screen
        self.settings = snake_game.settings
        self.screen_rect = snake_game.screen.get_rect()
        self.color = self.settings.snake_color
        self.rect = pygame.Rect(self.settings.snake_x, self.settings.snake_y,
                                self.settings.snake_size,
                                self.settings.snake_size)
        self.snake_len = 1
        # Coordinates of each body segment, starting with just the head.
        self.snake_list = [[self.settings.snake_x, self.settings.snake_y]]

        # Store the snake's position as a decimal value.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Movement flags; at most one is True at a time.
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    # Function to update snake direction based on user input.
    def update(self):
        """Move the snake's head one tile in its current direction."""
        if self.moving_right:
            self.x +=self.settings.tile_size
        elif self.moving_left:
            self.x -=self.settings.tile_size
        elif self.moving_up:
            self.y -=self.settings.tile_size
        elif self.moving_down:
            self.y +=self.settings.tile_size

        # Sync the head's rect with its new position.
        self.rect.x = self.x
        self.rect.y = self.y

    def spawn_snake(self):
        """Place the snake's head at a random tile inside the play area."""
        new_pos = True
        while new_pos:
            snake_x = random.randint(
                self.settings.outline_size,
                self.settings.snake_screen_width
                - self.settings.snake_size - self.settings.outline_size)
            snake_y = random.randint(
                self.settings.outline_size,
                self.settings.snake_screen_height
                - self.settings.snake_size - self.settings.outline_size)

            # Only accept positions that line up with the tile grid.
            if (snake_x % self.settings.tile_size == 0
                    and snake_y % self.settings.tile_size == 0):
                self.x = snake_x
                self.y = snake_y
                new_pos = False

    def draw_snake(self):
        """Draw every segment of the snake to the screen."""
        for x, y in self.snake_list:
            pygame.draw.rect(self.screen, self.color, (x, y,
                             self.settings.snake_size,
                             self.settings.snake_size))

    def increment_snake(self):
        """Grow the snake by one segment when an apple is eaten."""
        self.snake_len += 1

    def track_snake_coordinates(self):
        """Record the head's position and trim the body to the snake's length."""
        snake_coord = [self.x, self.y]
        self.snake_list.append(snake_coord)

        # Drop the oldest segment so the list is never longer than the snake.
        if len(self.snake_list) > self.snake_len:
            del self.snake_list[0]

    def check_snake_collision(self):
        """Check whether the head has run into the snake's own body.

        Returns:
            bool: True if the head overlaps any other body segment,
                otherwise False.
        """
        # Compare the head against every segment except the head itself.
        for each_segment in self.snake_list[:-1]:
            if each_segment == [self.x, self.y]:
                return True
        return False


    def check_side_collisions(self):
        """Check whether the head has left the playable area.

        Returns:
            bool: True if the head has hit any edge of the play area,
                otherwise False.
        """
        if (
            self.x + self.settings.snake_size > self.settings.snake_screen_width or
            self.x < self.settings.outline_size or
            self.y + self.settings.snake_size > self.settings.snake_screen_height or
            self.y < self.settings.outline_size
        ):
            return True
        return False
