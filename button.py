#https://stackoverflow.com/questions/42577197/pygame-how-to-correctly-use-get-rect

#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      xanam
#
# Created:     25/11/2023
# Copyright:   (c) xanam 2023
# Licence:     <your licence>
#-------------------------------------------------------------------------------
'''
The 'button.py' module holds the object oriented paradigms set up for the
buttons found on the settings and pause menu. The 'Button' class has objects
then instantiated from it in the 'main.py' module.
'''
import pygame
import sys

pygame.init()
pygame.font.init()

font = pygame.font.SysFont("lucidaconsole", 40)

white = (248,248,248)
green = (117,192,106)

class Button(pygame.sprite.Sprite):
    def __init__(self,x,y,txt,btn,btnB,val,check1):
        super().__init__()
        self.img = btn
        self.img1 = btnB
        self.val = val
        self.check1 = check1
        self.x = x
        self.y = y
        self.txt = txt
        self.rect = self.img.get_rect(topleft=(self.x,self.y))
        self.txt1 = font.render(self.txt, "True", white)
        self.txtRect = self.txt1.get_rect(topleft=((self.x)+15,(self.y)+6.5))

    def display(self, screen):
        if self.check1==0:
            screen.blit(self.img, self.rect)
        else:
            screen.blit(self.img1, self.rect)
        screen.blit(self.txt1, self.txtRect)

    def input(self, position, value, screen,soundEffect):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            value = self.val
            if self.y==280:
                soundEffect.set_volume(value/5)
            soundEffect.play()
            screen.blit(self.img1, self.rect)
            self.check1 = 1
            return value, self.check1
        else:
            return value, self.check1

    def hover(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.txt1 = font.render(self.txt, True, green)
        else:
            self.txt1 = font.render(self.txt, True, white)