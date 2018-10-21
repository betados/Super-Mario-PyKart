import math
from drawing import Drawing
from OpenGL.GL import *
from vector_2d import *


class Player(object):
    def __init__(self, eye):
        self.eye = Vector(*eye[:2])
        self.eye_z = eye[2]
        self.axis = [0, 0, 1]
        self.speed = 0.0
        self.acel = 0.0000005
        self.throttle = False
        self.turnD = {'right': -1, 'left': 1, 'none': 0}
        self.texture = {'right': Drawing.getTexture('images/yoshiRight.png'),
                        'left': Drawing.getTexture('images/yoshiLeft.png'),
                        'none': Drawing.getTexture('images/yoshiStraight.png'),
                        }
        self.turn = 'none'

        self.pos = Vector(1, 0)
        self.prof = 60
        self.lookat = self.pos * self.prof + self.eye
        self.lookat_z = -1

    def gas(self, throttle):
        self.throttle = throttle

    def reverse(self):
        self.eye -= self.pos
        self.lookat -= self.pos

    # DEBUGGING FUNCTIONS
    def right(self):
        for i in [0, 1]:
            self.eye[i] += self.normalVector[i]
            self.lookat[i] += self.normalVector[i]

    def left(self):
        for i in [0, 1]:
            self.eye[i] -= self.normalVector[i]
            self.lookat[i] -= self.normalVector[i]

    def up(self):
        self.eye[2] += 0.01

    def down(self):
        self.eye[2] -= 0.01

    def draw(self):
        Drawing.loadScene(self.texture[self.turn])
        height = 0.05
        a = height * 230
        print(a)
        p = self.pos / 3 + self.eye
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(*p(), 0)
        glTexCoord2f(0, 1)
        glVertex3f(*p(), height)
        glTexCoord2f(1, 1)
        glVertex3f(*(p + self.pos.normal() / a), height)
        glTexCoord2f(1, 0)
        glVertex3f(*(p + self.pos.normal() / a), 0)
        glEnd()

    def actualize(self, t):
        # acelerador
        self.speed += self.throttle * self.acel * t - 4 * self.speed ** 2  # rozamiento viscoso
        self.eye += self.pos * self.speed * t
        self.lookat = self.pos * self.prof + self.eye

        # FIXME que no gire si no hay velocidad
        #  giro
        self.lookat = self.eye + self.pos * self.prof + self.pos.normal() * self.turnD[self.turn] * 1.9
        self.setPos()

        return self.eye.get_comps() + (self.eye_z,) + self.lookat.get_comps() + (self.lookat_z,) + tuple(self.axis)

    def setPos(self):
        self.pos = (self.lookat - self.eye).unit()
    #
    # @property
    # def normalVector(self):
    #     """ 90 grados en sentido horario """
    #     v = self.pos
    #     vn = v[1], -v[0]
    #     return vn[0], vn[1]
    #
    # @staticmethod
    # def getUnitVector(i, j):
    #     vector = [j[0] - i[0], j[1] - i[1]]
    #     modulo = math.sqrt(math.pow(vector[0], 2) + math.pow(vector[1], 2))
    #     if modulo != 0:
    #         return [vector[0] / modulo, vector[1] / modulo]
    #     else:
    #         return [0, 0]
