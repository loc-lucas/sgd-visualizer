from libs.window import Window
# from shapes import *
import glfw                         # lean windows system wrapper for OpenGL
import numpy as np
from example.triangle import (Triangle)

def main():
    window = Window()
    t1 = np.array([
        [-0.5, 1.0, 0],
        [0, 0, 0],
        [-1.0, 0, 0]
    ], dtype=np.float32)

    t2 = np.array([
        [0.5, 1.0, 0],
        [1.0, 0, 0],
        [0, 0, 0]
    ], dtype=np.float32)
    t3 = np.array([
        [-0.5, -1.0, 0],
        [0.0, 0, 0],
        [0.5, -1.0, 0]
    ], dtype=np.float32)

    c2 = np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ], dtype=np.float32)

    window.add(Triangle("./triangle/flat.vert", "./triangle/flat.frag", t1))
    # window.add(Triangle("./triangle/gouraud.vert", "./triangle/gouraud.frag", t2, colors=c2))
    # window.add(LightenTriangle("./triangle/phong.vert", "./triangle/phong.frag", t3, colors=c2))

    # start rendering loop
    window.show()

if __name__ == '__main__':
    glfw.init()  # initialize windows system glfw
    main()
    glfw.terminate()


