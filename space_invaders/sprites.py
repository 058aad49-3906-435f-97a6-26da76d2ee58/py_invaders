"""Pixel-art bitmaps for the aliens and the player ship.

Each sprite is a list of strings.  A '1' means a filled pixel and a '0'
means transparent.  They are drawn at runtime, so no image files are
needed and the game stays self-contained.
"""

import random

# --- Alien bitmaps (8x8) ------------------------------------------------

SQUID = [
    "00011000",
    "00111100",
    "01111110",
    "11011011",
    "11111111",
    "00100100",
    "01011010",
    "10100101",
]

CRAB = [
    "00100100",
    "00011000",
    "01111110",
    "11011011",
    "11111111",
    "10111101",
    "10000001",
    "01000010",
]

OCTOPUS = [
    "00111100",
    "01111110",
    "11011011",
    "11111111",
    "00100100",
    "01011010",
    "10000001",
    "01000010",
]

# A round alien.  The silhouette is a circle so it reads as a spherical
# scout ship rather than the angular invaders above.
ORB = [
    "00111100",
    "01111110",
    "11111111",
    "11111111",
    "11111111",
    "11111111",
    "01111110",
    "00111100",
]

# (bitmap, points, colour-name) for each alien type, most valuable first.
ALIEN_TYPES = [
    (SQUID, 30, "MAGENTA"),
    (CRAB, 20, "CYAN"),
    (OCTOPUS, 10, "YELLOW"),
    (ORB, 5, "WHITE"),
]

# Which alien type occupies each row is randomised every wave so the
# different ship types show up in a fresh order as the levels progress.
def random_row_types(rows):
    """Return ``rows`` alien type indices in a random order.

    The type indices are shuffled and then cycled, so every alien type
    appears at least once whenever ``rows`` is at least the number of
    types.  Each wave therefore shows all ship types, just arranged
    differently.
    """
    types = list(range(len(ALIEN_TYPES)))
    random.shuffle(types)
    return [types[i % len(types)] for i in range(rows)]


# --- Player ship (11x6) -------------------------------------------------

PLAYER = [
    "00000100000",
    "00001110000",
    "00001110000",
    "01111111110",
    "11111111111",
    "11111111111",
]
