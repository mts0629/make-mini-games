import pygame

# Setup
pygame.init()

screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")

    # Double buffering
    pygame.display.flip()

    # 60 FPS
    clock.tick(60)

pygame.quit()
