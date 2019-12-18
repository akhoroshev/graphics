#version 130

varying vec3 normal;
varying vec3 eye;

void main() {
    eye = normalize(vec3(gl_ModelViewMatrix * gl_Vertex));
    normal = normalize(gl_NormalMatrix * gl_Normal);
    gl_Position = ftransform();
}