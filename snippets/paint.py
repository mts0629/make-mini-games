"""Simple paint."""

import pygame


def main():
    """Main loop."""

    pygame.init()

    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 480
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Canvas area
    CANVAS_WIDTH = 600
    CANVAS_HEIGHT = 440
    CANVAS_BEGIN = (
        int((SCREEN_WIDTH - CANVAS_WIDTH) / 2),
        int((SCREEN_HEIGHT - CANVAS_HEIGHT) / 2),
    )
    canvas = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
    canvas = canvas.convert()
    canvas.fill("White")

    FONT_SIZE = 20
    font = pygame.font.Font(pygame.font.get_default_font(), FONT_SIZE)

    clock = pygame.time.Clock()

    # Pen colors
    pen_colors = ["Black", "Red", "Blue", "Green", "Yellow", "White"]
    color_index = 0
    current_pen_color = pen_colors[color_index]

    color_button_pressed = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Quit game by the ESC key
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            running = False

        screen.fill("gray")

        screen.blit(canvas, CANVAS_BEGIN)

        # Get mouse status
        x, y = pygame.mouse.get_pos()
        button1, _, button3 = pygame.mouse.get_pressed()

        # Info
        color_info = font.render(
            f"Pen color: ",
            True,
            "Black",
        )
        screen.blit(color_info, (0, 0))
        color_info = font.render(
            f"{current_pen_color}",
            True,
            current_pen_color,
        )
        screen.blit(color_info, (110, 0))

        # Change a pen color by button 3 (right click)
        if button3:
            # Change a pen color by button3 trigger
            if not color_button_pressed:
                color_index += 1
                if color_index >= len(pen_colors):
                    color_index = 0
                current_pen_color = pen_colors[color_index]
            color_button_pressed = True
        else:
            if color_button_pressed:
                color_button_pressed = False

        # Draw a dot by button 1 (left click)
        if button1:
            # Fix a drawing position by canvas's position
            draw_pos = (x - CANVAS_BEGIN[0], y - CANVAS_BEGIN[1])
            pygame.draw.circle(canvas, current_pen_color, draw_pos, 3.0)

        pygame.display.flip()

        _ = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
