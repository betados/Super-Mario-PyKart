import math


class Player(object):
    def __init__(self, eye):
        self.eye = eye
        self.lookat = [40, 40, -1]
        self.axis = [0, 0, 1]
        self.speed = 0.0
        self.acel = 0.000005
        self.throttle = False
        self.turnD = {'right': 1, 'left': -1, 'none': 0}
        self.where = 0

    def gas(self, throttle):
        self.throttle = throttle

    def reverse(self):
        for i in [0, 1]:
            self.eye[i] -= self.getVector()[i]
            self.lookat[i] -= self.getVector()[i]

    def turn(self, where):
        self.where = self.turnD[where]

    # DEBUGGING FUNCTIONS
    def right(self):
        for i in [0, 1]:
            self.eye[i] += self.getNormalVector()[i]
            self.lookat[i] += self.getNormalVector()[i]

    def left(self):
        for i in [0, 1]:
            self.eye[i] -= self.getNormalVector()[i]
            self.lookat[i] -= self.getNormalVector()[i]

    def up(self):
        self.eye[2] += 0.01

    def down(self):
        self.eye[2] -= 0.01

    def actualize(self, t):
        # acelerador
        self.speed += self.throttle * self.acel * t \
            - 1*(self.speed * self.speed)  # rozamiento viscoso
        for i in [0, 1]:
            self.eye[i] += self.getVector()[i] * self.speed * t
            # self.lookat[i] += self.getVector()[i] * 40

        #  giro
        for i in [0, 1]:
            self.lookat[i] = self.eye[i] + self.getVector()[i] * 40 + self.where * self.getNormalVector()[i] * 0.5

        return self.eye + self.lookat + self.axis

    def getVector(self):
        v = self.getUnitVector(self.eye, self.lookat)
        return v[0], v[1]

    def getNormalVector(self):
        """ 90 grados en sentido horario """
        v = self.getVector()
        vn = v[1], -v[0]
        return vn[0], vn[1]

    def getUnitVector(self, i, j):
        vector = [j[0] - i[0], j[1] - i[1]]
        modulo = math.sqrt(math.pow(vector[0], 2) + math.pow(vector[1], 2))
        if modulo != 0:
            return [vector[0] / modulo, vector[1] / modulo]
        else:
            return [0, 0]

