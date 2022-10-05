import OpenGL.GL as GL              # standard Python OpenGL wrapper
import numpy as np
import pandas as pd

from libs.shader import Shader
import libs.transform as T
from libs.buffer import *
from libs.gobject import GObject


class Triangle(GObject):
    def __init__(self, vert_shader, frag_shader,
                 vertices: np.array,
                 colors: np.array = None):
        super(Triangle, self).__init__(vert_shader, frag_shader)
        self.vertices = vertices
        self.colors = colors
        self.__setup()


    def __setup(self):
        self.vao = VAO(self.shader.identifier())
        vbo_vertices = VBO("vertices", self.vertices)
        self.vao.add_vbo(vbo_vertices, "vertex")
        if self.colors is not None:
            vbo_colors = VBO("colors", self.colors)
            self.vao.add_vbo(vbo_colors, "color")

    def draw(self, projection, view, model):
        # activate VAO
        self.vao.activate()
        # draw
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)

    def __del__(self):
        del self.vao

class LightenTriangle(GObject):
    def __init__(self, vert_shader, frag_shader,
                 vertices: np.array,
                 colors: np.array = None):
        super().__init__(vert_shader, frag_shader)

        self.vertices = vertices
        self.colors = colors

        # Normals
        normals = np.random.normal(0, 3, (3, 3)).astype(np.float32)
        normals[:, 2] = np.abs(normals[:, 2])
        self.normals = normals / np.linalg.norm(normals, axis=1, keepdims=True)

        # Light
        self.light_attrs = np.array([
            [0.9, 0.4, 0.6],  # diffuse
            [0.9, 0.4, 0.6],  # specular
            [0.9, 0.4, 0.6]  # ambient
        ], dtype=np.float32)
        self.light_pos = np.array([0, 0.5, 0.9], dtype=np.float32)

        # Materials
        self.materials = np.array([
            [0.6, 0.4, 0.7],  # diffuse
            [0.6, 0.4, 0.7],  # specular
            [0.6, 0.4, 0.7]  # ambient
        ], dtype=np.float32)
        self.shininess = 100.0

        self.__setup()


    def __setup(self):
        self.vao = VAO(self.shader.identifier())
        vbo_vertices = VBO("vertices", self.vertices)
        self.vao.add_vbo(vbo_vertices, "vertex")
        if self.colors is not None:
            vbo_colors = VBO("colors", self.colors)
            self.vao.add_vbo(vbo_colors, "color")
        vbo_normals = VBO("normals", self.normals)
        self.vao.add_vbo(vbo_normals, "normal")

    def draw(self, projection, view, model):
        # activate VAO
        self.vao.activate()

        # draw
        projection = T.ortho(-1, 1, -1, 1, -1, 1)
        modelview = np.identity(4, 'f')
        self.vao.upload_uniform_matrix4fv(projection, 'projection', True)
        self.vao.upload_uniform_matrix4fv(modelview, 'modelview', True)
        self.vao.upload_uniform_matrix3fv(self.light_attrs, 'I_light', False)
        self.vao.upload_uniform_vector3fv(self.light_pos, 'light_pos')
        self.vao.upload_uniform_matrix3fv(self.materials, 'K_materials', False)
        self.vao.upload_uniform_scalar1f(self.shininess, 'shininess')

        # draw triangle as GL_TRIANGLE vertex array, draw array call
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)
