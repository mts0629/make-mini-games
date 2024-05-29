"""Projection of the ball."""

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
    def __init__(self, pos, v, theta, radius, color):
        self.pos = pos
        self.v = pygame.Vector2(
            v * math.cos(theta), v * math.sin(theta)
        )
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

        self.v.y += (9.81 * 10) * dt

        # Stop at the screen's edge
        if (self.pos.x + self.radius) >= screen.get_width() or \
           (self.pos.y + self.radius) >= screen.get_height():
            self.v.x = 0
            self.v.y = 0

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

    pos = pygame.Vector2(10, screen.get_height() - 10)
    v = 300
    balls = [
        Ball(pos, v, -random.uniform(0, 90) / 180 * math.pi, 5, "green"),
        Ball(pos, v, -random.uniform(0, 90) / 180 * math.pi, 5, "red"),
    ]

    clock = pygame.time.Clock()
    dt = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill("black")

        for ball in balls:
            ball.draw(screen)
            ball.move(screen, dt)

        pygame.display.flip()

        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
