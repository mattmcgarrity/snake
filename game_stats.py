"""Game statistics module for Snake.

Defines the GameStats class, which tracks the state and score of the game.
"""

import json

class GameStats:
	"""Track statistics for Snake.

	Attributes:
		settings: The shared Settings instance.
		score: The player's score in the current game.
		game_active: True while a game is in progress.
		high_score: The best score saved across all games.
		level: The current level.
	"""

	def __init__(self, game):
		"""Initialize statistics.

		Args:
			game: The running SnakeGame instance, used to access settings.
		"""
		self.settings = game.settings
		self.reset_stats()

		# Start Snake in an inactive state.
		self.game_active = False

		# High score should never be reset from saved score.
		filename = 'snake_high_score.json'
		with open(filename, 'r') as f:
			self.high_score = json.load(f)

		self.level = 1

	def reset_stats(self):
		"""Initialize statistics that can change during the game."""
		self.score = 0
		
