import os
import pygame as pg

if not pg.font:
    print("Warning, fonts disabled")
if not pg.mixer:
    print("Warning, sound disabled")


main_dir = os.path.split(os.path.abspath(__file__))[0]
# Subdirectory for game data
# Data are in the example directory of pygame
data_dir = os.path.join(main_dir, "data")


def load_image(name, colorkey=None, scale=1):
    """Load an image data."""
    fullname = os.path.join(data_dir, name)
    image = pg.image.load(fullname)

    # Scale the image
    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pg.transform.scale(image, size)

    image = image.convert()
    # Set the colorkey
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))  # Top-left pixel
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()


def load_sound(name):
    """Load a sound data."""

    class NoneSound:
        """Dummy sound class."""

        def play(self):
            pass

    # If the mixer is not available, return the dummy class
    if not pg.mixer or not pg.mixer.get_init():
        return NoneSound()

    fullname = os.path.join(data_dir, name)
    sound = pg.mixer.Sound(fullname)

    return sound


class Fist(pg.sprite.Sprite):
    """Moves a clenched fist on the screen, following the mouse."""

    def __init__(self):
        pg.sprite.Sprite.__init__(self)  # Initialize a Sprite
        self.image, self.rect = load_image("fist.png", -1)
        self.fist_offset = (-235, -80)
        self.punching = False

    def update(self):  # Called once per frame for all Sprites
        """Move the fist based on the mouse position."""
        pos = pg.mouse.get_pos()
        self.rect.topleft = pos
        self.rect.move_ip(self.fist_offset)
        if self.punching:
            self.rect.move_ip(15, 25)

    def punch(self, target):
        """Returns True if the fist collides with the target."""
        if not self.punching:
            self.punching = True
            hitbox = self.rect.inflate(-5, -5)
            return hitbox.colliderect(target.rect)

    def unpunch(self):
        """Pull the fist back."""
        self.punching = False


class Chimp(pg.sprite.Sprite):
    """Moves a monkey critter across the screen.
    It can spin the monkey when it is punched.
    """

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("chimp.png", -1, 4)
        screen = pg.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10, 90
        self.move = 18
        self.dizzy = False

    def update(self):
        """Walk or spin, depending on the monkey's state."""
        if self.dizzy:
            self._spin()
        else:
            self._walk()

    def _walk(self):
        """Move the monkey across the screen, and turn at the ends."""
        newpos = self.rect.move((self.move, 0))
        if not self.area.contains(newpos):
            if self.rect.left < self.area.left or self.rect.right > self.area.right:
                self.move = -self.move
                newpos = self.rect.move((self.move, 0))
                self.image = pg.transform.flip(self.image, True, False)
        self.rect = newpos

    def _spin(self):
        """Spin the monkey image."""
        center = self.rect.center
        self.dizzy = self.dizzy + 12
        if self.dizzy >= 360:
            self.dizzy = False
            self.image = self.original
        else:
            rotate = pg.transform.rotate
            self.image = rotate(self.original, self.dizzy)
        self.rect = self.image.get_rect(center=center)

    def punched(self):
        """Start spinning the monkey."""
        if not self.dizzy:
            self.dizzy = True
            self.original = self.image


def main():
    """Main routine."""
    # Initialization
    pg.init()
    screen = pg.display.set_mode((1280, 480), pg.SCALED)
    pg.display.set_caption("Monkey Fever")
    pg.mouse.set_visible(False)

    # Create the background
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((170, 238, 187))

    # Put text on the background, centered
    if pg.font:
        font = pg.font.Font(None, 64)
        text = font.render("Pummenl The Chimp, And Win $$$", True, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width() / 2, y=10)
        background.blit(text, textpos)

    # Display the background
    screen.blit(background, (0, 0))
    pg.display.flip()

    # Prepare game objects
    whiff_sound = load_sound("whiff.wav")
    punch_sound = load_sound("punch.wav")
    chimp = Chimp()
    fist = Fist()
    allsprites = pg.sprite.RenderPlain((chimp, fist))
    clock = pg.time.Clock()

    # Main loop
    going = True
    while going:
        clock.tick(60)

        # Handle input events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                going = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if fist.punch(chimp):
                    punch_sound.play()  # Punch
                    chimp.punched()
                else:
                    whiff_sound.play()  # Miss
            elif event.type == pg.MOUSEBUTTONUP:
                fist.unpunch()

        allsprites.update()

        # Draw everything
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pg.display.flip()

    # Game over
    pg.quit()


if __name__ == "__main__":
    main()
