"""Unit tests for the most important Snake game logic."""

import pygame


def press(game, key):
    """Send a KEYDOWN event for key to the game's steering handler."""
    game._check_keydown_events(pygame.event.Event(pygame.KEYDOWN, key=key))


def test_wall_collision_detected_only_outside_play_area(game):
    """The snake dies at each edge of the play area but not inside it."""
    snake = game.snake
    s = game.settings
    last_ok = s.snake_screen_width - s.snake_size

    # Every tile just inside the boundary is safe.
    for x, y in [(s.outline_size, s.outline_size), (last_ok, last_ok),
                 (s.outline_size, last_ok), (last_ok, s.outline_size)]:
        snake.x = x
        snake.y = y
        assert snake.check_side_collisions() is False

    # One tile past any edge is a collision.
    for x, y in [(s.outline_size - s.tile_size, 300),
                 (last_ok + s.tile_size, 300),
                 (300, s.outline_size - s.tile_size),
                 (300, last_ok + s.tile_size)]:
        snake.x = x
        snake.y = y
        assert snake.check_side_collisions() is True


def test_self_collision_only_when_head_overlaps_body(game):
    """Hitting the body ends the game; the head alone never collides."""
    snake = game.snake
    snake.x = 128
    snake.y = 128

    # A lone head does not collide with itself.
    snake.snake_list = [[128, 128]]
    assert snake.check_snake_collision() is False

    # Head on a clear tile: no collision.
    snake.snake_list = [[96, 128], [96, 160], [128, 160], [128, 128]]
    assert snake.check_snake_collision() is False

    # Head lands on an earlier body segment: collision.
    snake.snake_list = [[128, 128], [96, 128], [96, 160], [128, 160],
                        [128, 128]]
    assert snake.check_snake_collision() is True


def test_body_tracks_head_and_grows_when_apple_eaten(game):
    """The body keeps its length, and grows by one after increment_snake()."""
    snake = game.snake
    snake.snake_list = [[game.settings.snake_x, game.settings.snake_y]]
    snake.x = 320
    snake.y = 320
    snake.snake_len = 1
    snake.moving_right = True

    for _ in range(3):
        snake.update()
        snake.track_snake_coordinates()
    assert len(snake.snake_list) == 1
    assert snake.snake_list[-1] == [snake.x, snake.y]

    snake.increment_snake()
    for _ in range(3):
        snake.update()
        snake.track_snake_coordinates()
    assert snake.snake_len == 2
    assert len(snake.snake_list) == 2
    # The head is the last element and the tail trails one tile behind.
    assert snake.snake_list[-1][0] - snake.snake_list[0][0] == \
        game.settings.tile_size


def test_apple_never_spawns_on_the_snake(game):
    """An apple always lands on a free tile, even when the board is nearly full."""
    grid = game.grid_positions

    # Snake covers every tile except one: the apple must go there.
    free_tile = grid[100]
    body = [list(pos) for pos in grid if pos != free_tile]
    for _ in range(25):
        game.apple.spawn_apple(body, grid)
        assert (game.apple.apple_x, game.apple.apple_y) == free_tile

    # With a short snake, the apple is never on the body over many spawns.
    short_body = [list(pos) for pos in grid[:10]]
    occupied = {tuple(pos) for pos in short_body}
    for _ in range(300):
        game.apple.spawn_apple(short_body, grid)
        assert (game.apple.apple_x, game.apple.apple_y) not in occupied


def test_steering_blocks_reversal_even_with_two_quick_key_presses(game):
    """A long snake can't reverse, including Up then Left in a single frame."""
    snake = game.snake
    snake.snake_len = 3
    snake.x = 320
    snake.y = 320

    # Heading right, a direct Left press is ignored.
    press(game, pygame.K_RIGHT)
    snake.update()
    press(game, pygame.K_LEFT)
    assert snake.moving_right and not snake.moving_left

    # Two quick presses before the next move: Up is accepted, Left is not.
    press(game, pygame.K_UP)
    press(game, pygame.K_LEFT)
    assert snake.moving_up and not snake.moving_left

    # A legal turn on the following frame still works.
    snake.update()
    press(game, pygame.K_LEFT)
    assert snake.moving_left

    # A length-1 snake has no body, so it may reverse.
    game._prep_game()
    snake.snake_len = 1
    press(game, pygame.K_RIGHT)
    snake.update()
    press(game, pygame.K_LEFT)
    assert snake.moving_left