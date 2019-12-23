#version 130

varying vec3 normal;
varying vec3 eye;

varying vec3 tex;

uniform sampler2D oneChanelTex;

void main() {
    float light = dot(normal, eye);// (-1, 1)

    vec4 finalColor = vec4(0.3, 0.4, 0.3, 0) + vec4(1, 0.9, 0.8, 0) * light;

    if (tex.x >= 0 && tex.x <= 1 && tex.y >= 0 && tex.y <= 1 && tex.z >= 0 && tex.z <= 1) {
        finalColor = vec4(
        texture(oneChanelTex, vec2(tex.x, tex.y))[0],
        texture(oneChanelTex, vec2(tex.x, tex.y))[0],
        texture(oneChanelTex, vec2(tex.x, tex.y))[0], 1);
    }

    gl_FragColor = finalColor;
}
