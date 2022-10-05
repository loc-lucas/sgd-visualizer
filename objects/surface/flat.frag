#version 330 core

in vec3 frag_pos;

out vec4 FragColor;

uniform float zMin;
uniform float zRange;

// color gradient function
vec4 getColor(float z, float constrast) {

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

    diffRed = (diffRed * percentFade) + startRed;
    diffGreen = (diffGreen * percentFade) + startGreen;
    diffBlue = (diffBlue * percentFade) + startBlue;

    return vec4(diffRed * constrast, diffGreen * constrast, diffBlue * constrast, 1.0);
}

void main() {
    float contrast = 1.2;
    FragColor = getColor(frag_pos.z, contrast);
}
