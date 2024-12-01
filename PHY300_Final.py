'''
Authors: Adrian Liborio and Julio De Jesus 
Date: 11.29.2024
Description: ...
Credits: ...
'''
#all imported modules
import pymunk as pm 
import math
import pygame  
import pymunk.pygame_util
import matplotlib.pyplot as plt

# hjhj
#initialize pygame
pygame.init()

WIDTH, HEIGHT = 800, 600 #width and height of the window
window = pygame.display.set_mode((WIDTH, HEIGHT)) #create the window
def calculate_distance(p1,p2):
    return math.sqrt((p2[1] - p1[1]**2 + (p2[0] - p1[0])**2))

def calculate_angle(p1,p2):
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])

def draw(space,window,draw_option,line): #function to draw the objects
    window.fill('white') #fill the window with white color. Might change to other. 

    if line: 
        pygame.draw.line(window, "black", line[0], line[1], 3)
    
    space.debug_draw(draw_option) #draw the objects
    pygame.display.update() #update the display

#function to create a object
def add_object(space, radius, mass, pos): # if we want to have multiple similar shapes we can add more paraemter for postion. 
    body = pm.Body(body_type = pymunk.Body.STATIC) #creating a body
    body.position = pos #position of the object
    shape = pm.Circle(body, radius) #creating a circle shape
    shape.mass = mass #mass of the object
    shape.elasticity = 0.95 #elasticity of the object
    shape.friction = 0.9 #friction of the object
    shape.color = (0,0,0,50) #color of the object (R,G,B,Alpha(opacisty))
    space.add(body,shape) #add the body and shape to the space
    return shape #return the shape

def create_boundaries(space,width,height):
    rect = [
        [(width/2,height - 10), (width,20)],
        [(width/2, 10), (width,20)],
        [(10, height/2), (20,height)],
        [(width-10, height/2 ), (20,height)]
    ] # list of boundaries. Measuremurent of the boundaries.
    for pos, size in rect:
        body = pm.Body(body_type=pm.Body.STATIC) # creates for the boudnaries to remian statis. If removed the boundaries will move. If removing static command add a mass to body. 
        body.position = pos #set the postion of the boundaries
        shape = pm.Poly.create_box(body, size) #creating a box shape
        shape.elasticity = 0.95 # elasctity of the boudnaries 
        shape.friction = 0.9 # friction of the nboundaries
        space.add(body, shape) 


#function to run the simulation
def run(window,width,height):
    run = True 
    clock = pygame.time.Clock()
    fps  = 60 #frames per second
    delta = 1 / fps #displacement in time

    space = pm.Space()


    
    create_boundaries(space,width,height)

    draw_option = pymunk.pygame_util.DrawOptions(window)

    pressed_pos = None
    ball = None

    while run: 
        line = None
        if ball and pressed_pos: 
            line = [pressed_pos,pygame.mouse.get_pos()]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   #if the user closes the window
                run = False

            #this might be temporary.
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not ball: 
                    pressed_pos = pygame.mouse.get_pos()
                    ball = add_object(space,20,10, pressed_pos)
                elif pressed_pos:
                    ball.body.body_type = pymunk.Body.DYNAMIC
                    ball.body.apply_impulse_at_local_point((10000, 0),(0,0)) #qpplying force to the ball. (force being applied on x,y axis), (location on the shape))
                    pressed_pos = None
                else: 
                    space.remove(ball.body, ball)
                    ball = None

        draw(space,window,draw_option, line) #draw the objects
        space.step(delta) #step the simulation
        clock.tick(fps) #tick the clock

    pygame.QUIT()

#main function
if __name__ == "__main__":
    run(window, WIDTH, HEIGHT)


