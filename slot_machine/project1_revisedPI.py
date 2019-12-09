# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 17:56:37 2019

@author: Lori
"""

import pygame

import os

import random
from pygame import mixer
#PI settings

#set up assests
game_folder=os.path.dirname(__file__)
img_folder=os.path.join(game_folder,"slot_images")
snd_dir = os.path.join(game_folder, "slot_sounds")

font_name = pygame.font.match_font('arial')
WIDTH=1366
HEIGHT=768
FPS=40

bank=1000

bet=1

 

#define colors
BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)

pygame.init()

screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Fairytale Slots")
clock=pygame.time.Clock()

background = pygame.image.load(os.path.join(img_folder, "background.JPG")).convert()
background_rect = background.get_rect()
mask1=pygame.image.load(os.path.join(img_folder, "mask.JPG")).convert()
mask1_rect=mask1.get_rect()
mask1_rect.y = 1

all_sprites=pygame.sprite.Group()


class Reel(pygame.sprite.Sprite):
    #sprite for reels
    
    def __init__(self,x,y):
       
        pygame.sprite.Sprite.__init__(self)
    
        self.image = pygame.Surface((240, 219))
        self.outcome()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y=y
        self.state = 0

        self.display=0
        
    def outcome(self):
        
        icon=random.choice(["book.png","carriage.png","frog.png","lamp.png","pegasus.png","wolf.jpg"])
        self.image = pygame.image.load(os.path.join(img_folder,icon)).convert()
        self.display=icon
        
    def update(self):
        if self.state == 0:
            if self.rect.y < 535:
                self.rect.y += 10
                if self.rect.y > 535:
                    self.rect.y = 535
        elif self.state == 1:
            if self.rect.y < 700:
                self.rect.y += 20
            if self.rect.y >= 700:
                self.rect.y = 300
                self.outcome()
def show_bonus_screen():#bonus screen
    draw_text(screen, "BONUS ROUND!", 100, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "BEWARE of WOLF!", 50,
              WIDTH / 2, HEIGHT / 6)
    draw_text(screen, "Press BUTTON to SPIN", 50,
              WIDTH / 2, HEIGHT / 2)
                     
def bank_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect= (12,87)#location
    surf.blit(text_surface, text_rect)
    
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
    
def show_go_screen():#start screen
    
    draw_text(screen, "Fairytale Slots", 100, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Press BUTTON to SPIN", 50,
              WIDTH / 2, HEIGHT / 2)

        
#initialize pygame and create window

all_sprites = pygame.sprite.Group()
reel1 = Reel(20,300)
reel2=Reel(335,300)
reel3=Reel(653,300)
reel4=Reel(986,300)
all_sprites.add(reel1,reel2,reel3,reel4)

def play_bonus():
    running=True
    bank=0
    timer=0
    game_state=0
    show_bonus_screen()
    
    while running:
    
        clock.tick(FPS)
        for event in pygame.event.get():
            #check for closing window
            if event.type==pygame.QUIT:
                running=False
            #if GPIO.event_detected(18):
            if event.type == pygame.KEYUP:
                
                if game_state == 0:
                    pygame.mixer.stop()
                    game_state = 1
                
                    reel1.state = 1
                    reel2.state = 1
                    reel3.state = 1
                    reel4.state = 1
          
             #update
        all_sprites.update()
        
         #draw and render       
    
        
       
        if game_state == 0:
             
            show_bonus_screen()#change to bonus screen create def
            begin = pygame.mixer.Sound(os.path.join(snd_dir,"bonus.wav"))
            begin.play()
            
        elif game_state == 1:
            
            timer=timer+1
            spin_sound=pygame.mixer.Sound(os.path.join(snd_dir,"spinning.wav"))
            spin_sound.play()
            
            if timer == 100:
                reel1.state=0
            if timer==120:
                reel2.state=0
            if timer==140:
                reel3.state=0
            if timer==160:
                reel4.state=0
                game_state = 2
                pygame.mixer.stop()
                
        elif game_state == 2:
            reel1.state = 2
            reel2.state = 2
            reel3.state = 2
            reel4.state = 2
        
            if (reel1.display==("book.png") and reel2.display==("book.png") and reel3.display==("book.png") and reel4.display==("book.png")):
                
                you_win=pygame.mixer.Sound(os.path.join(snd_dir,"jackpot.wav"))
                you_win.play()
                bank=bank+10000
                game_state = 5
                
            elif (reel1.display==reel2.display==reel3.display==reel4.display):
                
                you_win=pygame.mixer.Sound(os.path.join(snd_dir,"jackpot.wav"))
                you_win.play()
                bank=bank+1000
                game_state = 5
                
            elif (reel2.display==reel3.display==reel4.display):
                
                you_win=pygame.mixer.Sound(os.path.join(snd_dir,"jackpot.wav"))
                you_win.play()
                bank=bank+100
                game_state = 5
                
                
            elif (reel1.display==reel2.display==reel3.display):
                
                you_win=pygame.mixer.Sound(os.path.join(snd_dir,"jackpot.wav"))
                you_win.play()
                bank=bank+100
                game_state = 5
                
            elif (reel1.display==reel3.display==reel4.display):
                
                you_win=pygame.mixer.Sound(os.path.join(snd_dir,"jackpot.wav"))
                you_win.play()
                bank=bank+100
                game_state = 5
                
            elif (reel1.display==reel2.display==reel4.display):
                
                you_win=pygame.mixer.Sound(os.path.join(snd_dir,"jackpot.wav"))
                you_win.play()
                bank=bank+100
                game_state = 5     
                
            elif (reel1.display=="wolf.jpg" or reel2.display=="wolf.jpg" or reel3.display=="wolf.jpg" or reel4.display=="wolf.jpg"):
                you_lose=pygame.mixer.Sound(os.path.join(snd_dir,"game_over.wav"))
                you_lose.play()
                game_state=3
                
            else:
                
                you_lose=pygame.mixer.Sound(os.path.join(snd_dir,"game_over.wav"))
                you_lose.play()
                game_state=5
            
        elif game_state == 5:
           
            #RESET EVERYTHING
            game_state = 0
            timer = 0          
           
          #after drawing everything flip display again?????How do I makwe bank a global var???
   
       
#game loop
running=True

# game_state 0 is waiting mode
game_state = 0
timer=0    
  
while running:
    
    clock.tick(FPS)
    for event in pygame.event.get():
        #check for closing window
        if event.type==pygame.QUIT:
            running=False
        #if GPIO.event_detected(18):
        if event.type == pygame.KEYUP:
            
            if game_state == 0:
                pygame.mixer.stop()
                game_state = 1
            
                reel1.state = 1
                reel2.state = 1
                reel3.state = 1
                reel4.state = 1
                
              #need to reset game after every payout  
      
    #update
    all_sprites.update()
    
     #draw and render       

    screen.fill(BLACK)
   
    screen.blit(background,background_rect)
    all_sprites.draw(screen)
    screen.blit(mask1,mask1_rect)

    if game_state == 0:
        show_go_screen()
        begin = pygame.mixer.Sound(os.path.join(snd_dir,"beginning.ogg"))
        begin.play()
        
    elif game_state == 1:
        
        timer=timer+1
        spin_sound=pygame.mixer.Sound(os.path.join(snd_dir,"spinning.wav"))
        spin_sound.play()
        
        if timer == 100:
            reel1.state=0
        if timer==120:
            reel2.state=0
        if timer==140:
            reel3.state=0
        if timer==160:
            reel4.state=0
            game_state = 2
            pygame.mixer.stop()
            
    elif game_state == 2:
        reel1.state = 2
        reel2.state = 2
        reel3.state = 2
        reel4.state = 2

        if (reel1.display==("book.png") and reel2.display==("book.png") and reel3.display==("book.png") and reel4.display==("book.png")):
            
            you_win=pygame.mixer.Sound(os.path.join(snd_dir,"jackpot.wav"))
            you_win.play()
            bank=bank+10000-bet
            game_state = 3
            
        elif (reel1.display==reel2.display==reel3.display==reel4.display):
            
            you_win=pygame.mixer.Sound(os.path.join(snd_dir,"jackpot.wav"))
            you_win.play()
            bank=bank+1000-bet
            game_state = 3
            
        elif (reel2.display==reel3.display==reel4.display):
            
            you_win=pygame.mixer.Sound(os.path.join(snd_dir,"jackpot.wav"))
            you_win.play()
            bank=bank+100-bet
            game_state = 3
            
            
        elif (reel1.display==reel2.display==reel3.display):
            
            you_win=pygame.mixer.Sound(os.path.join(snd_dir,"jackpot.wav"))
            you_win.play()
            bank=bank+100-bet
            game_state = 3
            
        elif (reel1.display==reel3.display==reel4.display):
            
            you_win=pygame.mixer.Sound(os.path.join(snd_dir,"jackpot.wav"))
            you_win.play()
            bank=bank+100-bet
            game_state = 3
            
        elif (reel1.display==reel2.display==reel4.display):
            
            you_win=pygame.mixer.Sound(os.path.join(snd_dir,"jackpot.wav"))
            you_win.play()
            bank=bank+100-bet
            game_state = 3     
            
        elif reel4.display==("book.png"):
            bonus=pygame.mixer.Sound(os.path.join(snd_dir,"bonus.wav"))
            bonus.play()
            game_state=4
            if game_state==4:
                play_bonus()
                    
                    
                    
                    
        else:
            
            you_lose=pygame.mixer.Sound(os.path.join(snd_dir,"game_over.wav"))
            you_lose.play()
            bank=bank-bet
            game_state = 3
              
            
    
    elif game_state == 3:
        #RESET EVERYTHING
        game_state = 0
        timer = 0
        

        
    #after drawing everything flip display
    
    bank_text(screen, str(bank), 50, WIDTH / 2, 10)
    pygame.display.flip()
  
pygame.quit()

