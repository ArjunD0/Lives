# Import librarys
import pygame, sys
import random
import math
from random import randint
import threading
import tkinter as tk
from tkinter import Tk, Button, PhotoImage
import time

# --------------------------------------------------------------------------------------------------------------------------------------------------------------

# Initialize pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1066, 600))  # Screen size


    

def main_game():
    
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
            self.speed = 2  # Set speed
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
            self.range = 10
            self.up = False
            self.down = False
            self.left = False
            self.right = False
            self.bow_picked = False
            self.has_piercing = False
            self.hurt_wav = pygame.mixer.Sound("Sounds/player_hurt.wav")
            self.currentsound = pygame.mixer.Sound("Sounds/sword_hit.wav")
            
            
        def gain_xp(self, amount):
            self.xp = min(self.xp + amount, self.max_xp)

            
        def take_damage(self, amount):
            if current_time - player.last_damage_time >= 3000:  # 3.5 secs before attack again
                if player.shield != 0:
                    enemy.attackwav.play()
                    player.shield -= 0.5
                    player.hurt_wav.play()
                    player.last_damage_time = current_time
                else:
                    enemy.attackwav.play()
                    player.health -= 0.5
                    player.hurt_wav.play()
                    player.last_damage_time = current_time
                if self.health < 0:
                    enemy.attackwav.play()
                    player.hurt_wav.play()
                    self.health = 0 # Update the last damage time
        
        
        def heal(self, amount):
            self.health += amount
            if self.health > self.max_health:
                self.health = self.max_health



        # Define player movement and simple animations
        def input(self):
            keys = pygame.key.get_pressed()
            self.direction.x = 0
            self.direction.y = 0

            if keys[pygame.K_w]:
                
                player.up = True
                
                player.down = False
                player.left = False
                player.right = False
                
                
                self.image = pygame.image.load('Assets/KB1.png').convert_alpha()
                self.direction.y = -self.speed
            if keys[pygame.K_s]:
                
                player.down = True
                player.up = False
                player.left = False
                player.right = False
                
                self.image = pygame.image.load('Assets/Knight_v1.png').convert_alpha()
                self.direction.y = self.speed
            if keys[pygame.K_d]:
                
                player.right = True
                player.down = False
                player.left = False
                player.up = False
                
                self.image = pygame.image.load('Assets/KR1.png').convert_alpha()
                self.direction.x = self.speed              
            if keys[pygame.K_a]:
                
                player.left = True
                player.down = False
                player.up = False
                player.right = False
                
                self.image = pygame.image.load('Assets/KL1.png').convert_alpha()
                self.direction.x = -self.speed
            if keys[pygame.K_SPACE]:
                self.image = pygame.image.load('Assets/KnightS1.png').convert_alpha()
            
            if keys[pygame.K_w] and not keys[pygame.K_SPACE]:
                
                player.up = True
                player.down = False
                player.left = False
                player.right = False
                
                self.image = pygame.image.load('Assets/KB1.png').convert_alpha()
                self.direction.y = -self.speed
            if keys[pygame.K_s] and not keys[pygame.K_SPACE]:
                
                player.down = True
                player.up = False
                player.left = False
                player.right = False
                
                self.image = pygame.image.load('Assets/Knight_v1.png').convert_alpha()
                self.direction.y = self.speed
            if keys[pygame.K_d] and not keys[pygame.K_SPACE]:
                
                player.right = True
                player.down = False
                player.left = False
                player.up = False
                
                self.image = pygame.image.load('Assets/KR1.png').convert_alpha()
                self.direction.x = self.speed              
            if keys[pygame.K_a] and not keys[pygame.K_SPACE]:
                
                player.left = True
                player.down = False
                player.up = False
                player.right = False
                
                self.image = pygame.image.load('Assets/KL1.png').convert_alpha()
                self.direction.x = -self.speed
            if keys[pygame.K_SPACE]:
                self.image = pygame.image.load('Assets/KnightS1.png').convert_alpha()
    

            if keys[pygame.K_w] and keys[pygame.K_SPACE]:
                
                player.up = True
                player.down = False
                player.left = False
                player.right = False
                    
                self.image = pygame.image.load('Assets/KSB.5.png').convert_alpha()
                self.direction.y = -self.speed
            if keys[pygame.K_s] and keys[pygame.K_SPACE]:
                
                player.down = True
                player.up = False
                player.left = False
                player.right = False
                
                self.image = pygame.image.load('Assets/KnightS1.png').convert_alpha()
                self.direction.y = self.speed
            if keys[pygame.K_d] and keys[pygame.K_SPACE]:
                
                player.right = True
                player.down = False
                player.left = False
                player.up = False
                    
                self.image = pygame.image.load('Assets/KRS.4.png').convert_alpha()
                self.direction.x = self.speed              
            if keys[pygame.K_a] and keys[pygame.K_SPACE]:
                
                player.left = True
                player.down = False
                player.up = False
                player.right = False
                
                self.image = pygame.image.load('Assets/KLS.4.png').convert_alpha()
                self.direction.x = -self.speed
    
                

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
            self.image_array = ['Assets/enemy_1.png','Assets/enemy_2.png','Assets/enemy_3.png']
            self.image = pygame.image.load(self.image_array[randint(0,2)]).convert_alpha()
            self.rect = self.image.get_rect(topleft=(x,y))
            self.position = pygame.math.Vector2(x, y)
            self.speed = random.uniform(0.5, 2.5)                         # Set initial speed
            self.max_health = randint(10, 50)
            self.health = self.max_health
            self.health_fill_width = 200
            self.last_damage_time = 0
            self.damage_amount = 0
            self.min_xp = 10
            self.max_xp = 40
            self.dps = 1000
            self.spawnrate = 10
            self.hurtwav = pygame.mixer.Sound("Sounds/enemydie.wav")
            self.attackwav = pygame.mixer.Sound("Sounds/enemyattack.wav")
            
        def move_towards_player(self, player, enemies):
            dirvect = pygame.math.Vector2(player.rect.center) - self.position
            distance = dirvect.length()

            if distance > 1:  
                dirvect = dirvect.normalize() * self.speed  #Normalize direction 

                # Apply a repulsion 
                for enemy in enemies:
                    if enemy != self:  # Don't push itself
                        separation = self.position - enemy.position
                        if 0 < separation.length() < 50:  
                            dirvect += separation.normalize() * 1  # Push apart

                self.position += dirvect  # Update 

            self.rect.topleft = self.position
            

        def damage_enemy(enemy, damage_amount, current_time, player, camera_group):
            # Check if 1 second has passed since last damage
            if current_time - enemy.last_damage_time >= enemy.dps:  # 1 s
                enemy.health -= player.damage
                if enemy.health <= 0:
                    enemy.health = 0 # Prevent health from going below 0
                    enemy.hurtwav.play()
                    enemy.kill()
                    player.heal(0.25)
                    player.gain_xp(randint(50, 150))
                    r_xp = (randint(enemy.min_xp, enemy.max_xp)*  player.xp_gain_rate) #xp gain from killing enemy
                    camera_group.xp_fill_width =  min(camera_group.xp_fill_width + r_xp, (camera_group.xp_target_width + lvl_popup_instance.xp_addition))
                    
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
            self.xp_target_width = 200

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

        def menue_key_text(self, screen):
            self.xtrafontm = pygame.font.SysFont('Impact', 20)
            self.txtm = 'M = Back to Menu'
            self.textm_surf = self.xtrafontm.render(self.txtm, True, (0, 0, 0)) 
            self.textm_rect = self.textm_surf.get_rect(center=(80, 580))
            screen.blit(self.textm_surf, self.textm_rect)

        
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
            bar_width = min((200 + lvl_popup_instance.xp_addition), 700)  # Width of the XP bar
            bar_height = 15  # Height of the XP bar

            # Draw the empty XP bar
            pygame.draw.rect(screen, (169, 169, 169), (x, y, bar_width, bar_height))

            # Calculate target XP width based on the player's XP
            self.xp_target_width = ((player.xp / player.max_xp) * bar_width) +  lvl_popup_instance.xp_addition

            
           
            # Ensure the xp fill width doesn't exceed the target width
            lvl_pop_up_instance = LvlPopUp()
            if self.xp_fill_width > bar_width:
                self.xp_fill_width = bar_width
                lvl_pop_up_instance.open_pause_menu()
                     

            pygame.draw.rect(screen, (255, 255, 0), (x, y, self.xp_fill_width, bar_height))
            


        def custom_draw(self, player, enemy, arrow):
            self.center_target_camera(player)

            # Draw the tiled background
            self.draw_tiled_background()

            for enemy in enemy_group:
                offset_pos = enemy.rect.topleft - self.offset
                self.display_surface.blit(enemy.image, offset_pos)

                self.draw_health_bar_enemy(self.display_surface, enemy)

            for arrow in arrow_group:  
                offset_pos = arrow.rect.topleft - self.offset
                self.display_surface.blit(arrow.image, offset_pos)
                
            # Draw sprites
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)

            self.draw_health_bar(self.display_surface, player)
            self.draw_xp_bar(self.display_surface, player)
            self.menue_key_text(self.display_surface)
    

# --------------------------------------------------------------------------------------------------------------------------------------------------------------

    class LvlPopUp:
        def __init__(self):
            super().__init__()
            self.root = ''
            self.xp_addition = 0
            self.levelupwav = pygame.mixer.Sound("Sounds/level_up.wav")
            self.upgradewav = pygame.mixer.Sound("Sounds/Upgrade.wav")
            
        def resume_game(self):
            global running
            running = True  # Unpause the game
            root.destroy()  # Close Tkinter window
            lvl_popup_instance.upgradewav.play()
            camera_group.xp_fill_width = 0
            
        # Function to open pause menu
        def open_pause_menu(self):

            self.levelupwav.play()
            
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
                button = tk.Button(frame, text=f"{random_name}!", command=action, bg="#00afcc", fg="black", width = 40, height = 4)
                button.pack(pady=5)
            
            root.mainloop()  # Show the menu

        def check_xp(self):
            if self.xp_fill_width >= self.xp_target_width + self.xp_addition:  # XP bar is full
                popup = LvlPopUp()  # Create an instance of LvlPopUp
                popup.open_pause_menu()  # Show the Tkinter window


            

        
# --------------------------------------------------------------------------------------------------------------------------------------------------------------

    class Arrow(pygame.sprite.Sprite):
        def __init__(self, x, y, group, facing, damage=3, piercing = False):
            super().__init__(group)
            self.piercing = piercing
             
            if facing == 'up':
                self.image = pygame.image.load('Assets/up_arrow.png').convert_alpha()
            elif facing == 'down':
                self.image = pygame.image.load('Assets/down_arrow.png').convert_alpha()
            elif facing == 'left':
                self.image = pygame.image.load('Assets/left_arrow.png').convert_alpha()
            elif facing == 'right':
                self.image = pygame.image.load('Assets/right_arrow.png').convert_alpha()

            else:
                self.image = pygame.image.load('Assets/right_arrow.png').convert_alpha()

            
            self.rect = self.image.get_rect(topleft=(x - 5,y - 5))
            self.speed = 3                        
            self.damage = damage

            self.facing = facing # Determin what arrow image to load

        def move(self):
            if self.facing == 'up':
                self.rect.y -= self.speed
            elif self.facing == 'down':
                self.rect.y += self.speed
            elif self.facing == 'left':
                self.rect.x -= self.speed
            elif self.facing == 'right':
                self.rect.x += self.speed 


# --------------------------------------------------------------------------------------------------------------------------------------------------------------
    

    # Set up the clock and bounds
    clock = pygame.time.Clock()
    bounds = {'min_x': 3.5, 'max_x': 3000, 'min_y': 3.5, 'max_y': 3000}

    # Setup
    camera_group = CameraGroup()
    player = Player((640, 360), camera_group, bounds)
    
    lvl_popup_instance = LvlPopUp()

    enemy_group = pygame.sprite.Group()

    arrow_group = pygame.sprite.Group()

    arrows = []
    # List of enemies
    enemies = []

    last_fire_time = 0  
    fire_cooldown = 1500

    # Spawn trees
    for i in range(100):
        random_x = randint(0, 4000) 
        random_y = randint(0, 4000)
        Tree((random_x, random_y), camera_group)

    spawn = pygame.time.get_ticks()
    spawns = 30000 # timer for spawning enemies

    for i in range(10): # how many spawn
        if len(enemies) != 50: # limit to stop inf number of enemies spawning
            random_x = randint(0, 3000)
            random_y = randint(0, 3000)
            new_enemy = Enemy(random_x, random_y, enemy_group)
            enemy_group.add(new_enemy)

    last_hit_c = 0
    hit_check = 2000 # time intervel to check if the player is bieng hit increse for more DPS

    despawn_arrow = True

    start_time = pygame.time.get_ticks()

    

    # Timer for top of screen
    def timer_txt(timer):
        xtrafontt = pygame.font.SysFont('Impact', 20)
        active_time = pygame.time.get_ticks() // 1000
        txtt = str(timer + active_time)
        textt_surf = xtrafontt.render(txtt, True, (0, 0, 0)) 
        textt_rect = textt_surf.get_rect(center=(533, 40))
        screen.blit(textt_surf, textt_rect)

    

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------  
    
# Power ups

    def health_pwr():
        player.heal(0.5)
        lvl_popup_instance.upgradewav.play()
        
        if (camera_group.xp_target_width + lvl_popup_instance.xp_addition) < 700:
                lvl_popup_instance.xp_addition += 10
                
        lvl_popup_instance.resume_game()
            
    def shield_pwr():
        if player.shield != 1:
            player.shield = 1
            lvl_popup_instance.upgradewav.play()
            
            if (camera_group.xp_target_width + lvl_popup_instance.xp_addition) < 700:
                lvl_popup_instance.xp_addition += 10
                
        else: 
            player.heal(1)
            lvl_popup_instance.upgradewav.play()
            
            if (camera_group.xp_target_width + lvl_popup_instance.xp_addition) < 700:
                lvl_popup_instance.xp_addition += 10
        
        lvl_popup_instance.resume_game()

        
    def attack_pwr():
        player.damage += 5
        lvl_popup_instance.upgradewav.play()
        
        if (camera_group.xp_target_width + lvl_popup_instance.xp_addition) < 700:
                lvl_popup_instance.xp_addition += 10
                
        lvl_popup_instance.resume_game()

    def speed_pwr():
        player.speed += 0.25
        lvl_popup_instance.upgradewav.play()
        
        if (camera_group.xp_target_width + lvl_popup_instance.xp_addition) < 700:
                lvl_popup_instance.xp_addition += 10
                
        lvl_popup_instance.resume_game()

    def xp_pwr():
        player.xp_gain_rate += 1.2
        player.xp_gain_rate = round( player.xp_gain_rate, 2)
        lvl_popup_instance.upgradewav.play()
        
        if (camera_group.xp_target_width + lvl_popup_instance.xp_addition) < 700:
                lvl_popup_instance.xp_addition += 10
                
        lvl_popup_instance.resume_game()

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------  
        
    # Weapons  

    def sword():
        player.damage = 20
        enemy.dps = 1000
        player.bow_picked = False
        player.has_piercing = False
        player.currentsound = pygame.mixer.Sound("Sounds/sword_hit.wav")
        
        if (camera_group.xp_target_width + lvl_popup_instance.xp_addition) < 700:
                lvl_popup_instance.xp_addition += 10
                
        lvl_popup_instance.resume_game()

    def knife():
        player.damage = 5
        enemy.dps = 100
        player.bow_picked = False
        player.has_piercing = False
        player.currentsound = pygame.mixer.Sound("Sounds/sword_hit.wav")
        
        if (camera_group.xp_target_width + lvl_popup_instance.xp_addition) < 700:
                lvl_popup_instance.xp_addition += 10
                
        lvl_popup_instance.resume_game()

    def great_sword():
        player.damage = 25
        enemy.dps = 4000
        player.bow_picked = False
        player.has_piercing = False
        player.currentsound = pygame.mixer.Sound("Sounds/sword_hit.wav")
        
        if (camera_group.xp_target_width + lvl_popup_instance.xp_addition) < 700:
                lvl_popup_instance.xp_addition += 10
                
        lvl_popup_instance.resume_game()
        

    def bow():
        player.damage = 15
        enemy.dps = 1500
        player.bow_picked = True
        player.currentsound = pygame.mixer.Sound("Sounds/bow_shoot.wav")
        
        if (camera_group.xp_target_width + lvl_popup_instance.xp_addition) < 700:
                lvl_popup_instance.xp_addition += 10
                
        lvl_popup_instance.resume_game()

    def pierce_arrow_pwr():
        if not player.has_piercing:
            player.has_piercing = True
        else:
            player.damage += 3
        lvl_popup_instance.resume_game()
        
            

# Power ups dict

    pwr_actions = {
        'Receive a Shield':shield_pwr,
        'Heal 1/2 Heart':health_pwr,
        'Increased Attack':attack_pwr,
        'Increased Speed':speed_pwr,
        'Choose Sword':sword,
        'Choose Knife':knife,
        'Choose Great Sword':great_sword,
        'Choose Bow':bow,
        'Receive Piercing Arrows':pierce_arrow_pwr
    }


    last_time = pygame.time.get_ticks()
# --------------------------------------------------------------------------------------------------------------------------------------------------------------

    # Main game loop
    game_run = True
    spawnrate = 10  # inital spawnrate for enemies
    start_sound = 0

    music = pygame.mixer.music.load("Sounds/game_music.wav")
    pygame.mixer.music.play(-1)
    
    while game_run:

        
        if player.health <= 0: # check for player death if so load game over screen
            game_over()
            
        keys = pygame.key.get_pressed()# Debug and testing key remove
        if keys[pygame.K_g]:
            print(camera_group.xp_target_width + lvl_popup_instance.xp_addition, camera_group.xp_fill_width)
            print(player.shield, player.health, player.speed, player.damage, player.xp_gain_rate)
            print(player.damage, enemy.dps, player.bow_picked, despawn_arrow)
            print(spawnrate)

            
        delta_time = clock.tick(60) / 1000.0  # Time in seconds since last frame
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                click.play()
                music = pygame.mixer.music.load("Sounds/menu_music.wav")
                pygame.mixer.music.play(-1)
                game_run = False
                time.sleep(0.1)
                
            # remove debug and testing key T check
            if event.type == pygame.KEYDOWN and event.key == pygame.K_t or camera_group.xp_fill_width >= (camera_group.xp_target_width + lvl_popup_instance.xp_addition):
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
            for i in range(spawnrate):
                random_x = randint(1000, 3000)
                random_y = randint(1000, 3000)
                new_enemy = Enemy(random_x, random_y, enemy_group)

        if pygame.time.get_ticks() - start_time >= 60000: # How long untill new wave of enemies
            spawnrate += 10
            start_time = pygame.time.get_ticks()
            print(spawnrate)

       
        if keys[pygame.K_SPACE] and player.bow_picked == False:
            if pygame.time.get_ticks() - start_sound >= 500:  # 1-second cooldown
            
                player.currentsound.play()
                start_sound = pygame.time.get_ticks()
                
                

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            for enemy in pygame.sprite.spritecollide(player, enemy_group, False):
                enemy.damage_enemy(player.damage, current_time, player, camera_group)
            

        # When the player presses space and the bow is picked
        if keys[pygame.K_SPACE] and player.bow_picked:
            
            facing = None
            if current_time - last_fire_time > fire_cooldown:
                player.currentsound.play()
                if player.up:
                    facing = 'up'
                    offset = (0, -30) 
                    last_fire_time = current_time
                elif player.down:
                    facing = 'down'
                    offset = (0, 30) 
                    last_fire_time = current_time
                elif player.left:
                    facing = 'left'
                    offset = (-30, 0)
                    last_fire_time = current_time
                elif player.right:
                    facing = 'right'
                    offset = (30, 0)
                    last_fire_time = current_time

                if facing:
                    arrow_x = player.rect.centerx + offset[0]
                    arrow_y = player.rect.centery + offset[1]

                    # Create the arrow
                    new_arrow = Arrow(arrow_x, arrow_y, arrow_group, facing, piercing=player.has_piercing)
                    arrow_group.add(new_arrow)


        for arrow in arrow_group:
            arrow.move()  # Move the arrow
            # Check for collisions with enemies
            for enemy in pygame.sprite.spritecollide(arrow, enemy_group, False):
                enemy.damage_enemy(player.damage, current_time, player, camera_group)
                if not arrow.piercing:
                    arrow.kill()

        #if pygame.sprite.spritecollide(player, enemy_group, False):
            #player.xp_gain_rate = 20
        #else:
            #player.xp_gain_rate = 5

        
        # Update and move enemies
        for enemy in enemy_group:
            enemy.move_towards_player(player, enemy_group)
            #print(enemy.health)

        for arrow in arrow_group:
            arrow.move()
        
        
        
        # Update player and draw everything
        player.update()
        camera_group.custom_draw(player, enemy, arrow_group)
        clock.tick(60)
        timer_txt(0)
        pygame.display.update()
    
# --------------------------------------------------------------------------------------------------------------------------------------------------------------

# Tutorial and tutorial methode
def tutorial():
    time.sleep(0.1)
    tutorial_run = True

    

    tutorial_img =  pygame.image.load('Assets/tutoiral.png').convert_alpha() # tutorials image
    buttons = {"Back": pygame.Rect(380, 540, 300, 50)}
    b_colour ='#5a2d2c'

    def draw_button(text, button):
        pygame.draw.rect(screen, b_colour , button)  # Draw the button
        text_surf = font.render(text, True, (255,255,255))  # White text
        text_rect = text_surf.get_rect(center=button.center)
        screen.blit(text_surf, text_rect)

    while tutorial_run:

        
        screen.blit(tutorial_img,(0,0)) # add the bg

        for label, button in buttons.items():
            draw_button(label, button)

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN: # check when button is pressed
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                for label, button in buttons.items():
                    if button.collidepoint(mouse_x, mouse_y):
                        if label == "Back":
                            click.play()
                            tutorial_run = False
                            time.sleep(0.1)
                            menu_run = True
                            return
                            
                    
    

# --------------------------------------------------------------------------------------------------------------------------------------------------------------

def game_over():
    time.sleep(0.1)
    game_over = True
    game_over_img =  pygame.image.load('Assets/game_over.png').convert_alpha()
    buttons = {"Play": pygame.Rect(380, 300, 300, 50), "Quit": pygame.Rect(380, 400, 300, 50)}
    b_colour ='#605e04'
    music = pygame.mixer.music.load("Sounds/game_over.wav")
    pygame.mixer.music.play(-1)

    def draw_button(text, button):
        pygame.draw.rect(screen, b_colour , button)  # Draw the button
        text_surf = font.render(text, True, (255,255,255))  # White text
        text_rect = text_surf.get_rect(center=button.center)
        screen.blit(text_surf, text_rect)

    while game_over:

        time.sleep(0.1)
        screen.blit(game_over_img,(0,0)) # add the bg

        for label, button in buttons.items():
            draw_button(label, button)

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN: # check when button is pressed
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                for label, button in buttons.items():
                    if button.collidepoint(mouse_x, mouse_y):
                        if label == "Play":
                            click.play()
                            main_game()
                        
                        elif label == "Quit":
                            click.play()
                            pygame.quit()
                            sys.exit()
                            

# --------------------------------------------------------------------------------------------------------------------------------------------------------------


# Menu items
bg_img =  pygame.image.load('Assets/menu_bg.png').convert_alpha()
bg_img = pygame.transform.scale(bg_img, (1066, 600))

click = pygame.mixer.Sound("Sounds/select.wav")

font = pygame.font.SysFont('impact', 40)
buttons = {"Play": pygame.Rect(380, 300, 300, 50), "Tutorial": pygame.Rect(380, 400, 300, 50), "Quit": pygame.Rect(380, 500, 300, 50)} # buttons dict
b_colour ='#1E90FF'

def draw_button(text, button):
    pygame.draw.rect(screen, b_colour , button)  # Draw the button
    text_surf = font.render(text, True, (255,255,255))  # White text
    text_rect = text_surf.get_rect(center=button.center)
    screen.blit(text_surf, text_rect)

music = pygame.mixer.music.load("Sounds/menu_music.wav")
pygame.mixer.music.play(-1)

menu_run = True

while menu_run:
    

    
    screen.blit(bg_img,(0,0)) # add the bg

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu_run = False

    # Draw buttons
    for label, button in buttons.items():
        draw_button(label, button)

    # Check for mouse click on buttons
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        for label, button in buttons.items():
            if button.collidepoint(mouse_x, mouse_y):
                time.sleep(0.1)
                if label == "Play":
                    click.play()
                    main_game()
                    
                elif label == "Tutorial":
                    click.play()
                    tutorial()
                     
                elif label == "Quit":
                    click.play()
                    menu_run = False
                    
                    

    pygame.display.flip()  # Update screen
# --------------------------------------------------------------------------------------------------------------------------------------------------------------
    
pygame.quit()
sys.exit()
