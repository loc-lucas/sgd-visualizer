#version 330 core

layout(location = 0) in vec3 vertex;
uniform mat4 projection, modelview;

out vec3 frag_pos;

void main()
{
    gl_Position = projection * modelview * vec4(vertex, 1.0);
    frag_pos = vertex;
}