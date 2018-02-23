import math

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from player import Player


def Cube():
    verticies = (
        (1, -1, -1),
        (1, 1, -1),
        (-1, 1, -1),
        (-1, -1, -1),
        (1, -1, 1),
        (1, 1, 1),
        (-1, -1, 1),
        (-1, 1, 1)
    )

    edges = (
        (0, 1),
        (0, 3),
        (0, 4),
        (2, 1),
        (2, 3),
        (2, 7),
        (6, 3),
        (6, 4),
        (6, 7),
        (5, 1),
        (5, 4),
        (5, 7)
    )

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()


def loadScene(bgImg):
    img = pygame.image.load(bgImg)
    textureData = pygame.image.tostring(img, "RGBA", True)
    width = img.get_width()
    height = img.get_height()
    bgImgGL = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, bgImgGL)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
    glEnable(GL_TEXTURE_2D)

# def loadScene3D(bgImg):
#     img = pygame.image.load(bgImg)
#     textureData = pygame.image.tostring(img, "RGB", True)
#     width = img.get_width()
#     height = img.get_height()
#     bgImgGL = glGenTextures(1)
#     glBindTexture(GL_TEXTURE_2D, bgImgGL)
#     glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
#     glTexImage3D(GL_TEXTURE_3D, 0, GL_RGB, width, height, 2, 0, GL_RGB, GL_UNSIGNED_BYTE, textureData)
#     glEnable(GL_TEXTURE_3D)


def placeScene():
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


def placeSceneOctogono(radius, sides, h):
    alpha = math.pi/(sides/2)

    points = [(radius * math.cos(alpha * i), radius * math.sin(alpha * i)) for i in range(1, sides+1)]

    for i in range(sides):
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(points[i][0], points[i][1], 0)
        glTexCoord2f(0, 1)
        glVertex3f(points[i][0], points[i][1], h)
        glTexCoord2f(1, 1)
        glVertex3f(points[i-1][0], points[i-1][1], h)
        glTexCoord2f(1, 0)
        glVertex3f(points[i-1][0], points[i-1][1], 0)
        glEnd()


def draw(player, display, t):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_BLEND)

    glViewport(0, 0, display[0], display[1])
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, float(display[0]) / float(display[1]), 0.1, 300.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    gluLookAt(*player.actualize(t))
    loadScene('images/marioCircuit4.png')
    placeScene()
    loadScene('images/fondo.png')
    placeSceneOctogono(250, 8, 10)
    loadScene('images/arboles.png')
    placeSceneOctogono(50, 4, 2.5)

    pygame.display.flip()


def main():
    pygame.init()
    display = (1200, 800)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    clock = pygame.time.Clock()

    player = Player([0, 0, 1])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_LEFT, pygame.K_a]:
                player.turn('left')
            if event.key in [pygame.K_RIGHT, pygame.K_d]:
                player.turn('right')

            if event.key in [pygame.K_UP, pygame.K_w]:
                player.gas(True)
            if event.key in [pygame.K_DOWN, pygame.K_s]:
                player.reverse()


            # DEBUGGING KEYS
            if event.key == pygame.K_j:
                player.left()
            if event.key == pygame.K_l:
                player.right()
            if event.key == pygame.K_i:
                player.up()
            if event.key == pygame.K_k:
                player.down()

        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_UP, pygame.K_w]:
                player.gas(False)
            if event.key in [pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d]:
                player.turn('none')


        t = clock.tick(100)
        draw(player, display, t)


if __name__ == "__main__":
    main()
