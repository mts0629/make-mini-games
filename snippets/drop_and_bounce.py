"""Projection of the ball."""

import math
import random

import pygame

# Scale for gravity
SCALE = 50
# Coefficient of restitution
COR = 0.8
# Drop speed
SPEED = 200
# Range of drop angle
DROP_ANGLE_RANGE = [30, 150]
# Lifetime of balls
LIFE_SEC = 10
# Radius of balls
RADIUS = 5


class Ball:
    def __init__(self, pos, v, radius):
        self.pos = pos.copy()
        self.d_pos = pygame.Vector2(0, 0)
        self.v = v.copy()
        self.radius = radius
        self.color = pygame.Color(0, 255, 0)
        self.life_sec = LIFE_SEC

    def is_alive(self):
        return self.life_sec > 0

    def move(self, dt):
        # Add gravity
        self.v.y += SCALE * 9.8 * dt
        self.pos += self.v * dt

    def check_collide(self, balls):
        self.d_pos = pygame.Vector2(0, 0)

        for ball in balls:
            if ball == self:
                continue

            d = self.pos - ball.pos
            dist_sq = d.magnitude_squared()

            d_center = self.radius + ball.radius

            if dist_sq < math.pow(d_center, 2):
                # Correct position
                self.d_pos += (d_center - math.sqrt(dist_sq)) * d.normalize()
                # Bounce
                if d.x < d_center:
                    self.v.x = -COR * self.v.x
                if d.y < d_center:
                    self.v.y = -COR * self.v.y

    def update(self, screen, dt):
        self.pos += self.d_pos

        # Bounce at the screen's edge
        if (self.pos.x - self.radius) < 0:
            self.v.x = -COR * self.v.x
            self.pos.x = self.radius
        elif (self.pos.x + self.radius) > screen.get_width():
            self.v.x = -COR * self.v.x
            self.pos.x = screen.get_width() - self.radius
        if (self.pos.y - self.radius) < 0:
            self.v.y = -COR * self.v.y
            self.pos.y = self.radius
        elif (self.pos.y + self.radius) > screen.get_height():
            self.v.y = -COR * self.v.y
            self.pos.y = screen.get_height() - self.radius

        # Decrease lifetime
        self.life_sec -= 1 * dt

    def draw(self, screen):
        if self.is_alive():
            pygame.draw.circle(screen, self.color, self.pos, self.radius)


def deg2rad(deg):
    return deg / 180 * math.pi


def main():
    pygame.init()

    screen = pygame.display.set_mode((640, 480))

    clock = pygame.time.Clock()
    dt = 0

    balls = []

    # Help text
    font = pygame.font.Font(pygame.font.get_default_font(), 20)
    help_text = font.render("Click: drop a ball/Esc: quit", True, (255, 255, 255))

    clicked = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            running = False

        screen.fill("black")

        # Get mouse status
        x, y = pygame.mouse.get_pos()
        button1, _, _ = pygame.mouse.get_pressed()

        # Drop ball on left click
        if button1:
            if not clicked:
                theta = -random.uniform(*DROP_ANGLE_RANGE)
                v = SPEED * pygame.Vector2(
                    math.cos(deg2rad(theta)), math.sin(deg2rad(theta))
                )
                balls.append(Ball(pygame.Vector2(x, y), v, RADIUS))
                clicked = True
        else:
            if clicked:
                clicked = False

        for ball in balls:
            ball.move(dt)

        for ball in balls:
            ball.check_collide(balls)
            ball.update(screen, dt)
            ball.draw(screen)

        # Delete dead balls
        balls = [ball for ball in balls if ball.is_alive()]

        screen.blit(help_text, (5, 5))

        pygame.display.flip()

        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
