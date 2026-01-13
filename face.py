"""
Class of faces of a 3D object.
Each face stores the vertices defining it
and the coordinate of its center (as a vertex).
"""

from random import randint

from vertex import *


# Calculate the center of the given vertices in 3D
# and return that center vertex
def calc_center(vertices):
    x = 0
    y = 0
    z = 0
    for vertex in vertices:
        x += vertex.x
        y += vertex.y
        z += vertex.z
    x = x / len(vertices)
    y = y / len(vertices)
    z = z / len(vertices)

    return Vertex([x, y, z, 0])


class Face:

    def __init__(self, vertices, color="#FF0000"):

        self.__vertices = vertices
        self.__color = color
        
        self.__center = calc_center(vertices)

    @property
    def vertices(self):
        return self.__vertices

    @property
    def color(self):
        return self.__color

    @property
    def center(self):
        return self.__center

    def __eq__(self, other):
        return self.center == other.center

    # Recalculate the face's center
    def update_center(self):
        self.__center = calc_center(self.vertices)
