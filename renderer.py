"""
Class for object renderers

Coordinates:
X: towards the screen
Y: left to right
Z: bottom to top
"""

from time import sleep

from random import randint

from turtle import *

from pynput import keyboard

from shape import *

from utils import *


# Open a shape into a window and listen for movement input


class Renderer:

    def __init__(self):
        # Set defaults for parameters
        self.__width = 720
        self.__height = 720
        self.__bgcolor = "#000000"
        self.__drawcolor = "#FFFFFF"
        self.__fillfaces = False
        self.__usefaces = False
        self.__shape = None
        self.__rotspeed = 1
        self.__scalespeed = 0.1
        self.__interactive = True
        self.__vertex_size = 0

        self.__load_settings()

    # Load settings from a file
    def __load_settings(self):
        try:
            settings_file = open("settings.txt", mode='r')
        except OSError:
            return

        for setting in settings_file:
            tokens = setting.split()

            match tokens[0]:
                case "size":
                    # Set screen size
                    self.__width = int(tokens[1])
                    self.__height = int(tokens[2])
                case "bgcolor":
                    # Set background color
                    self.__bgcolor = tokens[1]
                case "drawcolor":
                    # Set turtle draw color
                    self.__drawcolor = tokens[1]
                case "fillfaces":
                    # Set whether the shape's faces are colored in
                    if tokens[1] == "true":
                        self.__fillfaces = True
                    if tokens[1] == "false":
                        self.__fillfaces = False
                case "usefaces":
                    # Set whether faces or vertices
                    # are used for drawing the shape
                    if tokens[1] == "true":
                        self.__usefaces = True
                    if tokens[1] == "false":
                        self.__usefaces = False
                case "shape":
                    # Load shape from a file (required)
                    try:
                        shape_file = open(f"shapes/{tokens[1]}.txt", mode='r')
                    except OSError:
                        continue
                    self.__shape = build_shape(shape_file)
                    shape_file.close()
                case "rotspeed":
                    # Set the rotation speed for the shape
                    self.__rotspeed = int(tokens[1])
                case "scalespeed":
                    # Set the scaling speed for the shape
                    self.__scalespeed = float(tokens[1])
                case "interactive":
                    # Set whether the shape rotates
                    # by itself or by user input
                    if tokens[1] == "true":
                        self.__interactive = True
                    if tokens[1] == "false":
                        self.__interactive = False
                case "vertex_highlight":
                    # Set the size for the vertex highlights
                    self.__vertex_size = int(tokens[1])

        settings_file.close()
    
    def start_visualization(self):

        # Create a turtle screen
        screen = Screen()
        screen.title("3D Object Visualizer")
        tracer(0)

        # Create a turtle
        turtle = Turtle()
        turtle.hideturtle()
        turtle.speed(0)
        turtle.pensize(1)
        turtle.pendown()

        # Apply loaded settings
        screen.setup(self.__width, self.__height)
        turtle.color(self.__drawcolor)
        screen.bgcolor(self.__bgcolor)

        # Calculate the windows "depth" and multipliers for drawing
        window_depth = (screen.window_height() + screen.window_width()) / 2
        h_mult = 0.5 * screen.window_height() / 2
        w_mult = 0.5 * screen.window_width() / 2
        d_mult = 0.5 * window_depth / 2

        # Print starting conditions
        print("Settings:")
        print(f"Draw color: {self.__drawcolor}")
        print(f"Background color: {self.__bgcolor}")
        print()
        print("Window:")
        print(f"Width: {screen.window_width()}")
        print(f"Height: {screen.window_height()}")
        print(f"Depth: {window_depth}")
        print()
        print(f"Starting vertex coordinates ({len(self.__shape.vertices)} in total):")
        for vertex in self.__shape.vertices:
            print(f"X: {vertex.x}\tY: {vertex.y}\tZ: {vertex.z}")


        # Calculate the negative distance from
        # the face's center to the "camera"
        def dist_from_cam(face):
            return -face.center.calc_dist(Vertex([window_depth / 2, 0, 0, 0]))

        # Redraw the screen
        def refresh():

            turtle.clear()

            if self.__usefaces:
                if self.__fillfaces:
                    for face in sorted(self.__shape.faces, key=dist_from_cam):
                        vertices = face.vertices
                        turtle.teleport(vertices[0].y * w_mult, vertices[0].z * h_mult)
                        turtle.fillcolor(face.color)
                        turtle.begin_fill()
                        for i in range(1, len(vertices)):
                            turtle.dot(self.__vertex_size)
                            turtle.goto(vertices[i].y * w_mult, vertices[i].z * h_mult)
                        turtle.dot(self.__vertex_size)
                        turtle.goto(vertices[0].y * w_mult, vertices[0].z * h_mult)
                        turtle.end_fill()
                else:
                    for face in self.__shape.faces:
                        vertices = face.vertices
                        turtle.teleport(vertices[0].y * w_mult, vertices[0].z * h_mult)
                        turtle.dot(self.__vertex_size)
                        for i in range(1, len(vertices)):
                            turtle.goto(vertices[i].y * w_mult, vertices[i].z * h_mult)
                            turtle.dot(self.__vertex_size)
                        turtle.goto(vertices[0].y * w_mult, vertices[0].z * h_mult)
            else:
                for vertex in self.__shape.vertices:
                    turtle.teleport(vertex.y * w_mult, vertex.z * h_mult)
                    turtle.dot(max([20, self.__vertex_size]))

                    neighbours = vertex.neighbours(self.__shape.vertices)
                    for neighbour in neighbours:
                        turtle.goto(neighbour.y * w_mult, neighbour.z * h_mult)
                        turtle.teleport(vertex.y * w_mult, vertex.z * h_mult)

            screen.update()

        # Rotate shape up
        def rot_up():
            for vertex in self.__shape.vertices:
                vertex.rotate(0, self.__rotspeed)
            for face in self.__shape.faces:
                face.update_center()
            refresh()

        # Rotate shape down
        def rot_down():
            for vertex in self.__shape.vertices:
                vertex.rotate(0, -self.__rotspeed)
            for face in self.__shape.faces:
                face.update_center()
            refresh()

        # Rotate shape right
        def rot_right():
            for vertex in self.__shape.vertices:
                vertex.rotate(self.__rotspeed, 0)
            for face in self.__shape.faces:
                face.update_center()
            refresh()

        # Rotate shape left
        def rot_left():
            for vertex in self.__shape.vertices:
                vertex.rotate(-self.__rotspeed, 0)
            for face in self.__shape.faces:
                face.update_center()
            refresh()

        # Scale shape up
        def scale_up():
            for vertex in self.__shape.vertices:
                vertex.scale(self.__scalespeed, d_mult)
            refresh()

        # Scale shape down
        def scale_down():
            for vertex in self.__shape.vertices:
                vertex.scale(-self.__scalespeed, d_mult)
            refresh()


        # Draw shape's starting state
        refresh()

        if self.__interactive:
            # Assign keys for manipulating the shape
            screen.onkeypress(rot_up, "Up")
            screen.onkeypress(rot_down, "Down")
            screen.onkeypress(rot_right, "Right")
            screen.onkeypress(rot_left, "Left")
            screen.onkeypress(scale_up, "d")
            screen.onkeypress(scale_down, "a")

            screen.listen()
        else:
            # Move the shape around
            for i in range(randint(1, 3)):
                rot_down()
            while True:
                rot_right()
                sleep(1/60)