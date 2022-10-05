import math
from time import time

import numpy as np

from libs.buffer import *
from libs.gobject import GObject
import libs.transform as T
from libs.shader import Shader


class Ball(GObject):
    def __init__(self, x, y, z, optimizer, color, learn_rate, momentum=0, max_iter=10000, radius=0.25):
        self.x = x
        self.y = y
        self.z = z
        self.radius = radius
        self.vertices, self.indices = self.gen_vertices_and_indices()
        self.colors = self.get_color(color)
        self.current_pos_idx = 0
        self.optimizer = optimizer
        t = time()
        self.path, _ = self.optimizer.gradient_descent_with_momentum(
            start=np.array([x,y], dtype=np.float32),
            learn_rate=learn_rate,
            gamma=momentum,
            max_iter=max_iter
        )
        # z_coord =
        print(f"{color}-{len(self.path)}-{time()-t}s")
        vbo_vertices = VBO("vbo_vertices", self.vertices)
        vbo_colors = VBO("vbo_colors", self.colors)
        # vbo_normals = VBO("vbo_normals", self.normals)

        self.shader = Shader('./objects/ball/ball.vert', './objects/ball/ball.frag')
        self.vao = VAO(self.shader.identifier())
        self.vao.add_vbo(vbo_vertices, "vertex")
        self.vao.add_vbo(vbo_colors, "color")
        # self.vao.add_vbo(vbo_normals, "normal")
        ebo = EBO("indices", self.indices)
        self.vao.add_ebo(ebo)

    def get_color(self, color):
        if color == 'yellow':
            return np.array([[1, 5, 0]] * len(self.vertices), dtype=np.float32)
        if color == 'cyan':
            return np.array([[0, 1, 5]] * len(self.vertices), dtype=np.float32)
        if color == 'white':
            return np.array([[1, 1, 1]] * len(self.vertices), dtype=np.float32)
        if color == 'black':
            return np.array([[0, 0, 0]] * len(self.vertices), dtype=np.float32)
        if color == 'purple':
            return np.array([[0.4, 0, 0.5]] * len(self.vertices), dtype=np.float32)

    def gen_vertices_and_indices(self, lats=512, longs=512):
        vertices = []
        indices = []
        idx = 0
        radius = self.radius
        for i in range(lats + 1):
            lat0 = math.pi * (-0.5 + (i - 1) / lats)
            z0 = math.sin(lat0) * radius
            zr0 = math.cos(lat0) * radius
            lat1 = math.pi * (-0.5 + i / lats)
            z1 = math.sin(lat1) * radius
            zr1 = math.cos(lat1) * radius

            for j in range(longs+1):
                lng = 2 * math.pi * (j - 1) / longs
                x = math.cos(lng)
                y = math.sin(lng)

                vertices.append([x * zr0, y * zr0, z0])
                indices.append(idx)
                idx += 1

                vertices.append([x * zr1, y * zr1, z1])
                indices.append(idx)
                idx += 1

            indices.append(GL.GL_PRIMITIVE_RESTART_FIXED_INDEX)
        return np.array(vertices, dtype=np.float32), np.array(indices, dtype=np.uint32)

    def draw(self, projection, view, model):
        self.vao.activate()

        model = T.translate(self.x, self.y, self.z)
        GL.glUseProgram(self.shader.render_idx)
        modelview = view @ model

        self.vao.upload_uniform_matrix4fv(projection, 'projection', True)
        self.vao.upload_uniform_matrix4fv(modelview, 'modelview', True)
        # self.vao.upload_uniform_matrix3fv(self.light_attrs, 'I_light', False)
        # self.vao.upload_uniform_vector3fv(self.light_pos, 'light_pos')
        # self.vao.upload_uniform_matrix3fv(self.materials, 'K_materials', False)
        # self.vao.upload_uniform_scalar1f(self.shininess, 'shininess')
        GL.glDrawElements(GL.GL_TRIANGLE_STRIP, self.indices.shape[0], GL.GL_UNSIGNED_INT, None)

    def set_pos(self):
        if self.current_pos_idx < len(self.path):
            pos = self.path[self.current_pos_idx]
            self.x = pos[0]
            self.y = pos[1]
            self.z = pos[2] + self.radius
            self.current_pos_idx += 1

    def reset_pos(self):
        self.current_pos_idx = 0
        self.x, self.y, self.z = self.path[0]
        self.z += self.radius

    def __del__(self):
        del self.vao

