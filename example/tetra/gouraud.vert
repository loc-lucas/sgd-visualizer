#version 330 core

// input attribute variable, given per vertex
layout(location = 0) in vec3 position;
layout(location = 1) in vec3 color;

uniform mat4 projection, modelview;
out vec3 colorInterp;

out vec3 fragment_color;
void main(){
    colorInterp = color;
    gl_Position = projection * modelview * vec4(position, 1.0);
}
