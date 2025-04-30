"""
Class of 3D objects (collections of vertexes and faces).
Each shape stores the faces and vertexes defining it.
"""

from face import *

class Shape:

    def __init__(self, faces):
        self.__faces = faces

        vertex_list = []
        for face in faces:
            for vertex in face.vertexes:
                if vertex not in vertex_list:
                    vertex_list.append(vertex)
        self.__vertexes = vertex_list

    @property
    def faces(self):
        return self.__faces

    @property
    def vertexes(self):
        return self.__vertexes
