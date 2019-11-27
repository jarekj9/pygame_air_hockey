import pygame
import time
import random

pygame.init()
SCREEN_W,SCREEN_H=500,700
screen=pygame.display.set_mode([SCREEN_W,SCREEN_H])
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
GREEN = (20, 255, 140)
GREY = (210, 210 ,210)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
BLACK = (0, 0, 0)
BLUE = ( 0,0,255)


class PAD(pygame.sprite.Sprite):
    def __init__(self,x,y,player):
        super().__init__()
        self.player = player
        self.width,self.height = 100,25
        self.corner_width = 20
        self.image = pygame.Surface([self.width,self.height])
        self.image = pygame.image.load("pad.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x,y
        self.xspeed,self.yspeed = 0,0

    def move(self):
        self.xspeed,self.yspeed = 0,0
        #react to arrow keys:
        if self.player == 'player1':
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_RIGHT]: self.xspeed= 5
            if keys_pressed[pygame.K_UP]:    self.yspeed=-5
            if keys_pressed[pygame.K_DOWN]:  self.yspeed= 5
            if keys_pressed[pygame.K_LEFT]:  self.xspeed=-5
        if self.player == 'cpu':
            if ball.rect.x + ball.width/2 > self.rect.x + self.width/2:
                  self.xspeed=  5
            else: self.xspeed= -5

        self.rect.y += self.yspeed
        self.rect.x += self.xspeed
        #set some movement limits
        if self.rect.x > SCREEN_W-self.width:  self.rect.x = SCREEN_W-self.width
        if self.rect.x < 0:                    self.rect.x = 0
        if self.rect.y > SCREEN_H-self.height: self.rect.y = SCREEN_H-self.height
        if self.rect.y < 0:                    self.rect.y = 0

class BALL(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.width,self.height = 25,25
        self.image = pygame.Surface([self.width,self.height])
        self.image = pygame.image.load("ball.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x,y
        self.xspeed, self.yspeed = 6,6

    def move(self):
        self.pad_bounce(pad1)
        self.pad_bounce(pad2)
        self.detect_goal(gate1,score1)
        self.detect_goal(gate2,score2)
        self.rect.x += self.xspeed
        self.rect.y += self.yspeed
        #set some movement limits
        if self.rect.x > SCREEN_W-self.width:   self.xspeed = -abs(self.xspeed)
        if self.rect.x < 0:                     self.xspeed =  abs(self.xspeed)
        if self.rect.y > SCREEN_H-self.height : self.yspeed = -abs(self.yspeed)
        if self.rect.y < 0:                     self.yspeed =  abs(self.yspeed)
        #set some speed limits when ball slows down:
        if self.xspeed >  5: self.xspeed-=0.5
        if self.xspeed < -5: self.xspeed+=0.5
        if self.yspeed >  5: self.yspeed-=0.5
        if self.yspeed < -5: self.yspeed+=0.5

    def pad_bounce(self,pad):
        #hit pad from the top (center)
        if (self.rect.x < pad.rect.x + pad.width - pad.corner_width  and
            self.rect.x + self.width > pad.rect.x + pad.corner_width and
            self.rect.y + self.height > pad.rect.y and
            self.rect.y < pad.rect.y + pad.rect.height):
            #change ball speed depending on pad speed
            self.xspeed += pad.xspeed/2
            self.yspeed = -self.yspeed + pad.yspeed/2
            self.rect.y += pad.yspeed #to avoid ball lock inside pad
        #hit pad right corener
        if (self.rect.x < pad.rect.x + pad.width      and
            self.rect.x > pad.rect.x + pad.width - pad.corner_width and
            self.rect.y + self.height > pad.rect.y and
            self.rect.y < pad.rect.y + pad.rect.height):

            if self.xspeed < 0: self.xspeed = -self.xspeed + pad.xspeed/2 #only if ball comes from right side
            else:               self.xspeed += pad.xspeed/2                
            self.yspeed = -self.yspeed + pad.yspeed/2

        #hit pad left corener
        if (self.rect.x + self.width > pad.rect.x      and
            self.rect.x + self.width < pad.rect.x + pad.corner_width and
            self.rect.y + self.height > pad.rect.y and
            self.rect.y < pad.rect.y + pad.rect.height):

            if self.xspeed > 0: self.xspeed = -self.xspeed + pad.xspeed/2   #only if ball comes from left side
            else:               self.xspeed += pad.xspeed/2                
            self.yspeed = -self.yspeed + pad.yspeed/2

    def detect_goal(self,gate,score):
        #detect collision with gate
        if (self.rect.x + self.width > gate.rect.x and
            self.rect.x < gate.rect.x + gate.width and
            self.rect.y + self.height > gate.rect.y and
            self.rect.y < gate.rect.y + gate.height):
            
            score.goals+=1
            #display goal message:
            image = pygame.Surface([100, 30], pygame.SRCALPHA, 32)   
            rect = image.get_rect()
            image.fill(BLACK)
            Font = pygame.font.SysFont("Times New Roman", 38)   
            ImageFailCount = Font.render("GOAL !", 1, RED)
            screen.blit(ImageFailCount, (180, 300)) 
            pygame.display.flip()  

            pygame.time.delay(2000)
            global play_again
            play_again = 1

class GATE(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.width,self.height = 100,30
        self.image = pygame.Surface([self.width,self.height])
        pygame.draw.rect(self.image, BLUE, [0, 0, self.width, self.height], 0)
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x,self.rect.y = x,y

#display goals for each gate
class SCORE(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()   
        self.x,self.y = x,y   
        self.image = pygame.Surface([100, 30], pygame.SRCALPHA, 32)   
        self.rect = self.image.get_rect()
        self.image.fill(BLACK)
        self.Font = pygame.font.SysFont("Times New Roman", 24)
        self.goals=0
    def update(self):       
        self.ImageFailCount = self.Font.render("Goals: "+str(self.goals), 1, RED)
        screen.blit(self.ImageFailCount, (self.x, self.y)) 
        pygame.display.flip()  


score1=SCORE(205,10)
score2=SCORE(205,660)
def initialize_objects(): 
    global gate1,gate2,pad1,pad2,ball,score1,score2,all_sprites_list,play_again
    #initialize objects
    gate1=GATE(200,10)
    gate2=GATE(200,660)
    pad1=PAD(300,600,'player1')
    pad2=PAD(300,70,'cpu')
    ball=BALL(200,200)
    #prepare sprites
    all_sprites_list = pygame.sprite.Group()
    all_sprites_list.add(score1,score2,gate1,gate2,pad1,pad2,ball)
    all_sprites_list.update()
    all_sprites_list.draw(screen)
    pygame.display.flip()
    play_again = 0


#main loop
running = True
initialize_objects()
while running:
    pace=clock.tick(60)     #pace is time for single frame
    screen.fill(BLACK)
    all_sprites_list.draw(screen)
    pygame.display.update()
    
    #press Esc to quit
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False

    pad1.move()
    pad2.move()
    ball.move()
    score1.update()
    score2.update()

    if play_again: initialize_objects() #reset all except scores
