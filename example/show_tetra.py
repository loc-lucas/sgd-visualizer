from libs.window import Window
# from shapes import *
import glfw                         # lean windows system wrapper for OpenGL
from example.tetra.tetra import (Tetrahedron)

def main():
    window = Window()

    window.add(Tetrahedron("./example/tetra/phong.vert", "./example/tetra/phong.frag"))
    # start rendering loop
    window.show()

if __name__ == '__main__':
    glfw.init()  # initialize windows system glfw
    main()
    glfw.terminate()


