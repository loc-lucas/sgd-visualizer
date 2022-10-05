#version 330 core

// input attribute variable, given per vertex
layout(location = 0) in vec3 vertex;

void main() {
    gl_Position = vec4(vertex, 1);
}
