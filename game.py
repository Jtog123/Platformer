import pygame
import sys

from scripts.utils import load_image, load_images, Animation
from scripts.tilemap import Tilemap
from scripts.entities import PhysicsEntity, Player

#Jump, level editor, colliosions head hits bottom are off


class Game:
    def __init__(self) -> None:
        
        pygame.init()

        self.screen = pygame.display.set_mode((640,480))
        
        self.clock = pygame.time.Clock()
        self.display = pygame.Surface((320,240))
        self.movement = [False, False]

        
        self.assets = {
            'player': load_image('entities\player\idle\\0.png'),
            'stone': load_images('tiles\stone\\'),
            'decor': load_images('tiles/decor'),
            'player/idle': Animation(load_images('entities\player\idle')),
            'player/run' : Animation(load_images('entities\player\\run')),
            'player/jump':Animation(load_images('entities\player\jump'))
        }
        self.player = Player(self, (50,50),(14,18))
        self.tilemap = Tilemap(self, tile_size=16)
        self.tilemap.load('map.json')

        self.scroll = [0,0]

        print(self.assets['stone'][0])

    
    def update(self):
        pass

    def run(self):
        while True:
            #39,39,68
            self.display.fill((39,39,68))

            self.scroll[0] += (self.player.rect().centerx - (self.display.get_width() / 2) - self.scroll[0]) / 30

            self.scroll[1] += (self.player.rect().centery - (self.display.get_height() / 2) - self.scroll[1]) / 30

            self.render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, offset=self.render_scroll)

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=self.render_scroll)

            pygame.draw.rect(self.display, 'red', self.player.rect(),1)
            pygame.draw.circle(self.display, 'blue', (self.player.rect().centerx, self.player.rect().bottom), 2)
            pygame.draw.circle(self.display, 'green', ((self.player.rect().centerx - (self.display.get_width() / 2) - self.scroll[0]) / 30, self.player.rect().bottom), 2)
            #print(self.player.rect())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.player.velocity[1] = -3

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))

            pygame.display.update()
            self.clock.tick(60)
                

Game().run()
    

    