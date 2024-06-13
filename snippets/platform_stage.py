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
        self.jumping = True

    def move(self, screen, dt):
        """Move on the screen.

        Args:
            screen (pygame.Surface): Drawing screen.
            dt (float): Elapsed time[sec] from the previous frame.
        """
        if not self.jumping:
            self.v = pygame.Vector2(0, 0)

            # If not in jumping, move a player by the key inputs
            # Jump
            if pygame.key.get_pressed()[pygame.K_w]:
                self.v.y = -5
                self.jumping = True
            # Left/right
            if pygame.key.get_pressed()[pygame.K_a]:
                self.v.x = -1
            elif pygame.key.get_pressed()[pygame.K_d]:
                self.v.x = 1
        else:
            # Falling, add the G
            self.v.y += 0.2

        # Move the player
        prev_pos = self.pos.copy()
        self.pos += self.speed * self.v * dt

        # Stop at the screen's edge
        self.pos.x = pygame.math.clamp(
            self.pos.x, self.radius, screen.get_width() - self.radius
        )
        # self.pos.y = pygame.math.clamp(
        #     self.pos.y, self.radius, screen.get_height() - self.radius
        # )

        # Stop falling at the bottom of the screen
        if self.pos.y == screen.get_height() - self.radius:
            self.jumping = False

    def check_collision(self, objective):
        """Check whether the player collides with an objective.

        Args:
            objective (Platform): Objective to be checked.

        Returns:
            (bool): Flag, True if the player collides with the objective.
        """
        player_l = self.pos.x - self.radius
        player_r = self.pos.x + self.radius
        player_u = self.pos.y - self.radius
        player_d = self.pos.y + self.radius

        objective_l = objective.pos.x - objective.width / 2
        objective_r = objective.pos.x + objective.width / 2
        objective_u = objective.pos.y - objective.height / 2
        objective_d = objective.pos.y + objective.height / 2

        # Collision by rectangles
        # L      R
        # +------+ U
        # |      |
        # |    +-|------+
        # +------+ D    |
        #      |        |
        #      +--------+

        if ((objective_l < player_r < objective_r) or (objective_l < player_l < objective_r)) and \
           ((objective_u < player_u < objective_d) or (objective_u < player_d < objective_d)):
           return True

        return False


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
        Rect (pygame.Rect): Drawn rectangle.
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
        self.rect = pygame.Rect(
            pos.x - width / 2, pos.y - height / 2,
            width, height
        )

    def draw(self, screen):
        """Draw on the screen.

        Args:
            screen (pygame.Surface): Drawing screen.
        """
        pygame.draw.rect(screen, "white", self.rect)


def main():
    """Main loop."""

    pygame.init()

    screen = pygame.display.set_mode((640, 480))

    # Help text
    font = pygame.font.Font(pygame.font.get_default_font(), 20)
    help_text = font.render(
        "[W] Jump/[A] Left/[D] Right/[ESC] Quit",
        True, (255, 255, 255)
    )

    player = Player(
        pygame.Vector2(screen.get_width() / 2, screen.get_height() - 10)
    )

    S_WIDTH = screen.get_width()
    S_HEIGHT = screen.get_height()

    # Platforms
    platforms = [
        Platform(pygame.Vector2(S_WIDTH / 2, S_HEIGHT + 5), S_WIDTH, 10),  # Floor
        Platform(pygame.Vector2(-5, S_HEIGHT / 2), 10, S_HEIGHT),  # Left wall
        Platform(pygame.Vector2(S_WIDTH + 5, S_HEIGHT / 2), 10, S_HEIGHT),  # Right wall
        Platform(pygame.Vector2(S_WIDTH / 2 - 200, S_HEIGHT - 300), 150, 30),
        Platform(pygame.Vector2(S_WIDTH / 2, S_HEIGHT - 150), 200, 30),
        Platform(pygame.Vector2(S_WIDTH / 2 + 200, S_HEIGHT - 300), 150, 30)
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

        prev_pos = player.pos.copy()

        player.move(screen, dt)

        for platform in platforms:
            if player.check_collision(platform):
                if prev_pos.y < platform.pos.y:
                    player.jumping = False
            platform.draw(screen)

        player.draw(screen)

        screen.blit(help_text, (5, 5))

        pygame.display.flip()

        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
