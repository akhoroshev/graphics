#version 130

varying vec3 normal;
varying vec3 eye;

varying vec3 tex;

uniform vec3 pt;
uniform vec3 oz;
uniform vec3 ox;
uniform vec3 oy;


void main() {
    eye = normalize(vec3(gl_ModelViewMatrix * gl_Vertex));
    normal = gl_Normal;
    gl_Position = ftransform();

    float u = dot(normalize(ox), (gl_Vertex.xyz - pt)) / length(ox) + 0.5;
    float v = dot(normalize(oy), (gl_Vertex.xyz - pt)) / length(oy) + 0.5;
    float w = dot(normalize(oz), (gl_Vertex.xyz - pt)) / length(oz) + 0.5;

    tex = vec3(u, v, w);
}