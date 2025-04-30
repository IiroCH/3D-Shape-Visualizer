"""
Class of faces (collections of points) of a 3D object.
Each face stores the vertexes defining it
and the coordinate of its center (as a vertex).
"""

from random import randint

from vertex import *


# Calculate the center of the given vertexes in 3D
# and return that center vertex
def calc_center(vertexes):
    x = 0
    y = 0
    z = 0
    for vertex in vertexes:
        x += vertex.x
        y += vertex.y
        z += vertex.z
    x = x / len(vertexes)
    y = y / len(vertexes)
    z = z / len(vertexes)

    return Vertex([x, y, z, 0])


class Face:

    def __init__(self, vertexes, color="#FF0000"):

        self.__vertexes = vertexes
        self.__color = color
        
        self.__center = calc_center(vertexes)

    @property
    def vertexes(self):
        return self.__vertexes

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
        self.__center = calc_center(self.vertexes)
