"""
Command line interface class
"""

from renderer import *

class CLI:

    def __init__(self):
        pass

    # Read input from the command line
    def read(self):
        print("LOOK\nVERSION 0")

        while True:
            line = input("> ")
            if line.lower() == "exit":
                break
            print(line)
        #renderer = Renderer()
        #renderer.start_visualization()
