import math
from drawing import Drawing
from OpenGL.GL import *
from vector_2d import *


class Player(object):
    def __init__(self, eye):
        self.eye = Vector(*eye[:2])
        self.eye_z = eye[2]
        self.axis = (0, 0, 1)
        self.speed = 0.0
        self.accel = 0.0000005
        self.throttle = False
        self.turnD = {'right': -1,
                      'left': 1,
                      'none': 0,
                      }
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
        self.eye += self.pos.normal()
        self.lookat += self.pos.normal()

    def left(self):
        self.eye -= self.pos.normal()
        self.lookat -= self.pos.normal()

    def up(self):
        self.eye_z += 0.01

    def down(self):
        self.eye_z -= 0.01

    def draw(self):
        Drawing.loadScene(self.texture[self.turn])
        height = 0.05
        a = height * 230
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
        # accelerator
        self.speed += self.throttle * self.accel * t - \
                      4 * self.speed ** 2  # viscous friction
        self.eye += self.pos * self.speed * t
        self.lookat = self.pos * self.prof + self.eye

        # turn
        self.lookat = self.eye + self.pos * self.prof + self.pos.normal() * self.turnD[self.turn] * self.speed * 1560
        self.pos = (self.lookat - self.eye).unit()

        return self.eye.get_comps() + (self.eye_z,) + self.lookat.get_comps() + (self.lookat_z,) + self.axis
