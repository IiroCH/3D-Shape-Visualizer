"""
Class for object renderers

Coordinates:
X: towards the screen
Y: left to right
Z: bottom to top
"""

import sys

from time import sleep

from random import randint

from turtle import *

from pynput import keyboard

from shape import *

from utils import *

# Open a shape into a window and listen for movement input
def start_visualization():

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

    # Set defaults for parameters
    width = 1000
    height = 1000
    bgcolor = "#000000"
    drawcolor = "#FFFFFF"
    fillfaces = False
    usefaces = False
    shape = None
    rotspeed = 1
    scalespeed = 0.1
    interactive = False
    vertex_size = 0

    # Load settings from a file
    try:
        settings_file = open("settings.txt", mode='r')
    except OSError:
        print("Error: Settings file not found")
        sys.exit("Error: Settings file not found")

    for setting in settings_file:
        tokens = setting.split()

        match tokens[0]:
            case "size":
                # Set screen size
                width = int(tokens[1])
                height = int(tokens[2])
            case "bgcolor":
                # Set background color
                bgcolor = tokens[1]
            case "drawcolor":
                # Set turtle draw color
                drawcolor = tokens[1]
            case "fillfaces":
                # Set whether the shape's faces are colored in
                if tokens[1] == "true":
                    fillfaces = True
                if tokens[1] == "false":
                    fillfaces = False
            case "usefaces":
                # Set whether faces or vertices
                # are used for drawing the shape
                if tokens[1] == "true":
                    usefaces = True
                if tokens[1] == "false":
                    usefaces = False
            case "shape":
                # Load shape from a file (required)
                try:
                    shape_file = open(f"shapes/{tokens[1]}.txt", mode='r')
                except OSError:
                    print("Error: Shape file not found")
                    sys.exit("Error: Shape file not found")
                shape = build_shape(shape_file)
                shape_file.close()
            case "rotspeed":
                # Set the rotation speed for the shape
                rotspeed = int(tokens[1])
            case "scalespeed":
                # Set the scaling speed for the shape
                scalespeed = float(tokens[1])
            case "interactive":
                # Set whether the shape rotates
                # by itself or by user input
                if tokens[1] == "true":
                    interactive = True
                if tokens[1] == "false":
                    interactive = False
            case "vertex_highlight":
                # Set the size for the vertex highlights
                vertex_size = int(tokens[1])

    settings_file.close()

    # Apply loaded settings
    screen.setup(width, height)
    turtle.color(drawcolor)
    screen.bgcolor(bgcolor)

    # Calculate the windows "depth" and multipliers for drawing
    window_depth = (screen.window_height() + screen.window_width()) / 2
    h_mult = 0.5 * screen.window_height() / 2
    w_mult = 0.5 * screen.window_width() / 2
    d_mult = 0.5 * window_depth / 2

    # Print starting conditions
    print("Settings:")
    print(f"Draw color: {drawcolor}")
    print(f"Background color: {bgcolor}")
    print()
    print("Window:")
    print(f"Width: {screen.window_width()}")
    print(f"Height: {screen.window_height()}")
    print(f"Depth: {window_depth}")
    print()
    print(f"Starting vertex coordinates ({len(shape.vertices)} in total):")
    for vertex in shape.vertices:
        print(f"X: {vertex.x}\tY: {vertex.y}\tZ: {vertex.z}")


    # Calculate the negative distance from
    # the face's center to the "camera"
    def dist_from_cam(face):
        return -face.center.calc_dist(Vertex([window_depth / 2, 0, 0, 0]))

    # Redraw the screen
    def refresh():

        turtle.clear()

        if usefaces:
            if fillfaces:
                for face in sorted(shape.faces, key=dist_from_cam):
                    vertices = face.vertices
                    turtle.teleport(vertices[0].y * w_mult, vertices[0].z * h_mult)
                    turtle.fillcolor(face.color)
                    turtle.begin_fill()
                    for i in range(1, len(vertices)):
                        turtle.dot(vertex_size)
                        turtle.goto(vertices[i].y * w_mult, vertices[i].z * h_mult)
                    turtle.dot(vertex_size)
                    turtle.goto(vertices[0].y * w_mult, vertices[0].z * h_mult)
                    turtle.end_fill()
            else:
                for face in shape.faces:
                    vertices = face.vertices
                    turtle.teleport(vertices[0].y * w_mult, vertices[0].z * h_mult)
                    turtle.dot(vertex_size)
                    for i in range(1, len(vertices)):
                        turtle.goto(vertices[i].y * w_mult, vertices[i].z * h_mult)
                        turtle.dot(vertex_size)
                    turtle.goto(vertices[0].y * w_mult, vertices[0].z * h_mult)
        else:
            for vertex in shape.vertices:
                turtle.teleport(vertex.y * w_mult, vertex.z * h_mult)
                turtle.dot(max([20, vertex_size]))

                neighbours = vertex.neighbours(shape.vertices)
                for neighbour in neighbours:
                    turtle.goto(neighbour.y * w_mult, neighbour.z * h_mult)
                    turtle.teleport(vertex.y * w_mult, vertex.z * h_mult)

        screen.update()

    # Rotate shape up
    def rot_up():
        for vertex in shape.vertices:
            vertex.rotate(0, rotspeed)
        for face in shape.faces:
            face.update_center()
        refresh()

    # Rotate shape down
    def rot_down():
        for vertex in shape.vertices:
            vertex.rotate(0, -rotspeed)
        for face in shape.faces:
            face.update_center()
        refresh()

    # Rotate shape right
    def rot_right():
        for vertex in shape.vertices:
            vertex.rotate(rotspeed, 0)
        for face in shape.faces:
            face.update_center()
        refresh()

    # Rotate shape left
    def rot_left():
        for vertex in shape.vertices:
            vertex.rotate(-rotspeed, 0)
        for face in shape.faces:
            face.update_center()
        refresh()

    # Scale shape up
    def scale_up():
        for vertex in shape.vertices:
            vertex.scale(scalespeed, d_mult)
        refresh()

    # Scale shape down
    def scale_down():
        for vertex in shape.vertices:
            vertex.scale(-scalespeed, d_mult)
        refresh()


    # Draw shape's starting state
    refresh()

    if interactive:
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