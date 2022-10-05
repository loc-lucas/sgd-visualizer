import OpenGL.GL as GL              # standard Python OpenGL wrapper
import numpy as np
import pandas as pd

from libs.shader import Shader
from libs.buffer import *
import libs.transform as T
import ctypes




class BadPatch(object):
    def __init__(self):
        """
        Bad: why?
        Because: repeated vertices => cost memory
        """
        self.vertices = np.array([
            [0, 0, 0],  # A
            [0, 1, 0],  # B
            [1, 0, 0],  # C => ABC
            [0, 1, 0],  # B
            [1, 1, 0],  # D
            [1, 0, 0],  # C => BDC
            [1, 0, 0],  # C
            [1, 1, 0],  # D
            [2, 0, 0],  # E => CDE
            [1, 1, 0],  # D
            [2, 1, 0],  # F
            [2, 0, 0],  # E => DFE
        ], dtype=np.float32)
        self.colors = np.array([
            [0.0, 0.0, 0.0],  # A
            [1.0, 0.0, 0.0],  # B
            [0.0, 1.0, 0.0],  # C => ABC
            [1.0, 0.0, 0.0],  # B
            [0.0, 0.0, 1.0],  # D
            [0.0, 1.0, 0.0],  # C => BDC
            [0.0, 1.0, 0.0],  # C
            [0.0, 0.0, 1.0],  # D
            [1.0, 0.0, 0.0],  # E => CDE
            [0.0, 0.0, 1.0],  # D
            [1.0, 1.0, 1.0],  # F
            [1.0, 0.0, 0.0]   # E => DFE
        ], dtype=np.float32)
        self.shader =  Shader("./patch/gouraud.vert", "./patch/gouraud.frag")

        self.vao = VAO(self.shader.identifier())
        vbo_vertices = VBO("vertices", self.vertices)
        self.vao.add_vbo(vbo_vertices, "vertex")
        vbo_colors = VBO("colors", self.colors)
        self.vao.add_vbo(vbo_colors, "color")

    def draw(self, projection, view, model):
        # activate VAO
        self.vao.activate()

        # draw
        projection = T.ortho(0, 2, -0.5, 1.5, -1, 1)
        modelview = np.identity(4, 'f')
        self.vao.upload_uniform_matrix4fv(projection, 'projection', True)
        self.vao.upload_uniform_matrix4fv(modelview, 'modelview', True)

        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 4*3)

    def __del__(self):
        del self.vao


class StillBadPatch(object):
    def __init__(self):
        """
        still bad
        because: repeated indices
        """
        self.vertices = np.array([
            [0, 0, 0],  # A
            [0, 1, 0],  # B
            [1, 0, 0],  # C
            [1, 1, 0],  # D
            [2, 0, 0],  # E
            [2, 1, 0],  # F
        ], dtype=np.float32)
        self.colors = np.array([
            [0.0, 0.0, 0.0],  # A:0
            [1.0, 0.0, 0.0],  # B:1
            [0.0, 1.0, 0.0],  # C:2
            [0.0, 0.0, 1.0],  # D:3
            [1.0, 0.0, 0.0],  # E:4
            [1.0, 1.0, 1.0],  # F:5
        ], dtype=np.float32)
        self.indices = np.array([
            0, 1, 2,  # ABC
            1, 3, 2,  # BDC
            2, 3, 4,  # CDE
            3, 5, 4  # DFE
        ], dtype=np.uint32)

        self.shader =  Shader("./patch/gouraud.vert", "./patch/gouraud.frag")

        self.vao = VAO(self.shader.identifier())
        vbo_vertices = VBO("vertices", self.vertices)
        self.vao.add_vbo(vbo_vertices, "vertex")
        vbo_colors = VBO("colors", self.colors)
        self.vao.add_vbo(vbo_colors, "color")
        ebo_indices = EBO("indices", self.indices)
        self.vao.add_ebo(ebo_indices)
        print("StillBadPatch")

    def draw(self, projection, view, model):
        # activate VAO
        self.vao.activate()

        # draw
        projection = T.ortho(0, 2, -0.5, 1.5, -1, 1)
        modelview = np.identity(4, 'f')
        self.vao.upload_uniform_matrix4fv(projection, 'projection', True)
        self.vao.upload_uniform_matrix4fv(modelview, 'modelview', True)

        GL.glDrawElements(GL.GL_TRIANGLES, 4*3, GL.GL_UNSIGNED_INT, None)

    def __del__(self):
        del self.vao

class SimplePatch(object):
    def __init__(self):
        """
        """
        # self.vertices = np.array([
        #     [0, 0, 0],  # A
        #     [0, 1, 0],  # B
        #     # [0, 2, 0],
        #     [1, 0, 0],  # C
        #     [1, 1, 0],  # D
        #     # [1, 2, 0],
        #     [2, 0, 0],  # E
        #     [2, 1, 0],  # F
        #     # [2, 2, 0]
        # ], dtype=np.float32)

        self.vertices = np.array([
            [0, 0, 0],
            [0, 1, 0],
            [0, 2, 0],
            [1, 0, 0],
            [1, 1, 0],
            [1, 2, 0],
            [2, 0, 0],
            [2, 1, 0],
            [2, 2, 0]
        ], dtype=np.float32)
        self.colors = np.array([
            [0.0, 0.0, 0.0],  # A:0
            [1.0, 0.0, 0.0],  # B:1
            [0.0, 1.0, 0.0],  # C:2
            [0.0, 0.0, 1.0],  # D:3
            [1.0, 0.0, 0.0],  # E:4
            [1.0, 1.0, 1.0],  # F:5
        ], dtype=np.float32)
        indices = []
        rows = 3
        cols = 3
        for r in range(rows-1):
            if r > 0:
                indices += [r * cols]
            for c in range(cols):
                indices += [r * cols + c]
                indices += [(r + 1) * cols + c]
            if r < rows - 2:
                indices += [(r+1)*cols + rows - 1]
        print(indices)
        self.indices = np.array(indices, dtype=np.uint32)
        self.shader = Shader("./patch/gouraud.vert", "./patch/gouraud.frag")

        self.vao = VAO(self.shader.identifier())
        vbo_vertices = VBO("vertices", self.vertices)
        self.vao.add_vbo(vbo_vertices, "vertex")
        # vbo_colors = VBO("colors", self.colors)
        # self.vao.add_vbo(vbo_colors, "color")
        ebo_indices = EBO("indices", self.indices)
        self.vao.add_ebo(ebo_indices)
        print("SimplePatch")

    def draw(self, projection, view, model):
        # activate VAO
        self.vao.activate()

        # draw
        # modelview = np.identity(4, 'f')
        view = T.translate(-1, -1, 0)
        modelview = view @ model
        self.vao.upload_uniform_matrix4fv(projection, 'projection', True)
        self.vao.upload_uniform_matrix4fv(modelview, 'modelview', True)

        GL.glDrawElements(GL.GL_TRIANGLE_STRIP, len(self.indices), GL.GL_UNSIGNED_INT, None)

    def __del__(self):
        del self.vao

class Patch(object):
    def __init__(self):
        """
        """
        self.vertex_attrs = np.array([
        #    v.x  v.y  v.z  c.r  c.g  c.b
            [0,   0,   0,   0.0, 0.0, 0.0],  # A
            [0,   1,   0,   1.0, 0.0, 0.0],  # B
            [1,   0,   0,   0.0, 1.0, 0.0],  # C
            [1,   1,   0,   0.0, 0.0, 1.0],  # D
            [2,   0,   0,   1.0, 0.0, 0.0],  # E
            [2,   1,   0,   1.0, 1.0, 1.0],  # F
        ], dtype=np.float32)
        self.indices = np.array([
            0,1,2,3,4,5
        ], dtype=np.uint32)

        self.shader =  Shader("./patch/gouraud.vert", "./patch/gouraud.frag")

        self.vao = VAO(self.shader.identifier())
        vertex_attrs = VBO("vertex_attrs", self.vertex_attrs)

        stride = 6 * 4 # 6: 6 attributes; 4: size in bytes of each attribute
        offset_v = ctypes.c_void_p(0)  # None
        offset_c = ctypes.c_void_p(3 * 4)

        self.vao.add_vbo(vertex_attrs, "vertex",
                         ncomponents=3, dtype=GL.GL_FLOAT, normalized=False, stride=stride, offset=offset_v)
        self.vao.add_vbo(vertex_attrs, "color",
                         ncomponents=3, dtype=GL.GL_FLOAT, normalized=False, stride=stride, offset=offset_c)

        ebo_indices = EBO("indices", self.indices)
        self.vao.add_ebo(ebo_indices)
        print("Patch")

    def draw(self, projection, view, model):
        # activate VAO
        self.vao.activate()

        # draw
        projection = T.ortho(0, 2, -0.5, 1.5, -1, 1)
        modelview = np.identity(4, 'f')
        self.vao.upload_uniform_matrix4fv(projection, 'projection', True)
        self.vao.upload_uniform_matrix4fv(modelview, 'modelview', True)

        GL.glDrawElements(GL.GL_TRIANGLE_STRIP, 6, GL.GL_UNSIGNED_INT, None)

    def __del__(self):
        del self.vao

class TexturedPatch(object):
    def __init__(self):
        """
        """
        self.vertex_attrs = np.array([
        #    v.x  v.y  v.z  c.r  c.g  c.b   t.x  t.y
            [0,   0,   0,   0.0, 0.0, 0.0,  0.0, 1.0],  # A
            [0,   1,   0,   1.0, 0.0, 0.0,  0.0, 0.0],  # B
            [1,   0,   0,   0.0, 1.0, 0.0,  0.5, 1.0],  # C
            [1,   1,   0,   0.0, 0.0, 1.0,  0.5, 0.0],  # D
            [2,   0,   0,   1.0, 0.0, 0.0,  1.0, 1.0],  # E
            [2,   1,   0,   1.0, 1.0, 1.0,  1.0, 0.0],  # F
        ], dtype=np.float32)
        self.indices = np.array([
            0,1,2,3,4,5
        ], dtype=np.uint32)

        self.shader =  Shader("./patch/texture.vert", "./patch/texture.frag")

        self.vao = VAO(self.shader.identifier())
        vertex_attrs = VBO("vertex_attrs", self.vertex_attrs)

        stride = 8 * 4 # 8: 8 attributes; 4: size in bytes of each attribute
        offset_v = ctypes.c_void_p(0)  # None
        offset_c = ctypes.c_void_p(3 * 4)
        offset_t = ctypes.c_void_p(6 * 4)

        self.vao.add_vbo(vertex_attrs, "vertex",
                         ncomponents=3, dtype=GL.GL_FLOAT, normalized=False, stride=stride, offset=offset_v)
        self.vao.add_vbo(vertex_attrs, "color",
                         ncomponents=3, dtype=GL.GL_FLOAT, normalized=False, stride=stride, offset=offset_c)
        self.vao.add_vbo(vertex_attrs, "texcoord",
                         ncomponents=3, dtype=GL.GL_FLOAT, normalized=False, stride=stride, offset=offset_t)

        ebo_indices = EBO("indices", self.indices)
        self.vao.add_ebo(ebo_indices)

        self.vao.setup_texture("texture1", "./patch/image/texture1.jpeg")
        print("TexturedPatch")

    def draw(self, projection, view, model):
        # activate VAO
        self.vao.activate()

        # draw
        projection = T.ortho(0, 2, -0.5, 1.5, -1, 1)
        modelview = np.identity(4, 'f')
        self.vao.upload_uniform_matrix4fv(projection, 'projection', True)
        self.vao.upload_uniform_matrix4fv(modelview, 'modelview', True)

        GL.glDrawElements(GL.GL_TRIANGLE_STRIP, 6, GL.GL_UNSIGNED_INT, None)

    def __del__(self):
        del self.vao


class LightenPatch(object):
    def __init__(self):
        """
        """
        self.vertex_attrs = np.array([
        #    v.x  v.y  v.z  c.r  c.g  c.b   t.x  t.y
            [0,   0,   0,   0.0, 0.0, 0.0,  0.0, 1.0],  # A
            [0,   1,   0,   1.0, 0.0, 0.0,  0.0, 0.0],  # B
            [1,   0,   0,   0.0, 1.0, 0.0,  0.5, 1.0],  # C
            [1,   1,   0,   0.0, 0.0, 1.0,  0.5, 0.0],  # D
            [2,   0,   0,   1.0, 0.0, 0.0,  1.0, 1.0],  # E
            [2,   1,   0,   1.0, 1.0, 1.0,  1.0, 0.0],  # F
        ], dtype=np.float32)
        # random normals (facing +z)
        normals = np.random.normal(0, 5, (self.vertex_attrs.shape[0], 3)).astype(np.float32)
        normals[:, 2] = np.abs(normals[:, 2])  # (facing +z)
        normals = normals / np.linalg.norm(normals, axis=1, keepdims=True)
        self.vertex_attrs = np.concatenate([self.vertex_attrs, normals], axis=1)
        # now, self.vertex_attrs: v.x  v.y  v.z  c.r  c.g  c.b   t.x  t.y, n.x, n.y, n.z  (11 elements/row)

        self.indices = np.array([
            0,1,2,3,4,5
        ], dtype=np.uint32)

        self.shader =  Shader("./patch/phong_texture.vert", "./patch/phong_texture.frag")

        self.vao = VAO(self.shader.identifier())
        vertex_attrs = VBO("vertex_attrs", self.vertex_attrs)

        stride = 11 * 4 # 11: 11 attributes; 4: size in bytes of each attribute
        offset_v = ctypes.c_void_p(0)  # None
        offset_c = ctypes.c_void_p(3 * 4)
        offset_t = ctypes.c_void_p(6 * 4)
        offset_n = ctypes.c_void_p(8 * 4)

        self.vao.add_vbo(vertex_attrs, "vertex",
                         ncomponents=3, dtype=GL.GL_FLOAT, normalized=False, stride=stride, offset=offset_v)
        self.vao.add_vbo(vertex_attrs, "color",
                         ncomponents=3, dtype=GL.GL_FLOAT, normalized=False, stride=stride, offset=offset_c)
        self.vao.add_vbo(vertex_attrs, "texcoord",
                         ncomponents=3, dtype=GL.GL_FLOAT, normalized=False, stride=stride, offset=offset_t)
        self.vao.add_vbo(vertex_attrs, "normal",
                         ncomponents=3, dtype=GL.GL_FLOAT, normalized=False, stride=stride, offset=offset_n)

        ebo_indices = EBO("indices", self.indices)
        self.vao.add_ebo(ebo_indices)

        self.vao.setup_texture("texture1", "./patch/image/texture1.jpeg")

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
        self.phong_factor = 0.3

        print("LightenPatch")

    def draw(self, projection, view, model):
        # activate VAO
        self.vao.activate()

        # draw
        projection = T.ortho(0, 2, -0.5, 1.5, -1, 1)
        modelview = np.identity(4, 'f')
        self.vao.upload_uniform_matrix4fv(projection, 'projection', True)
        self.vao.upload_uniform_matrix4fv(modelview, 'modelview', True)
        self.vao.upload_uniform_matrix3fv(self.light_attrs, 'I_light', False)
        self.vao.upload_uniform_vector3fv(self.light_pos, 'light_pos')
        self.vao.upload_uniform_matrix3fv(self.materials, 'K_materials', False)
        self.vao.upload_uniform_scalar1f(self.shininess, 'shininess')
        self.vao.upload_uniform_scalar1f(self.phong_factor, 'phong_factor')

        GL.glDrawElements(GL.GL_TRIANGLE_STRIP, 6, GL.GL_UNSIGNED_INT, None)

    def __del__(self):
        del self.vao