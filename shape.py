"""
Class of 3D objects.
Each shape stores the faces and vertices defining it.
"""

from face import *

class Shape:

    def __init__(self, faces):
        self.__faces = faces

        vertex_list = []
        for face in faces:
            for vertex in face.vertices:
                if vertex not in vertex_list:
                    vertex_list.append(vertex)
        self.__vertices = vertex_list

    @property
    def faces(self):
        return self.__faces

    @property
    def vertices(self):
        return self.__vertices
