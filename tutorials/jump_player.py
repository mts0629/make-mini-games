"""Jump a player by the key input."""

import math
import random

import pygame


class Player:
    """Player object.

    Attributes:
        pos (pygame.Vector2): Position (x, y).
        v (pygame.Vector2): Velocity (x, y).
        speed (float): Moving speed.
        jumping (bool): Flag, True if while jumping.
        radius (int): Radius (size of the player).
    """

    def __init__(self, pos):
        """Initialize.

        Args:
            pos (pygame.Vector2): Initial position (x, y).
        """
        self.pos = pos.copy()
        self.speed = 200
        self.v = pygame.Vector2(0, 0)
        self.radius = 20
        self.jumping = True

    def move(self, screen, dt):
        """Move on the screen.

        Args:
            screen (pygame.Surface): Drawing screen.
            dt (float): Elapsed time[sec] from the previous frame.
        """
        if not self.jumping:
            self.v = pygame.Vector2(0, 0)

            # If not in jumping, move a player by the key inputs
            # Jump
            if pygame.key.get_pressed()[pygame.K_w]:
                self.v.y = -5
                self.jumping = True
            # Left/right
            if pygame.key.get_pressed()[pygame.K_a]:
                self.v.x = -1
            elif pygame.key.get_pressed()[pygame.K_d]:
                self.v.x = 1
        else:
            # Falling, add the G
            self.v.y += 0.2

        # Move the player
        self.pos += self.speed * self.v * dt

        # Stop at the screen's edge
        self.pos.x = pygame.math.clamp(
            self.pos.x, self.radius, screen.get_width() - self.radius
        )
        self.pos.y = pygame.math.clamp(
            self.pos.y, self.radius, screen.get_height() - self.radius
        )

        # Stop falling at the bottom of the screen
        if self.pos.y == screen.get_height() - self.radius:
            self.jumping = False

    def draw(self, screen):
        """Draw on the screen.

        Args:
            screen (pygame.Surface): Drawing screen.
        """
        # Body
        pygame.draw.circle(screen, "green", self.pos, self.radius)

        # Eyes
        eye_pos = [(-5, 0), (5, 0)]
        # Move along with the player's direction
        for pos in eye_pos:
            pygame.draw.circle(screen, "black", self.pos + self.v * 5 + pos, 3)


def main():
    """Main loop."""

    pygame.init()

    screen = pygame.display.set_mode((640, 480))

    # Help text
    font = pygame.font.Font(pygame.font.get_default_font(), 20)
    help_text = font.render(
        "[W] Jump/[A] Left/[D] Right/[ESC] Quit",
        True, (255, 255, 255)
    )

    player = Player(
        pygame.Vector2(screen.get_width() / 2, screen.get_height() - 10)
    )

    clock = pygame.time.Clock()
    dt = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Quit game by the ESC key
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            running = False
        
        screen.fill("black")

        player.move(screen, dt)
        player.draw(screen)

        screen.blit(help_text, (5, 5))

        pygame.display.flip()

        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
