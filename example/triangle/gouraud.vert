#version 330 core

// input attribute variable, given per vertex
layout(location = 0) in vec3 vertex;
layout(location = 1) in vec3 color;

out vec3 fragment_color;
void main(){
    fragment_color = vec3(color);
    gl_Position = vec4(vertex, 1.0);
}
