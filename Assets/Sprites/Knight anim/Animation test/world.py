from settings import *

BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class World:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.player = pygame.Rect(270,180,50,50)
        self.player_colour = RED
        self.block_colour = BLUE
        self.targets = []

        self.move_y = 5
        self.move_x = 5

        #Collisions
        self.left_col = False
        self.right_col = False
        self.up_col = False
        self.down_col = False



    def draw_rects(self, y_axis): #Rects that the player collides with

        for _ in range(1):
            self.target_rect = pygame.Rect(150, y_axis, 50, 50)
            self.targets.append(self.target_rect)
            y_axis += 50

        #Draw rectangles
        for self.target_rect in self.targets:
            pygame.draw.rect(self.display_surface, self.block_colour, self.target_rect)

    def collision(self):
        
        for self.target_rect in self.targets:
            # X collision Right
            if self.targets[0].colliderect(self.player.x + self.move_x, self.player.y , 50,50):
                self.right_col = True
            else:
                self.right_col = False

            #X collision left
            if self.targets[0].colliderect(self.player.x - self.move_x, self.player.y , 50,50):
                self.left_col = True
            else:
                self.left_col = False

            #Y collision Bottom
            if self.targets[0].colliderect(self.player.x, self.player.y + self.move_y, 50,50):
                self.down_col = True
            else:
                self.down_col = False

            #Y collision Top
            if self.targets[0].colliderect(self.player.x, self.player.y - self.move_y, 50,50):
                self.up_col = True
            else:
                self.up_col = False


    #shows where the collision occurs
    def show_collision(self):

        if self.right_col:
            right_col = pygame.Rect(self.player.x + 40, self.player.y + 5, 10,40)
            pygame.draw.rect(self.display_surface, YELLOW, right_col)

        if self.left_col:
            right_col = pygame.Rect(self.player.x, self.player.y + 5, 10,40)
            pygame.draw.rect(self.display_surface, YELLOW, right_col)

        if self.up_col:
            right_col = pygame.Rect(self.player.x + 5, self.player.y, 40,10)
            pygame.draw.rect(self.display_surface, YELLOW, right_col)

        if self.down_col:
            right_col = pygame.Rect(self.player.x + 5, self.player.y + 45, 40,10)
            pygame.draw.rect(self.display_surface, YELLOW, right_col)


        

    def run(self):
        self.display_surface.fill(GREY)

        pygame.draw.rect(self.display_surface, self.player_colour, self.player)
        
        #Collision
        # if self.player.collidelist(self.targets) >= 0:
        #     self.player_colour = 'green'
        # else:
        #     self.player_colour = 'red'


        #Draw Rectangles
        self.draw_rects(180)


        #user input
        key = pygame.key.get_pressed()

        if key[pygame.K_a] == True and not self.left_col:
            self.player.x -= self.move_x
        if key[pygame.K_d] == True and not self.right_col:
            self.player.x += self.move_x
        if key[pygame.K_w] == True and not self.up_col:
            self.player.y -= self.move_y
        if key[pygame.K_s] == True and not self.down_col:
            self.player.y += self.move_y

        self.collision()
        self.show_collision()
