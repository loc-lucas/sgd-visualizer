from libs.window import Window
import glfw                         # lean windows system wrapper for OpenGL
from example.patch import (LightenPatch)

def main():
    window = Window()

    #window.add(BadPatch())
    #window.add(StillBadPatch())
    #window.add(SimplePatch())
    #window.add(Patch())
    #window.add(TexturedPatch())
    window.add(LightenPatch())
    # start rendering loop
    window.show()

if __name__ == '__main__':
    glfw.init()  # initialize windows system glfw
    main()
    glfw.terminate()


