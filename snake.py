import pygame
import sys
import random

from pygame.sprite import Sprite

class Snake(Sprite):

    def __init__(self, snake_game): 
        """Initialize the snake and set its starting position."""
        super().__init__()
        self.screen = snake_game.screen
        self.settings = snake_game.settings
        self.screen_rect = snake_game.screen.get_rect()
        self.color = self.settings.snake_color
        self.rect = pygame.Rect(self.settings.snake_x, self.settings.snake_y,
                                self.settings.snake_size, 
                                self.settings.snake_size)
        self.snake_len = 1
        self.snake_list = [[self.settings.snake_x, self.settings.snake_y]] #Empty list to store snake coordinates

        # Store the snake's position as a decimal value
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Movement flags
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
    
    # Function to update snake direction based on user input
    def update(self):
        if self.moving_right:
            self.x +=self.settings.tile_size
        elif self.moving_left:
            self.x -=self.settings.tile_size
        elif self.moving_up:
            self.y -=self.settings.tile_size
        elif self.moving_down:
            self.y +=self.settings.tile_size

        # Update snake body position
        self.rect.x = self.x
        self.rect.y = self.y

    def spawn_snake(self):
        """Center snake on screen"""
        new_pos = True
        while new_pos:
            snake_x = random.randint(self.settings.outline_size, self.settings.snake_screen_width - self.settings.snake_size - self.settings.outline_size)
            snake_y = random.randint(self.settings.outline_size, self.settings.snake_screen_height - self.settings.snake_size - self.settings.outline_size)

            if snake_x % self.settings.tile_size == 0 and snake_y % self.settings.tile_size == 0:
               self.x = snake_x
               self.y = snake_y
               new_pos = False
    
    def draw_snake(self):
        """Draws the snake to the screen"""
        for x, y in self.snake_list:
            pygame.draw.rect(self.screen, self.color, (x, y, 
                             self.settings.snake_size,
                             self.settings.snake_size))

    def increment_snake(self):
        """Adds to snake body when apple is eaten"""
        self.snake_len += 1

    def track_snake_coordinates(self):
        """Keep track of the coordinates of the snake"""
        snake_coord = [self.x, self.y]
        self.snake_list.append(snake_coord)

        # Keep list only as long as snake
        if len(self.snake_list) > self.snake_len:
            del self.snake_list[0]

    def check_snake_collision(self):
        # If snake runs into itself
        for each_segment in self.snake_list[:-1]:
            if each_segment == [self.x, self.y]:
                return True
        return False


    def check_side_collisions(self):
        """Returns true if snake hits edges or itself"""
        if ( 
            self.x + self.settings.snake_size > self.settings.snake_screen_width or
            self.x < self.settings.outline_size or
            self.y + self.settings.snake_size > self.settings.snake_screen_height or
            self.y < self.settings.outline_size
        ):
            return True
        return False