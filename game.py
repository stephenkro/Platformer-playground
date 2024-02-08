import os
import random
import math
import pygame, sys
from os import listdir
from os.path import isfile, join
import Game.game_button
import Game.Classes.player
import Game.Classes.object
import Game.Functions.load
import Game.Functions.physics
from Menu.menu_button import TextButton
import Game.Classes.enemy

pygame.init()



WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_VEL = 5
Player = Game.Classes.player.Player
Trophy = Game.Classes.object.Trophy
Fruit = Game.Classes.object.Fruit
Slime = Game.Classes.enemy.Slime
Fire = Game.Classes.object.Fire
Block = Game.Classes.object.Block
get_background = Game.Functions.load.get_background
handle_move = Game.Functions.physics.handle_move
menu_background = pygame.image.load("assets/Background/Sky.png")
menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))
create_platform = Game.Functions.load.create_platform
create_fruit = Game.Functions.load.create_fruit
create_fire = Game.Functions.load.create_fire



window = pygame.display.set_mode((WIDTH, HEIGHT))
menu_button = Game.game_button
pygame.display.set_caption("Cute Platformer")

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)
    
def draw(window, background, bg_image, player, objects, offset_x, menu_items, heart, score_text):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x)

    player.draw(window, offset_x)
    menu_items.draw(window)
    window.blit(score_text, (125, 5))
   
    i = 0
    x_heart = 0
    while i < player.health : 
        window.blit(heart, (x_heart, 0))
        x_heart += 25
        i+=1
    

    pygame.display.update()


def main(window):
    FINAL_SCORE=0
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")
    block_size = 96
    back_button_img = pygame.image.load("assets/Menu/Buttons/Back.png") 
    back_button = menu_button.GameButton(970,0, back_button_img, 2)
    heart_img = pygame.image.load('assets/Other/Heart.png')
    hearts = pygame.transform.scale(heart_img, (25, 25))
    trophy = Trophy(3100, 450, 120, 120)
    
    
    player = Player(0, 100, 50, 50)
    slime = [Slime(150, 645, 44, 30), Slime(500, 645, 44, 30)]
    first_layer_items = [*create_fruit(320, 370, 4, Fruit, 30, 30, 'Melon'), *create_fruit(-600, 370, 4, Fruit, 30, 30, 'Bananas'), *create_fruit(1200, 370, 2, Fruit, 30, 30, 'Kiwi')]
    items = [*first_layer_items]
    floor_fire = [*create_fire(150, 64, 6, block_size, Fire)]
    for fire in floor_fire:
        fire.on()
    floor = [Block(i * block_size, HEIGHT - block_size, block_size) for i in range(-WIDTH * 3 // block_size, (WIDTH * 3) // block_size)]
    first_layer_platform = [*create_platform(300, 4, 4, block_size, Block), 
                            *create_platform(-600, 4, 4, block_size, Block),
                            *create_platform(-1200, 4, 4, block_size, Block), 
                            *create_platform(1200, 4, 2, block_size, Block), 
                            *create_platform(2000, 4, 4, block_size, Block)]
    second_layer_platform = [*create_platform(800, 6, 4, block_size, Block), *create_platform(1600, 6, 4, block_size, Block)]
    rising_level = [*create_platform(0, 2, 1, block_size, Block), *create_platform(-95, 2, 1, block_size, Block), *create_platform(1200, 2, 1, block_size, Block), *create_platform(3000, 3, 3, block_size, Block)]
    platforms = [*floor, *first_layer_platform, *second_layer_platform, *rising_level]
    
    objects = [*platforms, *floor_fire, *slime, trophy, *items]
    enemy_objects = [*rising_level]

    offset_x = 0
    scroll_area_width = 200

    run = True
    while run:
        clock.tick(FPS)
        score_text = get_font(20).render(f'Score:{player.score}', True, "#d7fcd4")
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                run = False
                break
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()
                if event.key == pygame.K_x:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.draw(window) == True:
                    menu(window)

        player.loop(FPS)
        for enemy in slime:
            enemy.loop(enemy_objects)
        # slime.loop(enemy_objects)
        # slime2.loop(enemy_objects)
        for fire in floor_fire:
            fire.loop()
        
        handle_move(player, objects)
        draw(window, background, bg_image, player, objects, offset_x, back_button, hearts, score_text)
        FINAL_SCORE = player.score
     
        if player.rect.y > 800 :
            game_over(window, False, FINAL_SCORE)
        if player.health == 0:
            game_over(window, False, FINAL_SCORE)
        if handle_move(player, objects) == True:
            game_over(window, True, FINAL_SCORE)
        

        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

    pygame.quit()
    quit()

def game_over(window, win, score):
    run = True
    while run:
        if(win == False):
            window.fill("BLACK")
            menu_text = get_font(55).render("GAME OVER", True, "#d7fcd4")
            menu_rect = menu_text.get_rect(center=(500, 100))
            menu_mouse_pos = pygame.mouse.get_pos()
            score_text = get_font(50).render(f'FINAL SCORE: {score}', True, "#d7fcd4")
            score_rect = score_text.get_rect(center=(500, 200))
            
            
            play_again_button = TextButton(image=pygame.image.load("assets/Menu/Buttons/Play Rect.png"), pos=(500, 350), 
                                text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
            main_menu_button = TextButton(image=pygame.image.load("assets/Menu/Buttons/Play Rect.png"), pos=(500, 500), 
                                text_input="MENU", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
            quit_button = TextButton(image=pygame.image.load("assets/Menu/Buttons/Quit Rect.png"), pos=(500, 650), 
                                text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
            window.blit(menu_text, menu_rect)
            window.blit(score_text, score_rect)
            
            for button in [play_again_button, main_menu_button, quit_button]:
                button.changeColor(menu_mouse_pos)
                button.update(window)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_again_button.checkForInput(menu_mouse_pos):
                        main(window)
                    if main_menu_button.checkForInput(menu_mouse_pos):
                        menu(window)
                    if quit_button.checkForInput(menu_mouse_pos):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()
        else:
           window.fill("BLACK")
           menu_text = get_font(55).render("YOU WIN!", True, "#d7fcd4")
           menu_rect = menu_text.get_rect(center=(500, 100))
           menu_mouse_pos = pygame.mouse.get_pos()
           score_text = get_font(50).render(f'FINAL SCORE: {score}', True, "#d7fcd4")
           score_rect = score_text.get_rect(center=(500, 250))
           
           main_menu_button = TextButton(image=pygame.image.load("assets/Menu/Buttons/Play Rect.png"), pos=(500, 400), 
                                text_input="MENU", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
           quit_button = TextButton(image=pygame.image.load("assets/Menu/Buttons/Quit Rect.png"), pos=(500, 550), 
                                text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
           window.blit(menu_text, menu_rect)
           window.blit(score_text, score_rect)
            
           for button in [main_menu_button, quit_button]:
                button.changeColor(menu_mouse_pos)
                button.update(window)
           for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # if score_button.checkForInput(menu_mouse_pos):
                    #     print("SCORE")
                    if main_menu_button.checkForInput(menu_mouse_pos):
                        menu(window)
                    if quit_button.checkForInput(menu_mouse_pos):
                        pygame.quit()
                        sys.exit()

           pygame.display.update()      



def menu(window):
    run = True
    while run:
        window.blit(menu_background, (0,0))
     

        menu_mouse_pos = pygame.mouse.get_pos()
        menu_text = get_font(55).render("CUTE PLATFORMER", True, "#d7fcd4")
        menu_rect = menu_text.get_rect(center=(500, 100))

        window.blit(menu_text, menu_rect)

        play_button = TextButton(image=pygame.image.load("assets/Menu/Buttons/Play Rect.png"), pos=(500, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        options_button = TextButton(image=pygame.image.load("assets/Menu/Buttons/Options Rect.png"), pos=(500, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        quit_button = TextButton(image=pygame.image.load("assets/Menu/Buttons/Quit Rect.png"), pos=(500, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        for button in [play_button, options_button, quit_button]:
            button.changeColor(menu_mouse_pos)
            button.update(window)

        for event in pygame.event.get():
           if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_pos):
                    main(window)
                if options_button.checkForInput(menu_mouse_pos):
                    print('OPTIONS')
                if quit_button.checkForInput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        

menu(window)
