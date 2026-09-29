"""Scoreboard module for Snake.

Defines the Scoreboard class, which renders the title, score, level, and
high score, and saves new high scores to disk.
"""

import pygame.font
import json

class Scoreboard:
	"""Report scoring information to the player.

	Attributes:
		game: The running SnakeGame instance.
		screen: The pygame display surface the scoreboard is drawn on.
		screen_rect: Rect describing the full display surface.
		settings: The shared Settings instance.
		stats: The GameStats instance holding the current scores.
		text_color: RGB tuple used for all scoreboard text.
		font: Default pygame Font.
		score_font: pygame Font for the score and high score.
		level_font: pygame Font for the level.
		title_font: pygame Font for the game title.
	"""

	def __init__(self, game):
		"""Initialize scorekeeping attributes.

		Args:
			game: The running SnakeGame instance.
		"""
		self.game = game
		self.screen = game.screen
		self.screen_rect = self.screen.get_rect()
		self.settings = game.settings
		self.stats = game.stats

		# Font settings for game information.
		self.text_color = (0, 255, 0)
		self.font = pygame.font.SysFont(None, 38)
		self.score_font = pygame.font.SysFont(None, 26)
		self.level_font = pygame.font.SysFont(None, 44)
		self.title_font = pygame.font.SysFont(None, 56)

		# Prepare the initial title, score, level, and high score images.
		self.prep_title()
		self.prep_score()
		self.prep_level()
		self.prep_high_score()

	def prep_title(self):
		"""Turn the game title into a rendered image."""
		self.title_image = self.title_font.render("SNAKE", True, 
		        self.text_color)
		self.title_rect = self.title_image.get_rect()
		self.title_rect.centerx = self.screen_rect.centerx
		self.title_rect.top = self.screen_rect.top + 20

	def prep_level(self):
		"""Turn the current level into a rendered image."""
		score_str = "Level " + str(self.settings.snake_level)
		self.level_image = self.level_font.render(score_str, True,
				self.text_color)

		# Display the level in the bottom middle of the screen.
		self.level_rect = self.level_image.get_rect()
		self.level_rect.right = self.screen_rect.right - 300
		self.level_rect.top = 650

	def prep_score(self):
		"""Turn the current score into a rendered image."""
		rounded_score = round(self.stats.score)
		score_str = "Score: " + "{:,}".format(rounded_score)
		self.score_image = self.score_font.render(score_str, True,
				self.text_color)

		# Display the score at the top right of the screen.
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = 20

	def prep_high_score(self):
		"""Turn the high score into a rendered image."""
		high_score = round(self.stats.high_score, -1)
		high_score_str = "{:,}".format(high_score)
		self.high_score_image = self.score_font.render("High Score: " + 
				high_score_str, True, self.text_color)

		# Display the high score at the top left of the screen, level with
		# the current score.
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.left = self.screen_rect.left + 20
		self.high_score_rect.top = self.score_rect.top

	def check_high_score(self):
		"""Update the high score if the current score has beaten it."""
		if self.stats.score > self.stats.high_score:
			self.stats.high_score = round(self.stats.score)
			self.prep_high_score()

	def save_high_score(self):
		"""Save the high score to disk if it exceeds the stored value."""
		filename = 'snake_high_score.json'
		with open(filename, 'r') as f:
			saved_score = json.load(f)
			if self.stats.high_score > float(saved_score):
				saved_score = self.stats.high_score
		with open(filename, 'w') as s:
			json.dump(saved_score, s)

	def show_overall_info(self):
		"""Draw the high score and title to the screen."""
		self.screen.blit(self.high_score_image, self.high_score_rect)
		self.screen.blit(self.title_image, self.title_rect)
	
	def show_game_info(self):
		"""Draw the current score and level to the screen."""
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.level_image, self.level_rect)