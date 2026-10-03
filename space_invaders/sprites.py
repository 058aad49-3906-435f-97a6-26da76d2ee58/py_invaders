"""Pixel-art bitmaps for the aliens and the player ship.

Each sprite is a list of strings.  A '1' means a filled pixel and a '0'
means transparent.  They are drawn at runtime, so no image files are
needed and the game stays self-contained.
"""

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

# (bitmap, points, colour-name) for each alien type, most valuable first.
ALIEN_TYPES = [
    (SQUID, 30, "MAGENTA"),
    (CRAB, 20, "CYAN"),
    (OCTOPUS, 10, "YELLOW"),
]

# Which alien type occupies each row of the fleet (top row first).
ROW_TYPES = [0, 1, 1, 2]

# --- Player ship (11x6) -------------------------------------------------

PLAYER = [
    "00000100000",
    "00001110000",
    "00001110000",
    "01111111110",
    "11111111111",
    "11111111111",
]
