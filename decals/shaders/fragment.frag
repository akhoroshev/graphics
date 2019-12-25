#version 130

varying vec3 normal;
varying vec3 eye;

varying vec3 tex;

uniform sampler2D textureNormals;
uniform sampler2D textureAlpha;

uniform mat3 normalRotation;

uniform int saveNormal = 0;

void main() {
    if (saveNormal == 1) {
        gl_FragColor = vec4(normalize(normal), 0) * 0.5 + 0.5;
        return;
    }

    vec3 finalNormal = normal;
    vec4 finalColor = vec4(1, 0.9, 0.8, 0);

    if (tex.x >= 0 && tex.x <= 1 && tex.y >= 0 && tex.y <= 1 && tex.z >= 0 && tex.z <= 1) {
        vec3 tmpNormal = vec3(
        texture(textureNormals, vec2(tex.x, tex.y))[0],
        texture(textureNormals, vec2(tex.x, tex.y))[1],
        texture(textureNormals, vec2(tex.x, tex.y))[2]);
        float scale = texture(textureAlpha, vec2(tex.x, tex.y))[3];
        finalNormal = finalNormal * (1 - scale) +  normalRotation * tmpNormal * scale;
    }

    float light = dot(normalize(gl_NormalMatrix * finalNormal), eye);// (-1, 1)

    gl_FragColor = vec4(0.2, 0.4, 0.3, 0) + finalColor * light;
}
