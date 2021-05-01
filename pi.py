import pygame
import math

NUM_OF_DIGITS = int(input("Enter the number of digits you want to compute: "))  # Set the number of digits

WIDTH, HEIGHT = 1280, 720  # Setting the windows dimensions
WHITE = (255,255,255)  # Set the RGB color of WHITE
GRAY = (190,190,190)  # Set the RGB color of GRAY
RED = (200,0,0)  # Set the RGB color of RED
BLUE = (0, 128, 255)  # Set the RGB color of BLUE

# Create the blok class
class Block(object):
    # Initialize the block dimenssions
    def __init__(self, size, XY, mass, velocity):
        self.x = XY[0]
        self.y = XY[1]
        self.mass = mass
        self.v = velocity
        self.size = size
    
    # Determine wheter a collision happen or not
    def collision(self, other_block):
        return not (self.x + self.size < other_block.x or self.x > other_block.x + other_block.size)

    # Calculate the new velocity
    def NewVelocity(self, other_block):
        sumM = self.mass + other_block.mass
        newV = (self.mass - other_block.mass)/sumM * self.v
        newV += (2 * other_block.mass/ sumM) * other_block.v
        return newV

    # Check wheter if a block collide with the wall or not
    def collide_wall(self):
        if self.x <= 0:
            self.v *= -1
            return True

    # Update the new velocity
    def update(self):
        self.x += self.v

    # Draw the two blocks
    def draw(self, windows, other_block):
        if self.x < other_block.size:
            pygame.draw.rect(windows, RED, [other_block.size, self.y , self.size, self.size])
            pygame.draw.rect(windows, BLUE, [0, other_block.y , other_block.size, other_block.size])
        else:
            pygame.draw.rect(windows, RED, [self.x, self.y , self.size, self.size])
            pygame.draw.rect(windows, BLUE, [other_block.x, other_block.y , other_block.size, other_block.size])

# Calculating the frames per second
def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 1, pygame.Color("coral"))
    return fps_text

# Redraw the blocks
def redraw():
    windows.fill(WHITE)
    pygame.draw.rect(windows, GRAY, [0 , 0, 1280, 600])
    windows.blit(update_fps(), (10,0))
    big_block.draw(windows, small_block)
    font = pygame.font.SysFont(None, 50)
    text = font.render("Number of collisions : " + str(count), True, (0,0,0))
    windows.blit(text, [50, 650])
    clock.tick(120)
    pygame.display.update()

# Initialize pygame
pygame.init()

# Collision sound
clack_sound = pygame.mixer.Sound("clack.wav")

# Set the time step
time_step = 10**(NUM_OF_DIGITS-1)
power = math.pow(100, NUM_OF_DIGITS-1)

windows = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont('Fira mono', 22)

big_block = Block(60*NUM_OF_DIGITS, (320,600-60*NUM_OF_DIGITS), power, -1/time_step)
small_block = Block(60, (100, 600-60), 1, 0)

count = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    for i in range(time_step):
        if(small_block.collision(big_block)):
            clack_sound.play()
            count+=1
            v1 = small_block.NewVelocity(big_block)
            v2 = big_block.NewVelocity(small_block)
            big_block.v = v2
            small_block.v = v1
        if small_block.collide_wall():
            clack_sound.play()
            count+=1
        big_block.update()
        small_block.update()
    redraw()

pygame.quit()