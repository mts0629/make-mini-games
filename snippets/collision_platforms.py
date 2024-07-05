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
        jumping (bool): Flag, True if while the player is jumping.
        width (int): Width.
        height (int): Height.
        rect (pygame.Rect): Collision area.
        color (str): Drawn color.
        jump_key_pressing (bool): Flag, True while the jump key is pressing.
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
        self.jumping = True
        self.width = 40
        self.height = 40
        self.rect = pygame.Rect(
            self.pos.x - self.width / 2,
            self.pos.y - self.height / 2,
            self.width,
            self.height,
        )
        self.color = "green"

        self.jump_key_pressing = False

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
        if self.jumping:
            # Free fall
            self.v.y += FALLING_SPEED

            # Limit fall speed
            if self.v.y > MAX_SPEED:
                self.v.y = MAX_SPEED
        else:
            # If not in jumping, move a player by the key inputs
            self.v.update(0, 0)

            # Jump
            if pygame.key.get_pressed()[pygame.K_w]:
                if not self.jump_key_pressing:
                    self.v.y = -self.jumping_speed
                    self.jump_key_pressing = True
            else:
                if self.jump_key_pressing:
                    self.jump_key_pressing = False

            # Move to Left/right
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

        self.jumping = True

        # Collision check
        for objective in objectives:
            obj_rect = objective.rect

            on_player_top, on_player_bottom, on_player_left, on_player_right = (
                self.check_collision(rect, obj_rect)
            )

            if (on_player_top or on_player_bottom) and (
                on_player_left or on_player_right
            ):
                between_obj_width = on_player_left and on_player_right
                between_obj_height = on_player_top and on_player_bottom

                # Limit player's position and velocity
                if on_player_top and between_obj_width:
                    # Stop on the object's bottom
                    if self.v.y < 0:  # When the player collide from the lower side
                        pos.y = obj_rect.bottom + self.height / 2
                    self.v.y = 0
                elif on_player_bottom and between_obj_width:
                    # Stop on the object's top
                    if self.v.y > 0:  # From the upper side
                        pos.y = obj_rect.top - self.height / 2
                    self.v.y = 0
                    # If jumping, set the flag to false
                    if self.jumping:
                        self.jumping = False
                elif on_player_left and between_obj_height:
                    # Stop on the object's right
                    if self.v.x < 0:  # From the left side
                        pos.x = obj_rect.right + self.width / 2
                    self.v.x = 0
                elif on_player_right and between_obj_height:
                    # Stop on the object's left
                    if self.v.x > 0:  # From the right side
                        pos.x = obj_rect.left - self.width / 2
                    self.v.x = 0
                elif on_player_top and on_player_left:
                    # Stop on the object's lower right when:
                    if self.rect.top >= obj_rect.bottom:  # Collide at this frame
                        # And when the player is not on the object's edge
                        if self.rect.left != obj_rect.right:
                            if self.v.y < 0:  # And from the upper side
                                pos.y = obj_rect.bottom + self.height / 2
                            self.v.y = 0
                    if self.rect.left >= obj_rect.right:
                        if self.rect.top != obj_rect.bottom:
                            if self.v.x < 0:
                                pos.x = obj_rect.right + self.width / 2
                            self.v.x = 0
                elif on_player_top and on_player_right:
                    # Stop on the object's lower left
                    if self.rect.top >= obj_rect.bottom:
                        if self.rect.right != obj_rect.left:
                            if self.v.y < 0:
                                pos.y = obj_rect.bottom + self.height / 2
                            self.v.y = 0
                    if self.rect.right <= obj_rect.left:
                        if self.rect.top != obj_rect.bottom:
                            if self.v.x > 0:
                                pos.x = obj_rect.left - self.width / 2
                            self.v.x = 0
                elif on_player_bottom and on_player_left:
                    # Stop on the object's upper right
                    if self.rect.bottom <= obj_rect.top:
                        if self.rect.left != obj_rect.right:
                            if self.v.y > 0:
                                pos.y = obj_rect.top - self.height / 2
                            self.v.y = 0
                            if self.jumping:
                                self.jumping = False
                    if self.rect.left >= obj_rect.right:
                        if self.rect.bottom != obj_rect.top:
                            if self.v.x < 0:
                                pos.x = obj_rect.right + self.width / 2
                            self.v.x = 0
                elif on_player_bottom and on_player_right:
                    # Stop on the object's upper left
                    if self.rect.bottom <= obj_rect.top:
                        if self.rect.right != obj_rect.left:
                            if self.v.y > 0:
                                pos.y = obj_rect.top - self.height / 2
                            self.v.y = 0
                            if self.jumping:
                                self.jumping = False
                    if self.rect.right <= obj_rect.left:
                        if self.rect.bottom != obj_rect.top:
                            if self.v.x > 0:
                                pos.x = obj_rect.left - self.width / 2
                            self.v.x = 0
            # Fix the position when the player slipped through the objective between 2 frames
            if (on_player_left or on_player_right) and (rect.bottom >= obj_rect.bottom):
                if self.rect.top < obj_rect.top:
                    pos.y = obj_rect.top - self.height / 2
                    self.v.y = 0
            if (on_player_left or on_player_right) and (rect.top <= obj_rect.top):
                if self.rect.bottom > obj_rect.bottom:
                    pos.y = obj_rect.bottom + self.height / 2
                    self.v.y = 0

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
            f"jumping={player.jumping}",
            True,
            (255, 255, 255),
        )
        screen.blit(debug_text, (5, 25))

        pygame.display.flip()

        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
