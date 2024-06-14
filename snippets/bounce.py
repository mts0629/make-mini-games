"""Bouncing ball."""

import math
import random

import pygame


class Ball:
    """Ball object.

    Attributes:
        pos (pygame.Vector2): Initial position (x, y).
        v (pygame.Vector2): Initial velocity (x, y).
        radius (int): Radius.
        color (str): Color.
    """

    def __init__(self, pos, v, radius, color):
        self.pos = pos
        self.v = v
        self.radius = radius
        self.color = color

    def move(self, screen, dt):
        """Move on the screen.

        Args:
            screen (pygame.Surface): Drawing screen.
            dt (float): Elapsed time[sec] from the previous frame.
        """

        self.pos.x += self.v.x * dt
        self.pos.y += self.v.y * dt

        # Reflect at the screen's edges
        if (self.pos.x + self.radius) > screen.get_width() or (
            self.pos.x - self.radius
        ) < 0:
            self.v.x *= -1
        if (self.pos.y + self.radius) > screen.get_height() or (
            self.pos.y - self.radius
        ) < 0:
            self.v.y *= -1

    def draw(self, screen):
        """Draw on the screen.

        Args:
            screen (pygame.Surface): Drawing screen.
        """

        pygame.draw.circle(screen, self.color, self.pos, self.radius)


def main():
    """Main loop."""

    pygame.init()

    screen = pygame.display.set_mode((640, 480))

    theta = random.uniform(0, 2 * math.pi)

    ball = Ball(
        pos=pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2),
        # Initialize with random direction
        v=pygame.Vector2(400 * math.cos(theta), 400 * math.sin(theta)),
        radius=20,
        color="green",
    )

    clock = pygame.time.Clock()
    dt = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")

        ball.draw(screen)

        ball.move(screen, dt)

        pygame.display.flip()

        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
