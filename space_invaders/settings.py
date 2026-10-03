"""Configuration constants for the Space Invaders game."""

# --- Display ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Space Invaders"

# --- Colours ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 60, 60)
CYAN = (0, 220, 255)
YELLOW = (255, 220, 0)
MAGENTA = (255, 80, 200)

# --- Player ---
PLAYER_PIXEL_SIZE = 4
PLAYER_SPEED = 6
PLAYER_BOTTOM_MARGIN = 40
PLAYER_SHOOT_COOLDOWN = 12        # frames between shots
PLAYER_INVULNERABLE_FRAMES = 90   # ~1.5 s of blinking after being hit

# --- Bullets ---
BULLET_WIDTH = 4
BULLET_HEIGHT = 14
PLAYER_BULLET_SPEED = 10
ALIEN_BULLET_SPEED = 5
MAX_ALIEN_BULLETS = 8

# --- Aliens ---
ALIEN_PIXEL_SIZE = 4
ALIEN_ROWS = 4
ALIEN_COLS = 8
ALIEN_H_SPACING = 20
ALIEN_V_SPACING = 20
ALIEN_TOP_MARGIN = 70
ALIEN_BASE_SPEED = 1.2
ALIEN_SPEED_PER_KILL = 0.18
ALIEN_DROP_DISTANCE = 24
ALIEN_SHOOT_CHANCE = 0.003        # per column, per frame

# --- Game rules ---
STARTING_LIVES = 3
