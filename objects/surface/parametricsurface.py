import math

import glfw
import numpy as np

from libs.buffer import *
from libs.gobject import GObject
import libs.transform as T
from libs.shader import Shader
from time import time


# import multiprocessing


class ParametricSurface(GObject):
    def __init__(self,
                 equation_parser,
                 slope_func,
                 colors: np.array = None):
        super(ParametricSurface, self).__init__('./objects/surface/phong.vert', './objects/surface/phong.frag')
        self.equation_parser = equation_parser
        self.slope_func = slope_func
        self.pos_min = -25
        self.pos_max = 25
        self.interval = 0.1
        self.size = int((self.pos_max - self.pos_min) / self.interval)
        self.z_min = 1e15
        self.z_max = -1e15
        self.grid = np.array([], dtype=np.float32)
        self.vertices = []
        self.indices = []
        self.colors = colors

        self.balls = []

    def add_ball(self, ball):
        self.balls += [ball]

    # noinspection PyPep8Naming
    def _generate_vertices(self):
        del self.grid

        t = time()

        self.grid = []
        x = self.pos_min
        while x <= self.pos_max:
            y = self.pos_min
            while y <= self.pos_max:
                self.grid += [[x, y]]
                y += self.interval
            x += self.interval
        self.grid = np.array(self.grid, dtype=np.float32)

        vertices = []
        normals = []
        for i in range(len(self.grid)):
            slope = self.slope_func([self.grid[i][0], self.grid[i][1]])
            planeVectorX = [1., 0., slope[0]]
            planeVectorY = [0., 1., slope[1]]
            vertices += [
                [
                    # x,y,z coor
                    self.grid[i][0],
                    self.grid[i][1],
                    self._f(self.grid[i][0], self.grid[i][1]),
                ]
            ]
            normals += [
                [
                    (planeVectorX[1] * planeVectorY[2]) - (planeVectorX[2] * planeVectorY[1]),
                    (planeVectorX[2] * planeVectorY[0]) - (planeVectorX[0] * planeVectorY[2]),
                    (planeVectorX[0] * planeVectorY[1]) - (planeVectorX[1] * planeVectorY[0])
                ]
            ]

        print(f"run time {time() - t}")
        vertices = np.array(vertices, dtype=np.float32)
        z_coor = vertices[:, 2]
        self.z_max = z_coor.max()
        self.z_min = z_coor.min()
        self.normals = np.array(normals, dtype=np.float32)
        return vertices

    def _f(self, x, y):
        z = self.equation_parser.evaluate(x, y)
        return z

    def _generate_indices(self):
        indices = []
        for r in range(self.size - 1):
            if r > 0:
                indices += [r * self.size]
            for c in range(self.size):
                indices += [r * self.size + c]
                indices += [(r + 1) * self.size + c]
            if r < self.size - 2:
                indices += [(r + 1) * self.size + self.size - 1]

        # for x in range(self.size):
        #     for y in range(self.size - 1):
        #         indices += [x * self.size + y]
        #         indices += [x * self.size + y + 1]
        #
        # for y in range(self.size):
        #     for x in range(self.size - 1):
        #         indices += [x * self.size + y]
        #         indices += [(x + 1) * self.size + y]

        return np.array(indices, dtype=np.uint32)

    def setup(self):
        self.vertices = self._generate_vertices()
        self.indices = self._generate_indices()
        # self.normals = generate_normals(self.vertices, self.indices)
        self.vao = VAO(self.shader.identifier())
        vbo_vertices = VBO("vertices", self.vertices)
        vbo_normals = VBO("vbo_normals", self.normals)
        self.vao.add_vbo(vbo_vertices, "vertex")
        ebo_indices = EBO("indices", self.indices)
        self.vao.add_ebo(ebo_indices)
        self.vao.add_vbo(vbo_normals, "normal")


    def setup_cube(self):
        self.cube_vertices = np.array([
            [self.pos_max, self.pos_min, self.z_min],
            [self.pos_max, self.pos_max, self.z_min],
            [self.pos_min, self.pos_max, self.z_min],
            [self.pos_min, self.pos_min, self.z_min],
            [self.pos_max, self.pos_min, self.z_max],
            [self.pos_max, self.pos_max, self.z_max],
            [self.pos_min, self.pos_max, self.z_max],
            [self.pos_min, self.pos_min, self.z_max]
        ], dtype=np.float32)

        self.cube_indices = np.array([
            0, 1, 1, 2, 2, 3, 3, 0,
            4, 5, 5, 6, 6, 7, 7, 4,
            0, 4, 1, 5, 2, 6, 3, 7
        ], dtype=np.uint32)
        self.cube_shader = Shader("./objects/surface/cube.vert", "./objects/surface/cube.frag")

        self.cube_vao = VAO(self.cube_shader.identifier())
        vbo_vertices = VBO("vertices", self.cube_vertices)
        self.cube_vao.add_vbo(vbo_vertices, "vertex")
        ebo_indices = EBO("indices", self.cube_indices)
        self.cube_vao.add_ebo(ebo_indices)

    # def setup_axis(self):
    #     self.axis_vertices = np.array([
    #         [self.pos_max, self.pos_min, self.z_min],
    #         [self.pos_max, self.pos_max, self.z_min],
    #         [self.pos_min, self.pos_max, self.z_min],
    #         [self.pos_min, self.pos_min, self.z_min],
    #         [self.pos_max, self.pos_min, self.z_max],
    #         [self.pos_max, self.pos_max, self.z_max],
    #         [self.pos_min, self.pos_max, self.z_max],
    #         [self.pos_min, self.pos_min, self.z_max]
    #     ], dtype=np.float32)
    #
    #     self.cube_indices = np.array([
    #         0, 1, 1, 2, 2, 3, 3, 0,
    #         4, 5, 5, 6, 6, 7, 7, 4,
    #         0, 4, 1, 5, 2, 6, 3, 7
    #     ], dtype=np.uint32)
    #     self.cube_shader = Shader("./objects/surface/cube.vert", "./objects/surface/cube.frag")
    #
    #     self.cube_vao = VAO(self.cube_shader.identifier())
    #     vbo_vertices = VBO("vertices", self.cube_vertices)
    #     self.cube_vao.add_vbo(vbo_vertices, "vertex")
    #     # vbo_colors = VBO("colors", self.colors)
    #     # self.vao.add_vbo(vbo_colors, "color")
    #     ebo_indices = EBO("indices", self.cube_indices)
    #     self.cube_vao.add_ebo(ebo_indices)

    def draw_cube(self, projection, view, model):
        # activate VAO
        self.cube_vao.activate()

        # draw
        # modelview = np.identity(4, 'f')
        model = T.identity()
        modelview = view @ model
        self.cube_vao.upload_uniform_matrix4fv(projection, 'projection', True)
        self.cube_vao.upload_uniform_matrix4fv(modelview, 'modelview', True)

        GL.glDrawElements(GL.GL_LINES, len(self.cube_indices), GL.GL_UNSIGNED_INT, None)

    def draw(self, projection, view, model):
        # activate VAO
        self.vao.activate()

        # draw
        # modelview = np.identity(4, 'f')
        # view = T.translate(0, 0, 0)
        GL.glUseProgram(self.shader.render_idx)
        model = T.identity()
        modelview = view @ model
        self.vao.upload_uniform_matrix4fv(projection, 'projection', True)
        self.vao.upload_uniform_matrix4fv(modelview, 'modelview', True)
        self.vao.upload_uniform_matrix3fv(self.light_attrs, 'I_light', False)
        self.vao.upload_uniform_vector3fv(self.light_pos, 'light_pos')
        self.vao.upload_uniform_matrix3fv(self.materials, 'K_materials', False)
        self.vao.upload_uniform_scalar1f(self.shininess, 'shininess')

        GL.glDrawElements(GL.GL_TRIANGLE_STRIP, self.indices.shape[0], GL.GL_UNSIGNED_INT, None)

        # self.setup_axis()
        self.setup_cube()
        self.draw_cube(projection, view, model)
        # self.draw_axis(projection, view, model)

        # set ball position
        for ball in self.balls:
            ball.set_pos()
            ball.draw(projection, view, model)

    def set_z_color(self):
        self.vao.upload_uniform_scalar1f(self.z_min, 'zMin')
        self.vao.upload_uniform_scalar1f(self.z_max - self.z_min, 'zRange')

    def key_handler(self, key):
        if key == glfw.KEY_SPACE:
            for ball in self.balls:
                ball.reset_pos()

    def __del__(self):
        del self.vao
        del self.cube_vao
        del self.balls

def normal_of_face(A, B, C):
    A = np.array(A)
    B = np.array(B)
    C = np.array(C)
    AC = C - A
    AB = B - A
    n = np.cross(AC, AB)
    n = n/np.linalg.norm(n)
    return n


def normal_of_vert(adjacent_face_normals):
    n = np.sum(adjacent_face_normals, axis=0)
    if np.linalg.norm(n) == 0:  # [0, 0, 0] vector
        return [0, 0, 0]
    n = n / np.linalg.norm(n)
    return n


def generate_normals(vertices, indices):
    faces = []
    for i in range(int(len(indices)/3)):
        # list cannot be used as dict key
        face_vertices = tuple([tuple(vertices[index]) for index in indices[i*3:(i+1)*3]])
        faces.append(face_vertices)

    face_normals = {}
    for face in faces:
        face_vertex_1, face_vertex_2, face_vertex_3 = face
        face_normals[face] = normal_of_face(face_vertex_1, face_vertex_2, face_vertex_3)

    vertex_normals = []
    for vertex in vertices:
        adjacent_faces = filter(lambda face: vertex in face, faces)
        adjacent_face_normals = [face_normals[face] for face in adjacent_faces]

        vertex_normals.append(normal_of_vert(adjacent_face_normals))

    return vertex_normals
