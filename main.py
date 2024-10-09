import pygame, sys
import os
from random import randint



class Tree(pygame.sprite.Sprite):
    def __init__(self,pos,group):
        super().__init__(group)
        self.image = pygame.image.load('Assets/rocket1.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,group):
        super().__init__(group)
        self.image = pygame.image.load('Assets/Knight_v1.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.direction = pygame.math.Vector2()
        self.speed = 5

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = 0
        self.direction.y = 0
        
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1

        if keys[pygame.K_d]:
            self.direction.x = 1                
        elif keys[pygame.K_a]:
            self.direction.x = -1


    def update(self):
        self.input()
        self.rect.center += self.direction * self.speed

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

#setup
camera_group = pygame.sprite.Group()
Player((640, 360),camera_group)

for i in range(20):
    random_x = randint(0,1000)
    random_y = randint(0,1000)
    Tree((random_x, random_y),camera_group)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((113, 221, 238))
    
    camera_group.update()
    camera_group.draw(screen)

    pygame.display.update()
    clock.tick(60)

