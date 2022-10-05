#version 330 core

// receiving interpolated color for fragment shader
in vec3 color_interp;

// output fragment color for OpenGL
out vec4 out_color;

void main() {
    out_color = vec4(color_interp, 1);
}
