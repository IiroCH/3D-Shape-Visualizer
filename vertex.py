"""
Class of vertexes (points) of a 3D object.
Each vertex stores its coordinates (x, y, z)
and its number of neighbouring vertexes (stored as "edges").


Coordinates:

X: towards the screen
Y: left to right
Z: bottom to top

R: distance from origin (center)
LONG: angle left or right
LAT: angle down or up
"""

import math


# Convert cartesian coordinates to polar
def to_polar(x, y, z):
    r = math.sqrt(x*x + y*y + z*z)

    if x == 0 and y == 0:
        long = 0
    else:
        long = math.degrees(math.acos(x / math.sqrt(x*x + y*y)))
        if y < 0:
            long *= -1

    lat = math.degrees(math.acos(z / r))
                            
    return r, long, lat


# Convert polar coordinates to cartesian
def to_cartesian(r, long, lat):
    x = r * math.sin(math.radians(lat)) * math.cos(math.radians(long))
        
    y = r * math.sin(math.radians(lat)) * math.sin(math.radians(long))
        
    z = r * math.cos(math.radians(lat))

    return x, y, z
        


class Vertex:

    def __init__(self, datalist):

        self.__x = datalist[0]
        self.__y = datalist[1]
        self.__z = datalist[2]
        self.__edges = datalist[3]

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, new_x):
        self.__x = new_x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, new_y):
        self.__y = new_y

    @property
    def z(self):
        return self.__z

    @z.setter
    def z(self, new_z):
        self.__z = new_z

    @property
    def edges(self):
        return self.__edges

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    # Calculate distance to other vertex
    def calc_dist(self, other):
        return math.sqrt( (self.x-other.x)**2 + (self.y-other.y)**2 + (self.z-other.z)**2 )

    # Return neighbouring vertexes
    def neighbours(self, vertexes):
        vertexes = sorted(vertexes, key=self.calc_dist)
        return vertexes[1:self.edges+1]

    # Rotate the vertex around the origin
    def rotate(self, h_angle, v_angle):

        # Horizontal rotation
        r, long, lat = to_polar(self.x, self.y, self.z)

        long += h_angle

        self.x, self.y, self.z = to_cartesian(r, long, lat)

        # Vertical rotation
        rm_x, rm_y, rm_z = self.x, self.z, -self.y
        
        r, long, lat = to_polar(rm_x, rm_y, rm_z)
        
        long += v_angle

        rm_x, rm_y, rm_z = to_cartesian(r, long, lat)

        self.x, self.y, self.z = rm_x, -rm_z, rm_y

    # Scale the vertex from the origin
    def scale(self, multiplier, max_scale):
        r, long, lat = to_polar(self.x, self.y, self.z)

        new_r = r * (1 + multiplier)
        
        if new_r > 0 and new_r <= max_scale:
            r = new_r

        self.x, self.y, self.z = to_cartesian(r, long, lat)
