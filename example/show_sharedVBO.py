from libs.window import Window
import glfw                         # lean windows system wrapper for OpenGL
from example.triangle.TriangleSharedVBO import (TriangleSharedVBO)

def main():
    window = Window()
    window.add(TriangleSharedVBO())

    # start rendering loop
    window.show()

if __name__ == '__main__':
    glfw.init()  # initialize windows system glfw
    main()
    glfw.terminate()


