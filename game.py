import pygame
import sys

from scripts.utils import load_image, load_images
from scripts.tilemap import Tilemap

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
    
    def render(self, surface):
        surface.blit(self.game.assets['player'], self.position)

#Next we need to design the tile for the floor


class Game:
    def __init__(self) -> None:
        
        pygame.init()

        self.screen = pygame.display.set_mode((640,320))
        self.clock = pygame.time.Clock()
        self.movement = [False, False]

        self.player = PhysicsEntity(self,'player', (50,50),(14,18))
        
        self.assets = {
            'player': load_image('entities\player\idle\\0.png'),
            'stone': load_images('tiles\stone\\')
        }
        self.tilemap = Tilemap(self, tile_size=16)

        print(self.assets['stone'][0])

    
    def update(self):
        pass

    def run(self):
        while True:
            
            self.screen.fill((100,10,10))
            self.tilemap.render(self.screen)

            self.player.update((self.movement[1] - self.movement[0], 0))
            self.player.render(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            pygame.display.update()
            self.clock.tick(60)
                

Game().run()
    

    