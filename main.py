import pygame, sys
import random
import math
from random import randint
import threading
import tkinter as tk
from tkinter import Tk, Button, PhotoImage

# --------------------------------------------------------------------------------------------------------------------------------------------------------------

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((1000, 600))  # Screen size

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
        self.xp = 0  # xp
        self.max_xp = 100
        self.xp_gain_rate = 1
        self.player_images = []
        self.player_images.append(pygame.image.load('Assets/Knight_v1.png').convert_alpha())
        self.last_damage_time = 0
        self.damage = 20
        self.shield = 0
        
    def gain_xp(self, amount):
        self.xp = min(self.xp + amount, self.max_xp)

        
    def take_damage(self, amount):
        if current_time - player.last_damage_time >= 3000:  # 3.5 secs before attack again
            if player.shield != 0:
                player.shield -= 0.5    
                player.last_damage_time = current_time
            else:
                player.health -= 0.5    
                player.last_damage_time = current_time
            if self.health < 0:
                self.health = 0 # Update the last damage time
    
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
            self.image = pygame.image.load('Assets/KB1.png').convert_alpha()
            self.player_images.append(pygame.image.load('Assets/KB1.png').convert_alpha())
            self.direction.y = -1
        if keys[pygame.K_s]:
            self.image = pygame.image.load('Assets/Knight_v1.png').convert_alpha()
            self.player_images.append(pygame.image.load('Assets/Knight_v1.png').convert_alpha())
            self.direction.y = 1
        if keys[pygame.K_d]:
            self.image = pygame.image.load('Assets/KR1.png').convert_alpha()
            self.player_images.append(pygame.image.load('Assets/KR1.png').convert_alpha())
            self.direction.x = 1                
        if keys[pygame.K_a]:
            self.image = pygame.image.load('Assets/KL1.png').convert_alpha()
            self.player_images.append(pygame.image.load('Assets/KL1.png').convert_alpha())
            self.direction.x = -1

    def update(self):
        
        self.gain_xp(self.xp_gain_rate)

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
        self.speed = random.uniform(0.5, 2.5)                         # Set initial speed
        self.max_health = randint(10, 50)
        self.health = self.max_health
        self.health_fill_width = 200
        self.last_damage_time = 0
        self.damage_amount = 0
    
        
    def move_towards_player(self, player, enemies):
        dirvect = pygame.math.Vector2(player.rect.center) - self.position
        distance = dirvect.length()

        if distance > 1:  
            dirvect = dirvect.normalize() * self.speed  #Normalize direction 

            # Apply a repulsion 
            for enemy in enemies:
                if enemy != self:  # Don't push itself
                    separation = self.position - enemy.position
                    if 0 < separation.length() < 30:  
                        dirvect += separation.normalize() * 0.5  # Push apart

            self.position += dirvect  # Update 

        self.rect.topleft = self.position

    def damage_enemy(enemy, damage_amount, current_time, player, camera_group):
        # Check if 1 second has passed since last damage
        if current_time - enemy.last_damage_time >= 1000:  # 1 s
            enemy.health -= player.damage
            if enemy.health <= 0:
                enemy.health = 0 # Prevent health from going below 0
                enemy.kill()
                player.gain_xp(randint(50, 150))
                r_xp = randint(10, 40) #xp gain from killing enemy
                camera_group.xp_fill_width =  min(camera_group.xp_fill_width + r_xp, 200)
                
            enemy.last_damage_time = current_time  # Update the last damage time

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

        self.xp_fill_width = 0
        self.health_fill_width = 200
        self.xp_target_width = 0

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


    def draw_health_bar(self, screen, player):
        full_heart = pygame.image.load('Assets/Real_Heart.png').convert_alpha()
        half_heart = pygame.image.load('Assets/Real_Half_Heart.png').convert_alpha()
        empty_heart = pygame.image.load('Assets/Real_Empty_Heart.png').convert_alpha()
        shield_image = pygame.image.load("Assets/shield_image.png").convert_alpha()
        half_shield_image = pygame.image.load("Assets/half_shield_image.png").convert_alpha()
        empty_shield = pygame.image.load("Assets/empty_shield.png").convert_alpha()
        
        heart_w, heart_h = full_heart.get_size()
        x, y = 20, 20  # Position of health bar

        for i in range(3):
            heart_pos = (x + i * heart_w, y)

            # Determine which heart to draw
            if player.health >= i + 1:  # Full heart
                screen.blit(full_heart, heart_pos)
            elif player.health > i and player.shield < 1:  # Half heart
                screen.blit(half_heart, heart_pos)
            else:  # Empty heart
                screen.blit(empty_heart, heart_pos)
        
        heart_pos = (x + 3 * heart_w, y)
        if player.shield == 1:
            screen.blit(shield_image, heart_pos)
        elif player.shield == 0.5:
            screen.blit(half_shield_image, heart_pos)
        elif player.shield == 0:
            screen.blit(empty_shield, heart_pos)
        

        
                

    def draw_health_bar_enemy(self, screen, enemy):
        # Offset enemy position with the camera
        offset_x = self.offset.x
        offset_y = self.offset.y

        # Health bar dimensions
        bar_width = enemy.max_health 
        bar_height = 5  

        # Calculate health proportion
        health_percentage = enemy.health / enemy.max_health
        health_fill_width = bar_width * health_percentage  # Scale width

        # Calculate health bar position 
        bar_x = enemy.rect.x + 40 - offset_x 
        bar_y = enemy.rect.y + 3 - offset_y

        # Draw the empty background
        pygame.draw.rect(screen, (169, 169, 169), (bar_x, bar_y, bar_width, bar_height))

        # Draw the health fill
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, health_fill_width, bar_height))

    def draw_xp_bar(self, screen, player):
        x, y = 20, 60  # Position of XP bar
        bar_width = 200  # Width of the XP bar
        bar_height = 15  # Height of the XP bar
        count_z = 5

        # Draw the empty XP bar
        pygame.draw.rect(screen, (169, 169, 169), (x, y, bar_width, bar_height))

        # Calculate target XP width based on the player's XP
        self.xp_target_width = (player.xp / player.max_xp) * bar_width

        
        if self.xp_fill_width < self.xp_target_width:
            # Increase the xp fill width 
            #increment = 1 
            #self.xp_fill_width += increment

            # Ensure the xp fill width doesn't exceed the target width
            if self.xp_fill_width >= self.xp_target_width:
                self.xp_fill_width = self.xp_target_width
                LvlPopUp.open_pause_menu()
                 

        pygame.draw.rect(screen, (255, 255, 0), (x, y, self.xp_fill_width, bar_height))
        


    def custom_draw(self, player, enemy):
        self.center_target_camera(player)

        # Draw the tiled background
        self.draw_tiled_background()

        for enemy in enemy_group:
            offset_pos = enemy.rect.topleft - self.offset
            self.display_surface.blit(enemy.image, offset_pos)

            self.draw_health_bar_enemy(self.display_surface, enemy)
            
        # Draw sprites
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

        self.draw_health_bar(self.display_surface, player)
        self.draw_xp_bar(self.display_surface, player)

# --------------------------------------------------------------------------------------------------------------------------------------------------------------

class LvlPopUp:
    def __init__(self):
        super().__init__()
        self.root = ''
        
    def resume_game(self):
        global running
        running = True  # Unpause the game
        root.destroy()  # Close Tkinter window
        camera_group.xp_fill_width = 0
        
    # Function to open pause menu
    def open_pause_menu(self):
        
        random_name = random.choice(list(pwr_actions.keys()))
        action = pwr_actions[random_name]
        
        global running, root
        running = False  # Pause the game
        root = tk.Tk()
        root.title("Level up menu")
        root.geometry("1000x600")

        bg_image = PhotoImage(file="Assets/lvlupbg.png")

        # Create a canvas and set the image
        canvas = tk.Canvas(root, width=1000, height=600)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=bg_image, anchor="nw")

        frame = tk.Frame(root, bg="#00afcc")
        frame.place(relx=0.5, rely=0.5, anchor="center")  # Center frame

        num_buttons = 3
         
        for i in range(num_buttons):
            random_name = random.choice(list(pwr_actions.keys()))
            action = pwr_actions[random_name]
        
            # Create a button with the dynamic command
            button = tk.Button(frame, text=f"Increased, {random_name}!", command=action, bg="#00afcc", fg="black", width = 40, height = 4)
            button.pack(pady=5)
        
        root.mainloop()  # Show the menu

    def check_xp(self):
        if self.xp_fill_width >= self.xp_target_width:  # XP bar is full
            popup = LvlPopUp()  # Create an instance of LvlPopUp
            popup.open_pause_menu()  # Show the Tkinter window


        

    
# --------------------------------------------------------------------------------------------------------------------------------------------------------------


lvl_popup_instance = LvlPopUp()

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
        enemy_group.add(new_enemy)

last_hit_c = 0
hit_check = 2000 # time intervel to check if the player is bieng hit increse for more DPS

def health_pwr():
    player.heal(0.5)
    lvl_popup_instance.resume_game()
        
def shield_pwr():
    if player.shield != 1:
        player.shield = 1
    else:
        player.heal(1)
    lvl_popup_instance.resume_game()

    
def attack_pwr():
    player.damage += 5
    lvl_popup_instance.resume_game()

def speed_pwr():
    player.speed += 1
    lvl_popup_instance.resume_game()

def xp_pwr():
    player.xp_gain_rate += 1.2
    lvl_popup_instance.resume_game()

    
pwr_actions = {
    'Shield':shield_pwr,
    'Health':health_pwr,
    'Attack':attack_pwr,
    'Speed':speed_pwr,
    'XP gain':xp_pwr
}


last_time = pygame.time.get_ticks()

# --------------------------------------------------------------------------------------------------------------------------------------------------------------

# Main game loop
while True:
    print(player.shield, player.health, player.speed, player.damage)
    delta_time = clock.tick(60) / 1000.0  # Time in seconds since last frame
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_t or camera_group.xp_fill_width >= 200:
            popup = LvlPopUp()  # Create an instance of LvlPopUp
            popup.open_pause_menu()  # Call the method to open the Tkinter window

    xp_current = pygame.time.get_ticks()
    if xp_current - last_time >= 1000:
        camera_group.xp_fill_width += player.xp_gain_rate
        last_time = xp_current
    

                
        
    current_time = pygame.time.get_ticks()
    if current_time - last_hit_c > hit_check:
        if pygame.sprite.spritecollide(player, enemy_group, False):
            r_dmg = random.uniform(0.15,1)
            e_dmg = round(r_dmg,1)
            player.take_damage(e_dmg)
            

            last_hit_c = current_time

    current = pygame.time.get_ticks()
    if current - spawn > spawns:
        spawn = current
        # Spawn enemies if none exist
        for i in range(10):
            random_x = randint(1000, 3000)
            random_y = randint(1000, 3000)
            new_enemy = Enemy(random_x, random_y, enemy_group)
    
    keys = pygame.key.get_pressed()
    if pygame.sprite.spritecollide(player, enemy_group, False) and keys[pygame.K_p]:
        player.image = pygame.image.load('Assets/KnightS1.png').convert_alpha()
        player.player_images.append(pygame.image.load('Assets/KnightS1.png').convert_alpha())
        for enemy in pygame.sprite.spritecollide(player, enemy_group, False):
            enemy.damage_enemy(10, current_time, player, camera_group)
    else:
        player.image = player.player_images[len(player.player_images) - 2]

    #if pygame.sprite.spritecollide(player, enemy_group, False):
        #player.xp_gain_rate = 20
    #else:
        #player.xp_gain_rate = 5

    
    # Update and move enemies
    for enemy in enemy_group:
        enemy.move_towards_player(player, enemy_group)
        #print(enemy.health)
    
    
    
    # Update player and draw everything
    player.update()
    camera_group.custom_draw(player, enemy)
    pygame.display.update()
    clock.tick(60)
