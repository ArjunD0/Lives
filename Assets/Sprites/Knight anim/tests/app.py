import pygame
import pygame.display
import pygame.transform
import pygame.sprite

from pygame.locals import *



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.player_stand = pygame.transform.rotozoom(
            pygame.image.load("assets/Player/player_stand.png"), 0, 2
        ) 
        self.player_jump = pygame.transform.rotozoom(
            pygame.image.load("assets/Player/jump.png"), 0, 2
        ) 



        self.player_walk_1 = pygame.transform.rotozoom(
            pygame.image.load("assets/Player/player_walk_1.png"), 0, 2
        ) 
        self.player_walk_2 = pygame.transform.rotozoom(
            pygame.image.load("assets/Player/player_walk_2.png"), 0, 2
        )

        self.sprites = []
        self.sprites.append(self.player_walk_1)
        self.sprites.append(self.player_walk_2)
        
        self.current_sprite = 0

        self.image = self.player_stand

        self.rect = pygame.Rect(300, get_platform(self.image), self.image.get_width(), self.image.get_height())

        self.left = False
        self.right = False

        self.gravity = 0


    def animate(self):
        if self.rect.y == get_platform(self.image):
            self.current_sprite += 0.2

            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0

            self.image = self.sprites[int(self.current_sprite)]

        if self.rect.y != get_platform(self.image):
            self.image = self.player_jump


    def movement(self):
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[K_a]:
            self.left = True
            self.animate()

        if keys_pressed[K_d]:
            self.right = True
            self.animate()

        if keys_pressed[K_SPACE] and self.rect.y == get_platform(self.image):
            self.gravity = -20

    def update(self):
        
        if self.right:
            self.rect.x += 10
            self.right = False

        if self.left:
            self.rect.x -= 10
            self.left = False    

        if self.rect.y != get_platform(self.image):
            self.image = self.player_jump

        else:
            self.image = self.player_stand

        self.gravity += 1
        self.rect.y += self.gravity

        if self.rect.y >= get_platform(self.image):
            self.rect.y = get_platform(self.image)




width, height = 1600, 850
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Animation with sprites")

ground = pygame.transform.rotozoom(
    pygame.image.load("assets/ground.png"), 0, 2
)
sky = pygame.transform.rotozoom(
    pygame.image.load("assets/sky.png"), 0, 2
)



# Getting Platform
def get_platform(image):
    return 600 - image.get_height()



# Player
player = Player()
player_group = pygame.sprite.Group()
player_group.add(player)

while 1:

    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == KEYDOWN:
            pass

    # Draw
    display.blit(sky, (0,0))
    display.blit(ground, (0, 600))
    
    player_group.draw(display)
    player_group.update()

    player.movement()
    
    pygame.display.update()