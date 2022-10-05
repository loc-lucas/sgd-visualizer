#version 330 core

layout(location = 0) in vec3 vertex;

uniform mat4 projection, modelview;

void main() {
    gl_Position = projection * modelview * vec4(vertex, 1.0);
}
