import pygame, sys
import random
import math
from random import randint

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((1000, 600))  # Screen size

# --------------------------------------------------------------------------------------------------------------------------------------------------------------

# Tree class for loading the tree image and scaling it 
class Tree(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.image.load('Assets/tree1.png').convert_alpha()  # Tree image
        self.rect = self.image.get_rect(center=pos)
        
# --------------------------------------------------------------------------------------------------------------------------------------------------------------

# Player class to define the movement, load the player image, define the boundaries, and set speed
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, bounds):
        super().__init__(group)
        self.image = pygame.image.load('Assets/Knight_v1.png').convert_alpha()  # Load player image
        self.rect = self.image.get_rect(topleft=pos)  
        self.direction = pygame.math.Vector2()
        self.speed = 3.5  # Set speed
        self.bounds = bounds  # Save boundary values
        self.health = 3
        self.max_health = 3
        

        
    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0
    
    def heal(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health



    # Define player movement 
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
        self.rect.center += self.direction * self.speed  # Apply speed to movement

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

# Enemy class to define movement and rendering
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, group):
        super().__init__(group)
        self.image = pygame.image.load('Assets/enemy_1.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x,y))
        self.position = pygame.math.Vector2(x, y)
        self.speed = randint(1,2)                         # Set initial speed

        

    def move_towards_player(self, player):
        # Calculate direction to the player
        dirvect = pygame.math.Vector2(player.rect.center) - self.position
        distance = dirvect.length()

        if distance > 0:  # Move only if not already at the player's position
            dirvect = dirvect / distance  # Normalize direction vector
            self.position += dirvect * self.speed  # Update position

        self.rect.topleft = self.position  # Sync rect with position

# --------------------------------------------------------------------------------------------------------------------------------------------------------------

# Camera class to handle scrolling and background tiling
class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # Offsetting the sprites
        self.offset = pygame.math.Vector2() 
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2
            
        # Load the ground tile
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

        # Start tiling
        for x in range(start_x, end_x, self.tile_size[0]):
            for y in range(start_y, end_y, self.tile_size[1]):
                tile_pos = pygame.math.Vector2(x, y) - self.offset
                self.display_surface.blit(self.tile_surf, tile_pos)

    def custom_draw(self, player):
        self.center_target_camera(player)

        # Draw the tiled background
        self.draw_tiled_background()

        for enemy in enemy_group:
            offset_pos = enemy.rect.topleft - self.offset
            self.display_surface.blit(enemy.image, offset_pos)
            
        # Draw sprites
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

        def draw_health_icons(screen, x, y, health, max_health, icon_full, icon_half, spacing = 40):
            self.icon_full = pygame.image.load('Assets/full_heart.png').convert_alpha()
            self.icon_half = pygame.image.load('Assets/half_heart.png').convert_alpha()

            for i in range(int(max_health)):
                if i < int(health):
                    screen.blit(icon_full, (x+i*spacing,y))
                elif i < health:
                    screen.blit(icon_full, (x+i*spacing,y))
                    


# --------------------------------------------------------------------------------------------------------------------------------------------------------------

# Set up the clock and bounds
clock = pygame.time.Clock()
bounds = {'min_x': 3.5, 'max_x': 3000, 'min_y': 3.5, 'max_y': 3000}

# Setup
camera_group = CameraGroup()
player = Player((640, 360), camera_group, bounds)

enemy_group = pygame.sprite.Group()
# List of enemies
enemies = []

# Spawn trees
for i in range(100):
    random_x = randint(0, 4000) 
    random_y = randint(0, 4000)
    Tree((random_x, random_y), camera_group)

spawn = pygame.time.get_ticks()
spawns = 30000 # timer for spawning enemies

for i in range(10): # how many spawn
    if len(enemies) != 40: # limit to stop inf number of enemies spawning
        random_x = randint(0, 3000)
        random_y = randint(0, 3000)
        new_enemy = Enemy(random_x, random_y, enemy_group)

last_hit_c = 0
hit_check = 3000 # time intervel to check if the player is bieng hit increse for more DPS
# --------------------------------------------------------------------------------------------------------------------------------------------------------------



# Main game loop
while True:
    delta_time = clock.tick(60) / 1000.0  # Time in seconds since last frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    current_time = pygame.time.get_ticks()
    if current_time - last_hit_c > hit_check:
        if pygame.sprite.spritecollide(player, enemy_group, False):
            r_dmg = random.uniform(0.15,1)
            e_dmg = round(r_dmg,1)
            player.take_damage(e_dmg)
            print(player.health)

        last_hit_c = current_time

    current = pygame.time.get_ticks()
    if current - spawn > spawns:
        spawn = current
        # Spawn enemies if none exist
        for i in range(10):
            random_x = randint(0, 3000)
            random_y = randint(0, 3000)
            new_enemy = Enemy(random_x, random_y, enemy_group)
            

    # Update and move enemies
    for enemy in enemy_group:
        enemy.move_towards_player(player)
    
    # Update player and draw everything
    player.update()
    camera_group.custom_draw(player)
    pygame.display.update()
    clock.tick(60)
