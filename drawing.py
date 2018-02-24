import pygame
from OpenGL.GL import *


class Drawing(object):
    @staticmethod
    def getTexture(img):
        img = pygame.image.load(img)
        return pygame.image.tostring(img, "RGBA", True), img.get_width(), img.get_height()

    @staticmethod
    def loadScene(texture):
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, texture[1], texture[2], 0, GL_RGBA, GL_UNSIGNED_BYTE, texture[0])
