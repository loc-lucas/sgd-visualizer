import OpenGL.GL as GL              # standard Python OpenGL wrapper
import numpy as np
import pandas as pd

from libs.shader import Shader
from libs.buffer import *
import libs.transform as T
import ctypes

class Circle(object):
    def __init__(self, nsegments=4):
        """
        """
        alpha = np.linspace(0, 2*np.pi, nsegments+1, endpoint=True)
        vertices = [np.cos(alpha).reshape(-1,1), np.sin(alpha).reshape(-1,1), np.zeros((nsegments +1, 1))]
        vertices = np.concatenate(vertices, axis=1)
        center = np.array([0.0, 0.0, 0.0]).reshape(1,-1)
        vertices = np.concatenate([center, vertices], axis=0).astype(np.float32)
        indices = np.arange(vertices.shape[0], dtype=np.uint32)


        self.shader =  Shader("./circle/flat.vert", "./circle/flat.frag")

        self.vao = VAO(self.shader.identifier())
        vertex_attrs = VBO("vertex_attrs", vertices)
        self.vao.add_vbo(vertex_attrs, "vertex")

        ebo_indices = EBO("indices", indices)
        self.vao.add_ebo(ebo_indices)
        self.num_points = indices.shape[0]

        print("Circle")

    def draw(self, projection, view, model):
        # activate VAO
        self.vao.activate()

        # draw
        projection = T.ortho(-1, 2, -1, 2, -1, 2)
        modelview = np.identity(4, 'f')
        self.vao.upload_uniform_matrix4fv(projection, 'projection', True)
        self.vao.upload_uniform_matrix4fv(modelview, 'modelview', True)

        GL.glDrawElements(GL.GL_TRIANGLE_FAN, self.num_points, GL.GL_UNSIGNED_INT, None)

    def __del__(self):
        del self.vao

class TexturedCircle(object):
    def __init__(self, nsegments=4):
        """
        """
        alpha = np.linspace(0, 2*np.pi, nsegments+1, endpoint=True)
        vertices = [np.cos(alpha).reshape(-1,1), np.sin(alpha).reshape(-1,1), np.zeros((nsegments +1, 1))]
        vertices = np.concatenate(vertices, axis=1)
        center = np.array([0.0, 0.0, 0.0]).reshape(1,-1)
        vertices = np.concatenate([center, vertices], axis=0).astype(np.float32)

        texcoords = -0.5*vertices + np.array([0.5, 0.5, 0.0]).reshape(1,-1)
        texcoords = texcoords[:,:2].astype(np.float32)
        print(texcoords.min())
        print(texcoords.max())
        print(texcoords.dtype)

        indices = np.arange(vertices.shape[0], dtype=np.uint32)


        self.shader =  Shader("./circle/texture.vert", "./circle/texture.frag")

        self.vao = VAO(self.shader.identifier())
        vertex_attrs = VBO("vertex_attrs", vertices)
        self.vao.add_vbo(vertex_attrs, "vertex")

        tex_vbo = VBO("tex_vbo", texcoords)
        self.vao.add_vbo(tex_vbo, "texcoord",
                         ncomponents=2, dtype=GL.GL_FLOAT, stride=0, offset=None)

        ebo_indices = EBO("indices", indices)
        self.vao.add_ebo(ebo_indices)
        self.num_points = indices.shape[0]

        self.vao.setup_texture("texture1", "./circle/image/tieuvi.jpeg")

        print("TexturedCircle")

    def draw(self, projection, view, model):
        # activate VAO
        self.vao.activate()

        # draw
        projection = T.ortho(-1, 1, -1, 1, -1, 1)
        modelview = np.identity(4, 'f')
        self.vao.upload_uniform_matrix4fv(projection, 'projection', True)
        self.vao.upload_uniform_matrix4fv(modelview, 'modelview', True)

        GL.glDrawElements(GL.GL_TRIANGLE_FAN, self.num_points, GL.GL_UNSIGNED_INT, None)

    def __del__(self):
        del self.vao