import pygame
import sys
import math
import time


from scripts.utils import load_image, load_images, Animation
from scripts.tilemap import Tilemap
from scripts.entities import PhysicsEntity, Player,Enemy,Enemy2
from scripts.clouds import Clouds
from scripts.finishflag import FinishFlag



class Game:
    def __init__(self, mixer) -> None:
        
        #pygame.init()

        self.mixer = mixer

        self.play_channel = self.mixer.Channel(1)
        self.game_won_channel = self.mixer.Channel(2)
        self.playing_song = 'assets/newplayingsong2.mp3'
        self.win_song = 'assets/winsong1.mp3'



        self.screen = pygame.display.set_mode((640,480))
        
        self.clock = pygame.time.Clock()
        self.display = pygame.Surface((320,240))
        #self.load_menu()
        self.movement = [False, False]

        
        self.assets = {
            'player': load_image('entities\player\idle\\0.png'),
            'enemy' : load_image('entities\enemy\idle\\0.png'),
            'enemy2': load_image('entities\enemy2\idle\\0.png'),
            'stone': load_images('tiles\stone\\'),
            'decor': load_images('tiles/decor'),
            'finishflag': load_images('tiles/finishflag'),
            'clouds' : load_images('clouds'),
            'player/idle': Animation(load_images('entities\player\idle')),
            'player/run' : Animation(load_images('entities\player\\run')),
            'player/jump':Animation(load_images('entities\player\jump')),
            'enemy/idle':Animation(load_images('entities\enemy\idle'), img_duration=10),
            'enemy2/idle': Animation(load_images('entities\enemy2\idle'))
        }

        self.clouds = Clouds(self.assets['clouds'], count = 16)
        self.player = Player(self, (50,50),(14,18))
        self.enemies = []
        self.enemies2 = []
        self.tilemap = Tilemap(self, tile_size=16)
        self.tilemap.load('map.json')
        self.start_time = pygame.time.get_ticks()


        print(self.assets['finishflag'])
        self.finish_flag_pairs= self.tilemap.extract([('finishflag', 0)])[0]
        print(self.finish_flag_pairs)
        self.finishflag = FinishFlag((int(self.finish_flag_pairs['pos'][0]),int(self.finish_flag_pairs['pos'][1])), self.assets['finishflag'][0], (10,100))
        #for flag in self.finishflag:
        #print(self.finishflag['pos'])
        

        #Gives information 'give type and variant'
        #print(self.tilemap.extract([('decor', 0)], keep = True))

        for spawner in self.tilemap.extract([('spawners',0), ('spawners', 1), ('spawners', 2)]):
            if spawner['variant'] == 0:
                self.player.position = spawner['pos']
            elif spawner['variant'] == 1:
                self.enemies.append(Enemy(self, spawner['pos'], (18,18)))
            elif spawner['variant'] == 2:
                self.enemies2.append(Enemy2(self,'enemy2', spawner['pos'], (18,18)))


        self.scroll = [0,0]

        self.game_end = 0
        self.touched = False

        self.play_channel.play(pygame.mixer.Sound(self.playing_song), loops=-1)



        

       # print(self.assets['stone'][0])
        

    
    def update(self):
        pass

    def load_lose_screen(self):

        font = pygame.font.SysFont('assets/Handy00-YV1o.ttf', 30)
        text_surface = font.render('Game Over!', False, (255,0,0))
        self.display.blit(text_surface,((self.display.get_width() / 2) - text_surface.get_width() / 2,
                                        (self.display.get_height() / 2) - text_surface.get_height()/ 2)) 

        self.now_time = pygame.time.get_ticks()
        seconds = (self.now_time - self.game_end) / 1000
        

        #print(seconds)

        if seconds >= .1:
            return seconds
        else:
            return .01
        
    def load_fall_screen(self):
        font = pygame.font.SysFont('assets/Handy00-YV1o.ttf', 30)
        text_surface = font.render('Game Over!', False, (255,0,0))
        self.display.blit(text_surface,((self.display.get_width() / 2) - text_surface.get_width() / 2,
                                        (self.display.get_height() / 2) - text_surface.get_height()/ 2)) 



    def load_win_screen(self):
        #Queue win music

        font = pygame.font.SysFont('assets/Handy00-YV1o.ttf', 30)
        text_surface = font.render('You Win!', False, (0,255,0))
        self.display.blit(text_surface,((self.display.get_width() / 2) - text_surface.get_width() / 2,
                                        (self.display.get_height() / 2) - text_surface.get_height()/2))
        
        self.win_time = pygame.time.get_ticks()
        seconds = (self.win_time - self.game_end) / 1000

        if seconds >= 2:
            return seconds
        else:
            return .01


        
        

        #if 3 seconds pass after death of character return True
        #print(seconds)
        #return True
        


    def run(self):
        while True:

            #self.start_time = time.time()
            
            self.display.fill((39,39,68))

            self.scroll[0] += (self.player.rect().centerx - (self.display.get_width() / 2) - self.scroll[0]) / 30

            self.scroll[1] += (self.player.rect().centery - (self.display.get_height() / 2) - self.scroll[1]) / 30

            self.render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.clouds.update()
            self.clouds.render(self.display, offset=self.render_scroll)

            self.tilemap.render(self.display, offset=self.render_scroll)

            self.finishflag.render(self.display, offset=self.render_scroll)

            for enemy in self.enemies.copy():
                enemy.update(self.tilemap, (0,0))
                enemy.render(self.display,self.render_scroll)
            
            for enemy in self.enemies2.copy():
                enemy.update(self.tilemap, enemy.position[1])
                enemy.render(self.display, self.render_scroll)

            


            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=self.render_scroll)


            #pygame.draw.rect(self.display, 'red', self.player.rect(),1)
            #pygame.draw.circle(self.display, 'blue', (self.player.rect().centerx, self.player.rect().bottom), 2)
            #pygame.draw.circle(self.display, 'green', ((self.player.rect().centerx - (self.display.get_width() / 2) - self.scroll[0]) / 30, self.player.rect().bottom), 2)
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
                        if self.player.can_jump:
                            self.player.velocity[1] = -3


                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            
            for enemy in self.enemies:
                if self.player.rect().colliderect(enemy.rect()):
                    if self.touched == False:
                        pygame.event.set_blocked(pygame.KEYDOWN)
                        self.game_end = pygame.time.get_ticks()
                    
                    self.touched = True
                    seconds = self.load_lose_screen()
                    if seconds >= .1:
                        pygame.event.set_allowed(pygame.KEYDOWN)
                        self.play_channel.stop()
                        return False
                    print(seconds)
                    
                    

            for enemy2 in self.enemies2:
                if self.player.rect().colliderect(enemy2.rect()):
                    if self.touched == False:
                        pygame.event.set_blocked(pygame.KEYDOWN)
                        self.game_end = pygame.time.get_ticks()

                    self.touched = True
                    seconds = self.load_lose_screen()
                    if seconds >= .1:
                        pygame.event.set_allowed(pygame.KEYDOWN)
                        self.play_channel.stop()
                        return False

                     
            if self.player.position[1] >= self.display.get_height(): 
                print(self.player.position[1], self.display.get_height())
                self.game_end = pygame.time.get_ticks()#or self.screen?
                self.load_fall_screen()#??????????????????
                if self.game_end / 1000 >= 3:
                    self.play_channel.stop()
                    return False
                

            if self.player.rect().colliderect(self.finishflag.rect()):
                if self.touched == False:
                    self.play_channel.stop()
                    self.game_won_channel.play(pygame.mixer.Sound(self.win_song))
                    pygame.event.set_blocked(pygame.KEYDOWN)
                    self.game_end = pygame.time.get_ticks()
                
                self.touched = True
                
                seconds = self.load_win_screen()

                if seconds >= 3:
                    pygame.event.set_allowed(pygame.KEYDOWN)
                    return False
      

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))

            pygame.display.update()
            self.clock.tick(60)
                

#Game().run()
    

    