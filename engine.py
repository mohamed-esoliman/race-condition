import pygame
from drawable import Drawable
from mobile import Mobile, Player
from os.path import join
from constants import *
from vector import vec, pyVec, rectAdd


class GameEngine(object):

    def __init__(self):
        self.kirby = Player((0, 0), "kirby.png", (0, 1))
        self.background = Drawable((0, 0), "background.png")
        self.waterLily = Drawable((250, 100), "water-lily.png")
        self.rose = Drawable((100, 100), "rose.png", pygame.Rect(4 * 34, 0, 34, 62))
        self.carrot = Drawable((150, 100), "plants.png", pygame.Rect(1, 650, 62, 78))
        self.subRainbow = Drawable(
            (150, 50), "rainbow.png", pygame.Rect(50, 50, 50, 50)
        )
        self.kirbySpeed = 100
        self.dragged = None

        self.mouseOffset = vec(0, 0)

        # pygame.mouse.set_visible(False)

    def draw(self, drawSurface):
        drawSurface.fill((255, 255, 255))

        self.background.draw(drawSurface)
        self.waterLily.draw(drawSurface)
        self.rose.draw(drawSurface)
        self.carrot.draw(drawSurface)
        self.subRainbow.draw(drawSurface)

        self.kirby.draw(drawSurface)

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            position = vec(*event.pos) // SCALE
            position += Drawable.CAMERA_OFFSET

            if self.kirby.getCollisionRect().collidepoint(position):
                self.dragged = self.kirby
                self.mouseOffset = self.kirby.getPosition() - position

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragged = None
        elif event.type == pygame.MOUSEMOTION:
            position = vec(*event.pos) // SCALE
            position += Drawable.CAMERA_OFFSET
            if self.dragged is not None:
                self.dragged.position = position + self.mouseOffset

        # elif event.type == pygame.MOUSEMOTION:
        #     position = vec(*event.pos) // SCALE
        #     if self.subRainbow.getCollisionRect().collidepoint(position):
        #         self.drawRainbow = self.hoverRainbow
        #     else:
        #         self.drawRainbow = self.subRainbow

        # elif event.type == pygame.MOUSEMOTION:
        #     position = vec(*event.pos) // SCALE
        #     self.carrot.position = position

        self.kirby.handleEvent(event)

    def update(self, seconds):
        self.kirby.update(seconds)

        # prevent leaving window
        if self.kirby.getPosition()[0] < 0:
            self.kirby.velocity[0] = 0
            self.kirby.position[0] = 0
        elif self.kirby.getPosition()[0] > WORLD_SIZE[0] - self.kirby.getWidth():
            self.kirby.velocity[0] = 0
            self.kirby.position[0] = WORLD_SIZE[0] - self.kirby.getWidth()

        if self.kirby.getPosition()[1] < 0:
            self.kirby.velocity[1] = 0
            self.kirby.position[1] = 0
        elif self.kirby.getPosition()[1] > WORLD_SIZE[1] - self.kirby.getHeight():
            self.kirby.velocity[1] = 0
            self.kirby.position[1] = WORLD_SIZE[1] - self.kirby.getHeight()

        collision = self.kirby.getCollisionRect().clip(
            self.subRainbow.getCollisionRect()
        )

        if collision.width != 0 and collision.height != 0:
            if collision.width < collision.height:

                self.kirby.velocity[0] = 0

                if self.kirby.getPosition()[0] < self.subRainbow.getPosition()[0]:
                    # push up
                    self.kirby.position[0] -= collision.width
                else:
                    # push down
                    self.kirby.position[0] += collision.width
            else:
                self.kirby.velocity[1] = 0
                if self.kirby.getPosition()[1] < self.subRainbow.getPosition()[1]:
                    # push left
                    self.kirby.position[1] -= collision.height
                else:
                    # push right
                    self.kirby.position[1] += collision.height

        Drawable.CAMERA_OFFSET = (
            self.kirby.getPosition() + self.kirby.getSize() / 2 - RESOLUTION // 2
        )

        for i in range(2):
            Drawable.CAMERA_OFFSET[i] = max(
                0, min(Drawable.CAMERA_OFFSET[i], WORLD_SIZE[i] - RESOLUTION[i])
            )
