"""Collision check between a player and objects."""

import pygame


class Player:
    """Player object.

    Attributes:
        pos (pygame.Vector2): Position (x, y).
        v (pygame.Vector2): Velocity (x, y).
        speed (float): Moving speed.
        width (int): Width.
        height (int): Height.
        rect (pygame.Rect): Collision area.
        color (str): Drawn color.
    """

    def __init__(self, pos):
        """Initialize.

        Args:
            pos (pygame.Vector2): Initial position (x, y).
        """
        self.pos = pos.copy()
        self.speed = 200
        self.v = pygame.Vector2(0, 0)
        self.width = 40
        self.height = 40
        self.rect = pygame.Rect(
            self.pos.x - self.width / 2,
            self.pos.y - self.height / 2,
            self.width,
            self.height,
        )
        self.color = "green"

    def check_collision(self, rect, obj):
        """Check whether the collision area collides with that of an objective.

        Args:
            rect (pygame.Rect): Collision area of the character.
            obj (pygame.Rect): Collision of the objective.

        Returns:
            (Tuple[bool, bool, bool, bool]): Collision flags for each direction,
                on the top/bottom/left/right of the character.
        """
        # Collision check by rectangles
        # +------+
        # | rect |
        # |    +-|-----+
        # +------+     |
        #      |  obj  |
        #      +-------+
        on_top = obj.top < rect.top <= obj.bottom
        on_bottom = obj.top <= rect.bottom < obj.bottom
        on_left = obj.left < rect.left <= obj.right
        on_right = obj.left <= rect.right < obj.right

        return (on_top, on_bottom, on_left, on_right)

    def move(self, screen, platforms, dt):
        """Move on the screen.

        Args:
            screen (pygame.Surface): Drawing screen.
            platforms (List[Platform]): Platforms.
            dt (float): Elapsed time[sec] from the previous frame.
        """
        self.v.update(0, 0)

        # If not in jumping, move a player by the key inputs
        # Move to upper/lower
        if pygame.key.get_pressed()[pygame.K_w]:
            self.v.y = -1
        elif pygame.key.get_pressed()[pygame.K_s]:
            self.v.y = 1
        # Move to Left/right
        if pygame.key.get_pressed()[pygame.K_a]:
            self.v.x = -1
        elif pygame.key.get_pressed()[pygame.K_d]:
            self.v.x = 1

        # Normalize the velocity
        mag = self.v.magnitude()
        if mag > 1:
            self.v = self.v.clamp_magnitude(1)
        self.v *= self.speed

        # Calculate a temporal position and a collision area
        pos = self.pos + self.v * dt
        rect = pygame.Rect(
            pos.x - self.width / 2,
            pos.y - self.height / 2,
            self.rect.width,
            self.rect.height,
        )

        # Collision check
        for platform in platforms:
            on_top, on_bottom, on_left, on_right = self.check_collision(
                rect, platform.rect
            )
            if (on_top or on_bottom) and (on_left or on_right):
                in_obj_width = on_left and on_right
                in_obj_height = on_top and on_bottom

                # Limit the position and the velocity
                if on_top and in_obj_width:
                    # Stop on the object's bottom
                    self.v.y = 0
                    pos.y = platform.rect.bottom + self.height / 2
                elif on_bottom and in_obj_width:
                    # Stop on the object's top
                    self.v.y = 0
                    pos.y = platform.rect.top - self.height / 2
                elif on_left and in_obj_height:
                    # Stop on the object's right
                    self.v.x = 0
                    pos.x = platform.rect.right + self.width / 2
                elif on_right and in_obj_height:
                    # Stop on the object's left
                    self.v.x = 0
                    pos.x = platform.rect.left - self.width / 2
                elif on_top and on_left:
                    # Stop on the object's lower right when:
                    if self.rect.top >= platform.rect.bottom:  # Collide at this frame
                        if self.rect.left != platform.rect.right:  # Not on the edge
                            self.v.y = 0
                            pos.y = platform.rect.bottom + self.height / 2
                    if self.rect.left >= platform.rect.right:
                        if self.rect.top != platform.rect.bottom:
                            self.v.x = 0
                            pos.x = platform.rect.right + self.width / 2
                elif on_top and on_right:
                    # Stop on the object's lower left
                    if self.rect.top >= platform.rect.bottom:
                        if self.rect.right != platform.rect.left:
                            self.v.y = 0
                            pos.y = platform.rect.bottom + self.height / 2
                    if self.rect.right <= platform.rect.left:
                        if self.rect.top != platform.rect.bottom:
                            self.v.x = 0
                            pos.x = platform.rect.left - self.width / 2
                elif on_bottom and on_left:
                    # Stop on the object's upper right
                    if self.rect.bottom <= platform.rect.top:
                        if self.rect.left != platform.rect.right:
                            self.v.y = 0
                            pos.y = platform.rect.top - self.height / 2
                    if self.rect.left >= platform.rect.right:
                        if self.rect.bottom != platform.rect.top:
                            self.v.x = 0
                            pos.x = platform.rect.right + self.width / 2
                elif on_bottom and on_right:
                    # Stop on the object's upper left
                    if self.rect.bottom <= platform.rect.top:
                        if self.rect.right != platform.rect.left:
                            self.v.y = 0
                            pos.y = platform.rect.top - self.height / 2
                    if self.rect.right <= platform.rect.left:
                        if self.rect.bottom != platform.rect.top:
                            self.v.x = 0
                            pos.x = platform.rect.left - self.width / 2

        # Update the positions
        self.pos.x = pos.x
        self.pos.y = pos.y
        self.rect.left = self.pos.x - self.width / 2
        self.rect.top = self.pos.y - self.height / 2

    def draw(self, screen):
        """Draw on the screen.

        Args:
            screen (pygame.Surface): Drawing screen.
        """
        # Body
        pygame.draw.rect(screen, self.color, self.rect)

        # Eyes
        eye_pos = [(-5, 0), (5, 0)]
        # Move along with the player's direction
        v = self.v.clamp_magnitude(1) if self.v.magnitude() != 0 else self.v
        for pos in eye_pos:
            pygame.draw.circle(screen, "black", self.pos + v * 5 + pos, 3)


class Block:
    """Block object.

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

    player = Player(pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2))

    S_WIDTH = screen.get_width()
    S_HEIGHT = screen.get_height()

    # Block objects
    blocks = [
        Block(pygame.Vector2(S_WIDTH / 2, -5), S_WIDTH, 10),  # Top wall
        Block(pygame.Vector2(S_WIDTH / 2, S_HEIGHT + 5), S_WIDTH, 10),  # Bottom wall
        Block(pygame.Vector2(-5, S_HEIGHT / 2), 10, S_HEIGHT),  # Left wall
        Block(pygame.Vector2(S_WIDTH + 5, S_HEIGHT / 2), 10, S_HEIGHT),  # Right wall
        Block(pygame.Vector2(S_WIDTH / 2 - 200, S_HEIGHT - 300), 100, 50),
        Block(pygame.Vector2(S_WIDTH / 2, S_HEIGHT - 150), 150, 50),
        Block(pygame.Vector2(S_WIDTH / 2 + 200, S_HEIGHT - 300), 50, 200),
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

        player.move(screen, blocks, dt)

        for block in blocks:
            block.draw(screen)

        player.draw(screen)

        screen.blit(help_text, (5, 5))

        pygame.display.flip()

        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
