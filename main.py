# Importing pygame and os
import pygame, sys
import os
from random import randint

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((1000, 600)) # Screen size

# --------------------------------------------------------------------------------------------------------------------------------------------------------------

# Tree class for loading the tree image and scaling it 
class Tree(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.image.load('Assets/tree1.png').convert_alpha() # tree image
        self.rect = self.image.get_rect(center=pos)
        
# --------------------------------------------------------------------------------------------------------------------------------------------------------------

# Player class to define the movement, load the player image and convert it, define the boundaries, and set speed
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, bounds):
        super().__init__(group)
        self.image = pygame.image.load('Assets/Knight_v1.png').convert_alpha()  # Loading player image
        self.rect = self.image.get_rect(topleft=pos)  
        self.direction = pygame.math.Vector2()
        self.speed = 3  # Setting speed
        self.bounds = bounds  # Save the boundary values

    # Defining the player movement 
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
        self.rect.center += self.direction * self.speed  # Player speed

        # Boundary checks to stop the player from leaving the area
        if self.rect.left < self.bounds['min_x']:
            self.rect.left = self.bounds['min_x']
        if self.rect.right > self.bounds['max_x']:
            self.rect.right = self.bounds['max_x']
        if self.rect.top < self.bounds['min_y']:
            self.rect.top = self.bounds['min_y']
        if self.rect.bottom > self.bounds['max_y']:
            self.rect.bottom = self.bounds['max_y']


# ------------------------------------------------------------------------------------------------------------
class Enemy():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen, camera_offset):  # Add camera_offset as a second argument
        enemy_image = pygame.image.load('Assets/enemy_1.png')  # Load the image into a Surface
        # Adjust the position by the camera's offset
        screen.blit(enemy_image, (self.x - camera_offset.x, self.y - camera_offset.y))

    def move(self): 
        self.x -= 3
# --------------------------------------------------------------------------------------------------------------------------------------------------------------

# Class for the camera which follows the player and creates the tiled background
class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # Offsetting the sprites
        self.offset = pygame.math.Vector2() 
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2
            
        # Load the ground tile and set world
        self.tile_surf = pygame.image.load('Assets/grasstile.png').convert_alpha()
        self.tile_size = self.tile_surf.get_size()
        self.world_size = (3000, 3000)  # Size of the world (bigger than the screen)

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def draw_tiled_background(self):
    # Calculate the start and end points for tiling
        start_x = -self.tile_size[0] + int(self.offset.x // self.tile_size[0]) * self.tile_size[0]
        start_y = -self.tile_size[1] + int(self.offset.y // self.tile_size[1]) * self.tile_size[1]

        end_x = self.world_size[0] + self.tile_size[0]
        end_y = self.world_size[1] + self.tile_size[1]

        # start tiling
        for x in range(start_x, end_x, self.tile_size[0]):
            for y in range(start_y, end_y, self.tile_size[1]):
            # Calculate position with offset
                tile_pos = pygame.math.Vector2(x, y) - self.offset
                self.display_surface.blit(self.tile_surf, tile_pos)

    def custom_draw(self, player):
        self.center_target_camera(player)

        # Draw the tiled background
        self.draw_tiled_background()

        for enemy in enemies:
            enemy.draw(self.display_surface, self.offset)
            
        # Active sprites
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
            
# --------------------------------------------------------------------------------------------------------------------------------------------------------------

# Set up the clock and bounds using a dictionary
clock = pygame.time.Clock()
bounds = {'min_x': 3.5, 'max_x': 3000, 'min_y': 3.5, 'max_y': 3000}

# Setup
camera_group = CameraGroup()
player = Player((640, 360), camera_group, bounds) # player size

# instance for enemy
enemies = []

# Spawning trees using random function
for i in range(100):
    random_x = randint(0, 4000) 
    random_y = randint(0, 4000)
    Tree((random_x, random_y), camera_group)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((85, 85, 85))  # Floor behind background color

    if len(enemies) == 0:  # Spawn enemies only if there are no enemies
        for i in range(50):  # You can spawn 
            random_x = randint(0, 3000)  # Random x position 
            random_y = randint(0, 3000)  # Random y position 
            new_enemy = Enemy(random_x, random_y)  
            enemies.append(new_enemy)
        for enemy in enemies:
            enemy.move()
        
    player.update()  # Update the player's position
    camera_group.custom_draw(player)  # Draw the camera group

    pygame.display.update()
    clock.tick(60) # fps

