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


def draw(player, display):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glViewport(0, 0, display[0], display[1])
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, float(display[0]) / float(display[1]), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    gluLookAt(*player.getAll())
    placeScene()
    Cube()

    glBegin(GL_TRIANGLES)
    glVertex3f(0, 0, 0)
    glVertex3f(1, 0, 0)
    glVertex3f(0, 0, 1)
    glEnd()

    pygame.display.flip()


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    clock = pygame.time.Clock()

    player = Player([0, 0, 1], [40, 40, -1])
    loadScene('MapMushroomCup1.png')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_LEFT, pygame.K_a]:
                player.left()
            if event.key in [pygame.K_RIGHT, pygame.K_d]:
                player.right()

            if event.key in [pygame.K_UP, pygame.K_w]:
                player.gas()
            if event.key in [pygame.K_DOWN, pygame.K_s]:
                player.reverse()

            if event.key == pygame.K_u:
                player.up()
            if event.key == pygame.K_j:
                player.down()




        draw(player, display)
        clock.tick(60)

if __name__ == "__main__":
    main()
