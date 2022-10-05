#version 330 core

precision mediump float;
in vec3 frag_pos;       // Vertex position
in vec3 normal_interp;  // Surface normal

out vec4 FragColor;

uniform float zMin;
uniform float zRange;
uniform mat3 K_materials;
uniform mat3 I_light;

uniform float shininess; // Shininess
uniform vec3 light_pos; // Light position

// color gradient function
vec3 getColor(float z, float constrast) {

    // end values
    float startRed = 0.05;
    float endRed = 1.0;
    float startGreen = 0.3;
    float endGreen = 0.2;
    float startBlue = 0.7;
    float endBlue = 0.5;

    float percentFade = (z-zMin)/zRange;

    float diffRed = endRed - startRed;
    float diffGreen = endGreen - startGreen;
    float diffBlue = endBlue - startBlue;

    diffRed = (diffRed * percentFade + startRed)/(startRed + endRed);
    diffGreen = (diffGreen * percentFade + startGreen)/(startGreen + endGreen);
    diffBlue = (diffBlue * percentFade + startBlue)/(startBlue + endBlue);

    return vec3(diffRed, diffGreen, diffBlue)*constrast;
}

void main() {
    float contrast = 0.9;
    vec3 base_color = getColor(frag_pos.z, contrast);
    vec3 N = normalize(normal_interp);
    vec3 L = normalize(light_pos - frag_pos);
    vec3 R = reflect(-L, N);      // Reflected light vector
    vec3 V = normalize(-frag_pos); // Vector to viewer

    float specAngle = max(dot(R, V), 0.0);
    float specular = pow(specAngle, shininess);
    vec3 g = vec3(max(dot(L, N), 0.0), specular, 1.0);
    vec3 rgb = matrixCompMult(K_materials, I_light) * g + base_color;
    FragColor = vec4(rgb, 1.0);
}
