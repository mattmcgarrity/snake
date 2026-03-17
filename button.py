import pygame.font

class Button:

	def __init__(self, game, msg, x, y):
		"""Initialize button attributes."""
		self.screen = game.screen
		self.screen_rect = self.screen.get_rect()

		# Set the dimensions and properties of the button.
		self.width, self.height = 200, 50
		self.button_color = (0, 255, 0)
		self.text_color = (255, 255, 255)
		self.font = pygame.font.SysFont(None, 48)

		# Build the button's rect object and center it.
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.center = (x,y)

		# The button message needs to be prepped only once.
		self._prep_msg(msg)
		self.msg = msg

	def _prep_msg(self, msg):
		"""Turn msg into rendered image and center text on the button."""
		self.msg_image = self.font.render(msg, True, self.text_color)
		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.center = self.rect.center

	def draw_button(self):
		# Draw blank button and then draw message.
		self.screen.fill(self.button_color, self.rect)
		self.screen.blit(self.msg_image, self.msg_image_rect)

	def _change_button_color(self):
		"""Change the button color to blue to show it is selected."""

	def _revert_button_color(self):
		"""Turn other difficulty buttons back to default when not selected."""

class DifficultyButton(Button):

	def __init__(self, game, msg, x, y):
		"""Initialize difficulty button attributes."""
		super().__init__(game, msg, x, y)

		# Set the dimensions and properties of the button.
		self.width, self.height = 160, 40
		self.button_color = (60, 60, 60)
		self.text_color = (0, 255, 0)
		self.font = pygame.font.SysFont(None, 48)

		# Build the button's rect object.
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.center = (x,y)

		# The button message needs to be prepped only once.
		self._prep_msg(msg)

	def _change_button_color(self):
		"""Change the button color to blue to show it is selected."""
		self.button_color = (0, 255, 0)
		self.text_color = (60, 60, 60)
		self._prep_msg(self.msg)

	def _revert_button_color(self):
		"""Turn other difficulty buttons back to default when not selected."""
		self.button_color = (60, 60, 60)
		self.text_color = (0, 255, 0)
		self._prep_msg(self.msg)