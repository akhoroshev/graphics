import sys

import pywavefront

from model import ModelView


def main(path):
    obj = pywavefront.Wavefront(path, create_materials=True)
    vertex_array = None
    vertex_size = None
    vertex_format = None
    for (name, material) in obj.materials.items():
        vertex_array = material.vertices
        vertex_size = material.vertex_size
        vertex_format = material.vertex_format
    if vertex_array is None:
        raise ValueError('vertex array not found')
    model = ModelView(vertex_array, vertex_format, vertex_size, fov=75)
    model.show()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        obj_file = 'models/FinalBaseMesh.obj'
    else:
        obj_file = sys.argv[1]
    main(obj_file)
