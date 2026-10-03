"""Game entities: the player ship, the aliens and the bullets."""

import pygame

from . import settings
from . import sprites


def _bitmap_size(bitmap, pixel_size):
    """Return the (width, height) in pixels of a bitmap at a given scale."""
    return len(bitmap[0]) * pixel_size, len(bitmap) * pixel_size


def draw_bitmap(surface, bitmap, x, y, pixel_size, color):
    """Draw a pixel-art bitmap at (x, y) using the given colour."""
    for row_index, row in enumerate(bitmap):
        for col_index, cell in enumerate(row):
            if cell == "1":
                rect = pygame.Rect(
                    x + col_index * pixel_size,
                    y + row_index * pixel_size,
                    pixel_size,
                    pixel_size,
                )
                surface.fill(color, rect)


class Player:
    """The laser cannon controlled by the player."""

    def __init__(self):
        self.pixel_size = settings.PLAYER_PIXEL_SIZE
        self.width, self.height = _bitmap_size(sprites.PLAYER, self.pixel_size)
        self.x = (settings.SCREEN_WIDTH - self.width) / 2
        self.y = (
            settings.SCREEN_HEIGHT
            - self.height
            - settings.PLAYER_BOTTOM_MARGIN
        )
        self.cooldown = 0
        self.invulnerable = 0

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= settings.PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.x += settings.PLAYER_SPEED
        self.x = max(0, min(self.x, settings.SCREEN_WIDTH - self.width))

        if self.cooldown > 0:
            self.cooldown -= 1
        if self.invulnerable > 0:
            self.invulnerable -= 1

    def can_shoot(self):
        return self.cooldown == 0

    def shoot(self):
        self.cooldown = settings.PLAYER_SHOOT_COOLDOWN
        return Bullet(
            self.x + self.width / 2 - settings.BULLET_WIDTH / 2,
            self.y - settings.BULLET_HEIGHT,
            -settings.PLAYER_BULLET_SPEED,
            settings.GREEN,
        )

    def hit(self):
        self.invulnerable = settings.PLAYER_INVULNERABLE_FRAMES

    def is_invulnerable(self):
        return self.invulnerable > 0

    def visible(self):
        """Blink while invulnerable so the player can see they were hit."""
        if self.invulnerable == 0:
            return True
        return (self.invulnerable // 6) % 2 == 0

    def draw(self, surface):
        draw_bitmap(
            surface,
            sprites.PLAYER,
            int(self.x),
            int(self.y),
            self.pixel_size,
            settings.GREEN,
        )


class Alien:
    """A single invader in the fleet."""

    def __init__(self, x, y, type_index, col):
        bitmap, points, color_name = sprites.ALIEN_TYPES[type_index]
        self.bitmap = bitmap
        self.points = points
        self.color = getattr(settings, color_name)
        self.pixel_size = settings.ALIEN_PIXEL_SIZE
        self.width, self.height = _bitmap_size(bitmap, self.pixel_size)
        self.x = x
        self.y = y
        self.col = col

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def draw(self, surface):
        draw_bitmap(
            surface,
            self.bitmap,
            int(self.x),
            int(self.y),
            self.pixel_size,
            self.color,
        )


class Bullet:
    """A simple rectangular projectile."""

    def __init__(self, x, y, speed, color):
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.width = settings.BULLET_WIDTH
        self.height = settings.BULLET_HEIGHT

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def update(self):
        self.y += self.speed

    def off_screen(self):
        return self.y + self.height < 0 or self.y > settings.SCREEN_HEIGHT

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
