"""Collision check between the player and platforms in a stage."""

import pygame

# Constants
# Falling speed
FALLING_SPEED = 20
# Maximum speed
MAX_SPEED = 650
# Size of character block
B_SIZE = 40
# Player's speed
PLAYER_SPEED_X = 200
# Jump speed
JUMP_SPEED = 650


class Player:
    """Player object.

    Attributes:
        pos (pygame.Vector2): Position (x, y).
        v (pygame.Vector2): Velocity (x, y).
        speed (float): Moving speed.
        jumping_speed (float): Jumping speed.
        on_ground (bool): Flag, True if while the player is on the top of an object.
        width (int): Width.
        height (int): Height.
        rect (pygame.Rect): Collision area.
        color (str): Drawn color.
        jump_key_is_holding (bool): Flag, True while the jump key is holding.
    """

    def __init__(self, pos):
        """Initialize.

        Args:
            pos (pygame.Vector2): Initial position (x, y).
        """
        self.pos = pos.copy()
        self.v = pygame.Vector2(0, 0)
        self.speed = PLAYER_SPEED_X
        self.jumping_speed = JUMP_SPEED
        self.on_ground = False
        self.width = B_SIZE
        self.height = B_SIZE
        self.rect = pygame.Rect(
            self.pos.x - self.width / 2,
            self.pos.y - self.height / 2,
            self.width,
            self.height,
        )
        self.color = "green"

        self.jump_key_is_holding = False

    def move(self, objects, dt):
        """Move on the screen.

        Args:
            objects (List[Block]): objects.
            dt (float): Elapsed time[sec] from the previous frame.
        """
        # Free fall
        self.v.y += FALLING_SPEED
        # Limit fall speed
        if self.v.y > MAX_SPEED:
            self.v.y = MAX_SPEED

        if self.on_ground:
            # If not in jumping, move a player by the key inputs
            self.v.x = 0

            # Jump
            if pygame.key.get_pressed()[pygame.K_w]:
                # Only when the jump key doesn't be holding
                if not self.jump_key_is_holding:
                    self.v.y = -self.jumping_speed
                    self.on_ground = False

                    self.jump_key_is_holding = True
            else:
                if self.jump_key_is_holding:
                    self.jump_key_is_holding = False

            # Move to left/right
            if pygame.key.get_pressed()[pygame.K_a]:
                self.v.x = -self.speed
            elif pygame.key.get_pressed()[pygame.K_d]:
                self.v.x = self.speed

        # Calculate a temporal position and a collision area
        pos = self.pos + self.v * dt
        rect = pygame.Rect(
            pos.x - self.width / 2,
            pos.y - self.height / 2,
            self.rect.width,
            self.rect.height,
        )

        def hit_x(player, object):
            """Check collision between two rectangles for x-axis.

            Args:
                player (pygame.Rect): Collision area of the player.
                object (pygame.Rect): Collision of the object.

            Returns:
                (Tuple[bool]): Collision flag for two directions,
                    [left, right] of the player.
            """
            on_left = object.left < player.left <= object.right
            on_right = object.left <= player.right < object.right
            return on_left, on_right
        
        def hit_y(player, object):
            """Check collision between two rectangles for y-axis.

            Args:
                player (pygame.Rect): Collision area of the player.
                object (pygame.Rect): Collision of the object.

            Returns:
                (Tuple[bool]): Collision flag for two directions,
                    [top, bottom] on the player.
            """
            on_top = object.top < player.top <= object.bottom
            on_bottom = object.top <= player.bottom < object.bottom
            return on_top, on_bottom

        # Collision check
        for object in objects:
            obj_rect = object.rect

            on_left, on_right = hit_x(rect, obj_rect)
            on_top, on_bottom = hit_y(rect, obj_rect)

            if (on_top or on_bottom) and (on_left or on_right):
                if on_left and (not on_right):
                    # From the right side, stop on the object's right
                    if self.v.x < 0:
                        self.v.x = 0
                        pos.x = obj_rect.right + self.width / 2
                if on_right and (not on_left):
                    # From the left side, stop on the object's left
                    if self.v.x > 0:
                        self.v.x = 0
                        pos.x = obj_rect.left - self.width / 2

                if on_bottom and (not on_top):
                    # From the upper side, stop on the object's top
                    if self.v.y > 0:
                        self.v.y = 0
                        pos.y = obj_rect.top - self.height / 2
                if on_top and (not on_bottom):
                    # From the lower side, stop on the object's bottom
                    if self.v.y < 0:
                        self.v.y = 0
                        pos.y = obj_rect.bottom + self.height / 2

                if (not on_top) and on_bottom and (on_left or on_right):
                    self.on_ground = True

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

    # Background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill("Black")

    # Help text
    font = pygame.font.Font(pygame.font.get_default_font(), 20)
    help_text = font.render(
        "[W] Jump/[A] Left/[D] Right/[ESC] Quit", True, (255, 255, 255)
    )

    player = Player(pygame.Vector2(screen.get_width() / 2, screen.get_height() - B_SIZE / 2))

    S_WIDTH = screen.get_width()
    S_HEIGHT = screen.get_height()

    # Platforms
    platforms = [
        # Celing
        Block(pygame.Vector2(S_WIDTH / 2, -B_SIZE / 2), S_WIDTH, B_SIZE),
        # Floor
        Block(pygame.Vector2(S_WIDTH / 2, S_HEIGHT + B_SIZE / 2), S_WIDTH, B_SIZE),
        # Left wall
        Block(pygame.Vector2(-B_SIZE / 2, S_HEIGHT / 2), B_SIZE, S_HEIGHT),
        # Right wall
        Block(pygame.Vector2(S_WIDTH + B_SIZE / 2, S_HEIGHT / 2), B_SIZE, S_HEIGHT),
        # Platforms in different sizes
        Block(pygame.Vector2(S_WIDTH / 2 - 200, S_HEIGHT - 300), B_SIZE * 2, B_SIZE),
        Block(pygame.Vector2(S_WIDTH / 2, S_HEIGHT - 150), 100, B_SIZE),
        Block(pygame.Vector2(S_WIDTH / 2 + 200, S_HEIGHT - 300), B_SIZE * 4, B_SIZE),
        Block(pygame.Vector2(S_WIDTH / 2 + 200, S_HEIGHT - 40), B_SIZE * 2, B_SIZE * 3),
        Block(pygame.Vector2(B_SIZE, S_HEIGHT - 120), B_SIZE * 4, B_SIZE),
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

        player.move(platforms, dt)

        screen.blit(background, (0, 0))

        for platform in platforms:
            platform.draw(screen)

        player.draw(screen)

        screen.blit(help_text, (5, 5))

        # Print debug info
        debug_text = font.render(
            f"(x,y)=({player.pos.x:.0f},{player.pos.y:.0f}),"
            f"(vx,vx)=({player.v.x:.0f},{player.v.y:.0f}),"
            f"on_ground={player.on_ground}",
            True,
            (255, 255, 255),
        )
        screen.blit(debug_text, (5, 25))

        pygame.display.flip()

        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
