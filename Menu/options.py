import pygame, sys
from Menu.menu_button import TextButton
from Menu.character_menu import character
from Menu.controls_menu import controls


pygame.display.set_caption("PySandPlat")




def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def options(window, menu, menu_background):
    run = True
    while run:
        window.blit(menu_background, (0,0))
     

        menu_mouse_pos = pygame.mouse.get_pos()
        menu_text = get_font(55).render("OPTIONS", True, "#d7fcd4")
        menu_rect = menu_text.get_rect(center=(500, 100))

        window.blit(menu_text, menu_rect)

        character_button = TextButton(image=pygame.image.load("assets/Menu/Buttons/Options Rect.png"), pos=(500, 250), 
                            text_input="CHARACTER", font=get_font(62), base_color="#d7fcd4", hovering_color="White")
        how_to_play_button = TextButton(image=pygame.image.load("assets/Menu/Buttons/Options Rect.png"), pos=(500, 400), 
                            text_input="CONTROLS", font=get_font(65), base_color="#d7fcd4", hovering_color="White")
        back_button = TextButton(image=pygame.image.load("assets/Menu/Buttons/Quit Rect.png"), pos=(500, 550), 
                            text_input="BACK", font=get_font(65), base_color="#d7fcd4", hovering_color="White")

        for button in [character_button, how_to_play_button, back_button]:
            button.changeColor(menu_mouse_pos)
            button.update(window)

        for event in pygame.event.get():
           if event.type == pygame.MOUSEBUTTONDOWN:
                if character_button.checkForInput(menu_mouse_pos):
                    character(window, menu, menu_background)
                if how_to_play_button.checkForInput(menu_mouse_pos):
                    controls(window, menu, menu_background)
                if back_button.checkForInput(menu_mouse_pos):
                    menu(window)
                    pygame.quit()
                    

        pygame.display.update()
        # pygame.quit()
        # quit()
    

