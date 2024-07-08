import pygame, sys
from Menu.menu_button import TextButton
import config

pygame.display.set_caption("PySandPlat")




def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def character(window, menu, menu_background, character_choice):
    run = True
    while run:
        window.blit(menu_background, (0,0))
     

        menu_mouse_pos = pygame.mouse.get_pos()
        menu_text = get_font(55).render("CHARACTER SELECT", True, "#d7fcd4")
        menu_rect = menu_text.get_rect(center=(500, 100))

        window.blit(menu_text, menu_rect)

        mask_button = TextButton(image=pygame.image.load("assets/Menu/Buttons/Options Rect.png"), pos=(500, 250), 
                            text_input="MASK DUDE", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        ninja_button = TextButton(image=pygame.image.load("assets/Menu/Buttons/Options Rect.png"), pos=(500, 350), 
                            text_input="NINJA FROG", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        pink_button = TextButton(image=pygame.image.load("assets/Menu/Buttons/Options Rect.png"), pos=(500, 450), 
                            text_input="PINK MAN", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        virtual_button = TextButton(image=pygame.image.load("assets/Menu/Buttons/Options Rect.png"), pos=(500, 550), 
                            text_input="VIRTUAL GUY", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        back_button = TextButton(image=pygame.image.load("assets/Menu/Buttons/Quit Rect.png"), pos=(500, 700), 
                            text_input="BACK", font=get_font(50), base_color="#d7fcd4", hovering_color="White")

        for button in [mask_button, ninja_button, pink_button, virtual_button, back_button]:
            button.changeColor(menu_mouse_pos)
            button.update(window)

        for event in pygame.event.get():
           if event.type == pygame.MOUSEBUTTONDOWN:
                if mask_button.checkForInput(menu_mouse_pos):
                    config.character_choice = "MaskDude"
                    menu(window)
                if ninja_button.checkForInput(menu_mouse_pos):
                    config.character_choice = "NinjaFrog"
                    menu(window)
                if pink_button.checkForInput(menu_mouse_pos):
                    config.character_choice = "PinkMan"
                    menu(window)
                if virtual_button.checkForInput(menu_mouse_pos):
                    config.character_choice = "VirtualGuy"
                    menu(window)
                if back_button.checkForInput(menu_mouse_pos):
                    menu(window)
                    print(config.character_choice)
                    pygame.quit()
                    

        pygame.display.update()
        # pygame.quit()
        # quit()
    

