"""
Class of 3D objects.
Each shape stores the faces and vertices defining it.
"""

from math import sqrt
phi = (1 + sqrt(5)) / 2

from face import *

from utils import *

# Construct a shape object from data in the given file
def build_shape(shape_file):
    vertex_table = {}
    faces = []
    parsing_faces = False
    for line in shape_file:
        if line.strip() == "end-vertices-begin-faces":
            parsing_faces = True
        elif not parsing_faces:
            tokens = line.strip().split(" > ")
            vertexdata = tokens[0].split("/")

            for i in range(len(vertexdata)-1):
                if vertexdata[i].find("phi") != -1:
                    vertexdata[i] = vertexdata[i].replace("phi", str(phi))
                vertexdata[i] = float(vertexdata[i])
            vertexdata[-1] = int(vertexdata[-1])
            
            vertex_table[int(tokens[1])] = Vertex(vertexdata)
        elif parsing_faces:
            vertices = []
            for vertex in line.split("/"):
                vertices.append(vertex_table[int(vertex)])
            faces.append(Face(vertices, random_color()))
    return Shape(faces)

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
