from settings import *
from world import World

BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Game:
    def __init__(self):
        pygame.init()
        self.WIN = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Collision Demo")

        self.clock = pygame.time.Clock()

        self.world_screen = World()
        


    def run(self):
        while True:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.QUIT()


            self.world_screen.run()

            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()
