"""The main game loop and state management."""

import random

import pygame

from . import settings
from . import sprites
from .entities import Alien, Bullet, Player


class Game:
    """Owns the window, the game state and the main loop."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
        )
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 28)
        self.big_font = pygame.font.Font(None, 64)
        self.reset()

    # ------------------------------------------------------------------
    # Setup / reset
    # ------------------------------------------------------------------
    def reset(self):
        self.player = Player()
        self.player_bullets = []
        self.alien_bullets = []
        self.aliens = []
        self.score = 0
        self.lives = settings.STARTING_LIVES
        self.wave = 0
        self.direction = 1
        self.state = "playing"
        self._spawn_fleet()

    def _spawn_fleet(self):
        """Build a fresh grid of aliens, centred horizontally."""
        self.aliens = []

        sample = sprites.ALIEN_TYPES[0][0]
        cell_w = len(sample[0]) * settings.ALIEN_PIXEL_SIZE
        cell_h = len(sample) * settings.ALIEN_PIXEL_SIZE

        fleet_w = (
            settings.ALIEN_COLS * cell_w
            + (settings.ALIEN_COLS - 1) * settings.ALIEN_H_SPACING
        )
        start_x = (settings.SCREEN_WIDTH - fleet_w) / 2

        # Each new wave starts a little lower, but never too low.
        y_offset = min(self.wave * 20, 200)

        for row in range(settings.ALIEN_ROWS):
            type_index = sprites.ROW_TYPES[row % len(sprites.ROW_TYPES)]
            for col in range(settings.ALIEN_COLS):
                x = start_x + col * (cell_w + settings.ALIEN_H_SPACING)
                y = (
                    settings.ALIEN_TOP_MARGIN
                    + y_offset
                    + row * (cell_h + settings.ALIEN_V_SPACING)
                )
                self.aliens.append(Alien(x, y, type_index, col))

        self.direction = 1

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------
    def run(self):
        running = True
        while running:
            self.clock.tick(settings.FPS)
            running = self._handle_events()
            if self.state == "playing":
                self._update()
            self._draw()
        pygame.quit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_SPACE and self.state == "game_over":
                    self.reset()
        return True

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------
    def _update(self):
        keys = pygame.key.get_pressed()
        self.player.update(keys)

        if keys[pygame.K_SPACE] and self.player.can_shoot():
            self.player_bullets.append(self.player.shoot())

        for bullet in self.player_bullets:
            bullet.update()
        for bullet in self.alien_bullets:
            bullet.update()

        self._move_aliens()
        self._alien_fire()
        self._resolve_collisions()

        self.player_bullets = [
            b for b in self.player_bullets if not b.off_screen()
        ]
        self.alien_bullets = [
            b for b in self.alien_bullets if not b.off_screen()
        ]

        # Clearing a wave spawns the next one, which starts lower.
        if not self.aliens:
            self.wave += 1
            self._spawn_fleet()

    def alien_speed(self):
        """The fleet speeds up as its numbers thin out."""
        total = settings.ALIEN_ROWS * settings.ALIEN_COLS
        killed = total - len(self.aliens)
        return settings.ALIEN_BASE_SPEED + killed * settings.ALIEN_SPEED_PER_KILL

    def _move_aliens(self):
        if not self.aliens:
            return

        dx = self.alien_speed() * self.direction
        would_hit_edge = any(
            alien.x + dx < 0
            or alien.x + alien.width + dx > settings.SCREEN_WIDTH
            for alien in self.aliens
        )

        if would_hit_edge:
            self.direction *= -1
            for alien in self.aliens:
                alien.y += settings.ALIEN_DROP_DISTANCE
        else:
            for alien in self.aliens:
                alien.x += dx

        # If the invaders reach the player's row, the game is over.
        for alien in self.aliens:
            if alien.rect.bottom >= self.player.rect.top:
                self.lives = 0
                self.state = "game_over"
                break

    def _alien_fire(self):
        if len(self.alien_bullets) >= settings.MAX_ALIEN_BULLETS:
            return

        # Only the lowest alien in each column is allowed to fire.
        lowest = {}
        for alien in self.aliens:
            current = lowest.get(alien.col)
            if current is None or alien.y > current.y:
                lowest[alien.col] = alien

        for alien in lowest.values():
            if random.random() < settings.ALIEN_SHOOT_CHANCE:
                self.alien_bullets.append(
                    Bullet(
                        alien.x + alien.width / 2 - settings.BULLET_WIDTH / 2,
                        alien.y + alien.height,
                        settings.ALIEN_BULLET_SPEED,
                        settings.RED,
                    )
                )

    def _resolve_collisions(self):
        # Player bullets vs aliens.
        for bullet in list(self.player_bullets):
            for alien in list(self.aliens):
                if bullet.rect.colliderect(alien.rect):
                    self.aliens.remove(alien)
                    self.player_bullets.remove(bullet)
                    self.score += alien.points
                    break

        # Alien bullets vs the player.
        for bullet in list(self.alien_bullets):
            if bullet.rect.colliderect(self.player.rect):
                self.alien_bullets.remove(bullet)
                if not self.player.is_invulnerable():
                    self.lives -= 1
                    self.player.hit()
                    self.alien_bullets.clear()
                    if self.lives <= 0:
                        self.state = "game_over"

    # ------------------------------------------------------------------
    # Draw
    # ------------------------------------------------------------------
    def _draw(self):
        self.screen.fill(settings.BLACK)
        self._draw_hud()

        for alien in self.aliens:
            alien.draw(self.screen)
        for bullet in self.player_bullets:
            bullet.draw(self.screen)
        for bullet in self.alien_bullets:
            bullet.draw(self.screen)
        if self.player.visible():
            self.player.draw(self.screen)

        if self.state == "game_over":
            self._draw_centered("GAME OVER", settings.RED, -40)
            self._draw_centered("Press SPACE to play again", settings.WHITE, 30)

        pygame.display.flip()

    def _draw_hud(self):
        score_surface = self.font.render(
            f"SCORE  {self.score}", True, settings.WHITE
        )
        self.screen.blit(score_surface, (20, 15))

        wave_surface = self.font.render(
            f"WAVE  {self.wave + 1}", True, settings.WHITE
        )
        self.screen.blit(
            wave_surface,
            (
                int(settings.SCREEN_WIDTH / 2 - wave_surface.get_width() / 2),
                15,
            ),
        )

        lives_surface = self.font.render(
            f"LIVES  {max(self.lives, 0)}", True, settings.WHITE
        )
        self.screen.blit(
            lives_surface,
            (settings.SCREEN_WIDTH - lives_surface.get_width() - 20, 15),
        )

    def _draw_centered(self, text, color, y_offset):
        surface = self.big_font.render(text, True, color)
        rect = surface.get_rect(
            center=(
                settings.SCREEN_WIDTH // 2,
                settings.SCREEN_HEIGHT // 2 + y_offset,
            )
        )
        self.screen.blit(surface, rect)
