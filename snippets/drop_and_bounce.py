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
        life_sec (int): Lifetime in seconds.
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

    def check_collide(self, balls):
        for ball in balls:
            dx = self.pos.x - ball.pos.x
            dy = self.pos.y - ball.pos.y

            if dx * dx + dy * dy < self.radius * self.radius:
                if dx < self.radius * 2:
                    if self.pos.x < ball.pos.x:
                        self.pos.x = ball.pos.x - self.radius * 2
                    else:
                        self.pos.x = ball.pos.x + self.radius * 2
                    self.v.x = -self.v.x

                if dy < self.radius * 2:
                    if self.pos.y < ball.pos.y:
                        self.pos.y = ball.pos.y - self.radius * 2
                    else:
                        self.pos.y = ball.pos.y + self.radius * 2
                    self.v.y = -self.v.y



    def move(self, screen, dt):
        """Move on the screen.

        Args:
            screen (pygame.Surface): Drawing screen.
            dt (float): Elapsed time[sec] from the previous frame.
        """
        # Gravity
        self.v.y += (9.8 * 50) * dt

        # Bounce at the screen's edge
        if (self.pos.x - self.radius) < 0 :
            self.v.x = -self.v.x * 0.7
            self.pos.x = self.radius
        elif (self.pos.x + self.radius) > screen.get_width():
            self.v.x = -self.v.x * 0.7
            self.pos.x = screen.get_width() - self.radius
        if (self.pos.y - self.radius) < 0:
            self.v.y = -self.v.y * 0.7
            self.pos.y = self.radius
        elif (self.pos.y + self.radius) > screen.get_height():
            self.v.y = -self.v.y * 0.7
            self.pos.y = screen.get_height() - self.radius

        # Projectile motion
        self.pos.x += self.v.x * dt
        self.pos.y += self.v.y * dt

        # Decrease lifetime
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

    # Help text
    font = pygame.font.Font(pygame.font.get_default_font(), 20)
    help_text = font.render(
        "Click: drop a ball", True, (255, 255, 255)
    )

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

        # Drop ball on left click
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
            others = [b for b in balls if not b == ball]
            ball.check_collide(others)
            ball.move(screen, dt)
            ball.draw(screen)

        # Delete dead balls
        balls = [
            ball for ball in balls if ball.is_alive()
        ]

        for ball in balls:
            ball.draw(screen)

        screen.blit(help_text, (5, 5))

        pygame.display.flip()

        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
