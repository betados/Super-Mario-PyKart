import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from player import Player
from scene import Scene


# def Cube():
#     verticies = (
#         (1, -1, -1),
#         (1, 1, -1),
#         (-1, 1, -1),
#         (-1, -1, -1),
#         (1, -1, 1),
#         (1, 1, 1),
#         (-1, -1, 1),
#         (-1, 1, 1)
#     )
#
#     edges = (
#         (0, 1),
#         (0, 3),
#         (0, 4),
#         (2, 1),
#         (2, 3),
#         (2, 7),
#         (6, 3),
#         (6, 4),
#         (6, 7),
#         (5, 1),
#         (5, 4),
#         (5, 7)
#     )
#
#     glBegin(GL_LINES)
#     for edge in edges:
#         for vertex in edge:
#             glVertex3fv(verticies[vertex])
#     glEnd()


def draw(player, display, scene, t, screen):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_BLEND)

    glViewport(0, 0, display[0], display[1])
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, float(display[0]) / float(display[1]), 0.1, 300.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    gluLookAt(*player.actualize(t, screen))
    scene.draw()
    player.draw()

    pygame.display.flip()


def main():
    pygame.init()
    display = (1200, 800)
    screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL | pygame.OPENGLBLIT)
    # screen = pygame.display.set_mode(display,  pygame.OPENGLBLIT)
    clock = pygame.time.Clock()
    scene = Scene()

    player = Player([0, 0, 0.15])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                # FIXME inverted temporarily, fix inside
                if event.key in [pygame.K_LEFT, pygame.K_a]:
                    player.turn = 'right'
                if event.key in [pygame.K_RIGHT, pygame.K_d]:
                    player.turn = 'left'

                if event.key in [pygame.K_UP, pygame.K_w]:
                    player.gas(True)
                if event.key in [pygame.K_DOWN, pygame.K_s]:
                    player.reverse()

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

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
                    player.turn = 'none'

        t = clock.tick(50)
        draw(player, display, scene, t, screen)


if __name__ == "__main__":
    main()
