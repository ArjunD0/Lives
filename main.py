
# Importing pygame and os
import pygame, sys
import os
from random import randint

# setting pygmae window dimensions
pygame.init()
screen = pygame.display.set_mode((1000, 600))

# --------------------------------------------------------------------------------------------------------------------------------------------------------------

#Tree class for loading the tree image and scaling it 
class Tree(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.image.load('Assets/rocket1.png').convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        
# --------------------------------------------------------------------------------------------------------------------------------------------------------------

# Player class to define the movement, Load the player image and convert it, define the boundries and set speed
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, bounds):
        super().__init__(group)
        self.image = pygame.image.load('Assets/Knight_v1.png').convert_alpha() # Loading player image
        self.rect = self.image.get_rect(topleft=pos)  
        self.direction = pygame.math.Vector2()
        self.speed = 3 # Setting speed
        self.bounds = bounds  # Save the boundary values

# defining the player movement 
    def input(self): 
        keys = pygame.key.get_pressed()
        self.direction.x = 0
        self.direction.y = 0
        
        if keys[pygame.K_w]:
            self.direction.y = -1
        if keys[pygame.K_s]:
            self.direction.y = 1
        if keys[pygame.K_d]:
            self.direction.x = 1                
        if keys[pygame.K_a]:
            self.direction.x = -1

    def update(self):
        self.input()
        self.rect.center += self.direction * self.speed # Player speed

        # Boundary checks
        if self.rect.left < self.bounds['min_x']:
            self.rect.left = self.bounds['min_x']
        if self.rect.right > self.bounds['max_x']:
            self.rect.right = self.bounds['max_x']
        if self.rect.top < self.bounds['min_y']:
            self.rect.top = self.bounds['min_y']
        if self.rect.bottom > self.bounds['max_y']:
            self.rect.bottom = self.bounds['max_y']
            
# --------------------------------------------------------------------------------------------------------------------------------------------------------------

# Class for the camera whhich follows the player also creates the background for the player by loading the image and offsetting it does the same with the trees
class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # offseting the sprites
        self.offset = pygame.math.Vector2() 
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2
            
        self.ground_surf = pygame.image.load('Assets/grasstile.png').convert_alpha()
        self.ground_rect = self.ground_surf.get_rect(topleft=(0, 0))
        self.background_surf = pygame.image.load('Assets/grasstile.png').convert()

        
    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def custom_draw(self, player):
        self.center_target_camera(player)
        # Background
        background_offset = -self.offset  # Offset for background
        self.display_surface.blit(self.background_surf, background_offset)

        # Ground
        ground_offset = self.ground_rect.topleft - self.offset
        self.display_surface.blit(self.ground_surf, ground_offset)

        # Active sprites
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
            
# --------------------------------------------------------------------------------------------------------------------------------------------------------------

# Set up the clock and bounds
clock = pygame.time.Clock()
bounds = {'min_x': 2.5, 'max_x': 1020, 'min_y': 2.5, 'max_y': 1020}

# Setup
camera_group = CameraGroup()
player = Player((640, 360), camera_group, bounds)

# Spawning trees using random function
for i in range(30):
    random_x = randint(0, 990)
    random_y = randint(0, 990)
    Tree((random_x, random_y), camera_group)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((85, 85, 85)) # Floor behinde background colour
    
    player.update()  # Update the player's position
    camera_group.custom_draw(player)  # Draw the camera group

    pygame.display.update()
    clock.tick(60)

