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

    def __init__(self, x, y, width, height, name=None , pace=0, turn_after = 0):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.x_vel = 0
        self.y_vel = 0
        self.animation_count = 0
        self.name = name
        self.pace_size = pace
        self.pace_count = 0
        self.turn_after  = turn_after
        self.fall_count = 0

  
    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))
    
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
    
 
    

class Slime(Enemy):
   def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, 'slime', 3, 350)
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.slime = load_sprite_sheets("Enemies", "Slime", width, height, True)
        self.animation_name = 'Idle-Run'
        self.direction = random.choice(['left', 'right'])
        self.image =self.slime['Idle-Run (44x30)_left'][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.pace_size = self.pace_size
        self.turn_after = self.turn_after
        

   def loop(self, objects):
        self.movement(self.direction, objects)
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
   
   def enemy_collide(self, objects):
        collided_object = None
        # self.update()
        for obj in objects:
            if pygame.sprite.collide_mask(self, obj):
                 collided_object = obj
                 break
        # self.update()
        return collided_object

    
   def movement(self, direction, objects):
        collide = self.enemy_collide(objects)
        if collide and direction == 'left':
            self.direction = 'right'
            self.pace_count = 0
            self.animation_count = 0
            
        elif collide and direction == 'right':
             self.direction = 'left'
             self.pace_count = 0
             self.animation_count = 0

        else:
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
       
        
        
       