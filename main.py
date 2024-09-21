import pygame
import os


WHITE = 255, 255, 255
WIDTH, HEIGHT = 900, 500
FPS = 60
VEL = 3

KNIGHT_WIDTH, KNIGHT_HEIGHT = 55, 55


KNIGHT = pygame.image.load(os.path.join('Assets', 'Knight_v1.png'))
KNIGHT = pygame.transform.scale(KNIGHT, (KNIGHT_WIDTH, KNIGHT_HEIGHT))


WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Lives v1')

def draw_window(knight):
    WIN.fill(WHITE)
    WIN.blit(KNIGHT, (knight.x, knight.y))
    pygame.display.update()

def knight_movement(keys_pressed, knight):
    if keys_pressed[pygame.K_a] and knight.x - VEL > 0:
            knight.x -= VEL
    if keys_pressed[pygame.K_d] and knight.x + VEL + knight.width < WIDTH:
            knight.x += VEL
    if keys_pressed[pygame.K_s] and knight.y + VEL + knight.height < HEIGHT:
            knight.y += VEL
    if keys_pressed[pygame.K_w] and knight.y + VEL > 0:
            knight.y -= VEL
            
def main():
    knight = pygame.Rect(450, 250, KNIGHT_WIDTH, KNIGHT_HEIGHT)
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()
        knight_movement(keys_pressed, knight)
                
        draw_window(knight)
                
    pygame.quit()

if __name__ == '__main__':
    main()

