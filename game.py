import pygame
import sys

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size) -> None:
        self.game = game
        self.screen = self.game.screen
        self.e_type = e_type
        self.position = list(pos)
        self.size = size
        self.velocity = [0,0]

    def update(self, movement = (0,0)):

        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.position[0] += frame_movement[0]

        self.position[1] += frame_movement[1]
    
    def render(self,surface):
        pass




class Game:
    def __init__(self) -> None:
        
        pygame.init()

        self.screen = pygame.display.set_mode((640,320))
        self.clock = pygame.time.Clock()


        self.assets = {}

    
    def update(self):
        pass

    def run(self):
        while True:
            self.clock.tick(60)
            self.screen.fill((0,0,0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                

Game().run()
    

    