"""Move a player by the key input."""

import math
import random

import pygame


class Player:
    """Player object.

    Attributes:
        pos (pygame.Vector2): Position (x, y).
        v (pygame.Vector2): Velocity (x, y).
        speed (float): Moving speed.
        radius (int): Radius.
        color (str): Color.
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
        self.color = "green"

    def move(self, screen, dt):
        """Move on the screen.

        Args:
            screen (pygame.Surface): Drawing screen.
            dt (float): Elapsed time[sec] from the previous frame.
        """
        self.v = pygame.Vector2(0, 0)

        # Upper/lower
        if pygame.key.get_pressed()[pygame.K_w]:
            self.v.y = -1
        elif pygame.key.get_pressed()[pygame.K_s]:
            self.v.y = 1 
        # Left/right
        if pygame.key.get_pressed()[pygame.K_a]:
            self.v.x = -1
        elif pygame.key.get_pressed()[pygame.K_d]:
            self.v.x = 1

        # Move the player
        self.pos += self.speed * self.v  * dt

        # Stop at the screen's edge
        if self.pos.x < self.radius:
            self.pos.x = self.radius
        if self.pos.x > (screen.get_width() - self.radius):
            self.pos.x = screen.get_width() - self.radius

        if self.pos.y < self.radius:
            self.pos.y = self.radius
        if  self.pos.y > (screen.get_width() - self.radius):
            self.pos.y = screen.get_width() - self.radius

    def draw(self, screen):
        """Draw on the screen.

        Args:
            screen (pygame.Surface): Drawing screen.
        """

        pygame.draw.circle(screen, self.color, self.pos, self.radius)


def deg2rad(deg):
    """Convert an angle from degree to radian.

    Args:
        deg (float): Angle[deg].

    Return:
        (float): Angle[rad].
    """

    return deg / 180 * math.pi


def main():
    """Main loop."""

    pygame.init()

    screen = pygame.display.set_mode((640, 480))

    player = Player(
        pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
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

        pygame.display.flip()

        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
