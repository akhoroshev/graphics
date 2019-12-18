import time
from collections import namedtuple
from math import cos, pi
from typing import List

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class ModelView:
    Point = namedtuple('Point', ['x', 'y'])

    def __init__(self, vertices: List[float],
                 vertex_shader="shaders/vertex.vert",
                 fragment_shader="shaders/fragment.frag",
                 width=800,
                 height=800, fov=45,
                 z_near=0.1, z_far=50,
                 win_name='HW2'):
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(width, height)
        glutCreateWindow(win_name)
        self.program = glCreateProgram()
        self.vertices = vertices
        self.fov = fov
        self.z_near = z_near
        self.z_far = z_far
        self.vertices = vertices
        self.prev_mouse = ModelView.Point(None, None)
        self.win_name = win_name
        self.vertex_shader = vertex_shader
        self.fragment_shader = fragment_shader

    def show(self):
        glAttachShader(self.program, ModelView.__load_shader(GL_FRAGMENT_SHADER, self.fragment_shader))
        glAttachShader(self.program, ModelView.__load_shader(GL_VERTEX_SHADER, self.vertex_shader))
        glLinkProgram(self.program)
        glUseProgram(self.program)

        glEnable(GL_DEPTH_TEST)

        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, self.vertices)

        glutDisplayFunc(self.__draw_event)
        glutReshapeFunc(self.__reshape_event)
        glutMouseFunc(self.__mouse_button_event)
        glutMotionFunc(self.__mouse_move_event)
        glutIdleFunc(self.__refresh_world)
        glutMainLoop()

    @staticmethod
    def __load_shader(shader_type, path):
        with open(path) as file:
            shader = glCreateShader(shader_type)
            glShaderSource(shader, file.read())
            glCompileShader(shader)
            return shader

    def __reshape_event(self, width, height):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glViewport(0, 0, width, height)
        gluPerspective(self.fov, width / height, self.z_near, self.z_far)
        gluLookAt(*(0.5, 0.5, 0.5), *(0, 0, 0), *(0, 1, 0))

    def __draw_event(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glDrawArrays(GL_TRIANGLES, 0, int(len(self.vertices) / 3))
        glutSwapBuffers()

    def __mouse_button_event(self, button, state, x, y):
        if state != GLUT_DOWN:
            return

        if button == GLUT_LEFT_BUTTON or button == GLUT_RIGHT_BUTTON:
            self.prev_mouse = ModelView.Point(x, y)

        # wheel
        if button == 3 or button == 4:
            scale = 1.1
            value = scale if button == 3 else 1 / scale
            glMatrixMode(GL_MODELVIEW)
            glScale(value, value, value)
            glutPostRedisplay()

    def __mouse_move_event(self, x, y):
        if self.prev_mouse != (None, None):
            delta_x = x - self.prev_mouse.x
            delta_y = y - self.prev_mouse.y

            glMatrixMode(GL_MODELVIEW)
            glRotate(0.2 * delta_x, *(0, 1, 0))
            glRotate(0.2 * delta_y, *(1, 0, 0))
            glutPostRedisplay()

            self.prev_mouse = ModelView.Point(x, y)

    @staticmethod
    def __clock():
        millis = int(round(time.time() * 1000))
        return millis

    def __refresh_world(self):
        cycle = 4000  # in ms
        progress = (self.__clock() % cycle) / cycle * 2 * pi

        glUniform1f(glGetUniformLocation(self.program, "noise"), cos(progress))
        glutPostRedisplay()

