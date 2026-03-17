import json
from apple import Apple

class GameStats:
	"""Track statistics for Snake."""

	def __init__(self, game):
		"""Initialize statistics."""
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
		
