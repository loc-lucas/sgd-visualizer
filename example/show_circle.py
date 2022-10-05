from libs.window import Window
# from shapes import *
import glfw                         # lean windows system wrapper for OpenGL
from example.circle import (Circle)

def main():
    window = Window()

    #window.add(BadPatch())
    #window.add(StillBadPatch())
    #window.add(SimplePatch())
    #window.add(Patch())
    #window.add(TexturedPatch())
    window.add(Circle(100))
    # window.add(TexturedCircle(100))

    # start rendering loop
    window.show()

if __name__ == '__main__':
    glfw.init()  # initialize windows system glfw
    main()
    glfw.terminate()


