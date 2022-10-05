from libs.shader import *
from libs import transform as T
from libs.buffer import *
import ctypes
import glfw



def normal_of_face(A, B, C):
    AB = B - A
    AC = C - A
    n = np.cross(AB, AC)
    n = n/np.linalg.norm(n)
    return n

def normal_of_vert(n1, n2, n3):
    n = n1 + n2 + n3
    n = n / np.linalg.norm(n)
    return n


class Tetrahedron(object):
    def __init__(self, vert_shader, frag_shader):
        X = 1
        P = np.array(
            [
                [-3, 0, -1],  # A
                [+1, X, +4],  # B
                [+3, X, -3]  # C
            ],
            dtype=np.float32
        )
        A, B, C = P[0, :], P[1, :], P[2, :]
        nABC = normal_of_face(A, B, C)
        D = A + 5.0 * nABC

        self.vertices = np.concatenate([
            A.reshape(1, -1),
            B.reshape(1, -1),
            C.reshape(1, -1),
            D.reshape(1, -1),
        ], axis=0)

        self.indices = np.array(
            [0, 3, 1, 3, 2, 3, 0, 3, 3, 0, 0, 1, 2],
            dtype=np.int32
        )

        # faces: ACB, DAB, DBC, DCA
        nACB = normal_of_face(A, C, B)
        nDAB = normal_of_face(D, A, B)
        nDBC = normal_of_face(D, B, C)
        nDCA = normal_of_face(D, C, A)
        nA = normal_of_vert(nACB, nDCA, nDAB)
        nB = normal_of_vert(nACB, nDAB, nDBC)
        nC = normal_of_vert(nACB, nDCA, nDBC)
        nD = normal_of_vert(nDAB, nDBC, nDCA)

        self.normals = np.concatenate([
            nA.reshape(1, -1),
            nB.reshape(1, -1),
            nC.reshape(1, -1),
            nD.reshape(1, -1),
        ], axis=0)

        # colors: RGB format
        self.colors = np.array(
            [  # R    G    B
                [1.0, 0.0, 0.0],  # A
                [0.0, 1.0, 0.0],  # B
                [0.0, 0.0, 1.0],  # C
                [0.0, 0.0, 0.0]  # D
            ],
            dtype=np.float32
        )
        # Make sure 32 bits
        self.vertices = self.vertices.astype(np.float32)
        self.normals = self.normals.astype(np.float32)

        #Setup VBO and VAO
        vbo_vertices = VBO("vbo_vertices", self.vertices)
        vbo_colors = VBO("vbo_colors", self.colors)
        vbo_normals = VBO("vbo_normals", self.normals)

        self.shader = Shader(vert_shader, frag_shader)
        self.vao = VAO(self.shader.identifier())
        self.vao.add_vbo(vbo_vertices, "vertex")
        self.vao.add_vbo(vbo_colors, "color")
        self.vao.add_vbo(vbo_normals, "normal")
        ebo = EBO("indices", self.indices)
        self.vao.add_ebo(ebo)

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
        self.vao.activate()

        model = T.translate(0, -2, -8)
        GL.glUseProgram(self.shader.render_idx)
        modelview = view @ model

        self.vao.upload_uniform_matrix4fv(projection, 'projection', True)
        self.vao.upload_uniform_matrix4fv(modelview, 'modelview', True)
        self.vao.upload_uniform_matrix3fv(self.light_attrs, 'I_light', False)
        self.vao.upload_uniform_vector3fv(self.light_pos, 'light_pos')
        self.vao.upload_uniform_matrix3fv(self.materiaqls, 'K_materials', False)
        self.vao.upload_uniform_scalar1f(self.shininess, 'shininess')
        GL.glDrawElements(GL.GL_TRIANGLE_STRIP, self.indices.shape[0], GL.GL_UNSIGNED_INT, None)
