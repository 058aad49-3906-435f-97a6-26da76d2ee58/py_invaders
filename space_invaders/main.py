"""Entry point for the Space Invaders game.

Run either as a module::

    python -m space_invaders.main

or directly::

    python space_invaders/main.py
"""

import os
import sys

if __package__ in (None, ""):
    # Running the file directly, so make the parent directory importable.
    sys.path.insert(
        0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    from space_invaders.game import Game
else:
    from .game import Game


def main():
    Game().run()


if __name__ == "__main__":
    main()
