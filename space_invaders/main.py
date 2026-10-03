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
    try:
        Game().run()
    except ModuleNotFoundError as exc:
        if exc.name == "pygame":
            print(
                "This game requires pygame, which is not installed for "
                "the current Python interpreter.\n"
                f"Interpreter: {sys.executable}\n\n"
                "Install it with one of:\n"
                "    python -m pip install pygame\n"
                "    python -m pip install pygame-ce\n",
                file=sys.stderr,
            )
            raise SystemExit(1)
        raise


if __name__ == "__main__":
    main()
