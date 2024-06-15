"""Player and a stage with platforms."""

import math
import random

import pygame


class Player:
    """Player object.

    Attributes:
        pos (pygame.Vector2): Position (x, y).
        v (pygame.Vector2): Velocity (x, y).
        speed (float): Moving speed.
        jumping (bool): Flag, True if while jumping.
        radius (int): Radius (size of the player).
        rect (pygame.Rect): Collision area.
    """

    def __init__(self, pos):
        """Initialize.

        Args:
            pos (pygame.Vector2): Initial position (x, y).
        """
        self.pos = pos.copy()
        self.speed = 200
        self.v = pygame.Vector2(0, 0)
        self.radius = 20

        self.rect = pygame.Rect(
            self.pos.x - self.radius,
            self.pos.y - self.radius,
            self.radius * 2,
            self.radius * 2,
        )

        self.jumping = True

    def check_collision(self, rect, obj):
        """Check whether the collision area collides with that of an objective.

        Args:
            rect (pygame.Rect): Collision area.
            obj (pygame.Rect): Collision of the objective.

        Returns:
            Tuple[bool, bool, bool, bool]: Collision flags for each directions,
                top/bottom/left/right.
        """
        # Collision check by rectangles
        # L      R
        # +------+ T
        # |      |
        # |    +-|------+
        # +------+ B    |
        #      |        |
        #      +--------+

        top = obj.top < rect.top <= obj.bottom
        bottom = obj.top <= rect.bottom <= obj.bottom
        left = obj.left < rect.left <= obj.right
        right = obj.left <= rect.right < obj.right

        return (top, bottom, left, right)

    def move(self, screen, platforms, dt):
        """Move on the screen.

        Args:
            screen (pygame.Surface): Drawing screen.
            platforms (List[Platform]): Platforms.
            dt (float): Elapsed time[sec] from the previous frame.
        """
        if not self.jumping:
            self.v = pygame.Vector2(0, 0)

            # If not in jumping, move a player by the key inputs
            # Jump
            if pygame.key.get_pressed()[pygame.K_w]:
                self.v.y = -4.5
                self.jumping = True

            # Move to Left/right
            if pygame.key.get_pressed()[pygame.K_a]:
                self.v.x = -1
            elif pygame.key.get_pressed()[pygame.K_d]:
                self.v.x = 1
        else:
            # Falling, add the G
            self.v.y += 0.15

        self.v = self.speed * self.v * dt

        # Collisiotn check
        for platform in platforms:
            top, bottom, left, right = self.check_collision(self.rect, platform.rect)
            if top or bottom:
                if self.jumping:
                    self.v.y = 0
                if bottom and self.jumping:
                    self.jumping = False
            if (left or right) and not (top or bottom):
                self.v.x = 0

        # Move the player and collision area
        self.pos += self.speed * self.v * dt
        self.rect.update(
            self.pos.x - self.radius,
            self.pos.y - self.radius,
            self.radius * 2,
            self.radius * 2,
        )

    def draw(self, screen):
        """Draw on the screen.

        Args:
            screen (pygame.Surface): Drawing screen.
        """
        # Body
        pygame.draw.circle(screen, "green", self.pos, self.radius)

        # Eyes
        eye_pos = [(-5, 0), (5, 0)]
        # Move along with the player's direction
        for pos in eye_pos:
            pygame.draw.circle(screen, "black", self.pos + self.v * 5 + pos, 3)


class Platform:
    """Platform object.

    Attributes:
        pos (pygame.Vector2): Position (x, y).
        width (int): Width.
        height (int): Height.
        rect (pygame.Rect): Drawn rectangle and collision area.
        color (str): Drawn color.
    """

    def __init__(self, pos, width, height):
        """Initialize.

        Args:
            pos (pygame.Vector2): Initial position (x, y).
            width (int): Width.
            height (int): Height.
        """
        self.pos = pos.copy()
        self.width = width
        self.height = height
        self.rect = pygame.Rect(pos.x - width / 2, pos.y - height / 2, width, height)

        self.color = "white"

    def draw(self, screen):
        """Draw on the screen.

        Args:
            screen (pygame.Surface): Drawing screen.
        """
        pygame.draw.rect(screen, self.color, self.rect)


def main():
    """Main loop."""

    pygame.init()

    screen = pygame.display.set_mode((640, 480))

    # Help text
    font = pygame.font.Font(pygame.font.get_default_font(), 20)
    help_text = font.render(
        "[W] Jump/[A] Left/[D] Right/[ESC] Quit", True, (255, 255, 255)
    )

    player = Player(pygame.Vector2(screen.get_width() / 2, screen.get_height() - 10))

    S_WIDTH = screen.get_width()
    S_HEIGHT = screen.get_height()

    # Platforms
    platforms = [
        Platform(pygame.Vector2(S_WIDTH / 2, S_HEIGHT + 5), S_WIDTH, 10),  # Floor
        Platform(pygame.Vector2(-5, S_HEIGHT / 2), 10, S_HEIGHT),  # Left wall
        Platform(pygame.Vector2(S_WIDTH + 5, S_HEIGHT / 2), 10, S_HEIGHT),  # Right wall
        Platform(pygame.Vector2(S_WIDTH / 2 - 200, S_HEIGHT - 300), 150, 30),
        Platform(pygame.Vector2(S_WIDTH / 2, S_HEIGHT - 150), 200, 30),
        Platform(pygame.Vector2(S_WIDTH / 2 + 200, S_HEIGHT - 300), 150, 30),
    ]

    clock = pygame.time.Clock()
    dt = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Quit game by the ESC key
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            running = False

        screen.fill("black")

        player.move(screen, platforms, dt)

        for platform in platforms:
            platform.draw(screen)

        player.draw(screen)

        screen.blit(help_text, (5, 5))

        pygame.display.flip()

        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
