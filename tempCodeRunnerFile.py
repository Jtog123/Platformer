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
                        
                    if QUIT_BUTTON.check_for_input(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()