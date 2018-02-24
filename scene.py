import math
from OpenGL.GL import *
from drawing import Drawing


class Scene(object):
    def __init__(self):
        self.trees = Drawing.getTexture('images/arboles.png')
        self.mountains = Drawing.getTexture('images/fondo.png')
        self.circuit = Drawing.getTexture('images/marioCircuit4.png')

        glBindTexture(GL_TEXTURE_2D, glGenTextures(1))
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glEnable(GL_TEXTURE_2D)

    def draw(self):
        Drawing.loadScene(self.circuit)
        self.placeScene()
        Drawing.loadScene(self.mountains)
        self.placeSceneArround(250, 8, 10)
        Drawing.loadScene(self.trees)
        self.placeSceneArround(18, 5, 0.8)


    def placeScene(self):
        side = 5
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(-side, -side, 0)
        glTexCoord2f(0, 1)
        glVertex3f(-side, side, 0)
        glTexCoord2f(1, 1)
        glVertex3f(side, side, 0)
        glTexCoord2f(1, 0)
        glVertex3f(side, -side, 0)
        glEnd()

    def placeSceneArround(self, radius, sides, h):
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


# ALSA lib pcm.c:7963:(snd_pcm_recover) underrun occurred