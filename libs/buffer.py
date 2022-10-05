import OpenGL.GL as GL
import cv2

class VBO(object):
    def __init__(self, name, data):
        buffer_idx = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, buffer_idx)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, data, GL.GL_STATIC_DRAW)
        self.name = name
        self.identifier = buffer_idx

    def __del__(self):
        GL.glDeleteBuffers(1, [self.identifier])

class EBO(object):
    def __init__(self, name, indices):
        buffer_idx = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, buffer_idx)
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indices, GL.GL_STATIC_DRAW)
        self.name = name
        self.identifier = buffer_idx

    def __del__(self):
        GL.glDeleteBuffers(1, [self.identifier])


class VAO(object):
    def __init__(self, shader_identifier):
        self.shader_identifier = shader_identifier

        """ Typically used 1 as a time """
        self.vao_identifier = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao_identifier)
        GL.glBindVertexArray(0)

        self.vbobjects = []
        self.ebo = None
        self.textures = {}

    def add_vbo(self, vbo, shader_attribute,
                     ncomponents=3, dtype=GL.GL_FLOAT, normalized=False, stride=0, offset=None):
        self.vbobjects.append(vbo)

        GL.glBindVertexArray(self.vao_identifier)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo.identifier)
        location = GL.glGetAttribLocation(self.shader_identifier, shader_attribute)
        GL.glVertexAttribPointer(location, ncomponents, dtype, normalized, stride, offset)
        GL.glEnableVertexAttribArray(location)

    def add_ebo(self, ebo):
        self.ebo = ebo

        GL.glBindVertexArray(self.vao_identifier)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ebo.identifier)

    def __del__(self):
        vbo_list = [vbo.identifier for vbo in self.vbobjects]
        GL.glDeleteBuffers(len(vbo_list), vbo_list)
        if self.ebo is not None:
            GL.glDeleteBuffers(1, [self.ebo.identifier])
        GL.glDeleteVertexArrays(1, [self.vao_identifier])

    def activate(self):
        GL.glUseProgram(self.shader_identifier)
        GL.glBindVertexArray(self.vao_identifier)  # activated

    def deactivate(self):
        GL.glBindVertexArray(0)

    @staticmethod
    def load_texture(filename):
        texture = cv2.cvtColor(cv2.imread(filename, 1), cv2.COLOR_BGR2RGB)
        return texture

    def _get_texture_loc(self):
        if not bool(self.textures):
            return 0
        else:
            locs = list(self.textures.keys())
            locs.sort(reverse=True)
            ret_id = locs[0] + 1
            return ret_id

    """
    * first call to setup_texture: activate GL.GL_TEXTURE0
        > use GL.glUniform1i to associate the activated texture to the texture in sgd-visualizer program (see fragment shader)
    * second call to setup_texture: activate GL.GL_TEXTURE1
        > use GL.glUniform1i to associate the activated texture to the texture in sgd-visualizer program (see fragment shader)
    * second call to setup_texture: activate GL.GL_TEXTURE2
        > use GL.glUniform1i to associate the activated texture to the texture in sgd-visualizer program (see fragment shader)
    and so on

    """

    def setup_texture(self, sampler_name, image_file):
        rgb_image = VAO.load_texture(image_file)

        GL.glUseProgram(self.shader_identifier)  # must call before calling to GL.glUniform1i
        texture_idx = GL.glGenTextures(1)
        binding_loc = self._get_texture_loc()
        self.textures[binding_loc] = {}
        self.textures[binding_loc]["id"] = texture_idx
        self.textures[binding_loc]["name"] = sampler_name

        GL.glActiveTexture(GL.GL_TEXTURE0 + binding_loc)  # activate texture GL.GL_TEXTURE0, GL.GL_TEXTURE1, ...
        GL.glBindTexture(GL.GL_TEXTURE_2D, texture_idx)
        GL.glUniform1i(GL.glGetUniformLocation(self.shader_identifier, sampler_name), binding_loc)

        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGB,
                        rgb_image.shape[1], rgb_image.shape[0], 0, GL.GL_RGB, GL.GL_UNSIGNED_BYTE, rgb_image)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)

    def upload_uniform_matrix4fv(self, matrix, name, transpose=True):
        GL.glUseProgram(self.shader_identifier)
        location = GL.glGetUniformLocation(self.shader_identifier, name)
        GL.glUniformMatrix4fv(location, 1, transpose, matrix)

    def upload_uniform_matrix3fv(self, matrix, name, transpose=False):
        GL.glUseProgram(self.shader_identifier)
        location = GL.glGetUniformLocation(self.shader_identifier, name)
        GL.glUniformMatrix3fv(location, 1, transpose, matrix)

    def upload_uniform_vector4fv(self, vector, name):
        GL.glUseProgram(self.shader_identifier)
        location = GL.glGetUniformLocation(self.shader_identifier, name)
        GL.glUniform4fv(location, 1, vector)

    def upload_uniform_vector3fv(self, vector, name):
        GL.glUseProgram(self.shader_identifier)
        location = GL.glGetUniformLocation(self.shader_identifier, name)
        GL.glUniform3fv(location, 1, vector)

    def upload_uniform_scalar1f(self, scalar, name):
        GL.glUseProgram(self.shader_identifier)
        location = GL.glGetUniformLocation(self.shader_identifier, name)
        GL.glUniform1f(location, scalar)

    def upload_uniform_scalar1i(self, scalar, name):
        GL.glUseProgram(self.shader_identifier)
        location = GL.glGetUniformLocation(self.shader_identifier, name)
        GL.glUniform1i(location, scalar)
