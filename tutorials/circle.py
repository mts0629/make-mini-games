"""Showing a circle moving on screen."""

import pygame


pygame.init()
screen = pygame.display.set_mode((1280, 720))

clock = pygame.time.Clock()
dt = 0

running = True

# Player's position
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen
    screen.fill("black")

    # Draw the player
    pygame.draw.circle(screen, "red", player_pos, 40)

    # Key inputs
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    pygame.display.flip()

    # Limits FPS to 60
    # dt is delta time in sec since last frame,
    # used for framerate-independet physics
    dt = clock.tick(60) / 1000

pygame.quit()
