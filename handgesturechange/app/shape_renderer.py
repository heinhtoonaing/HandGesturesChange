from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
import numpy as np

class ShapeRenderer:
    def __init__(self, display_size=(800, 600)):
        """
        Initializes the ShapeRenderer with OpenGL settings.

        Args:
            display_size (tuple): The size of the display window.
        """
        self.display_size = display_size
        self.initialize_opengl()
        self.cube_position = [0.0, 0.0, -5.0]  # Starting position
        self.cube_rotation = [0.0, 0.0, 0.0]  # Starting rotation

    def initialize_opengl(self):
        """
        Initializes OpenGL settings.
        """
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (self.display_size[0] / self.display_size[1]), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        glTranslatef(0.0, 0.0, -5)

    def clear(self):
        """
        Clears the OpenGL buffers.
        """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def render_shape(self, shape_type):
        """
        Renders the specified shape.

        Args:
            shape_type (str): The type of shape to render ("circle", "square", "triangle", "cube", "none").
        """
        self.clear()

        if shape_type == "circle":
            self.draw_circle()
        elif shape_type == "square":
            self.draw_square()
        elif shape_type == "triangle":
            self.draw_triangle()
        elif shape_type == "cube":
            self.render_cube()  # Render cube
        else:
            # Optionally, render nothing or a default shape
            pass

        glFlush()

    def draw_circle(self):
        """
        Draws a circle using triangle fan.
        """
        glColor3f(1.0, 0.0, 0.0)  # Red
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(0.0, 0.0)  # Center
        num_segments = 50
        radius = 1.0
        for i in range(num_segments + 1):
            angle = 2 * np.pi * i / num_segments
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            glVertex2f(x, y)
        glEnd()

    def draw_square(self):
        """
        Draws a square.
        """
        glColor3f(0.0, 1.0, 0.0)  # Green
        glBegin(GL_QUADS)
        glVertex3f(-1.0, 1.0, 0.0)
        glVertex3f(1.0, 1.0, 0.0)
        glVertex3f(1.0, -1.0, 0.0)
        glVertex3f(-1.0, -1.0, 0.0)
        glEnd()

    def draw_triangle(self):
        """
        Draws a triangle.
        """
        glColor3f(0.0, 0.0, 1.0)  # Blue
        glBegin(GL_TRIANGLES)
        glVertex3f(0.0, 1.0, 0.0)
        glVertex3f(-1.0, -1.0, 0.0)
        glVertex3f(1.0, -1.0, 0.0)
        glEnd()

    def render_cube(self):
        """
        Renders a cube from the cube.obj file.
        """
        glPushMatrix()  # Save the current matrix state
        glTranslatef(*self.cube_position)  # Move the cube
        glRotatef(self.cube_rotation[0], 1, 0, 0)  # Rotate around X
        glRotatef(self.cube_rotation[1], 0, 1, 0)  # Rotate around Y
        glRotatef(self.cube_rotation[2], 0, 0, 1)  # Rotate around Z

        vertices, faces = self.load_obj(r'C:\Users\Hein Htoo Naing\Computer_Vision\handgesturechange\assets\Cube.obj')  # Adjust the path as needed
        glBegin(GL_TRIANGLES)
        for face in faces:
            for vertex in face:
                glVertex3fv(vertices[vertex])
        glEnd()

        glPopMatrix()  # Restore the previous matrix state

    def load_obj(self, filename):
        """
        Loads a 3D object from an OBJ file.

        Args:
            filename (str): The path to the OBJ file.

        Returns:
            tuple: vertices and faces of the object.
        """
        vertices = []
        faces = []
        with open(filename, 'r') as file:
            for line in file:
                if line.startswith('v '):
                    vertex = list(map(float, line.strip().split()[1:]))
                    vertices.append(vertex)
                elif line.startswith('f '):
                    face = [int(i.split('/')[0]) - 1 for i in line.strip().split()[1:]]  # OBJ indices are 1-based
                    faces.append(face)
        return vertices, faces

    def close(self):
        """
        Closes the renderer. Placeholder for any cleanup if necessary.
        """
        pass
