"""Leaderboard module for Snake.

Defines the Leaderboard class, which stores and displays the top five
scores, persisted in snake_top_five.json.
"""

import pygame.font

class Leaderboard:
    """Keep track of and display the top five high scores.

    Attributes:
            game: The running SnakeGame instance.
            screen: The pygame display surface the leaderboard is drawn on.
            screen_rect: Rect describing the full display surface.
            settings: The shared Settings instance.
            stats: The GameStats instance holding the current score.
            text_color: RGB tuple used for leaderboard text.
            font: pygame Font used to render leaderboard text.
            top_five: List of the five best scores.
    """

    def __init__(self, game):
        """Initialize leaderboard attributes.

        Args:
                game: The running SnakeGame instance.
        """
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
        """Load the top five scores from snake_top_five.json."""
        filename = 'snake_top_five.json'
        with open(filename, 'r') as f:
            score = f.read()
            score_ints = [int(x) for x in score.split()]
            self.top_five = score_ints
            f.close()

    def add_new_leaderboard_score(self):
        """Add the current score to the top five if it qualifies."""
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
        """Render the leaderboard and draw it to the screen."""
        self.get_top_five()

        x = 0
        y = 160

        position = 1

        # Display Leaderboard Title Image.
        self.lb_title_image = self.font.render("LEADERBOARD", True,
                                               self.text_color)

        # Position the title near the top of the leaderboard.
        self.lb_title_rect = self.lb_title_image.get_rect()
        self.lb_title_rect.right = self.screen_rect.right - 245
        self.lb_title_rect.top = 96

        self.screen.blit(self.lb_title_image, self.lb_title_rect)

        # Display each score, one per row, rounded to the nearest ten.
        for score in self.top_five:
            rounded_score = round(score)
            score_str = "{:,}".format(rounded_score)

            self.lb_image = self.font.render(str(position) + ". " + score_str,
                                             True, self.text_color)

            # Position this row below the previous one.
            self.lb_rect = self.lb_image.get_rect()
            self.lb_rect.right = self.screen_rect.right - 300
            self.lb_rect.top = y
            x += 50
            self.screen.blit(self.lb_image, self.lb_rect)
            y += 32

            position += 1
