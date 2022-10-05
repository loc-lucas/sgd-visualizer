import OpenGL.GL as GL
import numpy as np

from libs.shader import Shader              # standard Python OpenGL wrapper
import glfw
from libs.buffer import VAO

class GObject(object):
    def __init__(self,  vert_shader, frag_shader):
        self.yrot_angle = 90
        self.xrot_angle = 45
        self.shader = Shader(vert_shader, frag_shader)
        self.vao = VAO(self.shader)
        # Light
        self.light_attrs = np.array([
            [0.7, 0.4, 0.6],  # diffuse
            [0.7, 0.4, 0.6],  # specular
            [0.7, 0.4, 0.6]  # ambient
        ], dtype=np.float32)
        self.light_pos = np.array([5, 0, 10], dtype=np.float32)

        # Materials
        self.materials = np.array([
            [0.4, 0.2, 0.8],  # diffuse
            [0.4, 0.4, 0.8],  # specular
            [0.4, 0.2, 0.8]  # ambient
        ], dtype=np.float32)
        self.shininess = 80.0

        GL.glUseProgram(self.shader.render_idx)

    def key_handler(self, key):
        if key == glfw.KEY_LEFT:
            self.yrot_angle += 5
        if key == glfw.KEY_RIGHT:
            self.yrot_angle -= 5
        if key == glfw.KEY_UP:
            self.xrot_angle += 5
        if key == glfw.KEY_DOWN:
            self.xrot_angle -= 5

    def draw(self, projection=None, view=None, model=None):
        pass

