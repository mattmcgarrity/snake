"""Shared pytest fixtures for the Snake tests.

pygame is told to use dummy video and audio drivers before it is imported,
so the tests run without a window or sound card (including in CI).
"""

import os
import shutil
import sys
from pathlib import Path

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pytest

# Make the game modules importable when pytest is run from anywhere.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture
def game(tmp_path, monkeypatch):
    """Create a SnakeGame in a temporary copy of the project folder.

    The game loads sounds and reads/writes score files using relative paths,
    so it runs from a temp directory. That way tests never touch the real
    snake_high_score.json or snake_top_five.json.
    """
    shutil.copytree(PROJECT_ROOT / "assets", tmp_path / "assets")
    (tmp_path / "snake_high_score.json").write_text("0")
    (tmp_path / "snake_top_five.json").write_text("0\n0\n0\n0\n0")
    monkeypatch.chdir(tmp_path)

    from snakegame import SnakeGame
    return SnakeGame()