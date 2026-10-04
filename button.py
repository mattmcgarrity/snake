"""Button module for Snake.

Defines the Button class for the menu's Play button and the
DifficultyButton subclass for the selectable difficulty options.
"""

import pygame.font

class Button:
    """A clickable on-screen button with a centered text label.

    Attributes:
            screen: The pygame display surface the button is drawn on.
            screen_rect: Rect describing the full display surface.
            width: Button width in pixels.
            height: Button height in pixels.
            button_color: RGB tuple for the button's fill color.
            text_color: RGB tuple for the label's color.
            font: pygame Font used to render the label.
            rect: pygame.Rect defining the button's position and size.
            msg: The label text.
            msg_image: The rendered label surface.
            msg_image_rect: Rect used to position the rendered label.
    """

    def __init__(self, game, msg, x, y):
        """Initialize button attributes.

        Args:
                game: The running SnakeGame instance, used to access the screen.
                msg: Text to display on the button.
                x: x pixel coordinate of the button's center.
                y: y pixel coordinate of the button's center.
        """
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        # Set colors to be used for buttons.
        self.green = (0, 255, 0)
        self.dark_gray = (60, 60, 60)
        self.white = (255, 255, 255)

        # Initialize dimensions and properties of the button.
        self.width = 200
        self.height = 50
        self.button_color = self.green
        self.text_color = self.white
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x,y)

        # The button message needs to be prepped only once.
        self._prep_msg(msg)
        self.msg = msg

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center it on the button.

        Args:
                msg: Text to render.
        """
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw the button and its label to the screen."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def _change_button_color(self):
        """Highlight the button to show it is selected.

        Overridden by DifficultyButton.
        """

    def _revert_button_color(self):
        """Restore the button's default colors when it is not selected.

        Overridden by DifficultyButton.
        """

class DifficultyButton(Button):
    """A smaller button for choosing a difficulty level.

    Unselected buttons are green text on a dark gray background; the
    selected button inverts these colors.
    """

    def __init__(self, game, msg, x, y):
        """Initialize difficulty button attributes.

        Args:
                game: The running SnakeGame instance, used to access the screen.
                msg: Text to display on the button.
                x: x pixel coordinate of the button's center.
                y: y pixel coordinate of the button's center.
        """
        super().__init__(game, msg, x, y)

        # Set the dimensions and properties of the button.
        self.width, self.height = 160, 40
        self.button_color = self.dark_gray
        self.text_color = self.green
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x,y)

        # The button message needs to be prepped only once.
        self._prep_msg(msg)

    def _change_button_color(self):
        """Invert the button's colors to show it is selected."""
        self.button_color = self.green
        self.text_color = self.dark_gray
        self._prep_msg(self.msg)

    def _revert_button_color(self):
        """Restore the default colors when the button is not selected."""
        self.button_color = self.dark_gray
        self.text_color = self.green
        self._prep_msg(self.msg)
