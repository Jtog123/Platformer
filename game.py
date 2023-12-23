import pygame
import sys

from scripts.utils import load_image, load_images, Animation
from scripts.tilemap import Tilemap

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size) -> None:
        self.game = game
        self.screen = self.game.screen
        self.e_type = e_type
        self.position = list(pos)
        self.size = size
        self.collisions = { 'up':False, 'down': False, 'right':False, 'left':False}
        self.velocity = [0,0]
        self.action = ''

        self.flip = False
        self.set_action('idle')

    def rect(self):
        return pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
    
    def set_action(self,action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.e_type + '/' + self.action].copy()
    
    def update(self, tilemap, movement = (0,0)):
        self.collisions = {'up':False, 'down': False, 'right': False, 'left': False}

        frame_movement = (movement[0] + self.velocity[0],
                        movement[1] + self.velocity[1])
        self.position[0] += frame_movement[0]
        entity_rect = self.rect()

        for rect in tilemap.physics_rects_around(self.position):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True

                self.position[0] = entity_rect.x

        self.position[1] += frame_movement[1]
        entity_rect = self.rect()

        for rect in tilemap.physics_rects_around(self.position):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom  = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True

                self.position[1] = entity_rect.y + 1
        
        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True


        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0
        
        self.animation.update()

    
    def render(self, surface):
        #surface.blit(self.game.assets['player'], self.position)
        surface.blit(pygame.transform.flip(self.animation.img(), self.flip, False), self.position)

#Next we need to design the tile for the floor


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
            'player/idle': Animation(load_images('entities\player\idle'))
        }
        self.player = PhysicsEntity(self, 'player', (50,50),(14,18))
        self.tilemap = Tilemap(self, tile_size=16)

        print(self.assets['stone'][0])

    
    def update(self):
        pass

    def run(self):
        while True:
            #39,39,68
            self.display.fill((39,39,68))
            self.tilemap.render(self.display)

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display)

            pygame.draw.rect(self.display, 'red', self.player.rect(),1)
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
    

    