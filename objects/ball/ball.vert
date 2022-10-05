#version 330 core

// input attribute variable, given per vertex
layout(location = 0) in vec3 vertex;
layout(location = 1) in vec3 color;

uniform mat4 projection, modelview;
out vec3 fragment_color;

void main(){
  fragment_color = color;
  vec4 vert_pos4 = modelview * vec4(vertex, 1.0);
  vert_pos4 = vert_pos4 / vert_pos4.w;

  gl_Position = projection * vert_pos4;
}
