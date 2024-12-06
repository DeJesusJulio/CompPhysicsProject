import math
import numpy as np
import pygame 


pygame.init()
WIDTH, HEIGHT = 1000, 500
window = pygame.display.set_mode((WIDTH,HEIGHT))

##creating a definiton for object
class CircularObject:
    ### creating the objects properties 
    def __init__(self,xpos,ypos,vx,vy,mass,radius, color):
        self.xpos = xpos
        self.ypos = ypos
        self.vx = vx
        self.vy = vy
        self.mass = mass
        self.radius = radius 
        self.color = color
    
    ### drawing the circle
    def draw(self, window):
        pygame.draw.circle(window, self.color, (int(self.xpos), int(self.ypos)), self.radius)

    def update_pos(self, delta):
        #motion detection
        self.xpos += self.vx * delta 
        self.ypos += self.vy * delta

class Line:
    def __init__(self, x, y, width, height, color):
        self.x = x  # X-coordinate of the line's top-left corner
        self.y = y  # Y-coordinate of the line's top-left corner
        self.width = width  # Width of the line
        self.height = height  # Thickness of the line
        self.color = color  # Color of the line

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        

class Physics:

    def __init__(self):
        self.objects = []
        self.gravity = 981 #Constant gravity
        self.elasticity = 1 #Elasticity factor for bounce (1.0 completly elastic anything less some energy is lost)
    
    def add_object(self, obj):
        self.objects.append(obj)

    ### gravity 
    def apply_gravity(self, obj, delta):
        obj.vy += self.gravity * delta
    
    ### has to be a little more complicated because i have to take into account width and length of rectange
    def check_horizontal_collision(self, obj, line):
    # Check if the ball is falling into the vertical bounds of the line
        if obj.ypos + obj.radius >= line.y and obj.ypos - obj.radius <= line.y + line.height:
            # Check if the ball is within the horizontal bounds of the line
            if obj.xpos >= line.x and obj.xpos <= line.x + line.width:
                obj.vy = 0  # Stop vertical movement
                obj.ypos = line.y - obj.radius  # Correct position to be on top of the line

    def check_vertical_wall_collision(self, obj, line):
        # Check for collision with the left vertical wall
        if obj.xpos - obj.radius <= line.x:  # Ball's left edge hits the wall
            obj.vx = -obj.vx  # Reverse horizontal velocity (bounce effect)
            obj.xpos = line.x + obj.radius  # Prevent the ball from passing through the wall
    
    def ball_to_ball_collision(self, obj1, obj2):
        # Calculate the distance between the centers of the two balls
        dx = obj2.xpos - obj1.xpos
        dy = obj2.ypos - obj1.ypos
        distance = math.sqrt(dx**2 + dy**2)

        # Check if the distance between the balls is less than or equal to the sum of their radii (collision check)
        if distance <= (obj1.radius + obj2.radius):
            # Elastic head-on collision equations

            #normalizing collision vectors
            


            # Calculate new velocities for both balls based on their masses and velocities
            v1x_new = (((obj1.mass - obj2.mass)/(obj1.mass + obj2.mass))*obj1.vx) - (((2 * obj2.mass) / (obj1.mass + obj2.mass))*obj2.vx)
            v2x_new = (((2 * obj1.mass) / (obj1.mass + obj2.mass))*obj1.vx) + (((obj1.mass - obj2.mass)/(obj1.mass + obj2.mass))*obj2.vx)
            #v1n_new = ((obj1.mass - obj2.mass) * obj1.vx + 2 * obj2.mass * obj2.vx) / (obj1.mass + obj2.mass)
            #v2n_new = ((obj2.mass - obj1.mass) * obj2.vx + 2 * obj1.mass * obj1.vx) / (obj1.mass + obj2.mass)

            # Update the velocities of the balls
            obj1.vx = v1x_new 
            obj2.vx = v2x_new 


    def update(self, delta, line_x=None, line_y=None):
        for obj in self.objects:
            self.apply_gravity(obj, delta)  # Apply gravity to each object
            obj.update_pos(delta)  # Update position of the object

            if line_x:
                self.check_horizontal_collision(obj, line_x)
            
            if line_y:
                self.check_vertical_wall_collision(obj, line_y)  # Check horizontal collision with a line
            
            for other_obj in self.objects:
                if other_obj != obj:
                    self.ball_to_ball_collision(obj, other_obj)

    

stationary_circle = CircularObject(300, 300, 0, 0, 1, 30,(0, 0, 0))
moving_circle = CircularObject(500, 300, -50, 0, 10, 30,(0, 0, 0))


horizontal_line = Line(200,300, 500, 10, (0,0,0))
verticle_line = Line(200,150,10,150,(0,0,0))

physics = Physics()
physics.add_object(stationary_circle)
physics.add_object(moving_circle)


def run():
    run = True
    fps = 30
    delta = 1 / fps
    clock = pygame.time.Clock()

    #doing the loop
    while run:
        window.fill('Gray')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        ##keeping track of the physics 
        physics.update(delta, line_x=horizontal_line, line_y=verticle_line) #line_y=line_y, line_x=line_x)


        ##creating the verticle lines
        #pygame.draw.line(window, (0, 0, 0), (100, line_y), (800, line_y), 4)  # Horizontal line
        #pygame.draw.line(window, (0, 0, 0), (line_x, 50), (line_x, 300), 4)  # Vertical line

        # Draw the ball and the line
        stationary_circle.draw(window)
        moving_circle.draw(window)
        horizontal_line.draw(window)
        verticle_line.draw(window)



        

        pygame.display.update()
        clock.tick(fps)
    pygame.quit()

if __name__ == "__main__":
    run()
