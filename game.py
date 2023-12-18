import pygame
import sys


screen = pygame.display.set_mode((300,300))
clock = pygame.time.Clock

running = True
while running:

    clock.tick(60)
    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    
    pygame.display.update()

    

    