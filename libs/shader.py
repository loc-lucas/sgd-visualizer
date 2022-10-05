import OpenGL.GL as GL              # standard Python OpenGL wrapper
import numpy as np
import pandas as pd
import sys
import os


class Shader:
    """ Helper class to create and automatically destroy shader program """
    def __init__(self, vertex_source, fragment_source):
        """ Shader can be initialized with raw strings or source file names """
        '''Create a shader handle'''
        self.render_idx = None
        vert = self._compile_shader(vertex_source, GL.GL_VERTEX_SHADER)
        frag = self._compile_shader(fragment_source, GL.GL_FRAGMENT_SHADER)
        if vert and frag:
            ''' Create an empty shader handler '''
            self.render_idx = GL.glCreateProgram()  # pylint: disable=E1111
            ''' Attach shader '''
            GL.glAttachShader(self.render_idx, vert)
            GL.glAttachShader(self.render_idx, frag)
            GL.glLinkProgram(self.render_idx)
            """ Always detach shaders after a successful link and destroy them """
            GL.glDetachShader(self.render_idx, vert)
            GL.glDetachShader(self.render_idx, frag)
            GL.glDeleteShader(vert)
            GL.glDeleteShader(frag)
            """ check whether the linking process succeed """
            status = GL.glGetProgramiv(self.render_idx, GL.GL_LINK_STATUS)
            if not status:
                print(GL.glGetProgramInfoLog(self.render_idx).decode('ascii'))
                sys.exit(1)

    def identifier(self):
        return self.render_idx

    def __del__(self):
        GL.glUseProgram(0)
        if self.render_idx:                      # if this is a valid shader object
            GL.glDeleteProgram(self.render_idx)  # object dies => destroy GL object

    @staticmethod
    def _compile_shader(src, shader_type):
        src = open(src, 'r').read() if os.path.exists(src) else src
        src = src.decode('ascii') if isinstance(src, bytes) else src
        shader = GL.glCreateShader(shader_type)
        GL.glShaderSource(shader, src)
        GL.glCompileShader(shader)
        status = GL.glGetShaderiv(shader, GL.GL_COMPILE_STATUS)
        src = ('%3d: %s' % (i + 1, l) for i, l in enumerate(src.splitlines()))
        if not status:
            log = GL.glGetShaderInfoLog(shader).decode('ascii')
            GL.glDeleteShader(shader)
            src = '\n'.join(src)
            print('Compile failed for %s\n%s\n%s' % (shader_type, log, src))
            sys.exit(1)
        return shader
