#version 130

varying vec3 normal;
varying vec3 eye;

uniform float noise = 1;

void main() {
    float light = dot(normal, eye); // (-1, 1)
    if (light > noise) {
        discard;
    }
    gl_FragColor = vec4(0.3, 0.4, 0.3, 0);
    gl_FragColor += vec4(1, 0.9, 0.8, 0) * light;
}
