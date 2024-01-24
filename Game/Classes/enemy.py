import pygame
from os import listdir
from os.path import isfile, join
import Game.Functions.load
import random


load_sprite_sheets = Game.Functions.load.load_sprite_sheets

class Enemy(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    ANIMATION_DELAY = 5

    def __init__(self, x, y, width, height, name=None , pace=0, turn_after = 20):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.animation_count = 0
        self.name = name
        self.pace_size = pace
        self.pace_count = 0
        self.turn_after  = turn_after

  
    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))
    
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
    
  

class Slime(Enemy):
   def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, 'slime', 3, 500)
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.slime = load_sprite_sheets("Enemies", "Slime", width, height, True)
        self.animation_name = 'Idle-Run'
        self.direction = 'left'
        self.image = None
        self.mask = None
        self.pace_size = self.pace_size
        self.turn_after = self.turn_after
        

   def loop(self):
        self.movement(self.direction)
        sprite_sheet_name = self.animation_name + " " + "(44x30)" + "_" + self.direction
        sprites = self.slime[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0
    
   def movement(self, direction):
        if self.rect.y < 645:
            self.rect.y += Enemy.GRAVITY
        if direction == 'left':
            self.pace_count += 1
            self.rect.x += self.pace_size
            if(self.pace_count >= self.turn_after):
                self.direction = 'right'
                self.pace_count = 0
                self.animation_count = 0

        if direction == 'right':
            self.pace_count += 1
            self.rect.x -= self.pace_size
            if(self.pace_count >= self.turn_after):
                self.direction = 'left'
                self.pace_count = 0
                self.animation_count = 0
   
   def update(self):
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)
       
        
        
       