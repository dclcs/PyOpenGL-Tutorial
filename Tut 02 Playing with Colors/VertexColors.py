# Mario Rosasco, 2016
# adapted from VertexColors.cpp, Copyright (C) 2010-2012 by Jason L. McKesson
# This file is licensed under the MIT License.

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from array import array
import os
import sys
import numpy as np
from ctypes import c_void_p
from framework import *

# A 1-D array of 3 4-D vertices (X,Y,Z,W)
# Note that this must be a numpy array, since as of 
# 170111 support for lists has not been implemented.
vertexPositions = np.array(
    [0.0, 0.5, 0.0, 1.0,
    0.5, -0.366, 0.0, 1.0, 
    -0.5, -0.366, 0.0, 1.0,
    1.0, 0.0, 0.0, 1.0,
    0.0, 1.0, 0.0, 1.0,
    0.0, 0.0, 1.0, 1.0],
    dtype='float32'
)

vertexDim = 4
nVertices = 3

# Global variable to represent the compiled shader program, written in GLSL
theProgram = None

# Global variable to represent the buffer that will hold the position vectors
vertexBufferObject = None

# Set up the list of shaders, and call functions to compile them
def initializeProgram():
    shaderList = []
    
    shaderList.append(loadShader(GL_VERTEX_SHADER, "VertexColors.vert"))
    shaderList.append(loadShader(GL_FRAGMENT_SHADER, "VertexColors.frag"))
    
    global theProgram 
    theProgram = createProgram(shaderList)
    
    for shader in shaderList:
        glDeleteShader(shader)

# Set up the vertex buffer that will store our vertex coordinates for OpenGL's access
def initializeVertexBuffer():
    global vertexBufferObject
    vertexBufferObject = glGenBuffers(1)
    
    glBindBuffer(GL_ARRAY_BUFFER, vertexBufferObject)
    glBufferData( # PyOpenGL allows for the omission of the size parameter
        GL_ARRAY_BUFFER,
        vertexPositions,
        GL_STATIC_DRAW
    )
    glBindBuffer(GL_ARRAY_BUFFER, 0)

# Initialize the OpenGL environment
def init():
    initializeProgram()
    initializeVertexBuffer()
    glBindVertexArray(glGenVertexArrays(1))

# Called to update the display. 
# Because we are using double-buffering, glutSwapBuffers is called at the end
# to write the rendered buffer to the display.
def display():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)
    
    glUseProgram(theProgram)
    
    glBindBuffer(GL_ARRAY_BUFFER, vertexBufferObject)
    glEnableVertexAttribArray(0)
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(0, vertexDim, GL_FLOAT, GL_FALSE, 0, None)
     # a ctype void pointer must be used to pass in the offset into the bound GL_ARRAY_BUFFER
     # also note that python's underlying float type is usally 64-bit, but
     # we have specified that our vertex array contains float32 data.
    colorOffset = c_void_p(vertexDim*nVertices*4)
    glVertexAttribPointer(1, vertexDim, GL_FLOAT, GL_FALSE, 0, colorOffset)
    
    glDrawArrays(GL_TRIANGLES, 0, nVertices)
    
    glDisableVertexAttribArray(0)
    glDisableVertexAttribArray(1)
    glUseProgram(0)
    
    glutSwapBuffers()
    glutPostRedisplay()

# keyboard input handler: exits the program if 'esc' is pressed
def keyboard(key, x, y):
    if ord(key) == 27: # ord() is needed to get the keycode
        glutLeaveMainLoop()
        return
    
# Called whenever the window's size changes (including once when the program starts)
def reshape(w, h):
    glViewport(0, 0, w, h)
    
# The main function
def main():
    glutInit()
    displayMode = GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH | GLUT_STENCIL;
    glutInitDisplayMode (displayMode)
    
    width = 500;
    height = 500;
    glutInitWindowSize (width, height)
    
    glutInitWindowPosition (300, 200)
    
    window = glutCreateWindow("Tutorial Window")
    
    init()
    glutDisplayFunc(display) 
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    
    glutMainLoop();

if __name__ == '__main__':
    main()
