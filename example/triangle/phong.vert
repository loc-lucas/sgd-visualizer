#version 330 core

// input attribute variable, given per vertex
layout(location = 0) in vec3 vertex;
layout(location = 1) in vec3 color;
layout(location = 2) in vec3 normal;
uniform mat4 projection, modelview;

out vec3 normal_interp;
out vec3 vert_pos;
out vec3 color_interp;

void main(){
  color_interp = color;
  vec4 vert_pos4 = modelview * vec4(vertex, 1.0);
  vert_pos = vec3(vert_pos4) / vert_pos4.w;

  mat4 normal_matrix = transpose(inverse(modelview));
  normal_interp = vec3(normal_matrix * vec4(normal, 0.0));
  gl_Position = projection * vert_pos4;
}
