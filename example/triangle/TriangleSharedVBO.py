import OpenGL.GL as GL              # standard Python OpenGL wrapper
import numpy as np
import pandas as pd

from libs.shader import Shader
import libs.transform as T
from libs.buffer import *
from libs.gobject import GObject
import glfw

class TriangleSharedVBO(object):
    FLAT = 0
    GOURAUD = 1
    PHONG = 2

    def __init__(self):
        self.mode = TriangleSharedVBO.FLAT

        self.vertices = np.array([
            [-1.0, -1.0, 0],
            [0, 1.0, 0],
            [1.0, -1.0, 0]
        ], dtype=np.float32)

        self.colors = np.array([
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0]
        ], dtype=np.float32)

        # Normals
        normals = np.random.normal(0, 3, (3, 3)).astype(np.float32)
        normals[:, 2] = np.abs(normals[:, 2])
        self.normals = normals / np.linalg.norm(normals, axis=1, keepdims=True)

        # Shaders
        self.flat_shader = Shader("./triangle/flat.vert", "./triangle/flat.frag")
        self.gouraud_shader = Shader("./triangle/gouraud.vert", "./triangle/gouraud.frag")
        self.phong_shader = Shader("./triangle/phong.vert", "./triangle/phong.frag")

        self.vbo = {}
        self.vao = {}
        # create VBO: vertices, color, normals
        vbo_vertices = VBO("vertices", self.vertices)
        vbo_colors = VBO("colors", self.colors)
        vbo_normals = VBO("normals", self.normals)

        #flat
        self.vao_flat = VAO(self.flat_shader.identifier())
        self.vao_flat.add_vbo(vbo_vertices, "vertex")

        self.vao_gouraud = VAO(self.gouraud_shader.identifier())
        self.vao_gouraud.add_vbo(vbo_vertices, "vertex")
        self.vao_gouraud.add_vbo(vbo_colors, "color")

        self.vao_phong = VAO(self.phong_shader.identifier())
        self.vao_phong.add_vbo(vbo_vertices, "vertex")
        self.vao_phong.add_vbo(vbo_colors, "color")
        self.vao_phong.add_vbo(vbo_normals, "normal")

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

    def draw(self, projection, view, model):
        # activate VAO
        if self.mode == TriangleSharedVBO.FLAT:
            self.vao_flat.activate()

        if self.mode == TriangleSharedVBO.GOURAUD:
            self.vao_gouraud.activate()

        if self.mode == TriangleSharedVBO.PHONG:
            self.vao_phong.activate()

            projection = T.ortho(-1, 1, -1, 1, -1, 1)
            modelview = np.identity(4, 'f')

            self.vao_phong.upload_uniform_matrix4fv(projection, 'projection', True)
            self.vao_phong.upload_uniform_matrix4fv(modelview, 'modelview', True)
            self.vao_phong.upload_uniform_matrix3fv(self.light_attrs, 'I_light', False)
            self.vao_phong.upload_uniform_vector3fv(self.light_pos, 'light_pos')
            self.vao_phong.upload_uniform_matrix3fv(self.materials, 'K_materials', False)
            self.vao_phong.upload_uniform_scalar1f(self.shininess, 'shininess')

        # draw
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)

    def __del__(self):
        del self.vao_flat
        del self.vao_gouraud
        del self.vao_phong

    def key_handler(self, key):
        if key == glfw.KEY_F:
            self.mode = TriangleSharedVBO.FLAT
        if key == glfw.KEY_G:
            self.mode = TriangleSharedVBO.GOURAUD
        if key == glfw.KEY_P:
            self.mode = TriangleSharedVBO.PHONG
