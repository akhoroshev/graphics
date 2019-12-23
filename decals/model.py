import time
from collections import namedtuple
from math import pi
from typing import List, Tuple

import noise as noise
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

Point2 = namedtuple('Point2', ['x', 'y'])
Point3 = namedtuple('Point3', ['x', 'y', 'z'])


class Cube:
    def __init__(self, basis: Tuple[Point3, Point3, Point3], center: Point3, size: float):
        self.size = size
        self.center = center
        self.basis = [*basis]

    def get_basis(self):
        return [np.array(self.basis[0], dtype=float) / np.linalg.norm(self.basis[0]) * self.size,
                np.array(self.basis[1], dtype=float) / np.linalg.norm(self.basis[1]) * self.size,
                np.array(self.basis[2], dtype=float) / np.linalg.norm(self.basis[2]) * self.size]

    def get_center(self):
        return np.array(self.center, dtype=float)

    def draw(self):
        pt = self.get_center()
        ox, oy, oz = self.get_basis()

        # glBegin(GL_LINES)
        # glColor3f(1.0, 0, 0)
        # glVertex3f(*pt)
        # glVertex3f(*(pt + ox))
        # glEnd()
        #
        # glBegin(GL_LINES)
        # glColor3f(0, 1.0, 0)
        # glVertex3f(*pt)
        # glVertex3f(*(pt + oy))
        # glEnd()

        glBegin(GL_LINES)
        glColor3f(0, 0, 1.0)
        glVertex3f(*pt)
        glVertex3f(*(pt + oz))
        glEnd()


class ModelView:
    def __init__(self, vertices: List[float], vertex_format, vertex_size,
                 vertex_shader="shaders/vertex.vert",
                 fragment_shader="shaders/fragment.frag",
                 width=800,
                 height=800, fov=45,
                 z_near=0.1, z_far=50,
                 win_name='HW3'):
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(width, height)
        glutCreateWindow(win_name)
        self.tex_id = glGenTextures(1)
        self.width = width
        self.height = height
        self.program = glCreateProgram()
        self.vertices = vertices
        self.vertex_format = vertex_format
        self.vertex_size = vertex_size
        self.fov = fov
        self.z_near = z_near
        self.z_far = z_far
        self.vertices = vertices
        self.prev_mouse = Point2(None, None)
        self.win_name = win_name
        self.vertex_shader = ModelView.__load_shader(GL_VERTEX_SHADER, vertex_shader)
        self.fragment_shader = ModelView.__load_shader(GL_FRAGMENT_SHADER, fragment_shader)
        self.cube = Cube((Point3(1, 0, 0), Point3(0, 1, 0), Point3(0, 0, 1)), Point3(-2.5, 8, 0), 1.5)

    def show(self):
        self.__fill_texture()

        glAttachShader(self.program, self.vertex_shader)
        glAttachShader(self.program, self.fragment_shader)

        glLinkProgram(self.program)
        glUseProgram(self.program)

        glEnable(GL_DEPTH_TEST)

        glInterleavedArrays(eval('GL_' + self.vertex_format), 0, (GLfloat * len(self.vertices))(*self.vertices))

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
        self.width = width
        self.height = height
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glViewport(0, 0, width, height)
        gluPerspective(self.fov, width / height, self.z_near, self.z_far)
        gluLookAt(*(0, 0, 20), *(0, 0, 0), *(0, 1, 0))

    def __draw_event(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glColor3f(0.5, 0.3, 0.1)
        glDrawArrays(GL_TRIANGLES, 0, int(len(self.vertices) / self.vertex_size))
        self.cube.draw()
        glutSwapBuffers()

    def __fill_texture(self):
        size = 256
        glBindTexture(GL_TEXTURE_2D, self.tex_id)
        noise_texture = [
            noise.pnoise2(1 / size * i, 1 / size * j, octaves=10, repeatx=1, repeaty=1)
            for i in range(size) for j in range(size)
        ]
        base = min(noise_texture)
        factor = max(noise_texture) - base
        noise_texture = [(x - base) / factor for x in noise_texture]
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RED, size, size,
                     0, GL_RED, GL_FLOAT, noise_texture)
        glGenerateMipmap(GL_TEXTURE_2D)

    def __mouse_button_event(self, button, state, x, y):
        if state != GLUT_DOWN:
            return

        if button == GLUT_RIGHT_BUTTON:
            z = glReadPixels(x, self.height - y, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)
            pt = gluUnProject(x, self.height - y, z)
            self.cube.center = pt
            glUniform3f(glGetUniformLocation(self.program, "pt"), *self.cube.get_center())
            glUniform3f(glGetUniformLocation(self.program, "ox"), *self.cube.get_basis()[0])
            glUniform3f(glGetUniformLocation(self.program, "oy"), *self.cube.get_basis()[1])
            glUniform3f(glGetUniformLocation(self.program, "oz"), *self.cube.get_basis()[2])

        if button == GLUT_LEFT_BUTTON or button == GLUT_RIGHT_BUTTON:
            self.prev_mouse = Point2(x, y)

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

            top_down_rotation = np.dot(glGetDoublev(GL_MODELVIEW_MATRIX), (1, 0, 0, 0))[:-1]
            glRotate(0.2 * delta_y, *top_down_rotation)
            glutPostRedisplay()

            self.prev_mouse = Point2(x, y)

    @staticmethod
    def __clock():
        millis = int(round(time.time() * 1000))
        return millis

    def __refresh_world(self):
        cycle = 4000  # in ms
        progress = (self.__clock() % cycle) / cycle * 2 * pi
        glutPostRedisplay()
