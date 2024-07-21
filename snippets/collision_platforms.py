"""Collision check between the player and platforms in a stage."""

from enum import Flag, auto

import pygame

# Constants
# Falling speed
FALLING_SPEED = 20
# Maximum speed
MAX_SPEED = 650


class CollisionFlag(Flag):
    """Collision flag of 2 rectangles for each direction."""

    NONE = 0  # No collision
    ON_BOTTOM = auto()
    ON_TOP = auto()
    ON_LEFT = auto()
    ON_RIGHT = auto()
    ON_BOTTOM_LEFT = ON_BOTTOM | ON_LEFT
    ON_BOTTOM_RIGHT = ON_BOTTOM | ON_RIGHT
    ON_TOP_LEFT = ON_TOP | ON_LEFT
    ON_TOP_RIGHT = ON_TOP | ON_RIGHT


def check_collision(target_rect, prev_target_rect, obj_rect):
    """Check whether the collision area of a target collides to that of an objective.

    Args:
        target_rect (pygame.Rect): Collision area of the target.
        prev_target_rect (pygame.Rect): Collision are of the target in the previous frame.
        obj_rect (pygame.Rect): Collision of the objective.

    Returns:
        (CollisionFlag): Collision flag for each direction between the rectangles.
    """
    # Collision check by rectangles
    #
    #           Left     Right
    #           :        :
    # Top ..... +--------+
    #           | target |
    #           |     +--|-----+
    # Bottom .. +--------+     |
    #                 |  obj   |
    #                 +--------+
    #
    on_top = obj_rect.top < target_rect.top <= obj_rect.bottom
    on_bottom = obj_rect.top <= target_rect.bottom < obj_rect.bottom
    on_left = obj_rect.left < target_rect.left <= obj_rect.right
    on_right = obj_rect.left <= target_rect.right < obj_rect.right

    if (not on_top) and on_bottom and on_left and on_right:
        return CollisionFlag.ON_BOTTOM
    elif on_top and (not on_bottom) and on_left and on_right:
        return CollisionFlag.ON_TOP
    elif on_top and on_bottom and on_left and (not on_right):
        return CollisionFlag.ON_LEFT
    elif on_top and on_bottom and (not on_left) and on_right:
        return CollisionFlag.ON_RIGHT
    elif (not on_top) and on_bottom and on_left and (not on_right):
        return CollisionFlag.ON_BOTTOM | CollisionFlag.ON_LEFT
    elif (not on_top) and on_bottom and (not on_left) and on_right:
        return CollisionFlag.ON_BOTTOM | CollisionFlag.ON_RIGHT
    elif on_top and (not on_bottom) and on_left and (not on_right):
        return CollisionFlag.ON_TOP | CollisionFlag.ON_LEFT
    elif on_top and on_bottom and (not on_left) and on_right:
        return CollisionFlag.ON_TOP | CollisionFlag.ON_RIGHT

    # Collision when the player slipped through the object between 2 frames
    # Bottom
    if (prev_target_rect.bottom <= obj_rect.top) and (
        target_rect.bottom > obj_rect.top
    ):
        if on_left and on_right:
            return CollisionFlag.ON_BOTTOM
        elif on_left and (not on_right):
            return CollisionFlag.ON_BOTTOM | CollisionFlag.ON_LEFT
        elif (not on_left) and on_right:
            return CollisionFlag.ON_BOTTOM | CollisionFlag.ON_RIGHT
    # Top
    if (prev_target_rect.top >= obj_rect.bottom) and (
        target_rect.top < obj_rect.bottom
    ):
        if on_left and on_right:
            return CollisionFlag.ON_TOP
        elif on_left and (not on_right):
            return CollisionFlag.ON_TOP | CollisionFlag.ON_LEFT
        elif (not on_left) and on_right:
            return CollisionFlag.ON_TOP | CollisionFlag.ON_RIGHT
    # Left
    if (prev_target_rect.left >= obj_rect.right) and (
        target_rect.left < obj_rect.right
    ):
        if on_top and on_bottom:
            return CollisionFlag.ON_LEFT
        elif on_top and (not on_bottom):
            return CollisionFlag.ON_TOP | CollisionFlag.ON_LEFT
        elif (not on_top) and on_bottom:
            return CollisionFlag.ON_BOTTOM | CollisionFlag.ON_LEFT
    # Right
    if (prev_target_rect.right <= obj_rect.left) and (
        target_rect.right > obj_rect.left
    ):
        if on_top and on_bottom:
            return CollisionFlag.ON_RIGHT
        elif on_top and (not on_bottom):
            return CollisionFlag.ON_TOP | CollisionFlag.ON_RIGHT
        elif (not on_top) and on_bottom:
            return CollisionFlag.ON_BOTTOM | CollisionFlag.ON_RIGHT

    return CollisionFlag.NONE


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

            flag = check_collision(rect, prev_rect, obj_rect)
            if flag != CollisionFlag.NONE:
                # Limit player's position and velocity
                if flag == CollisionFlag.ON_BOTTOM:
                    # From the upper side, stop on the object's top
                    if self.v.y > 0:
                        self.v.y = 0
                        pos.y = obj_rect.top - self.height / 2
                    if prev_rect.bottom <= obj_rect.top:
                        self.on_ground = True
                elif flag == CollisionFlag.ON_TOP:
                    # From the lower side, stop on the object's bottom
                    if self.v.y < 0:
                        self.v.y = 0
                        pos.y = obj_rect.bottom + self.height / 2
                elif flag == CollisionFlag.ON_LEFT:
                    # From the right side, stop on the object's right
                    if self.v.x < 0:
                        self.v.x = 0
                        pos.x = obj_rect.right + self.width / 2
                elif flag == CollisionFlag.ON_RIGHT:
                    # From the left side, stop on the object's left
                    if self.v.x > 0:
                        self.v.x = 0
                        pos.x = obj_rect.left - self.width / 2
                elif flag == CollisionFlag.ON_BOTTOM_LEFT:
                    # From the upper-left side
                    if (self.v.y > 0) and (rect.bottom >= obj_rect.top):
                        self.v.y = 0
                        pos.y = obj_rect.top - self.height / 2
                    if prev_rect.bottom <= obj_rect.top:
                        self.on_ground = True
                    if (self.v.x < 0) and (rect.left >= obj_rect.right):
                        self.v.x = 0
                        pos.x = obj_rect.right + self.width / 2
                elif flag == CollisionFlag.ON_BOTTOM_RIGHT:
                    # From the upper-right side
                    if (self.v.y > 0) and (rect.bottom >= obj_rect.top):
                        self.v.y = 0
                        pos.y = obj_rect.top - self.height / 2
                    if prev_rect.bottom <= obj_rect.top:
                        self.on_ground = True
                    if (self.v.x > 0) and (rect.right <= obj_rect.left):
                        self.v.x = 0
                        pos.x = obj_rect.left - self.width / 2
                elif flag == CollisionFlag.ON_TOP_LEFT:
                    # From the lower-left side
                    if (self.v.y < 0) and (rect.top <= obj_rect.bottom):
                        self.v.y = 0
                        pos.y = obj_rect.bottom + self.height / 2
                    if (self.v.x < 0) and (rect.left >= obj_rect.right):
                        self.v.x = 0
                        pos.x = obj_rect.right + self.width / 2
                elif flag == CollisionFlag.ON_TOP_RIGHT:
                    # From the lower-right side
                    if (self.v.y < 0) and (rect.top <= obj_rect.bottom):
                        self.v.y = 0
                        pos.y = obj_rect.bottom + self.height / 2
                    if (self.v.x > 0) and (rect.right <= obj_rect.left):
                        self.v.x = 0
                        pos.x = obj_rect.left - self.width / 2

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
        Block(pygame.Vector2(S_WIDTH / 2 - 200, S_HEIGHT - 300), 80, 10),
        Block(pygame.Vector2(S_WIDTH / 2, S_HEIGHT - 150), 100, 5),
        Block(pygame.Vector2(S_WIDTH / 2 + 200, S_HEIGHT - 300), 160, 20),
        Block(pygame.Vector2(S_WIDTH / 2 + 200, S_HEIGHT - 50), 80, 100),
        Block(pygame.Vector2(75, S_HEIGHT - 120), 150, 40),
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
