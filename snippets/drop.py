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
        """Initialize.

        Args:
            pos (pygame.Vector2): Initial position (x, y).
            v (float): Magnitude of an initial velocity.
            theta (float): Angle of an initial velocity.
            radius (int): Radius.
            color (str): Color.
        """

        self.pos = pos.copy()
        self.v = pygame.Vector2(v * math.cos(theta), v * math.sin(theta))
        self.radius = radius
        self.color = color
        self.life_sec = 10

    def is_alive(self):
        return self.life_sec > 0

    def move(self, screen, dt):
        """Move on the screen.

        Args:
            screen (pygame.Surface): Drawing screen.
            dt (float): Elapsed time[sec] from the previous frame.
        """

        # Projectile motion
        self.pos.x += self.v.x * dt
        self.pos.y += self.v.y * dt

        # Gravity
        self.v.y += (9.8 * 50) * dt

        # Stop at the screen's edge
        if (self.pos.x + self.radius) >= screen.get_width() or (
            self.pos.y + self.radius
        ) >= screen.get_height():
            self.v.x = -self.v.x * 0.8
            self.v.y = -self.v.y * 0.8

        self.life_sec -= 1 * dt

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

    radius = 5
    v = 300

    clock = pygame.time.Clock()
    dt = 0

    balls = []

    pressed = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")

        # Get mouse status
        x, y = pygame.mouse.get_pos()
        button1, _, _ = pygame.mouse.get_pressed()

        if button1:
            if not pressed:
                pos = pygame.Vector2(x, y)
                balls.append(
                    Ball(pos, v, deg2rad(-random.uniform(30, 120)), radius, "green"),
                )
                pressed = True
        else:
            if pressed:
                pressed = False

        for ball in balls:
            ball.draw(screen)
            ball.move(screen, dt)

        balls = [
            ball for ball in balls if ball.is_alive()
        ]

        pygame.display.flip()

        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
