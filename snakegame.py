"""Snake: the classic arcade game, built with pygame.

Run this module directly to start the game::

    python snakegame.py

Controls (menu):
    Enter / Play button: start a game.
    Up / Down arrows or mouse: choose the difficulty.
    Q: quit.

Controls (in game):
    Arrow keys: steer the snake.
"""

import sys
from time import sleep

import pygame

from snake import Snake
from apple import Apple
from settings import Settings
from button import Button
from button import DifficultyButton
from leaderboard import Leaderboard
from scoreboard import Scoreboard
from game_stats import GameStats

class SnakeGame:
    """Create and run an instance of the Snake game.

    This class owns the main game loop and coordinates the snake, apple,
    scoreboard, leaderboard, menu buttons, and sounds.

    Attributes:
        settings: The Settings instance holding all game configuration.
        screen: The pygame display surface.
        stats: The GameStats instance tracking score and game state.
        sb: The Scoreboard instance for score, level, and high score.
        lb: The Leaderboard instance for the top five scores.
        snake: The Snake instance controlled by the player.
        apple: The Apple instance the snake tries to eat.
        clock: pygame Clock used to cap the frame rate.
        play_button: The menu's Play button.
        easy_button: The Easy difficulty button.
        normal_button: The Normal difficulty button.
        hard_button: The Hard difficulty button.
        difficulty_level: The selected difficulty: 'easy', 'normal', or
            'hard'.
        grid_positions: List of (x, y) tuples for every tile in the play
            area.
    """

    def __init__(self):
        """Initialize pygame, the game objects, the menu, and the music."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((
			self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Snake")

        # Create an instance to store game statistics,
        # and create a scoreboard and leaderboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.lb = Leaderboard(self)
        
        self.snake = Snake(self)
        self.apple = Apple(self)

        self.clock = pygame.time.Clock()

        # Make the play button.
        self.play_button = Button(self, "Play", 350, 425)

        # Make the difficulty buttons.
        self.easy_button = DifficultyButton(self, "Easy", 350, 500)
        self.normal_button = DifficultyButton(self, "Normal", 350, 550)
		
        # Change color of normal button to symbolize default option.
        self.normal_button._change_button_color()
        self.hard_button = DifficultyButton(self, "Hard", 350, 600)

        # Normal is the default difficulty level.
        self.difficulty_level = 'normal'

        # Create a grid of every tile position in the playable area.
        self.grid_positions = []
        for x in range(self.settings.outline_size, 
                       self.settings.snake_screen_width
                       - self.settings.tile_size,
                       self.settings.tile_size):
            for y in range(self.settings.outline_size, 
                       self.settings.snake_screen_height 
                       - self.settings.tile_size,
                       self.settings.tile_size):
                self.grid_positions.append((x,y))

        # Start the menu music, looping indefinitely.
        pygame.mixer.music.load('assets/menu_music.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
            

    def _start_game(self):
        """Reset the snake, apple, display, and music to start a game.

        Called from _prep_game() when the player clicks Play or presses
        Enter.
        """
        self.stats.reset_stats()

        # Reset the snake to a single segment with no direction.
        self.snake.snake_len = 1
        self.snake.snake_list = [[self.settings.snake_x, self.settings.snake_y]]
        self.snake.moving_down = False
        self.snake.moving_up = False
        self.snake.moving_left = False
        self.snake.moving_right = False

        self.snake.spawn_snake()

        # Reset the apple.
        self.apple.apple_count = 0
        self.apple.spawn_apple(self.snake.snake_list, self.grid_positions)

        # Show current score information.
        self.sb.show_overall_info()
        self.sb.show_game_info()

        # Hide the mouse cursor during play.
        pygame.mouse.set_visible(False)

        # Play the startup sound, then switch to the in-game music.
        pygame.mixer.Sound.play(self.settings.startup)
        pygame.mixer.music.load('assets/game_music.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
    
    def run_game(self):
        """Start the main loop for the game.

        Each pass through the loop handles input and, while a game is
        active, moves the snake, checks for apples and collisions, and
        speeds the game up as apples are eaten. The screen is redrawn and
        the frame rate capped on every pass.
        """
        runflag = True
        while runflag:
            #Watch for keyboard and mouse events.
            self._check_events()
            
            if self.stats.game_active:
                self.snake.update()
                self.snake.track_snake_coordinates()
                self.snake.check_snake_collision()

                # Check whether the snake's head has reached the apple.
                collide = pygame.Rect.colliderect(self.snake.rect, 
                                                  self.apple.rect)
            
                if collide:
                    # Eat the apple: score points, respawn it, and grow.                   
                   pygame.mixer.Sound.play(self.settings.apple_sound)
                   self.apple.apple_count += 1
                   self.apple.spawn_apple(self.snake.snake_list, 
                                          self.grid_positions)
                   self.stats.score += (self.settings.apple_points 
                                        * self.settings.score_scale 
                                        * self.apple.apple_count)
                   self.sb.prep_score()
                   self.sb.prep_level()
                   self.sb.check_high_score()
                   self.snake.increment_snake()
        
                # End the game if the snake hits a wall or itself.                
                if (self.snake.check_side_collisions() or 
                    self.snake.check_snake_collision()):
                    pygame.mixer.music.stop()
                    pygame.mixer.Sound.play(self.settings.game_over)
                    self.stats.game_active = False
                    self.sb.save_high_score()
                    self.lb.add_new_leaderboard_score()
                    # Pause briefly so the game-over sound can play.
                    sleep(4)
                    pygame.mixer.music.load('assets/menu_music.mp3')
                    pygame.mixer.music.play(-1)
                    pygame.mouse.set_visible(True)

                # Speed the game up each time enough apples are eaten.
                if self.apple.apple_count >= self.settings.next_speed_increase:
                    self.settings.increase_speed(self.difficulty_level)
                    self.settings.next_speed_increase += self.settings.speed_step
                    self.settings.snake_level += 1
            
            self._update_screen()
            self.clock.tick(self.settings.FPS)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
                self._check_keydown_menu_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_difficulty_button(mouse_pos)
    
    def _prep_game(self):
        """Reset all game settings and stats for a fresh game."""
        # Reset the game settings. 
        self.settings.initialize_dynamic_settings()

		# Reset the game statistics.
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_level()
        self.sb.prep_score()

		# Start game.
        self._start_game()

    
    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play.

        Args:
            mouse_pos: (x, y) position of the mouse click.
        """        
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._prep_game()

    def _click_easy_button(self):
        """Select the Easy difficulty and update the button highlighting."""
        self.difficulty_level = 'easy'
        self.easy_button._change_button_color()
        self.normal_button._revert_button_color()
        self.hard_button._revert_button_color()

    def _click_normal_button(self):
        """Select the Normal difficulty and update the button highlighting."""
        self.difficulty_level = 'normal'
        self.easy_button._revert_button_color()
        self.normal_button._change_button_color()
        self.hard_button._revert_button_color()

    def _click_hard_button(self):
        """Select the Hard difficulty and update the button highlighting."""
        self.difficulty_level = 'hard'
        self.easy_button._revert_button_color()
        self.normal_button._revert_button_color()
        self.hard_button._change_button_color()

    def _check_difficulty_button(self, mouse_pos):
        """Set the difficulty based on which button, if any, was clicked.

        Args:
            mouse_pos: (x, y) position of the mouse click.
        """
        easy_button_clicked = self.easy_button.rect.collidepoint(mouse_pos)
        normal_button_clicked = self.normal_button.rect.collidepoint(mouse_pos)
        hard_button_clicked = self.hard_button.rect.collidepoint(mouse_pos)

        if easy_button_clicked:
            self._click_easy_button()
        elif normal_button_clicked:
            self._click_normal_button()
        elif hard_button_clicked:
            self._click_hard_button()

    def _check_keydown_menu_events(self, event):
        """Handle keyboard input for menu navigation and starting the game.

        Only active while no game is in progress. Enter starts a game, Q
        quits, and the Up/Down arrows move the difficulty selection.

        Args:
            event: The pygame KEYDOWN event to handle.
        """
        if not self.stats.game_active:
            if event.key == pygame.K_RETURN:
                self._prep_game()
            elif event.key == pygame.K_q:
                sys.exit() 
            elif event.key == pygame.K_UP:
                # Move the difficulty selection up one option.
                if self.difficulty_level == 'normal':
                    self._click_easy_button()
                elif self.difficulty_level == 'hard':
                    self._click_normal_button()
            elif event.key == pygame.K_DOWN:
                # Move the difficulty selection down one option.
                if self.difficulty_level == 'easy':
                    self._click_normal_button()
                elif self.difficulty_level == "normal":
                    self._click_hard_button()

    def _check_keydown_events(self, event):
        """Respond to arrow keypresses by steering the snake.

        Args:
            event: The pygame KEYDOWN event to handle.
        """
        # Ensures snake cannot move in the same direction it came.
        if self.snake.snake_len == 1:
            # A snake with a length of 1 can move in any direction.
            if  event.key == pygame.K_RIGHT: 
                self._moving_right()
            elif event.key == pygame.K_LEFT:
                self._moving_left()
            elif event.key == pygame.K_DOWN:
                self._moving_down()
            elif event.key == pygame.K_UP:
                self._moving_up()
        else:
            # Ensure the snake cannot reverse into its own body.
            if  event.key == pygame.K_RIGHT and self.snake.moving_left == False: 
                self._moving_right()
            elif event.key == pygame.K_LEFT and self.snake.moving_right == False:
                self._moving_left()
            elif event.key == pygame.K_DOWN and self.snake.moving_up == False:
                self._moving_down()
            elif event.key == pygame.K_UP and self.snake.moving_down == False:
                self._moving_up()
    
    def _moving_up(self):
        """Set the snake's direction to up."""
        self.snake.moving_down = False
        self.snake.moving_right = False
        self.snake.moving_left = False
        self.snake.moving_up = True
    
    def _moving_down(self):
        """Set the snake's direction to down."""
        self.snake.moving_right = False
        self.snake.moving_left = False
        self.snake.moving_down = True
        self.snake.moving_up = False

    def _moving_right(self):
        """Set the snake's direction to right."""
        self.snake.moving_up = False
        self.snake.moving_down = False
        self.snake.moving_right = True
        self.snake.moving_left = False

    def _moving_left(self):
        """Set the snake's direction to left."""
        self.snake.moving_up = False
        self.snake.moving_down = False
        self.snake.moving_left = True
        self.snake.moving_right = False

    def _update_screen(self):
        """Redraw everything on screen and flip to the new frame."""
        self.screen.fill(self.settings.bg_color)
        pygame.draw.rect(self.screen, self.settings.outline_colour, 
                         self.screen.get_rect(), self.settings.outline_size)
        self.snake.draw_snake()
        self.apple.draw_apple()
        self.sb.show_overall_info()

        # Show current score information during a game.
        if self.stats.game_active:
            self.sb.show_game_info()

        # Draw the menu (buttons and leaderboard) if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()
            self.easy_button.draw_button()
            self.normal_button.draw_button()
            self.hard_button.draw_button()
            self.lb.prep_leaderboard()
		#	self.lb.show_leaderboard()

        pygame.display.flip()
    
if __name__ == '__main__': 
    # Make a game instance and run the game.
    game = SnakeGame()
    game.run_game()
         
        