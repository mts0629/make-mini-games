"""Collision check between the player and platforms in a stage."""

from typing import List

import pygame


# Size of character block
BLOCK_SIZE = 40

# Falling speed
FALLING_SPEED = 20
# Maximum speed
MAX_SPEED = 650
# Player's speed
PLAYER_SPEED_X = 200
# Jumping speed
JUMPING_SPEED = 650


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
        holding_jump_key (bool): Flag, True while the jump key is holding.
    """

    def __init__(self, pos):
        """Initialize.

        Args:
            pos (pygame.Vector2): Initial position (x, y).
        """
        self.pos = pos.copy()

        self.v = pygame.Vector2(0, 0)
        self.speed = PLAYER_SPEED_X
        self.jumping_speed = JUMPING_SPEED

        self.on_ground = False

        self.width = BLOCK_SIZE
        self.height = BLOCK_SIZE
        self.rect = pygame.Rect(
            self.pos.x - self.width / 2,
            self.pos.y - self.height / 2,
            self.width,
            self.height,
        )
        self.color = "green"

        self.holding_jump_key = False

    def move(self, blocks, dt):
        """Move on the screen.

        Args:
            blocks (List[Block]): Blocks.
            dt (float): Elapsed time[sec] from the previous frame.
        """

        if self.on_ground:
            self.v.x = 0
            self.v.y = 0

            # If not in jumping, move a player by the key inputs
            # Jump
            if pygame.key.get_pressed()[pygame.K_w]:
                # Only when the jump key doesn't be holded
                if not self.holding_jump_key:
                    self.v.y = -self.jumping_speed
                    self.holding_jump_key = True
            else:
                if self.holding_jump_key:
                    self.holding_jump_key = False
            # Move to left/right
            if pygame.key.get_pressed()[pygame.K_a]:
                self.v.x = -self.speed
            elif pygame.key.get_pressed()[pygame.K_d]:
                self.v.x = self.speed
        else:
            # Free fall
            self.v.y += FALLING_SPEED
            # Limit fall speed
            if self.v.y > MAX_SPEED:
                self.v.y = MAX_SPEED

        # Calculate a temporal position and a collision area
        pos = self.pos + self.v * dt
        rect = self.rect.move(
            pos.x - self.rect.centerx, pos.y - self.rect.centery
        )

        # Collision
        idx = rect.collidelist([block.rect for block in blocks])

        if idx == -1:
            self.on_ground = False
        else:
            b = blocks[idx]

            # if b.rect.left < rect.left <= b.rect.right:
            #     if self.v.x < 0:
            #         self.v.x = 0
            #     x = b.rect.right + self.width / 2
            #     rect.move_ip(x - pos.x, pos.y)
            #     pos.x = x
            # elif b.rect.left <= rect.right < b.rect.right:
            #     if self.v.x > 0:
            #         self.v.x = 0
            #     x = b.rect.left - self.width / 2
            #     rect.move_ip(x - pos.x, pos.y)
            #     pos.x = x

            if b.rect.top < rect.top <= b.rect.bottom:
                if self.v.y < 0:
                    self.v.y = 0
                y = b.rect.bottom + self.height / 2
                rect.move_ip(pos.x, pos.y - y)
                pos.y = y
            elif b.rect.top <= rect.bottom < b.rect.bottom:
                if self.v.y > 0:
                    self.v.y = 0
                y = b.rect.top - self.height / 2
                rect.move_ip(pos.x, pos.y - y)
                pos.y = y
                self.on_ground = True

        # Update the position
        self.pos = pos
        self.rect.move_ip(
            rect.x - self.rect.x, rect.y - self.rect.y
        )

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


def _create_platforms(tile_data: List[int], tile_cols: int, block_size: int) -> List[Block]:
    """Create platforms from a tile data."""
    platforms = []
    for i, tile in enumerate(tile_data):
        if tile == 1:
            y = i // tile_cols
            x = i % tile_cols
            block = Block(
                pygame.Vector2(x * block_size + block_size / 2, y * block_size + block_size / 2),
                block_size, block_size
            )
            platforms.append(block)

    return platforms


def main():
    """Main loop."""

    pygame.init()

    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 480
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill("Black")

    # Help text
    font = pygame.font.Font(pygame.font.get_default_font(), 20)
    RED = (255, 0, 0)
    help_text = font.render(
        "[W] Jump/[A] Left/[D] Right/[ESC] Quit", True, RED
    )

    player = Player(
        pygame.Vector2(screen.get_width() / 2, screen.get_height() - BLOCK_SIZE - 200)
    )

    tile_data = [
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
        1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1,
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
        1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1,
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
        1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1,
        1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1,
        1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
    ]

    platforms = _create_platforms(tile_data, (SCREEN_WIDTH // BLOCK_SIZE), BLOCK_SIZE)

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
            f"(rx,rx)=({player.rect.centerx:.0f},{player.rect.centery:.0f}),"
            f"on_ground={player.on_ground}",
            True,
            RED
        )
        screen.blit(debug_text, (20, 40))

        pygame.display.flip()

        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
