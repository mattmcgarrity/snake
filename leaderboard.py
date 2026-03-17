import pygame.font
import json

class Leaderboard:
	"""A class to keep up track of the top 10 high scores."""

	def __init__(self, game):
		"""Initialize leaderboard attributes."""
		self.game = game
		self.screen = game.screen
		self.screen_rect = self.screen.get_rect()
		self.settings = game.settings
		self.stats = game.stats

		# Font settings for scores and names.
		self.text_color = (0, 255, 0)
		self.font = pygame.font.SysFont(None, 38)
		self.top_five = [0, 0, 0, 0, 0]

	def get_top_five(self):
		"""Retrieve the top five best scores."""
		filename = 'snake_top_five.json'
		with open(filename, 'r') as f:
			score = f.read()
			score_ints = [int(x) for x in score.split()]
			self.top_five = score_ints
			f.close()

	def add_new_leaderboard_score(self):
		"""Add a new score to the top five."""
		self.get_top_five()
		lowest_score = min(self.top_five)

		if self.stats.score > lowest_score:
			self.top_five.remove(lowest_score)
			self.top_five.append(round(self.stats.score))
			self.top_five.sort(reverse=True)

			x = 0
			filename = 'snake_top_five.json'
			with open(filename, 'w') as f:
				for score in self.top_five:
					score = str(score)
					self.top_five[x] = score
					x+=1

				f.write('\n'.join(self.top_five))

	def prep_leaderboard(self):
		"""Turn the leaderboard into a rendered image."""
		self.get_top_five()
		
		x = 0
		y = 160
		
		position = 1

		# Display Leaderboard Title Image.
		self.lb_title_image = self.font.render("LEADERBOARD", True,
				self.text_color)

		# Display the score in the middle of the screen.
		self.lb_title_rect = self.lb_title_image.get_rect()
		self.lb_title_rect.right = self.screen_rect.right - 245
		self.lb_title_rect.top = 96
			
		self.screen.blit(self.lb_title_image, self.lb_title_rect)

		# Display score images.
		for score in self.top_five:
			rounded_score = round(score, -1)
			score_str = "{:,}".format(rounded_score)

			self.lb_image = self.font.render(str(position) + ". " + score_str, True,
				self.text_color)

			# Display the score in the middle of the screen.
			self.lb_rect = self.lb_image.get_rect()
			self.lb_rect.right = self.screen_rect.right - 300
			self.lb_rect.top = y
			x += 50
			self.screen.blit(self.lb_image, self.lb_rect)
			y += 32
			
			position += 1
		


				



