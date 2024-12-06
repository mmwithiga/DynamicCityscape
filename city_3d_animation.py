import pygame

from pygame.locals import *

from OpenGL.GL import *

from OpenGL.GLU import *

import random

import math



# Initialize Pygame and OpenGL

pygame.init()

WIDTH, HEIGHT = 1024, 768

pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)

pygame.display.set_caption("3D City Animation")



def init_gl():

    glEnable(GL_DEPTH_TEST)

    glClearColor(0.5, 0.5, 1.0, 1.0)  # Sky blue background

    

    # Set up the camera and perspective

    glMatrixMode(GL_PROJECTION)

    glLoadIdentity()

    gluPerspective(45, (WIDTH/HEIGHT), 0.1, 100.0)

    

    glMatrixMode(GL_MODELVIEW)

    glLoadIdentity()

    glTranslatef(0.0, -5.0, -45.0)



class Building3D:

    def __init__(self, x, z):

        self.x = x

        self.z = z

        self.height = random.uniform(5, 15)

        self.width = 2.0

        self.depth = 2.0

        self.color = (random.uniform(0.3, 0.5),

                     random.uniform(0.3, 0.5),

                     random.uniform(0.3, 0.5))



    def draw(self):

        glPushMatrix()

        glTranslatef(self.x, 0, self.z)

        

        # Draw building as a cube

        glBegin(GL_QUADS)

        glColor3f(*self.color)

        

        # Front face

        glVertex3f(-self.width/2, 0, -self.depth/2)

        glVertex3f(self.width/2, 0, -self.depth/2)

        glVertex3f(self.width/2, self.height, -self.depth/2)

        glVertex3f(-self.width/2, self.height, -self.depth/2)

        

        # Back face

        glVertex3f(-self.width/2, 0, self.depth/2)

        glVertex3f(self.width/2, 0, self.depth/2)

        glVertex3f(self.width/2, self.height, self.depth/2)

        glVertex3f(-self.width/2, self.height, self.depth/2)

        

        # Right face

        glVertex3f(self.width/2, 0, -self.depth/2)

        glVertex3f(self.width/2, 0, self.depth/2)

        glVertex3f(self.width/2, self.height, self.depth/2)

        glVertex3f(self.width/2, self.height, -self.depth/2)

        

        # Left face

        glVertex3f(-self.width/2, 0, -self.depth/2)

        glVertex3f(-self.width/2, 0, self.depth/2)

        glVertex3f(-self.width/2, self.height, self.depth/2)

        glVertex3f(-self.width/2, self.height, -self.depth/2)

        

        # Top face

        glVertex3f(-self.width/2, self.height, -self.depth/2)

        glVertex3f(self.width/2, self.height, -self.depth/2)

        glVertex3f(self.width/2, self.height, self.depth/2)

        glVertex3f(-self.width/2, self.height, self.depth/2)

        glEnd()

        

        glPopMatrix()



def draw_ground():

    glBegin(GL_QUADS)

    glColor3f(0.2, 0.2, 0.2)  # Dark gray

    glVertex3f(-50, -0.1, -50)

    glVertex3f(50, -0.1, -50)

    glVertex3f(50, -0.1, 50)

    glVertex3f(-50, -0.1, 50)

    glEnd()



def main():

    init_gl()

    clock = pygame.time.Clock()

    

    # Create buildings in a grid

    buildings = []

    for x in range(-20, 21, 4):

        for z in range(-20, 21, 4):

            buildings.append(Building3D(x, z))

    

    rotation = 0

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()

                return



        # Clear screen and depth buffer

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        

        # Reset modelview matrix

        glLoadIdentity()

        glTranslatef(0.0, -5.0, -45.0)

        

        # Apply camera rotation

        glRotatef(15, 1, 0, 0)  # Tilt view

        glRotatef(rotation, 0, 1, 0)  # Rotate view

        

        # Draw ground

        draw_ground()

        

        # Draw buildings

        for building in buildings:

            building.draw()

        

        # Update rotation

        rotation += 0.5

        

        pygame.display.flip()

        clock.tick(60)



if __name__ == "__main__":

    main() 


