import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

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


def Cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()


def loadScene(bgImg):
    img = pygame.image.load(bgImg)
    textureData = pygame.image.tostring(img, "RGB", 1)
    width = img.get_width()
    height = img.get_height()
    bgImgGL = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, bgImgGL)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, textureData)
    glEnable(GL_TEXTURE_2D)


def placeScene():
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(-40, -40, 0)
    glTexCoord2f(0, 1)
    glVertex3f(-40, 40, 0)
    glTexCoord2f(1, 1)
    glVertex3f(40, 40, 0)
    glTexCoord2f(1, 0)
    glVertex3f(40, -40, 0)
    glEnd()


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    gluLookAt(0, # eyeX,
              0, # eyeY,
              0.5, # eyeZ,
              40, # centerX,
              20, # centerY,
              0, # centerZ,
              0, # upX,
              0, # upY,
              1 # upZ)
              )

    loadScene('MapMushroomCup1.png')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                glTranslatef(-0.2, 0, 0)
            if event.key == pygame.K_RIGHT:
                glTranslatef(0.2, 0, 0)

            if event.key == pygame.K_UP:
                glTranslatef(0, 0.2, 0)
            if event.key == pygame.K_DOWN:
                glTranslatef(0, -0.2, 0)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                glTranslatef(0, 0, 1.0)

            if event.button == 5:
                glTranslatef(0, 0, -1.0)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        placeScene()
        Cube()

        pygame.display.flip()
        pygame.time.wait(10)


main()
