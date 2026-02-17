from pygame import image, Surface, SRCALPHA
from os.path import join
from vector import vec, pyVec, rectAdd

from spriteManager import SpriteManager


class Drawable(object):

    CAMERA_OFFSET = vec(0, 0)

    def __init__(
        self,
        position=vec(0, 0),
        fileName="",
        offset=None,
    ):
        if fileName != "":

            sm = SpriteManager.getInstance()
            self.image = sm.getSprite(fileName, offset)
            # self.image = image.load(fileName)

            # if transparency:
            #     if offset is None:
            #         self.image = self.image.convert_alpha()
            #     else:
            #         surf = Surface(offset.size, SRCALPHA, 32)
            #         surf.blit(self.image, (0,0), offset)
            #         self.image = surf
            # else:
            #     if offset is not None:
            #         surf = Surface(offset.size)
            #         surf.blit(self.image, (0,0), offset)
            #         self.image = surf

            # if colorkey:
            #     self.image.set_colorkey(self.image.get_at((0,0)))

        self.position = vec(*position)

    def draw(self, drawSurface):
        drawSurface.blit(self.image, pyVec(self.position - Drawable.CAMERA_OFFSET))

    def getSize(self):
        return vec(*self.image.get_size())

    def getWidth(self):
        return self.getSize()[0]

    def getHeight(self):
        return self.getSize()[1]

    def getPosition(self):
        return self.position

    def setPosition(self, newPosition):
        self.position = vec(*newPosition)

    def getCollisionRect(self):
        return rectAdd(self.position, self.image.get_rect())

    def handleEvent(self, event):
        pass

    def update(self, seconds):
        pass
