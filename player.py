import math

class Player(object):
    def __init__(self, eye, lookat):
        self.eye = eye
        self.lookat = lookat
        self.axis = [0, 0, 1]

    # @property
    # def eye(self):
    #     return self.__eye

    def gas(self):
        for i in [0, 1]:
            self.eye[i] += self.getVector()[i]
            self.lookat[i] += self.getVector()[i]

    def reverse(self):
        for i in [0, 1]:
            self.eye[i] -= self.getVector()[i]
            self.lookat[i] -= self.getVector()[i]

    def up(self):
        self.eye[2] += 0.01

    def down(self):
        self.eye[2] -= 0.01

    def getAll(self):
        return self.eye + self.lookat + self.axis

    def getVector(self):
        v = self.getUnitVector(self.eye, self.lookat)
        return v[0]/5, v[1]/5

    def getUnitVector(self, i, j):
        vector = [j[0] - i[0], j[1] - i[1]]
        modulo = math.sqrt(math.pow(vector[0], 2) + math.pow(vector[1], 2))
        if modulo != 0:
            return [vector[0] / modulo, vector[1] / modulo]
        else:
            return [0, 0]

