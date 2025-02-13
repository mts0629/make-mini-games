"""Simple paint."""

from typing import Tuple

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

    def _fix_draw_pos(x: int, y: int) -> Tuple[int, int]:
        """Fix draw position based of canvas position."""
        return (x - CANVAS_BEGIN[0], y - CANVAS_BEGIN[1])

    FONT_SIZE = 20
    font = pygame.font.Font(pygame.font.get_default_font(), FONT_SIZE)

    clock = pygame.time.Clock()

    # Pen colors
    pen_colors = ["Black", "Red", "Blue", "Green", "Yellow", "White"]
    color_index = 0
    current_pen_color = pen_colors[color_index]

    color_button_pressed = False

    # Initial position
    prev_x, prev_y = pygame.mouse.get_pos()

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
            # On click
            if not color_button_pressed:
                # Change a pen color
                color_index += 1
                if color_index >= len(pen_colors):
                    color_index = 0
                current_pen_color = pen_colors[color_index]

                color_button_pressed = True
        else:
            if color_button_pressed:
                color_button_pressed = False

        # Draw a line by button 1 (left click)
        if button1:
            pygame.draw.line(
                canvas,
                current_pen_color,
                _fix_draw_pos(prev_x, prev_y),
                _fix_draw_pos(x, y),
                2,
            )

        prev_x, prev_y = x, y

        pygame.display.flip()

        _ = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
