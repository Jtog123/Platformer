import pygame
import sys
from game import Game
from button import Button

pygame.init()

SCREEN = pygame.display.set_mode((640, 480))
BG = pygame.image.load("assets/Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/Handy00-YV1o.ttf", size)

def play():

    new_game = Game()
    if new_game.run():
        new_game.run()
    else:
        #Load game over menu
        main_menu()


def main_menu():
    while True:
        SCREEN.blit(BG, (0,0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(50).render("MAIN MENU", True, "#fbf5ef")
        MENU_RECT = MENU_TEXT.get_rect(center=(SCREEN.get_width() / 2, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/playbutton.png"), pos=(SCREEN.get_width() / 2, 200), 
                                text_input="PLAY", font=get_font(25), base_color="#494d7e", hovering_color="#fbf5ef")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/playbutton.png"), pos=(SCREEN.get_width() / 2, 350), 
                                text_input="QUIT", font=get_font(25), base_color="#494d7e", hovering_color="#fbf5ef")
        

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.change_color(MENU_MOUSE_POS)
            button.update(SCREEN)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.check_for_input(MENU_MOUSE_POS):
                    play()
                #if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                #   options()
                if QUIT_BUTTON.check_for_input(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()


