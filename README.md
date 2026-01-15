# Look
An interactive visualizer for 3D objects


When run in IDLE, shapes can be rotated with the arrow keys and scaled down and up with A and D.


Shapes are stored in text files in the following format. Definitions of vertexes and faces are separated with the row "end-vertexes-begin-faces".

For vertexes: x-coordinate/y-coordinate/z-coordinate/number-of-neighboring-vertexes > id-of-vertex

For faces: id-of-vertex-1/id-of-vertex-2/.../id-of-vertex-n


Settings for running the visualizer are also stored in a text file. The settings are:

- size [width of the screen : positive integer] [height of the screen : positive integer]
	- recommended that width and height are equal
- bgcolor [color hex of the background : string]
- drawcolor [color hex for drawing the shape's outline : string]
- usefaces [whether the shape is drawn using its faces or neighboring vertexes (less restrictive): boolean]
- fillfaces [whether the shape's faces are colored in : boolean]
- shape [name of the file for the shape to be used : string]
- rotspeed [speed for rotating the shape : integer]
	- recommended 0-10
- scalespeed [multiplier for scaling the shape : float]
	- recommended 0-0.20
- interactive [whether the user can manipulate the shape (for running in IDLE) or the shape rotates by itself (for running without IDLE) : boolean]
- vertex_highlight [size of vertex highlight points : non-negative integer]
	- recommended small percentage of width and height