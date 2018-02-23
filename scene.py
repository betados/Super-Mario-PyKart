import math
import pygame
from OpenGL.GL import *



class Scene(object):
    def __init__(self):
        self.trees = self.getTexture('images/arboles.png')
        self.mountains = self.getTexture('images/fondo.png')
        self.circuit = self.getTexture('images/marioCircuit4.png')

    def draw(self):
        self.loadScene(self.circuit)
        self.placeScene()
        self.loadScene(self.mountains)
        self.placeSceneOctogono(250, 8, 10)
        self.loadScene(self.trees)
        self.placeSceneOctogono(50, 4, 2.5)

    def getTexture(self, img):
        img = pygame.image.load(img)
        return pygame.image.tostring(img, "RGBA", True), img.get_width(), img.get_height()

    def loadScene(self, texture):
        bgImgGL = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, bgImgGL)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, texture[1], texture[2], 0, GL_RGBA, GL_UNSIGNED_BYTE, texture[0])
        glEnable(GL_TEXTURE_2D)

    def placeScene(self):
        l = 5
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(-l, -l, 0)
        glTexCoord2f(0, 1)
        glVertex3f(-l, l, 0)
        glTexCoord2f(1, 1)
        glVertex3f(l, l, 0)
        glTexCoord2f(1, 0)
        glVertex3f(l, -l, 0)
        glEnd()

    def placeSceneOctogono(self, radius, sides, h):
        alpha = math.pi / (sides / 2)

        points = [(radius * math.cos(alpha * i), radius * math.sin(alpha * i)) for i in range(1, sides + 1)]

        for i in range(sides):
            glBegin(GL_QUADS)
            glTexCoord2f(0, 0)
            glVertex3f(points[i][0], points[i][1], 0)
            glTexCoord2f(0, 1)
            glVertex3f(points[i][0], points[i][1], h)
            glTexCoord2f(1, 1)
            glVertex3f(points[i - 1][0], points[i - 1][1], h)
            glTexCoord2f(1, 0)
            glVertex3f(points[i - 1][0], points[i - 1][1], 0)
            glEnd()
