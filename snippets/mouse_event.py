"""Mouse event."""

import pygame


def main():
    """Main loop."""

    pygame.init()

    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 480
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill("Black")

    font = pygame.font.Font(pygame.font.get_default_font(), 20)

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Quit game by the ESC key
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            running = False

        screen.fill("black")

        x, y = pygame.mouse.get_pos()
        btn1, btn2, btn3 = pygame.mouse.get_pressed()

        # Print mouse info
        mouse_pos = font.render(
            f"mouse (x,y) = ({x},{y})",
            True,
            (255, 255, 255)
        )
        button_info = font.render(
            f"{'button1 pressed ' if btn1 else ''}"
            f"{'button2 pressed ' if btn2 else ''}"
            f"{'button3 pressed' if btn3 else ''}",
            True,
            (255, 255, 255),
        )

        screen.blit(mouse_pos, (0, 0))
        screen.blit(button_info, (0, 20))

        pygame.display.flip()

        _ = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
