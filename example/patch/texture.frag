#version 330 core

precision mediump float;
in vec3 normal_interp;  // Surface normal
in vec3 vert_pos;       // Vertex position
in vec3 color_interp;
in vec2 texcoord_interp;

uniform sampler2D texture1;
out vec4 fragColor;


void main() {
  vec4 texture_color;
  texture_color = texture(texture1, texcoord_interp);

  fragColor = texture_color;
}
