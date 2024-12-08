import math
import numpy as np
import pygame 


pygame.init()
WIDTH, HEIGHT = 1000, 500
window = pygame.display.set_mode((WIDTH,HEIGHT))

##creating a definition for object
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

    ### allowing for movement left or right
    def update_pos(self, delta):
        #motion detection
        self.xpos += self.vx * delta 
        self.ypos += self.vy * delta
##creating a definition for the boundaries
class Line:
    ## properties of the line and boundaries
    def __init__(self, x, y, width, height, color):
        self.x = x  
        self.y = y  
        self.width = width  
        self.height = height  
        self.color = color  

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
##creating the physics for the the interactions with the objects in the enviornement we created     
class Physics:

    def __init__(self):
        self.objects = []
        self.gravity = 981 #Constant gravity
        self.elasticity = 1 #Elasticity factor for bounce (1.0 completly elastic anything less some energy is lost)
        self.collision_count = 0
    
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

            self.collision_count += 1
    
    def ball_to_ball_collision(self, obj1, obj2):
        # Calculate the distance between the centers of the two balls
        dx = obj2.xpos - obj1.xpos
        dy = obj2.ypos - obj1.ypos
        squared_distance = dx**2 + dy**2
        distance = math.sqrt(squared_distance)
        
        # Check if the distance between the balls is less than or equal to the sum of their radii (collision check)
        if squared_distance <= (obj1.radius + obj2.radius)**2:
            # Normalize the direction vector (unit vector of the collision axis)
            normal_dx = dx / distance
            normal_dy = dy / distance
            
            # Calculate the relative velocities along the collision axis (dot product)
            relative_velocity_x = obj1.vx - obj2.vx
            relative_velocity_y = obj1.vy - obj2.vy
            dot_product = (relative_velocity_x * normal_dx + relative_velocity_y * normal_dy)
            
            if dot_product > 0:  # Only resolve the collision if they are moving towards each other
                # Elastic collision response using mass and velocity components
                m1 = obj1.mass
                m2 = obj2.mass

                # Ratios for new velocities this works in optimizing the code and allowing for less computational "stress"
                ratio_1 = (m1 - m2) / (m1 + m2)
                ratio_2 = 2 * m2 / (m1 + m2)
                ratio_3 = (m2 - m1) / (m1 + m2)
                ratio_4 = 2 * m1 / (m1 + m2)
                
                # Calculate the new velocities for both objects in the x direction
                v1_new_vx = ratio_1 * obj1.vx + ratio_2 * obj2.vx
                v2_new_vx = ratio_3 * obj2.vx + ratio_4 * obj1.vx
                            
                # Updating the velocties
                obj1.vx = v1_new_vx
                obj2.vx = v2_new_vx

                #increasing the collision count
                self.collision_count += 1


    # updating the envionments, with the fps we created so that everything runs smoothly and accordingly
    def update(self, delta, line_x=None, line_y=None):
        for obj in self.objects:
            ### updating the physics like gravity, collisions on the objects
            self.apply_gravity(obj, delta)  
            obj.update_pos(delta)  
            if line_x:
                self.check_horizontal_collision(obj, line_x)
            if line_y:
                self.check_vertical_wall_collision(obj, line_y)  # Check horizontal collision with a line
            
            for other_obj in self.objects:
                if other_obj != obj:
                    self.ball_to_ball_collision(obj, other_obj)

    def get_collision_count(self):
        # collecting the collisions from the wall hits and the ball hits
        return self.collision_count

## setting the requirements for the being able to calculate PI n_digits is the number of pi digits you get back
pow_ten = 100
n_digits = 5

#creating the boundaries and circles
stationary_circle = CircularObject(300, 300, 0, 0, 1, 30,(0, 0, 0))
moving_circle = CircularObject(500, 300, -50, 0, (pow_ten**(n_digits - 1)), 30,(0, 0, 0))
horizontal_line = Line(200,300, 500, 10, (0,0,0))
verticle_line = Line(200,150,10,150,(0,0,0))

# making it so that the both objects follow the physics class created, basically gravity and collisions can effect the ball
physics = Physics()
physics.add_object(stationary_circle)
physics.add_object(moving_circle)


def run():
    run = True
    fps = 60
    delta = 1 / (fps * 1000)
    accumulated_time  = 0
    clock = pygame.time.Clock()

    #GAME LOOP
    while run:

        # measuring elapsed time since last frame, this should increase optimization and make it run better
        accumulated_time  += clock.tick(fps) /1000.0 #convert milliseconds to seconds
        window.fill('Gray')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        while accumulated_time  >= delta:
            physics.update(delta, line_x=horizontal_line, line_y=verticle_line)
            accumulated_time  -= delta

        # Drawing all the figures I previously created
        stationary_circle.draw(window)
        moving_circle.draw(window)
        horizontal_line.draw(window)
        verticle_line.draw(window)


        # Display the collision count on the screen with the use of pygame
        font = pygame.font.SysFont(None, 36)
        text = font.render(f'Ball-to-Ball Collisions: {physics.get_collision_count()}', True, (0, 0, 0))
        window.blit(text, (10, 10))

        pygame.display.update()
        clock.tick(fps)
    pygame.quit()

if __name__ == "__main__":
    run()