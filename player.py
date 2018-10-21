import math
from drawing import Drawing
from OpenGL.GL import *
from vector_2d import *


class Player(object):
    def __init__(self, eye):
        self.eye = eye
        self.axis = [0, 0, 1]
        self.speed = 0.0
        self.acel = 0.0000005
        self.throttle = False
        self.turnD = {'right': 1, 'left': -1, 'none': 0}
        self.texture = {'right': Drawing.getTexture('images/yoshiRight.png'),
                        'left': Drawing.getTexture('images/yoshiLeft.png'),
                        'none': Drawing.getTexture('images/yoshiStraight.png')}
        self.turn = 'none'

        self.vector = 1, 0
        self.prof = 60
        self.lookat = [v * self.prof + self.eye[i] for i, v in enumerate(self.vector)] + [-1]

    def gas(self, throttle):
        self.throttle = throttle

    def reverse(self):
        for i in [0, 1]:
            self.eye[i] -= self.vector[i]
            self.lookat[i] -= self.vector[i]

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
        p = [v / 3 + self.eye[i] for i, v in enumerate(self.vector)]
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(p[0], p[1], 0)
        glTexCoord2f(0, 1)
        glVertex3f(p[0], p[1], height)
        glTexCoord2f(1, 1)
        glVertex3f(p[0] + self.normalVector[0] / a, p[1] + self.normalVector[1] / a, height)
        glTexCoord2f(1, 0)
        glVertex3f(p[0] + self.normalVector[0] / a, p[1] + self.normalVector[1] / a, 0)
        glEnd()

    def actualize(self, t, screen):
        # acelerador
        self.speed += self.throttle * self.acel * t \
                      - 4 * (self.speed * self.speed)  # rozamiento viscoso
        # self.eye = [self.eye[i] + v * self.speed * t for i, v in enumerate(self.vector)] + [1]
        for i in [0, 1]:
            self.eye[i] += self.vector[i] * self.speed * t
        self.lookat = [v * self.prof + self.eye[i] for i, v in enumerate(self.vector)] + [-1]

        # FIXME que no gire si no hay velocidad
        #  giro
        self.lookat = [self.eye[i] + v * self.prof + self.normalVector[i] * self.turnD[self.turn] * 1.9
                       for i, v in enumerate(self.vector)] + [-1]
        self.setVector()

        return self.eye + self.lookat + self.axis

    def setVector(self):
        self.vector = self.getUnitVector(self.eye, self.lookat)

    @property
    def normalVector(self):
        """ 90 grados en sentido horario """
        v = self.vector
        vn = v[1], -v[0]
        return vn[0], vn[1]

    @staticmethod
    def getUnitVector(i, j):
        vector = [j[0] - i[0], j[1] - i[1]]
        modulo = math.sqrt(math.pow(vector[0], 2) + math.pow(vector[1], 2))
        if modulo != 0:
            return [vector[0] / modulo, vector[1] / modulo]
        else:
            return [0, 0]
