import pygame
import math
import random


 

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
        self.animation_offset = (0,0) #-3,3??

        self.flip = False
        self.air_time = 0
        self.set_action('idle')


        #Program jump aloowance
        self.can_jump = True
        #in jump code, if can_jump allow jump, if jumping can_jump = False
        #in update check if can_jump == True and we have collided with floor can_jump = True
        #else can jump = False

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

        #Second he starts falling velocity changes direction and can jump is true
        
        #single jump code
        if self.velocity[1] < 0:
            self.can_jump = False
        elif self.velocity[1] == 0:
            self.can_jump = True

        self.animation.update()


    
    def render(self, surface, offset = (0,0)):
        #surface.blit(self.game.assets['player'], self.position)
        surface.blit(pygame.transform.flip(self.animation.img(), self.flip, False),
                    (self.position[0] - offset[0] + self.animation_offset[0], self.position[1] - offset[1] + self.animation_offset[1])) #animation offset causing buffer???


class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0
    
    def update(self, tilemap, movement = (0,0)):
        super().update(tilemap, movement=movement)

        self.air_time += 1

        if self.collisions['down']:
            self.air_time = 0

        if self.air_time > 4:
            self.set_action('jump')
        elif movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')

class Enemy(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'enemy', pos, size)

        #self.max_pos = pos[0] + 50
        #self.min_pos = pos[0] - 50

        self.walking = 0

        #self.left = True
        #self.right= False
    
    def update(self, tilemap, movement = (0,0)):
        
        #maybe use sin function?
        if self.walking:
            if tilemap.solid_check((self.rect().centerx + (-7 if self.flip else 7), self.position[1] + 23)):
                movement = (movement[0]- 0.5 if self.flip else 0.5, movement[1])
            else:
                self.flip = not self.flip
            self.walking = max(0, self.walking)
        elif random.random() < .1:
            self.walking = random.randint(10,120)

        super().update(tilemap, movement=movement)

class Enemy2:
        def __init__(self, game, e_type, pos, size) -> None:
            self.game = game
            self.screen = self.game.screen
            self.e_type = e_type
            self.position = list(pos)
            self.size = size
            self.action=''
            self.flip = False
            self.animation_offset = (0,0)

            self.max_pos = self.position[1] + 100
            self.min_pos = self.position[1] - 100
            self.down = True
            self.up = False

            self.set_action('idle')

        def rect(self):
            return pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
        
        def set_action(self,action):
            if action != self.action:
                self.action = action
                self.animation = self.game.assets[self.e_type + '/' + self.action].copy()

        def update(self, tilemap, pos):
            if self.down and pos != self.min_pos:
                self.position[1] -= 1
            else:
                self.down = False
                self.up = True
            
            if self.up and pos != self.max_pos:
                self.position[1] += 1
            else:
                self.up = False
                self.down = True
            #self.position[1] = pos
            #print(self.position[1])

            self.animation.update()

        def render(self, surface, offset=(0,0)):
            surface.blit(pygame.transform.flip(self.animation.img(), self.flip, False),
                        (self.position[0] - offset[0] + self.animation_offset[0], self.position[1] - offset[1] + self.animation_offset[1]))
                    
            
        #need set_action function



        '''
                if self.left and self.position[0] != self.min_pos:
                    self.position[0] -= .5
                else:
                    self.left = False
                    self.right= True
                
                if self.right and self.position[0] != self.max_pos:
                    self.position[0] += .5
                else:
                    self.right = False
                    self.left= True
        '''


