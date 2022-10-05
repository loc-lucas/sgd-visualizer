#version 330 core

layout(location = 0) in vec3 vertex;
layout(location = 1) in vec3 normal;
uniform mat4 projection, modelview;

out vec3 frag_pos;
out vec3 normal_interp;

void main()
{
    gl_Position = projection * modelview * vec4(vertex, 1.0);
    mat4 normal_matrix = transpose(inverse(modelview));
    normal_interp = vec3(normal_matrix * vec4(normal, 0.0));
    frag_pos = vertex;
}