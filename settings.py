import pygame

class Settings:
	""" A class to store all settings for Snake """

	def __init__(self):
		"""Initialize game's static settings """
		# Screen settings
		self.screen_width = 704
		self.screen_height = 704
		self.bg_color = (20, 20, 20)
		self.outline_colour = (40, 40, 40)
		self.outline_size = 64
		self.tile_size = 32

		# Playable area for snake to roam
		self.snake_screen_width = 640
		self.snake_screen_height = 640

		# Snake settings
		self.snake_speed = 0.25
		self.snake_color = (50, 205, 50)
		self.snake_size = 32
		self.snake_x = 304
		self.snake_y = 340

		# Apple settings
		self.apple_size = 32
		self.apple_color = (255, 0, 0)

		# How quickly the game speeds up
		self.speedup_scale_easy = 1.02
		self.speedup_scale_normal = 1.05
		self.speedup_scale_hard = 1.07

		# Game Level
		self.snake_level = 1

		# Score multiplier
		self.score_scale = 1.5

		# Snake speed (Frame Rate)
		self.FPS = 8

		# Sounds
		self.apple_sound = pygame.mixer.Sound("assets/apple_sound.mp3")
		self.game_over = pygame.mixer.Sound("assets/game_over.mp3")
		self.startup = pygame.mixer.Sound("assets/startup.mp3")

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		"""Initialize settings that change throughout the game."""
		# Increase speed count
		self.speed_step = 5
		self.next_speed_increase = 5
		
		# Snake speed reset
		self.FPS = 8

		# Scoring
		self.apple_points = 10

		# Level reset
		self.snake_level = 1

	def increase_speed(self, difficulty):
		"""Increase speed"""
		if difficulty == 'easy':
			self.FPS *= self.speedup_scale_easy
		if difficulty == 'normal':
			self.FPS *= self.speedup_scale_normal
		if difficulty == 'hard':
			self.FPS *= self.speedup_scale_hard
