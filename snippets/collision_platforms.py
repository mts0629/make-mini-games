"""Collision check between the player and platforms in a stage."""

import pygame

# Constants
# Falling speed
FALLING_SPEED = 20
# Maximum speed
MAX_SPEED = 650


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
        self.speed = 200
        self.jumping_speed = 650
        self.on_ground = False
        self.width = 40
        self.height = 40
        self.rect = pygame.Rect(
            self.pos.x - self.width / 2,
            self.pos.y - self.height / 2,
            self.width,
            self.height,
        )
        self.color = "green"

        self.jump_key_is_holding = False

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

    def move(self, screen, objectives, dt):
        """Move on the screen.

        Args:
            screen (pygame.Surface): Drawing screen.
            objectives (List[Block]): Objectives.
            dt (float): Elapsed time[sec] from the previous frame.
        """
        if self.on_ground:
            # If not in jumping, move a player by the key inputs
            self.v.update(0, 0)

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
        else:
            # Free fall
            self.v.y += FALLING_SPEED
            # Limit fall speed
            if self.v.y > MAX_SPEED:
                self.v.y = MAX_SPEED

        # Previous collision area
        prev_rect = self.rect

        # Calculate a temporal position and a collision area
        pos = self.pos + self.v * dt
        rect = pygame.Rect(
            pos.x - self.width / 2,
            pos.y - self.height / 2,
            self.rect.width,
            self.rect.height,
        )

        self.on_ground = False

        # Collision check
        for objective in objectives:
            obj_rect = objective.rect

            on_player_top, on_player_bottom, on_player_left, on_player_right = (
                self.check_collision(rect, obj_rect)
            )

            if (on_player_top or on_player_bottom) and (
                on_player_left or on_player_right
            ):
                # Limit player's position and velocity
                if (
                    (not on_player_top)
                    and on_player_bottom
                    and on_player_left
                    and on_player_right
                ):
                    # From the upper side, stop on the object's top
                    if self.v.y > 0:
                        self.v.y = 0
                        pos.y = obj_rect.top - self.height / 2
                        self.on_ground = True
                elif (
                    on_player_top
                    and (not on_player_bottom)
                    and on_player_left
                    and on_player_right
                ):
                    # From the lower side, stop on the object's bottom
                    if self.v.y < 0:
                        self.v.y = 0
                        pos.y = obj_rect.bottom + self.height / 2
                elif (
                    on_player_top
                    and on_player_bottom
                    and on_player_left
                    and (not on_player_right)
                ):
                    # From the right side, stop on the object's right
                    if self.v.x < 0:
                        self.v.x = 0
                        pos.x = obj_rect.right + self.width / 2
                elif (
                    on_player_top
                    and on_player_bottom
                    and (not on_player_left)
                    and on_player_right
                ):
                    # From the left side, stop on the object's left
                    if self.v.x > 0:
                        self.v.x = 0
                        pos.x = obj_rect.left - self.width / 2
                elif (
                    (not on_player_top)
                    and on_player_bottom
                    and on_player_left
                    and (not on_player_right)
                ):
                    # From the upper-left side
                    if self.v.y > 0:
                        self.v.y = 0
                        pos.y = obj_rect.top - self.height / 2
                    self.on_ground = True
                    if self.v.x < 0:
                        self.v.x = 0
                        pos.x = obj_rect.right + self.width / 2
                elif (
                    (not on_player_top)
                    and on_player_bottom
                    and (not on_player_left)
                    and on_player_right
                ):
                    # From the upper-right side
                    if self.v.y > 0:
                        self.v.y = 0
                        pos.y = obj_rect.top - self.height / 2
                    self.on_ground = True
                    if self.v.x > 0:
                        self.v.x = 0
                        pos.x = obj_rect.left - self.width / 2
                elif (
                    on_player_top
                    and (not on_player_bottom)
                    and on_player_left
                    and (not on_player_right)
                ):
                    # From the lower-left side
                    if self.v.y < 0:
                        self.v.y = 0
                        pos.y = obj_rect.bottom + self.height / 2
                    if self.v.x < 0:
                        self.v.x = 0
                        pos.x = obj_rect.right + self.width / 2
                elif (
                    on_player_top
                    and (not on_player_bottom)
                    and (not on_player_left)
                    and on_player_right
                ):
                    # From the lower-right side
                    if self.v.y < 0:
                        self.v.y = 0
                        pos.y = obj_rect.bottom + self.height / 2
                    if self.v.x > 0:
                        self.v.x = 0
                        pos.x = obj_rect.left - self.width / 2

            # Stop when the player slipped through an object between 2 frames
            if on_player_left or on_player_right:
                if (prev_rect.bottom <= obj_rect.top) and (rect.bottom > obj_rect.top):
                    if self.v.y > 0:
                        self.v.y = 0
                        pos.y = obj_rect.top - self.height / 2
                    self.on_ground = True
                if (prev_rect.top >= obj_rect.bottom) and (rect.top < obj_rect.bottom):
                    if self.v.y < 0:
                        self.v.y = 0
                        pos.y = obj_rect.bottom + self.height / 2

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

    player = Player(pygame.Vector2(screen.get_width() / 2, screen.get_height() - 20))

    S_WIDTH = screen.get_width()
    S_HEIGHT = screen.get_height()

    # Platforms
    platforms = [
        Block(pygame.Vector2(S_WIDTH / 2, -5), S_WIDTH, 10),  # Ceiling
        Block(pygame.Vector2(S_WIDTH / 2, S_HEIGHT + 5), S_WIDTH, 10),  # Floor
        Block(pygame.Vector2(-5, S_HEIGHT / 2), 10, S_HEIGHT),  # Left wall
        Block(pygame.Vector2(S_WIDTH + 5, S_HEIGHT / 2), 10, S_HEIGHT),  # Right wall
        # Platforms in different sizes
        Block(pygame.Vector2(S_WIDTH / 2 - 200, S_HEIGHT - 300), 150, 10),
        Block(pygame.Vector2(S_WIDTH / 2, S_HEIGHT - 150), 200, 5),
        Block(pygame.Vector2(S_WIDTH / 2 + 200, S_HEIGHT - 300), 150, 20),
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

        # Debug info
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
