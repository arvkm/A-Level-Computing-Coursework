#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      CoderBox
#
# Created:     15/12/2023
# Copyright:   (c) CoderBox 2023
# Licence:     <your licence>
#-------------------------------------------------------------------------------
'''
This module, 'pieces.py' holds all object oriented paradigms for the tetrominoes
used during gameplay. Each specific piece of the tetromino is called as an
object in the 'main.py' menu to form whole pieces. Subclasses for all 7 unique
pieces are derived from the 'Piece' parent class.
'''
import pygame,sys
pygame.init()

class Piece(pygame.sprite.Sprite):
    def __init__(self,img,pnum,pplace,screen):
        super().__init__()
        self.img = img#piece's own image
        self.tile = pygame.image.load('tile.png').convert()#img that covers old piece.
        self.num = pnum#this determines which sprite it is in all of them
        self.place = pplace#this is which part of the piece it is
        self.rstate = 0#which rotation state it is in
        self.row = 0#row value used for hard dropping
        self.locked = False#whether piece is locked down and can no longer move
        self.first=True#variable to allow for no insta-locking
        self.newrstate = [0,0]

    def movement(self, matrixarray, check, screen):#matrix array shows where they're all stored, check determines which key was pressed(0-move down,1-left,2-right)
        '''
        any other number is used to signify which row to drop to during a hard drop when hardrop is true
        -1 as check value used to check if pieces are in same place meaning game should end
        '''
        if check==-1 and matrixarray[self.pInArray[0]][self.pInArray[1]]!=0:
            return True
        if check==0 and self.pInArray[0]!=19:#if piece not at bottom of array
            if matrixarray[self.pInArray[0]+1][self.pInArray[1]]==0:#check if there isn't piece underneathe where piece is
                self.first = True#piece has not touched bottom
                canMove = True
                return canMove
            else:
                canMove = False
                return canMove
        elif check==0 and (self.pInArray[0]==19):
            canMove = False
            return canMove
        if check==1 and self.pInArray[1]!=0:#if moving left and piece's position not already on side.
            if matrixarray[self.pInArray[0]][self.pInArray[1]-1]==0:
                canMove = True
                return canMove
            else:
                canMove = False
                return canMove
        elif check==1 and (self.pInArray[1]==0):
            canMove = False
            return canMove
        if check==2 and self.pInArray[1]!=9:#if moving right and piece's position not already on side.
            if matrixarray[self.pInArray[0]][self.pInArray[1]+1]==0:#if nothing obstructing to right
                canMove = True
                return canMove#return that it can move
            else:
                canMove = False
                return canMove#return that it cannot move
        elif check==2 and (self.pInArray[1]==9):#if on the side
            canMove = False
            return canMove#return that it cannot move

    def save2matrix(self, matrixarray):
        matrixarray[self.pInArray[0]][self.pInArray[1]] = self.num#save unique number to matrix array
        return matrixarray#return the array to main code

    def update(self,matrixarray,screen):
        if self.first==True:
            self.check1 = pygame.time.get_ticks()#check variable to check how long piece has been touching floor
            self.first=False
        else:
            self.check2 = pygame.time.get_ticks()
            if (self.check2-self.check1)>500:
                self.lock()

    '''
    def rotate(self,matrixarray,screen,newrstate,testNo):#check=0 - clockwise, check=1, counter
        if self.rstate==0:
            if newrstate==1:
                if self.name=="T":
                    if testNo==0:
                        if self.place==1 and matrixarray[self.pInArray[0]+1][self.pInArray[1]-1]==0:
                            return True
                        elif self.place==2 and matrixarray[self.pInArray[0]+1][self.pInArray[1]+1]==0:
                            return True
                        elif self.place==4 and matrixarray[self.pInArray[0]-1][self.pInArray[1]-1]==0:
                            return True
                        elif self.place==3:
                            return True
                        else:
                            return False
                    if testNo==1:
                        if self.place==1 and matrixarray[self.pInArray[0]][self.pInArray[1]-1]==0:
                            return True
                        elif self.place==2 and matrixarray[self.pInArray[0]][self.pInArray[1]+1]==0:
                            return True
                        elif self.place==3 and matrixarray[self.pInArray[0]-1][self.pInArray[1]]==0:
                            return True
                        elif self.place==4 and matrixarray[self.pInArray[0]-2][self.pInArray[1]-1]==0:
                            return True
                        else:
                            return False
    '''


    #def wallKick(self,matrixarray,screen,newrstate):
        #pass

    def hold(self,screen):
        screen.blit(self.tile,self.rect)#cover up where piece was

    def hardDrop(self, matrixarray, screen):
        for i in range(self.pInArray[0]+1,20):#check from row below one piece currently on down to row 19
            if matrixarray[i][self.pInArray[1]]!=0:#if row below contains something
                return i-1#return corresponding row
            elif i==19 and matrixarray[i][self.pInArray[1]]==0:#if last row is empty
                return i#return corresponding row
        return 19

    def lock(self):
        self.locked=True

class sO(Piece):
    def __init__(self,img,pnum,pplace,screen):
        super().__init__(img,pnum,pplace,screen)
        if self.place==1:
            self.x = 380
            self.y = 121
            self.bottomPiece=False
            self.leftPiece=True
            self.rightPiece=False
            self.pInArray = [0,4]
        elif self.place==2:
            self.x = 400
            self.y = 121
            self.bottomPiece=False
            self.leftPiece=False
            self.rightPiece=True
            self.pInArray = [0,5]
        elif self.place==3:
            self.x = 380
            self.y = 141
            self.bottomPiece=True
            self.leftPiece=True
            self.rightPiece=False
            self.pInArray = [1,4]
        elif self.place==4:
            self.x = 400
            self.y = 141
            self.bottomPiece=True
            self.leftPiece=False
            self.rightPiece=True
            self.pInArray = [1,5]
        self.rect = self.img.get_rect(topleft=(self.x,self.y))
        self.name="O"
        self.spawnM(screen)

    def spawnM(self,screen):
        screen.blit(self.img, self.rect)
        pygame.display.flip()

    def rotate(self,matrixarray,screen,newrstate,testNo):#check=0 - clockwise, check=1, counter
        if self.rstate==0:
            if newrstate==1:
                if testNo==0:
                    '''
                    if self.place==1 and matrixarray[self.pInArray[0]+1][self.pInArray[1]-1]==0:
                        return True
                    elif self.place==2 and matrixarray[self.pInArray[0]+1][self.pInArray[1]+1]==0:
                        return True
                    elif self.place==4 and matrixarray[self.pInArray[0]-1][self.pInArray[1]-1]==0:
                        return True
                    elif self.place==3:
                        return True
                    else:
                        return False
                    '''
                    pass
                if testNo==1:
                    '''
                    if self.place==1 and matrixarray[self.pInArray[0]][self.pInArray[1]-1]==0:
                        return True
                    elif self.place==2 and matrixarray[self.pInArray[0]][self.pInArray[1]+1]==0:
                        return True
                    elif self.place==3 and matrixarray[self.pInArray[0]-1][self.pInArray[1]]==0:
                        return True
                    elif self.place==4 and matrixarray[self.pInArray[0]-2][self.pInArray[1]-1]==0:
                        return True
                    else:
                        return False
                    '''
                    pass

    def movement1(self, matrixarray, check, screen, hardrop):
        '''
        any other number is used to signify which row to drop to during a hard drop when hardrop is true
        '''
        if hardrop==False:#var to check if a hardrop is occurring
            if check==0:
                self.pInArray[0]+=1
                if self.rstate==0:
                    if self.place==1 or self.place==2:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                self.rect.move_ip(0,20)#move rect 20 pixels down
                screen.blit(self.img,self.rect)#blit new piece
            elif check==1:
                self.pInArray[1]-=1
                if self.rstate==0:
                    if self.place==4 or self.place==2:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                self.rect.move_ip(-20,0)#move rect 20 pixels down
                screen.blit(self.img,self.rect)#blit new piece
            elif check==2:
                self.pInArray[1]+=1
                if self.rstate==0:
                    if self.place==1 or self.place==3:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                self.rect.move_ip(20,0)#move rect 20 pixels right
                screen.blit(self.img,self.rect)#blit new piece
        else:
            screen.blit(self.tile,self.rect)#cover up original tiles
            if self.rstate==0:#if in first rotation state
                if self.place==3 or self.place==4:#if bottom two pieces
                    displacement = check[0]-self.pInArray[0]#how far away og pos is to new pos
                else:
                    displacement = check[0]-1-self.pInArray[0]#how far away og pos is to new pos
            self.pInArray[0]+=displacement#new array position
            self.rect.move_ip(0,displacement*20)#move rect here
            screen.blit(self.img,self.rect)#blit new position

    def rotate1(self, screen, test, newrstate):
        self.rstate=newrstate

class sT(Piece):
    def __init__(self,img,pnum,pplace,screen):
        super().__init__(img,pnum,pplace,screen)
        if self.place==1:
            self.x = 400
            self.y = 121
            self.bottomPiece=False
            self.leftPiece=True
            self.rightPiece=True
            self.pInArray = [0,5]
        elif self.place==2:
            self.x = 380
            self.y = 141
            self.bottomPiece=True
            self.leftPiece=True
            self.rightPiece=False
            self.pInArray = [1,4]
        elif self.place==3:
            self.x = 400
            self.y = 141
            self.bottomPiece=True
            self.leftPiece=False
            self.rightPiece=False
            self.pInArray = [1,5]
        elif self.place==4:
            self.x = 420
            self.y = 141
            self.bottomPiece=True
            self.leftPiece=False
            self.rightPiece=True
            self.pInArray = [1,6]
        self.rect = self.img.get_rect(topleft=(self.x,self.y))
        self.name="T"
        self.spawnM(screen)
    def spawnM(self,screen):
        screen.blit(self.img, self.rect)
        pygame.display.flip()

    def rotate1(self,screen,newrstate,check):
        if check==0:
            screen.blit(self.tile,self.rect)
        else:
            if newrstate==0:
                if self.place==1:
                    self.bottomPiece=False
                    self.leftPiece=True
                    self.rightPiece=True
                elif self.place==2:
                    self.bottomPiece=True
                    self.leftPiece=True
                    self.rightPiece=False
                elif self.place==3:
                    self.bottomPiece=True
                    self.leftPiece=False
                    self.rightPiece=False
                elif self.place==4:
                    self.bottomPiece=True
                    self.leftPiece=False
                    self.rightPiece=True
            elif newrstate==1:
                if self.place==1:
                    self.bottomPiece=True
                    self.leftPiece=False
                    self.rightPiece=True
                elif self.place==2:
                    self.bottomPiece=False
                    self.leftPiece=True
                    self.rightPiece=True
                elif self.place==3:
                    self.bottomPiece=False
                    self.leftPiece=True
                    self.rightPiece=False
                elif self.place==4:
                    self.bottomPiece=True
                    self.leftPiece=True
                    self.rightPiece=True
            elif newrstate==2:
                if self.place==1:
                    self.bottomPiece=True
                    self.leftPiece=True
                    self.rightPiece=True
                elif self.place==2:
                    self.bottomPiece=True
                    self.leftPiece=False
                    self.rightPiece=True
                elif self.place==3:
                    self.bottomPiece=False
                    self.leftPiece=False
                    self.rightPiece=False
                elif self.place==4:
                    self.bottomPiece=True
                    self.leftPiece=True
                    self.rightPiece=False
            elif newrstate==3:
                if self.place==1:
                    self.bottomPiece=True
                    self.leftPiece=True
                    self.rightPiece=False
                elif self.place==2:
                    self.bottomPiece=True
                    self.leftPiece=False
                    self.rightPiece=True
                elif self.place==3:
                    self.bottomPiece=False
                    self.leftPiece=False
                    self.rightPiece=True
                elif self.place==4:
                    self.bottomPiece=False
                    self.leftPiece=True
                    self.rightPiece=True
            self.rstate = newrstate
            displacement1 = self.newrstate[0]-self.pInArray[0]
            displacement2 = self.newrstate[1]-self.pInArray[1]
            self.rect.move_ip(displacement2*20,displacement1*20)
            self.pInArray = self.newrstate
            screen.blit(self.img,self.rect)
            self.newrstate=[0,0]

    def rotate(self,matrixarray,newrstate):#matrixarray to check if next place is free/newrstate to which pos it is now in
        if self.rstate==0:#if new pos is 0th pos  #testNo to know which test the rotation is now checking.
            if newrstate==1:#if new rstate is 1 (if they rotated clockwise)
                if self.place==1 and self.pInArray[1]+1!=10:#check if pos where it would be is free
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]+1]#if it is, save this in a variable
                        return True#return true for loop to continue for all pieces
                elif self.place==2 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]+1]
                        return True
                elif self.place==4 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]-1]
                        return True
                elif self.place==3:
                    self.newrstate = [self.pInArray[0],self.pInArray[1]]
                    return True
                else:
                    return False#if untrue, return false for loop to stop
            elif newrstate==3:
                if self.place==1 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]-1]
                        return True
                elif self.place==2 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]+1]
                        return True
                elif self.place==3:
                    self.newrstate = [self.pInArray[0],self.pInArray[1]]
                    return True
                elif self.place==4 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]-1]
                        return True
                else:
                    return False
        elif self.rstate==1:
            if newrstate==2:
                if self.place==1 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]-1]
                        return True
                elif self.place==2 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]+1]
                        return True
                elif self.place==3:
                    self.newrstate = [self.pInArray[0],self.pInArray[1]]
                    return True
                elif self.place==4 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]-1]
                        return True
                else:
                    return False
            elif newrstate==0:
                if self.place==1 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]-1]
                        return True
                elif self.place==2 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]-1]
                        return True
                elif self.place==3:
                    self.newrstate = [self.pInArray[0],self.pInArray[1]]
                    return True
                elif self.place==4 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]+1]
                        return True
                else:
                    return False
        elif self.rstate==2:
            if newrstate==3:
                if self.place==1 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]-1]
                        return True
                elif self.place==2 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]-1]
                        return True
                elif self.place==3:
                    self.newrstate = [self.pInArray[0],self.pInArray[1]]
                    return True
                elif self.place==4 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]+1]
                        return True
                else:
                    return False
            elif newrstate==1:
                if self.place==1 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]+1]
                        return True
                elif self.place==2 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]-1]
                        return True
                elif self.place==3:
                    self.newrstate = [self.pInArray[0],self.pInArray[1]]
                    return True
                elif self.place==4 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]+1]
                        return True
                else:
                    return False
        elif self.rstate==3:
            if newrstate==2:
                if self.place==1 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]+1]
                        return True
                elif self.place==2 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]+1]
                        return True
                elif self.place==3:
                    self.newrstate = [self.pInArray[0],self.pInArray[1]]
                    return True
                elif self.place==4 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]-1]
                        return True
                else:
                    return False
            elif newrstate==0:
                if self.place==1 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]+1]
                        return True
                elif self.place==2 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]-1]
                        return True
                elif self.place==3:
                    self.newrstate = [self.pInArray[0],self.pInArray[1]]
                    return True
                elif self.place==4 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]+1]
                        return True
                else:
                    return False

    def movement1(self, matrixarray, check, screen, hardrop):
        if hardrop==False:#var to check if a hardrop is occurring
            if check==0:
                self.pInArray[0]+=1
                if self.rstate==0:
                    if self.place==1 or self.place==2 or self.place==4:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                elif self.rstate==1:
                    if self.place==1 or self.place==2:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                elif self.rstate==2:
                    if self.place==3 or self.place==2 or self.place==4:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                elif self.rstate==3:
                    if self.place==1 or self.place==4:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                self.rect.move_ip(0,20)#move rect 20 pixels down
                screen.blit(self.img,self.rect)#blit new piece
            elif check==1:
                self.pInArray[1]-=1
                if self.rstate==0:
                    if self.place==1 or self.place==4:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                elif self.rstate==1:
                    if self.place==1 or self.place==2 or self.place==4:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                elif self.rstate==2:
                    if self.place==1 or self.place==2:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                elif self.rstate==3:
                    if self.place==2 or self.place==4 or self.place==3:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                self.rect.move_ip(-20,0)#move rect 20 pixels left
                screen.blit(self.img,self.rect)#blit new piece
            elif check==2:
                self.pInArray[1]+=1
                if self.rstate==0:
                    if self.place==1 or self.place==2:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                elif self.rstate==1:
                    if self.place==2 or self.place==4 or self.place==3:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                elif self.rstate==2:
                    if self.place==1 or self.place==4:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                elif self.rstate==3:
                    if self.place==2 or self.place==4 or self.place==1:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                self.rect.move_ip(20,0)#move rect 20 pixels right
                screen.blit(self.img,self.rect)#blit new piece
        else:
            screen.blit(self.tile,self.rect)#cover up original tiles
            if self.rstate==0:#if in first rotation state
                if self.place==3 or self.place==4 or self.place==2:#if bottom two pieces
                    displacement = check[0]-self.pInArray[0]#how far away og pos is to new pos
                else:
                    displacement = check[0]-1-self.pInArray[0]#how far away og pos is to new pos
            if self.rstate==1:#if in first rotation state
                if check[1]==1:
                    if self.place==4:#if bottom two pieces
                        displacement = check[0]+1-self.pInArray[0]#how far away og pos is to new pos
                    elif self.place==3 or self.place==1:
                        displacement = check[0]-self.pInArray[0]#how far away og pos is to new pos
                    elif self.place==2:
                        displacement = check[0]-1-self.pInArray[0]#how far away og pos is to new pos
                else:
                    if self.place==4:#if bottom two pieces
                        displacement = check[0]-self.pInArray[0]#how far away og pos is to new pos
                    elif self.place==3 or self.place==1:
                        displacement = check[0]-1-self.pInArray[0]#how far away og pos is to new pos
                    elif self.place==2:
                        displacement = check[0]-2-self.pInArray[0]#how far away og pos is to new pos
            if self.rstate==3:#if in first rotation state
                if check[1]==1:
                    if self.place==2:#if bottom two pieces
                        displacement = check[0]+1-self.pInArray[0]#how far away og pos is to new pos
                    elif self.place==3 or self.place==1:
                        displacement = check[0]-self.pInArray[0]#how far away og pos is to new pos
                    elif self.place==4:
                        displacement = check[0]-1-self.pInArray[0]#how far away og pos is to new pos
                else:
                    if self.place==2:#if bottom two pieces
                        displacement = check[0]-self.pInArray[0]#how far away og pos is to new pos
                    elif self.place==3 or self.place==1:
                        displacement = check[0]-1-self.pInArray[0]#how far away og pos is to new pos
                    elif self.place==4:
                        displacement = check[0]-2-self.pInArray[0]#how far away og pos is to new pos
            if self.rstate==2:#if in first rotation state
                if check[1]==4 or check[1]==2:
                    if self.place==1:#if bottom two pieces
                        displacement = check[0]+1-self.pInArray[0]#how far away og pos is to new pos
                    else:
                        displacement = check[0]-self.pInArray[0]#how far away og pos is to new pos
                else:
                    if self.place==1:#if bottom two pieces
                        displacement = check[0]-self.pInArray[0]#how far away og pos is to new pos
                    else:
                        displacement = check[0]-1-self.pInArray[0]#how far away og pos is to new pos
            self.pInArray[0]+=displacement#new array position
            self.rect.move_ip(0,displacement*20)#move rect here
            screen.blit(self.img,self.rect)#blit new position

class sI(Piece):
    def __init__(self,img,pnum,pplace,screen):
        super().__init__(img,pnum,pplace,screen)
        if self.place==1:
            self.x = 360
            self.y = 121
            self.bottomPiece=True
            self.leftPiece=True
            self.rightPiece=False
            self.pInArray = [0,3]
        elif self.place==2:
            self.x = 380
            self.y = 121
            self.bottomPiece=True
            self.leftPiece=False
            self.rightPiece=False
            self.pInArray = [0,4]
        elif self.place==3:
            self.x = 400
            self.y = 121
            self.bottomPiece=True
            self.leftPiece=False
            self.rightPiece=False
            self.pInArray = [0,5]
        elif self.place==4:
            self.x = 420
            self.y = 121
            self.bottomPiece=True
            self.leftPiece=False
            self.rightPiece=True
            self.pInArray = [0,6]
        self.rect = self.img.get_rect(topleft=(self.x,self.y))
        self.name="I"
        self.spawnM(screen)
    def spawnM(self,screen):
        screen.blit(self.img, self.rect)
        pygame.display.flip()

    def rotate1(self,screen,newrstate,check):
        if check==0:
            screen.blit(self.tile,self.rect)
        else:
            if newrstate==0:
                if self.place==1:
                    self.bottomPiece=True
                    self.leftPiece=True
                    self.rightPiece=False
                elif self.place==2:
                    self.bottomPiece=True
                    self.leftPiece=False
                    self.rightPiece=False
                elif self.place==3:
                    self.bottomPiece=True
                    self.leftPiece=False
                    self.rightPiece=False
                elif self.place==4:
                    self.bottomPiece=True
                    self.leftPiece=False
                    self.rightPiece=True
            elif newrstate==1:
                if self.place==1:
                    self.bottomPiece=False
                    self.leftPiece=True
                    self.rightPiece=True
                elif self.place==2:
                    self.bottomPiece=False
                    self.leftPiece=True
                    self.rightPiece=True
                elif self.place==3:
                    self.bottomPiece=False
                    self.leftPiece=True
                    self.rightPiece=True
                elif self.place==4:
                    self.bottomPiece=True
                    self.leftPiece=True
                    self.rightPiece=True
            elif newrstate==2:
                if self.place==1:
                    self.bottomPiece=True
                    self.leftPiece=False
                    self.rightPiece=True
                elif self.place==2:
                    self.bottomPiece=True
                    self.leftPiece=False
                    self.rightPiece=False
                elif self.place==3:
                    self.bottomPiece=True
                    self.leftPiece=False
                    self.rightPiece=False
                elif self.place==4:
                    self.bottomPiece=True
                    self.leftPiece=True
                    self.rightPiece=False
            elif newrstate==3:
                if self.place==1:
                    self.bottomPiece=True
                    self.leftPiece=True
                    self.rightPiece=True
                elif self.place==2:
                    self.bottomPiece=False
                    self.leftPiece=True
                    self.rightPiece=True
                elif self.place==3:
                    self.bottomPiece=False
                    self.leftPiece=True
                    self.rightPiece=True
                elif self.place==4:
                    self.bottomPiece=False
                    self.leftPiece=True
                    self.rightPiece=True
            self.rstate = newrstate
            displacement1 = self.newrstate[0]-self.pInArray[0]
            displacement2 = self.newrstate[1]-self.pInArray[1]
            self.rect.move_ip(displacement2*20,displacement1*20)
            self.pInArray = self.newrstate
            screen.blit(self.img,self.rect)
            self.newrstate=[0,0]

    def rotate(self,matrixarray,newrstate):#matrixarray to check if next place is free/newrstate to which pos it is now in
        if self.rstate==0:#if new pos is 0th pos  #testNo to know which test the rotation is now checking.
            if newrstate==1:#if new rstate is 1 (if they rotated clockwise)
                if self.place==1 and (self.pInArray[1]+2!=10 or self.pInArray[1]+2!=11) and self.pInArray[0]!=0:#check if pos where it would be is free
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]+2]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]+2]#if it is, save this in a variable
                        return True#return true for loop to continue for all pieces
                elif self.place==2 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0],self.pInArray[1]+1]
                        return True
                elif self.place==3:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]]
                        return True
                elif self.place==4 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]+2][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]+2,self.pInArray[1]-1]
                        return True
                else:
                    return False#if untrue, return false for loop to stop
            elif newrstate==3:
                if self.place==1 and self.pInArray[1]+1!=10 and self.pInArray[0]!=0:
                    if matrixarray[self.pInArray[0]+2][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]+2,self.pInArray[1]+1]
                        return True
                elif self.place==2:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]]
                        return True
                elif self.place==3 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0],self.pInArray[1]-1]
                        return True
                elif self.place==4 and (self.pInArray[1]-2!=-1 and self.pInArray[1]-2!=-2):
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]-2]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]-2]
                        return True
                else:
                    return False
        if self.rstate==1:
            if newrstate==0:
                if self.place==1 and (self.pInArray[1]-2!=-1 and self.pInArray[1]-2!=-2):
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]-2]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]-2]
                        return True
                elif self.place==2 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0],self.pInArray[1]-1]
                        return True
                elif self.place==3 and matrixarray[self.pInArray[0]-1][self.pInArray[1]]==0:
                    self.newrstate = [self.pInArray[0]-1,self.pInArray[1]]
                    return True
                elif self.place==4 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]-2][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]-2,self.pInArray[1]+1]
                        return True
                else:
                    return False
            elif newrstate==2:
                if self.place==1 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]+2][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]+2,self.pInArray[1]+1]
                        return True
                elif self.place==2:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]]
                        return True
                elif self.place==3 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0],self.pInArray[1]-1]
                        return True
                elif self.place==4 and self.pInArray[1]-2!=-1 and self.pInArray[1]-2!=-2:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]-2]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]-2]
                        return True
                else:
                    return False
        if self.rstate==2:
            if newrstate==1:
                if self.place==1 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]-2][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]-2,self.pInArray[1]-1]
                        return True
                elif self.place==2 and matrixarray[self.pInArray[0]-1][self.pInArray[1]]==0:
                    self.newrstate = [self.pInArray[0]-1,self.pInArray[1]]
                    return True
                elif self.place==3 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0],self.pInArray[1]+1]
                        return True
                elif self.place==4 and (self.pInArray[1]+2!=10 and self.pInArray[1]+2!=11):
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]+2]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]+2]
                        return True
                else:
                    return False
            elif newrstate==3:
                if self.place==1 and self.pInArray[1]-2!=-1 and self.pInArray[1]-2!=-2:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]-2]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]-2]
                        return True
                elif self.place==2 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0],self.pInArray[1]-1]
                        return True
                elif self.place==3 and matrixarray[self.pInArray[0]-1][self.pInArray[1]]==0:###########
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]]
                        return True
                elif self.place==4 and self.pInArray[1]+1!=10:######
                    if matrixarray[self.pInArray[0]-2][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]-2,self.pInArray[1]+1]
                        return True
                else:
                    return False
        if self.rstate==3:#if new pos is 0th pos  #testNo to know which test the rotation is now checking.
            if newrstate==0:#if new rstate is 1 (if they rotated clockwise)
                if self.place==1 and self.pInArray[1]-1!=-1:#check if pos where it would be is free
                    if matrixarray[self.pInArray[0]-2][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]-2,self.pInArray[1]-1]#if it is, save this in a variable
                        return True#return true for loop to continue for all pieces
                elif self.place==2 and matrixarray[self.pInArray[0]-1][self.pInArray[1]]==0:
                    self.newrstate = [self.pInArray[0]-1,self.pInArray[1]]
                    return True
                elif self.place==3 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0],self.pInArray[1]+1]
                        return True
                elif self.place==4 and (self.pInArray[1]+2!=10 and self.pInArray[1]+2!=11):
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]+2]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]+2]
                        return True
                else:
                    return False#if untrue, return false for loop to stop
            elif newrstate==2:
                if self.place==1 and (self.pInArray[1]+2!=10 and self.pInArray[1]+2!=11):
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]+2]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]+2]
                        return True
                elif self.place==2 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0],self.pInArray[1]+1]
                        return True
                elif self.place==3:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]]
                        return True
                elif self.place==4 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]+2][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]+2,self.pInArray[1]-1]
                        return True
                else:
                    return False

    def movement1(self, matrixarray, check, screen, hardrop):
        if hardrop==False:#var to check if a hardrop is occurring
            if check==0:
                self.pInArray[0]+=1
                if self.rstate==0 or self.rstate==2:
                    screen.blit(self.tile,self.rect)#blit tile to cover previous place
                if self.rstate==1 and self.place==1:
                    screen.blit(self.tile,self.rect)#blit tile to cover previous place
                if self.rstate==3 and self.place==4:
                    screen.blit(self.tile,self.rect)#blit tile to cover previous place
                self.rect.move_ip(0,20)#move rect 20 pixels down
                screen.blit(self.img,self.rect)#blit new piece
            elif check==1:
                self.pInArray[1]-=1
                if self.rstate==0:
                    if self.place==4:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                if self.rstate==2:
                    if self.place==1:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                if self.rstate==1 or self.rstate==3:
                    screen.blit(self.tile,self.rect)#blit tile to cover previous place
                self.rect.move_ip(-20,0)#move rect 20 pixels left
                screen.blit(self.img,self.rect)#blit new piece
            elif check==2:
                self.pInArray[1]+=1
                if self.rstate==0:
                    if self.place==1:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                if self.rstate==2:
                    if self.place==4:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                if self.rstate==1 or self.rstate==3:
                    screen.blit(self.tile,self.rect)#blit tile to cover previous place
                self.rect.move_ip(20,0)#move rect 20 pixels right
                screen.blit(self.img,self.rect)#blit new piece
        else:
            screen.blit(self.tile,self.rect)#cover up original tiles
            if self.rstate==0 or self.rstate==2:#if in first rotation state
                displacement = check[0]-self.pInArray[0]#how far away og pos is to new pos
            elif self.rstate==1 or self.rstate==3:
                if (self.place==1 and self.rstate==1) or (self.place==4 and self.rstate==3):
                    displacement = check[0]-3-self.pInArray[0]#how far away og pos is to new pos
                if (self.place==2 and self.rstate==1) or (self.place==3 and self.rstate==3):
                    displacement = check[0]-2-self.pInArray[0]#how far away og pos is to new pos
                if (self.place==3 and self.rstate==1) or (self.place==2 and self.rstate==3):
                    displacement = check[0]-1-self.pInArray[0]#how far away og pos is to new pos
                if (self.place==4 and self.rstate==1) or (self.place==1 and self.rstate==3):
                    displacement = check[0]-self.pInArray[0]#how far away og pos is to new pos
            self.pInArray[0]+=displacement#new array position
            self.rect.move_ip(0,displacement*20)#move rect here
            screen.blit(self.img,self.rect)#blit new position

class sZ(Piece):
    def __init__(self,img,pnum,pplace,screen):
        super().__init__(img,pnum,pplace,screen)
        if self.place==1:
            self.x = 380
            self.y = 121
            self.bottomPiece=True
            self.leftPiece=True
            self.rightPiece=False
            self.pInArray = [0,4]
        elif self.place==2:
            self.x = 400
            self.y = 121
            self.bottomPiece=False
            self.leftPiece=False
            self.rightPiece=True
            self.pInArray = [0,5]
        elif self.place==3:
            self.x = 400
            self.y = 141
            self.bottomPiece=True
            self.leftPiece=True
            self.rightPiece=False
            self.pInArray = [1,5]
        elif self.place==4:
            self.x = 420
            self.y = 141
            self.bottomPiece=True
            self.leftPiece=False
            self.rightPiece=True
            self.pInArray = [1,6]
        self.rect = self.img.get_rect(topleft=(self.x,self.y))
        self.name="Z"
        self.spawnM(screen)
    def spawnM(self,screen):
        screen.blit(self.img, self.rect)
        pygame.display.flip()

    def rotate1(self,screen,newrstate,check):
        if check==0:
            screen.blit(self.tile,self.rect)
        else:
            if newrstate==0:
                if self.place==1:
                    self.bottomPiece=True
                    self.leftPiece=True
                    self.rightPiece=False
                elif self.place==2:
                    self.bottomPiece=False
                    self.leftPiece=False
                    self.rightPiece=True
                elif self.place==3:
                    self.bottomPiece=True
                    self.leftPiece=True
                    self.rightPiece=False
                elif self.place==4:
                    self.bottomPiece=True
                    self.leftPiece=False
                    self.rightPiece=True
            elif newrstate==1:
                if self.place==1:
                    self.bottomPiece=False
                    self.leftPiece=True
                    self.rightPiece=True
                elif self.place==2:
                    self.bottomPiece=True
                    self.leftPiece=False
                    self.rightPiece=True
                elif self.place==3:
                    self.bottomPiece=False
                    self.leftPiece=True
                    self.rightPiece=False
                elif self.place==4:
                    self.bottomPiece=True
                    self.leftPiece=True
                    self.rightPiece=True
            elif newrstate==2:
                if self.place==1:
                    self.bottomPiece=True
                    self.leftPiece=False
                    self.rightPiece=True
                elif self.place==2:
                    self.bottomPiece=True
                    self.leftPiece=True
                    self.rightPiece=False
                elif self.place==3:
                    self.bottomPiece=False
                    self.leftPiece=False
                    self.rightPiece=True
                elif self.place==4:
                    self.bottomPiece=True
                    self.leftPiece=True
                    self.rightPiece=False
            elif newrstate==3:
                if self.place==1:
                    self.bottomPiece=True
                    self.leftPiece=True
                    self.rightPiece=True
                elif self.place==2:
                    self.bottomPiece=False
                    self.leftPiece=True
                    self.rightPiece=False
                elif self.place==3:
                    self.bottomPiece=True
                    self.leftPiece=False
                    self.rightPiece=True
                elif self.place==4:
                    self.bottomPiece=False
                    self.leftPiece=True
                    self.rightPiece=True
            self.rstate = newrstate
            displacement1 = self.newrstate[0]-self.pInArray[0]
            displacement2 = self.newrstate[1]-self.pInArray[1]
            self.rect.move_ip(displacement2*20,displacement1*20)
            self.pInArray = self.newrstate
            screen.blit(self.img,self.rect)
            self.newrstate=[0,0]

    def rotate(self,matrixarray,newrstate):#matrixarray to check if next place is free/newrstate to which pos it is now in
        if self.rstate==0:#if new pos is 0th pos  #testNo to know which test the rotation is now checking.
            if newrstate==1:#if new rstate is 1 (if they rotated clockwise)
                if self.place==1 and self.pInArray[1]+2!=10 and self.pInArray[1]+2!=11:#check if pos where it would be is free
                    if matrixarray[self.pInArray[0]][self.pInArray[1]+2]==0:
                        self.newrstate = [self.pInArray[0],self.pInArray[1]+2]#if it is, save this in a variable
                        return True#return true for loop to continue for all pieces
                elif self.place==2 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]+1]
                        return True
                elif self.place==3:
                    self.newrstate = [self.pInArray[0],self.pInArray[1]]
                    return True
                elif self.place==4 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]-1]
                        return True
                else:
                    return False#if untrue, return false for loop to stop
            elif newrstate==3:#if new rstate is 1 (if they rotated clockwise)
                if self.place==1 and matrixarray[self.pInArray[0]+2][self.pInArray[1]]==0:#check if pos where it would be is free
                    self.newrstate = [self.pInArray[0]+2,self.pInArray[1]]#if it is, save this in a variable
                    return True#return true for loop to continue for all pieces
                elif self.place==2 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]-1]
                        return True
                elif self.place==3:
                    self.newrstate = [self.pInArray[0],self.pInArray[1]]
                    return True
                elif self.place==4 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]-1]
                        return True
                else:
                    return False#if untrue, return false for loop to stop
        if self.rstate==1:
            if newrstate==0:#if new rstate is 1 (if they rotated clockwise)
                if self.place==1 and self.pInArray[1]-2!=-1 and self.pInArray[1]-2!=-2:#check if pos where it would be is free
                    if matrixarray[self.pInArray[0]][self.pInArray[1]-2]==0:
                        self.newrstate = [self.pInArray[0],self.pInArray[1]-2]#if it is, save this in a variable
                        return True#return true for loop to continue for all pieces
                elif self.place==2 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]-1]
                        return True
                elif self.place==3:
                    self.newrstate = [self.pInArray[0],self.pInArray[1]]
                    return True
                elif self.place==4 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]+1]
                        return True
                else:
                    return False#if untrue, return false for loop to stop
            if newrstate==2:#if new rstate is 1 (if they rotated clockwise)
                if self.place==1 and matrixarray[self.pInArray[0]+2][self.pInArray[1]]==0:#check if pos where it would be is free
                    self.newrstate = [self.pInArray[0]+2,self.pInArray[1]]#if it is, save this in a variable
                    return True#return true for loop to continue for all pieces
                elif self.place==2 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]-1]
                        return True
                elif self.place==3:
                    self.newrstate = [self.pInArray[0],self.pInArray[1]]
                    return True
                elif self.place==4 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]-1]
                        return True
                else:
                    return False#if untrue, return false for loop to stop
        if self.rstate==2:
            if newrstate==1:#if new rstate is 1 (if they rotated clockwise)
                if self.place==1 and matrixarray[self.pInArray[0]-2][self.pInArray[1]]==0:#check if pos where it would be is free
                    self.newrstate = [self.pInArray[0]-2,self.pInArray[1]]#if it is, save this in a variable
                    return True#return true for loop to continue for all pieces
                elif self.place==2 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]+1]
                        return True
                elif self.place==3:
                    self.newrstate = [self.pInArray[0],self.pInArray[1]]
                    return True
                elif self.place==4 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]+1]
                        return True
                else:
                    return False#if untrue, return false for loop to stop
            elif newrstate==3:#if new rstate is 1 (if they rotated clockwise)
                if self.place==1 and self.pInArray[1]-2!=-1 and self.pInArray[1]-2!=-2:#check if pos where it would be is free
                    if matrixarray[self.pInArray[0]][self.pInArray[1]-2]==0:
                        self.newrstate = [self.pInArray[0],self.pInArray[1]-2]#if it is, save this in a variable
                        return True#return true for loop to continue for all pieces
                elif self.place==2 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]-1]
                        return True
                elif self.place==3:
                    self.newrstate = [self.pInArray[0],self.pInArray[1]]
                    return True
                elif self.place==4 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]+1]
                        return True
                else:
                    return False#if untrue, return false for loop to stop
        if self.rstate==3:
            if newrstate==0:#if new rstate is 1 (if they rotated clockwise)
                if self.place==1 and matrixarray[self.pInArray[0]-2][self.pInArray[1]]==0:#check if pos where it would be is free
                    self.newrstate = [self.pInArray[0]-2,self.pInArray[1]]#if it is, save this in a variable
                    return True#return true for loop to continue for all pieces
                elif self.place==2 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]+1]
                        return True
                elif self.place==3:
                    self.newrstate = [self.pInArray[0],self.pInArray[1]]
                    return True
                elif self.place==4 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]+1]
                        return True
                else:
                    return False#if untrue, return false for loop to stop
            elif newrstate==2:#if new rstate is 1 (if they rotated clockwise)
                if self.place==1 and self.pInArray[1]+2!=10 and self.pInArray[1]+2!=11:#check if pos where it would be is free
                    if matrixarray[self.pInArray[0]][self.pInArray[1]+2]==0:
                        self.newrstate = [self.pInArray[0],self.pInArray[1]+2]#if it is, save this in a variable
                        return True#return true for loop to continue for all pieces
                elif self.place==2 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]+1]
                        return True
                elif self.place==3:
                    self.newrstate = [self.pInArray[0],self.pInArray[1]]
                    return True
                elif self.place==4 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]-1]
                        return True
                else:
                    return False#if untrue, return false for loop to stop


    def movement1(self, matrixarray, check, screen, hardrop):
        if hardrop==False:#var to check if a hardrop is occurring
            if check==0:
                self.pInArray[0]+=1
                if self.rstate==0:
                    if self.place==1 or self.place==2 or self.place==4:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                elif self.rstate==1:
                    if self.place==1 or self.place==3:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                elif self.rstate==2:
                    if self.place==1 or self.place==4 or self.place==3:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                elif self.rstate==3:
                    if self.place==2 or self.place==4:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                self.rect.move_ip(0,20)#move rect 20 pixels down
                screen.blit(self.img,self.rect)#blit new piece
            elif check==1:
                self.pInArray[1]-=1
                if self.rstate==0:
                    if self.place==4 or self.place==2:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                elif self.rstate==1:
                    if self.place==4 or self.place==2 or self.place==1:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                elif self.rstate==2:
                    if self.place==3 or self.place==1:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                elif self.rstate==3:
                    if self.place==4 or self.place==3 or self.place==1:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                self.rect.move_ip(-20,0)#move rect 20 pixels down
                screen.blit(self.img,self.rect)#blit new piece
            elif check==2:
                self.pInArray[1]+=1
                if self.rstate==0:
                    if self.place==1 or self.place==3:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                elif self.rstate==1:
                    if self.place==1 or self.place==3 or self.place==4:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                elif self.rstate==2:
                    if self.place==4 or self.place==2:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                elif self.rstate==3:
                    if self.place==1 or self.place==2 or self.place==4:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                self.rect.move_ip(20,0)#move rect 20 pixels right
                screen.blit(self.img,self.rect)#blit new piece
        else:
            print(check)
            screen.blit(self.tile,self.rect)#cover up original tiles
            if self.rstate==0:#if in first rotation state
                if check[1]==1:
                    if self.place==3 or self.place==4:#if bottom two pieces
                        displacement = check[0]+1-self.pInArray[0]#how far away og pos is to new pos
                    else:
                        displacement = check[0]-self.pInArray[0]#how far away og pos is to new pos
                else:
                    if self.place==3 or self.place==4:#if bottom two pieces
                        displacement = check[0]-self.pInArray[0]#how far away og pos is to new pos
                    else:
                        displacement = check[0]-1-self.pInArray[0]#how far away og pos is to new pos
            if self.rstate==2:#if in first rotation state
                if check[1]==4:
                    if self.place==1 or self.place==2:#if bottom two pieces
                        displacement = check[0]+1-self.pInArray[0]#how far away og pos is to new pos
                    else:
                        displacement = check[0]-self.pInArray[0]#how far away og pos is to new pos
                else:
                    if self.place==2 or self.place==1:#if bottom two pieces
                        displacement = check[0]-self.pInArray[0]#how far away og pos is to new pos
                    else:
                        displacement = check[0]-1-self.pInArray[0]#how far away og pos is to new pos
            if self.rstate==1:#if in first rotation state
                if check[1]==2:
                    if self.place==4:#if bottom two pieces
                        displacement = check[0]+1-self.pInArray[0]#how far away og pos is to new pos
                    elif self.place==3 or self.place==2:
                        displacement = check[0]-self.pInArray[0]#how far away og pos is to new pos
                    else:
                        displacement = check[0]-1-self.pInArray[0]#how far away og pos is to new pos
                else:
                    if self.place==4:#if bottom two pieces
                        displacement = check[0]-self.pInArray[0]#how far away og pos is to new pos
                    elif self.place==3 or self.place==2:
                        displacement = check[0]-1-self.pInArray[0]#how far away og pos is to new pos
                    else:
                        displacement = check[0]-2-self.pInArray[0]#how far away og pos is to new pos
            if self.rstate==3:#if in first rotation state
                if check[1]==3:
                    if self.place==1:#if bottom two pieces
                        displacement = check[0]+1-self.pInArray[0]#how far away og pos is to new pos
                    elif self.place==3 or self.place==2:
                        displacement = check[0]-self.pInArray[0]#how far away og pos is to new pos
                    else:
                        displacement = check[0]-1-self.pInArray[0]#how far away og pos is to new pos
                else:
                    if self.place==1:#if bottom two pieces
                        displacement = check[0]-self.pInArray[0]#how far away og pos is to new pos
                    elif self.place==3 or self.place==2:
                        displacement = check[0]-1-self.pInArray[0]#how far away og pos is to new pos
                    else:
                        displacement = check[0]-2-self.pInArray[0]#how far away og pos is to new pos
            self.pInArray[0]+=displacement#new array position
            self.rect.move_ip(0,displacement*20)#move rect here
            screen.blit(self.img,self.rect)#blit new position

class sS(Piece):
    def __init__(self,img,pnum,pplace,screen):
        super().__init__(img,pnum,pplace,screen)
        if self.place==1:#if the first piece
            self.x = 420#the original x pos
            self.y = 121#original y pos
            self.bottomPiece=True#if it is the bottom piece in og pos
            self.leftPiece=False#if it is the left piece in og pos
            self.rightPiece=True#if it is the right piece in og pos
            self.pInArray = [0,6]#its og pos in whole array, the row and column
        elif self.place==2:#if the first piece
            self.x = 400
            self.y = 121
            self.bottomPiece=False
            self.leftPiece=True
            self.rightPiece=False
            self.pInArray = [0,5]
        elif self.place==3:#if the first piece
            self.x = 400
            self.y = 141
            self.bottomPiece=True
            self.leftPiece=False
            self.rightPiece=True
            self.pInArray = [1,5]
        elif self.place==4:#if the first piece
            self.x = 380
            self.y = 141
            self.bottomPiece=True
            self.leftPiece=True
            self.rightPiece=False
            self.pInArray = [1,4]#was previously [1,3]
        self.rect = self.img.get_rect(topleft=(self.x,self.y))#defining rect pos
        self.name="S"
        self.spawnM(screen)#create piece on screen.
    def spawnM(self,screen):
        screen.blit(self.img, self.rect)
        pygame.display.flip()

    def rotate1(self,screen,newrstate,check):
        if check==0:
            screen.blit(self.tile,self.rect)
        else:
            if newrstate==0:
                if self.place==1:
                    self.bottomPiece=True#if it is the bottom piece in og pos
                    self.leftPiece=False#if it is the left piece in og pos
                    self.rightPiece=True
                elif self.place==2:
                    self.bottomPiece=False
                    self.leftPiece=True
                    self.rightPiece=False
                elif self.place==3:
                    self.bottomPiece=True
                    self.leftPiece=False
                    self.rightPiece=True
                elif self.place==4:
                    self.bottomPiece=True
                    self.leftPiece=True
                    self.rightPiece=False
            elif newrstate==1:
                if self.place==1:
                    self.bottomPiece=True
                    self.leftPiece=True
                    self.rightPiece=True
                elif self.place==2:
                    self.bottomPiece=False
                    self.leftPiece=False
                    self.rightPiece=True
                elif self.place==3:
                    self.bottomPiece=True
                    self.leftPiece=True
                    self.rightPiece=False
                elif self.place==4:
                    self.bottomPiece=False
                    self.leftPiece=True
                    self.rightPiece=True
            elif newrstate==2:
                if self.place==1:
                    self.bottomPiece=True
                    self.leftPiece=True
                    self.rightPiece=False
                elif self.place==2:
                    self.bottomPiece=True
                    self.leftPiece=False
                    self.rightPiece=True
                elif self.place==3:
                    self.bottomPiece=False
                    self.leftPiece=True
                    self.rightPiece=False
                elif self.place==4:
                    self.bottomPiece=True
                    self.leftPiece=False
                    self.rightPiece=True
            elif newrstate==3:
                if self.place==1:
                    self.bottomPiece=False
                    self.leftPiece=True
                    self.rightPiece=True
                elif self.place==2:
                    self.bottomPiece=True
                    self.leftPiece=True
                    self.rightPiece=False
                elif self.place==3:
                    self.bottomPiece=False
                    self.leftPiece=False
                    self.rightPiece=True
                elif self.place==4:
                    self.bottomPiece=True
                    self.leftPiece=True
                    self.rightPiece=True
            self.rstate = newrstate
            displacement1 = self.newrstate[0]-self.pInArray[0]
            displacement2 = self.newrstate[1]-self.pInArray[1]
            self.rect.move_ip(displacement2*20,displacement1*20)
            self.pInArray = self.newrstate
            screen.blit(self.img,self.rect)
            self.newrstate=[0,0]

    def rotate(self,matrixarray,newrstate):#matrixarray to check if next place is free/newrstate to which pos it is now in
        if self.rstate==0:#if new pos is 0th pos  #testNo to know which test the rotation is now checking.
            if newrstate==1:#if new rstate is 1 (if they rotated clockwise)
                if self.place==1 and matrixarray[self.pInArray[0]+2][self.pInArray[1]]==0:#check if pos where it would be is free
                    self.newrstate = [self.pInArray[0]+2,self.pInArray[1]]#if it is, save this in a variable
                    return True#return true for loop to continue for all pieces
                elif self.place==2 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]+1]
                        return True
                elif self.place==3:
                    self.newrstate = [self.pInArray[0],self.pInArray[1]]
                    return True
                elif self.place==4 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]+1]
                        return True
                else:
                    return False#if untrue, return false for loop to stop
            elif newrstate==3:#if new rstate is 1 (if they rotated clockwise)
                if self.place==1 and self.pInArray[1]-2!=-1 and self.pInArray[1]-2!=-2:#check if pos where it would be is free
                    if matrixarray[self.pInArray[0]][self.pInArray[1]-2]==0:
                        self.newrstate = [self.pInArray[0],self.pInArray[1]-2]#if it is, save this in a variable
                        return True#return true for loop to continue for all pieces
                elif self.place==2 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]-1]
                        return True
                elif self.place==3:
                    self.newrstate = [self.pInArray[0],self.pInArray[1]]
                    return True
                elif self.place==4 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]+1]
                        return True
                else:
                    return False#if untrue, return false for loop to stop
        if self.rstate==1:
            if newrstate==0:#if new rstate is 1 (if they rotated clockwise)
                if self.place==1 and matrixarray[self.pInArray[0]-2][self.pInArray[1]]==0:#check if pos where it would be is free
                    self.newrstate = [self.pInArray[0]-2,self.pInArray[1]]#if it is, save this in a variable
                    return True#return true for loop to continue for all pieces
                elif self.place==2 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]-1]
                        return True
                elif self.place==3:
                    self.newrstate = [self.pInArray[0],self.pInArray[1]]
                    return True
                elif self.place==4 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]-1]==0:
                            self.newrstate = [self.pInArray[0]+1,self.pInArray[1]-1]
                            return True
                else:
                    return False#if untrue, return false for loop to stop
            if newrstate==2:#if new rstate is 1 (if they rotated clockwise)
                if self.place==1 and self.pInArray[1]-2!=-1 and self.pInArray[1]-2!=-2:#check if pos where it would be is free
                    if matrixarray[self.pInArray[0]][self.pInArray[1]-2]==0:
                        self.newrstate = [self.pInArray[0],self.pInArray[1]-2]#if it is, save this in a variable
                        return True#return true for loop to continue for all pieces
                elif self.place==2 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]-1]
                        return True
                elif self.place==3:
                    self.newrstate = [self.pInArray[0],self.pInArray[1]]
                    return True
                elif self.place==4 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]+1]
                        return True
                else:
                    return False#if untrue, return false for loop to stop
        if self.rstate==2:
            if newrstate==1:#if new rstate is 1 (if they rotated clockwise)
                if self.place==1 and self.pInArray[1]+2!=10 and self.pInArray[1]+2!=11:#check if pos where it would be is free
                    if matrixarray[self.pInArray[0]][self.pInArray[1]+2]==0:
                        self.newrstate = [self.pInArray[0],self.pInArray[1]+2]#if it is, save this in a variable
                        return True#return true for loop to continue for all pieces
                elif self.place==2 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]+1]
                        return True
                elif self.place==3:
                    self.newrstate = [self.pInArray[0],self.pInArray[1]]
                    return True
                elif self.place==4 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]-1]
                        return True
                else:
                    return False#if untrue, return false for loop to stop
            elif newrstate==3:#if new rstate is 1 (if they rotated clockwise)
                if self.place==1 and matrixarray[self.pInArray[0]-2][self.pInArray[1]]==0:#check if pos where it would be is free
                    self.newrstate = [self.pInArray[0]-2,self.pInArray[1]]#if it is, save this in a variable
                    return True#return true for loop to continue for all pieces
                elif self.place==2 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]-1]
                        return True
                elif self.place==3:
                    self.newrstate = [self.pInArray[0],self.pInArray[1]]
                    return True
                elif self.place==4 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]-1]
                        return True
                else:
                    return False#if untrue, return false for loop to stop
        if self.rstate==3:
            if newrstate==0:#if new rstate is 1 (if they rotated clockwise)
                if self.place==1 and self.pInArray[1]+2!=10 and self.pInArray[1]+2!=11:#check if pos where it would be is free
                    if matrixarray[self.pInArray[0]][self.pInArray[1]+2]==0:
                        self.newrstate = [self.pInArray[0],self.pInArray[1]+2]#if it is, save this in a variable
                        return True#return true for loop to continue for all pieces
                elif self.place==2 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]+1]
                        return True
                elif self.place==3:
                    self.newrstate = [self.pInArray[0],self.pInArray[1]]
                    return True
                elif self.place==4 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]-1]
                        return True
                else:
                    return False#if untrue, return false for loop to stop
            elif newrstate==2:#if new rstate is 1 (if they rotated clockwise)
                if self.place==1 and matrixarray[self.pInArray[0]+2][self.pInArray[1]]==0:#check if pos where it would be is free
                    self.newrstate = [self.pInArray[0]+2,self.pInArray[1]]#if it is, save this in a variable
                    return True#return true for loop to continue for all pieces
                elif self.place==2 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]+1]
                        return True
                elif self.place==3:
                    self.newrstate = [self.pInArray[0],self.pInArray[1]]
                    return True
                elif self.place==4 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]+1]
                        return True
                else:
                    return False#if untrue, return false for loop to stop

    def movement1(self, matrixarray, check, screen, hardrop):
        if hardrop==False:#var to check if a hardrop is occurring
            if check==0:
                self.pInArray[0]+=1
                if self.rstate==0:
                    if self.place==1 or self.place==2 or self.place==4:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                if self.rstate==2:
                    if self.place==1 or self.place==3 or self.place==4:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                if self.rstate==3:
                    if self.place==1 or self.place==3:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                if self.rstate==1:
                    if self.place==2 or self.place==4:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                self.rect.move_ip(0,20)#move rect 20 pixels down
                screen.blit(self.img,self.rect)#blit new piece
            elif check==1:
                self.pInArray[1]-=1
                if self.rstate==0:
                    if self.place==1 or self.place==3:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                if self.rstate==2:
                    if self.place==2 or self.place==4:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                if self.rstate==1:
                    if self.place==1 or self.place==2 or self.place==4:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                if self.rstate==3:
                    if self.place==1 or self.place==3 or self.place==4:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                self.rect.move_ip(-20,0)#move rect 20 pixels down
                screen.blit(self.img,self.rect)#blit new piece
            elif check==2:
                self.pInArray[1]+=1
                if self.rstate==2:
                    if self.place==1 or self.place==3:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                if self.rstate==0:
                    if self.place==2 or self.place==4:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                if self.rstate==3:
                    if self.place==1 or self.place==2 or self.place==4:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                if self.rstate==1:
                    if self.place==1 or self.place==3 or self.place==4:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                self.rect.move_ip(20,0)#move rect 20 pixels right
                screen.blit(self.img,self.rect)#blit new piece
        else:
            screen.blit(self.tile,self.rect)#cover up original tiles
            if self.rstate==0:#if in first rotation state
                if check[1]==1:
                    if self.place==3 or self.place==4:#if bottom two pieces
                        displacement = check[0]+1-self.pInArray[0]#how far away og pos is to new pos
                    else:
                        displacement = check[0]-self.pInArray[0]#how far away og pos is to new pos
                else:
                    if self.place==3 or self.place==4:#if bottom two pieces
                        displacement = check[0]-self.pInArray[0]#how far away og pos is to new pos
                    else:
                        displacement = check[0]-1-self.pInArray[0]#how far away og pos is to new pos
            if self.rstate==2:#if in first rotation state
                if check[1]==4:
                    if self.place==1 or self.place==2:#if bottom two pieces
                        displacement = check[0]+1-self.pInArray[0]#how far away og pos is to new pos
                    else:
                        displacement = check[0]-self.pInArray[0]#how far away og pos is to new pos
                else:
                    if self.place==2 or self.place==1:#if bottom two pieces
                        displacement = check[0]-self.pInArray[0]#how far away og pos is to new pos
                    else:
                        displacement = check[0]-1-self.pInArray[0]#how far away og pos is to new pos
            if self.rstate==1:#if in first rotation state
                if check[1]==3:
                    if self.place==1:#if bottom two pieces
                        displacement = check[0]+1-self.pInArray[0]#how far away og pos is to new pos
                    elif self.place==3 or self.place==2:
                        displacement = check[0]-self.pInArray[0]#how far away og pos is to new pos
                    else:
                        displacement = check[0]-1-self.pInArray[0]#how far away og pos is to new pos
                else:
                    print("haiaii")
                    if self.place==1:#if bottom two pieces
                        displacement = check[0]-self.pInArray[0]#how far away og pos is to new pos
                    elif self.place==3 or self.place==2:
                        displacement = check[0]-1-self.pInArray[0]#how far away og pos is to new pos
                    else:
                        displacement = check[0]-2-self.pInArray[0]#how far away og pos is to new pos
            if self.rstate==3:#if in first rotation state
                if check[1]==2:
                    if self.place==4:#if bottom two pieces
                        displacement = check[0]+1-self.pInArray[0]#how far away og pos is to new pos
                    elif self.place==3 or self.place==2:
                        displacement = check[0]-self.pInArray[0]#how far away og pos is to new pos
                    else:
                        displacement = check[0]-1-self.pInArray[0]#how far away og pos is to new pos
                else:
                    if self.place==4:#if bottom two pieces
                        displacement = check[0]-self.pInArray[0]#how far away og pos is to new pos
                    elif self.place==3 or self.place==2:
                        displacement = check[0]-1-self.pInArray[0]#how far away og pos is to new pos
                    else:
                        displacement = check[0]-2-self.pInArray[0]#how far away og pos is to new pos
            self.pInArray[0]+=displacement#new array position
            self.rect.move_ip(0,displacement*20)#move rect here
            screen.blit(self.img,self.rect)#blit new position

class sJ(Piece):
    def __init__(self,img,pnum,pplace,screen):
        super().__init__(img,pnum,pplace,screen)
        if self.place==1:
            self.x = 380
            self.y = 121
            self.bottomPiece=False
            self.leftPiece=True
            self.rightPiece=True
            self.pInArray = [0,4]#was [0,6]
        elif self.place==2:
            self.x = 380
            self.y = 141
            self.bottomPiece=True
            self.leftPiece=True
            self.rightPiece=False
            self.pInArray = [1,4]#was [1,6]
        elif self.place==3:
            self.x = 400
            self.y = 141
            self.bottomPiece=True
            self.leftPiece=False
            self.rightPiece=False
            self.pInArray = [1,5]
        elif self.place==4:
            self.x = 420
            self.y = 141
            self.bottomPiece=True
            self.leftPiece=False
            self.rightPiece=True
            self.pInArray = [1,6]#was [1,4]
        self.rect = self.img.get_rect(topleft=(self.x,self.y))
        self.name="J"
        self.spawnM(screen)
    def spawnM(self,screen):
        screen.blit(self.img, self.rect)
        pygame.display.flip()

    def rotate1(self,screen,newrstate,check):
        if check==0:
            screen.blit(self.tile,self.rect)
        else:
            if newrstate==0:
                if self.place==1:
                    self.bottomPiece=False
                    self.leftPiece=True
                    self.rightPiece=True
                elif self.place==2:
                    self.bottomPiece=True
                    self.leftPiece=True
                    self.rightPiece=False
                elif self.place==3:
                    self.bottomPiece=True
                    self.leftPiece=False
                    self.rightPiece=False
                elif self.place==4:
                    self.bottomPiece=True
                    self.leftPiece=False
                    self.rightPiece=True
            elif newrstate==1:
                if self.place==1:
                    self.bottomPiece=True
                    self.leftPiece=True
                    self.rightPiece=True
                elif self.place==2:
                    self.bottomPiece=False
                    self.leftPiece=True
                    self.rightPiece=False
                elif self.place==3:
                    self.bottomPiece=False
                    self.leftPiece=True
                    self.rightPiece=True
                elif self.place==4:
                    self.bottomPiece=True
                    self.leftPiece=False
                    self.rightPiece=True
            elif newrstate==2:
                if self.place==1:
                    self.bottomPiece=True
                    self.leftPiece=True
                    self.rightPiece=True
                elif self.place==2:
                    self.bottomPiece=False
                    self.leftPiece=False
                    self.rightPiece=True
                elif self.place==3:
                    self.bottomPiece=True
                    self.leftPiece=False
                    self.rightPiece=False
                elif self.place==4:
                    self.bottomPiece=True
                    self.leftPiece=True
                    self.rightPiece=False
            elif newrstate==3:
                if self.place==1:
                    self.bottomPiece=True
                    self.leftPiece=True
                    self.rightPiece=False
                elif self.place==2:
                    self.bottomPiece=True
                    self.leftPiece=False
                    self.rightPiece=True
                elif self.place==3:
                    self.bottomPiece=False
                    self.leftPiece=True
                    self.rightPiece=True
                elif self.place==4:
                    self.bottomPiece=False
                    self.leftPiece=True
                    self.rightPiece=True
            self.rstate = newrstate
            displacement1 = self.newrstate[0]-self.pInArray[0]
            displacement2 = self.newrstate[1]-self.pInArray[1]
            self.rect.move_ip(displacement2*20,displacement1*20)
            self.pInArray = self.newrstate
            screen.blit(self.img,self.rect)
            self.newrstate=[0,0]

    def rotate(self,matrixarray,newrstate):#matrixarray to check if next place is free/newrstate to which pos it is now in
        if self.rstate==0:#if new pos is 0th pos  #testNo to know which test the rotation is now checking.
            if newrstate==1:#if new rstate is 1 (if they rotated clockwise)
                if self.place==1 and self.pInArray[1]+2!=10 and self.pInArray[1]+2!=11:#check if pos where it would be is free
                    if matrixarray[self.pInArray[0]][self.pInArray[1]+2]==0:
                        self.newrstate = [self.pInArray[0],self.pInArray[1]+2]#if it is, save this in a variable
                        return True#return true for loop to continue for all pieces
                elif self.place==2 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]+1]
                        return True
                elif self.place==3:
                    self.newrstate = [self.pInArray[0],self.pInArray[1]]
                    return True
                elif self.place==4 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]-1]!=-1:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]-1]
                        return True
                else:
                    return False#if untrue, return false for loop to stop
            elif newrstate==3:#if new rstate is 1 (if they rotated clockwise)
                if self.place==1 and matrixarray[self.pInArray[0]+2][self.pInArray[1]]==0:#check if pos where it would be is free
                    self.newrstate = [self.pInArray[0]+2,self.pInArray[1]]#if it is, save this in a variable
                    return True#return true for loop to continue for all pieces
                elif self.place==2 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]+1]
                        return True
                elif self.place==3:
                    self.newrstate = [self.pInArray[0],self.pInArray[1]]
                    return True
                elif self.place==4 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]-1]
                        return True
                else:
                    return False#if untrue, return false for loop to stop
        if self.rstate==1:#if new pos is 0th pos  #testNo to know which test the rotation is now checking.
            if newrstate==0:#if new rstate is 1 (if they rotated clockwise)
                if self.place==1 and self.pInArray[1]-2!=-1 and self.pInArray[1]-2!=-2:#check if pos where it would be is free
                    if matrixarray[self.pInArray[0]][self.pInArray[1]-2]==0:
                        self.newrstate = [self.pInArray[0],self.pInArray[1]-2]#if it is, save this in a variable
                        return True#return true for loop to continue for all pieces
                elif self.place==2 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]-1]
                        return True
                elif self.place==3:
                    self.newrstate = [self.pInArray[0],self.pInArray[1]]
                    return True
                elif self.place==4 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]+1]
                        return True
                else:
                    return False#if untrue, return false for loop to stop
            elif newrstate==2:#if new rstate is 1 (if they rotated clockwise)
                if self.place==1 and matrixarray[self.pInArray[0]+2][self.pInArray[1]]==0:#check if pos where it would be is free
                    self.newrstate = [self.pInArray[0]+2,self.pInArray[1]]#if it is, save this in a variable
                    return True#return true for loop to continue for all pieces
                elif self.place==2 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]+1]
                        return True
                elif self.place==3:
                    self.newrstate = [self.pInArray[0],self.pInArray[1]]
                    return True
                elif self.place==4 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]-1]
                        return True
                else:
                    return False#if untrue, return false for loop to stop
        if self.rstate==2:#if new pos is 0th pos  #testNo to know which test the rotation is now checking.
            if newrstate==1:#if new rstate is 1 (if they rotated clockwise)
                if self.place==1 and matrixarray[self.pInArray[0]-2][self.pInArray[1]]==0:#check if pos where it would be is free
                    self.newrstate = [self.pInArray[0]-2,self.pInArray[1]]#if it is, save this in a variable
                    return True#return true for loop to continue for all pieces
                elif self.place==2 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]-1]
                        return True
                elif self.place==3:
                    self.newrstate = [self.pInArray[0],self.pInArray[1]]
                    return True
                elif self.place==4 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]+1]
                        return True
                else:
                    return False#if untrue, return false for loop to stop
            elif newrstate==3:#if new rstate is 1 (if they rotated clockwise)
                if self.place==1 and self.pInArray[1]-2!=-2 and self.pInArray[1]-2!=-1:#check if pos where it would be is free
                    if matrixarray[self.pInArray[0]][self.pInArray[1]-2]==0:
                        self.newrstate = [self.pInArray[0],self.pInArray[1]-2]#if it is, save this in a variable
                        return True#return true for loop to continue for all pieces
                elif self.place==2 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]-1]
                        return True
                elif self.place==3:
                    self.newrstate = [self.pInArray[0],self.pInArray[1]]
                    return True
                elif self.place==4 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]+1]
                        return True
                else:
                    return False#if untrue, return false for loop to stop
        if self.rstate==3:#if new pos is 0th pos  #testNo to know which test the rotation is now checking.
            if newrstate==2:#if new rstate is 1 (if they rotated clockwise)
                if self.place==1 and self.pInArray[1]+2!=10 and self.pInArray[1]+2!=11:#check if pos where it would be is free
                    if matrixarray[self.pInArray[0]][self.pInArray[1]+2]==0:
                        self.newrstate = [self.pInArray[0],self.pInArray[1]+2]#if it is, save this in a variable
                        return True#return true for loop to continue for all pieces
                elif self.place==2 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]+1]
                        return True
                elif self.place==3:
                    self.newrstate = [self.pInArray[0],self.pInArray[1]]
                    return True
                elif self.place==4 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]-1]
                        return True
                else:
                    return False#if untrue, return false for loop to stop
            elif newrstate==0:#if new rstate is 1 (if they rotated clockwise)
                if self.place==1 and matrixarray[self.pInArray[0]-2][self.pInArray[1]]==0:#check if pos where it would be is free
                    self.newrstate = [self.pInArray[0]-2,self.pInArray[1]]#if it is, save this in a variable
                    return True#return true for loop to continue for all pieces
                elif self.place==2 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]-1]
                        return True
                elif self.place==3:
                    self.newrstate = [self.pInArray[0],self.pInArray[1]]
                    return True
                elif self.place==4 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]+1]
                        return True
                else:
                    return False#if untrue, return false for loop to stop

    def movement1(self, matrixarray, check, screen, hardrop):
        if hardrop==False:#var to check if a hardrop is occurring
            if check==0:#if moving down
                self.pInArray[0]+=1#move its place down
                if self.rstate==0:#if rotated in first position
                    if self.place==1 or self.place==3 or self.place==4:#if the first, third, or fourth position piece
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                if self.rstate==2:#if rotated in first position
                    if self.place==3 or self.place==2 or self.place==4:#if the first, third, or fourth position piece
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                if self.rstate==1:#if rotated in first position
                    if self.place==1 or self.place==2:#if the first, third, or fourth position piece
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                if self.rstate==3:#if rotated in first position
                    if self.place==1 or self.place==4:#if the first, third, or fourth position piece
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                self.rect.move_ip(0,20)#move rect 20 pixels down
                screen.blit(self.img,self.rect)#blit new piece
            elif check==1:#if moving left
                self.pInArray[1]-=1#move it's place once to the left.
                if self.rstate==0:#if in first rotation state
                    if self.place==4 or self.place==1:#if the second, third, or fourth position piece
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                if self.rstate==2:#if in first rotation state
                    if self.place==2 or self.place==1:#if the second, third, or fourth position piece
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                if self.rstate==1:#if in first rotation state
                    if self.place==4 or self.place==1 or self.place==3:#if the second, third, or fourth position piece
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                if self.rstate==3:#if in first rotation state
                    if self.place==4 or self.place==2 or self.place==3:#if the second, third, or fourth position piece
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                self.rect.move_ip(-20,0)#move rect 20 pixels down
                screen.blit(self.img,self.rect)#blit new piece
            elif check==2:
                self.pInArray[1]+=1
                if self.rstate==0:
                    if self.place==1 or self.place==2:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                if self.rstate==2:#if in first rotation state
                    if self.place==4 or self.place==1:#if the second, third, or fourth position piece
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                if self.rstate==1:#if in first rotation state
                    if self.place==4 or self.place==2 or self.place==3:#if the second, third, or fourth position piece
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                if self.rstate==3:#if in first rotation state
                    if self.place==4 or self.place==1 or self.place==3:#if the second, third, or fourth position piece
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                self.rect.move_ip(20,0)#move rect 20 pixels right
                screen.blit(self.img,self.rect)#blit new piece
        else:
            screen.blit(self.tile,self.rect)#cover up original tiles
            if self.rstate==0:#if in first rotation state
                if self.place==3 or self.place==4 or self.place==2:#if bottom two pieces
                    displacement = check[0]-self.pInArray[0]#how far away og pos is to new pos
                else:
                    displacement = check[0]-1-self.pInArray[0]#how far away og pos is to new pos
            if self.rstate==1:#if in first rotation state
                if check[1]==1:
                    if self.place==1 or self.place==2:#if bottom two pieces
                        displacement = check[0]-self.pInArray[0]#how far away og pos is to new pos
                    elif self.place==3:
                        displacement = check[0]+1-self.pInArray[0]#how far away og pos is to new pos
                    elif self.place==4:
                        displacement = check[0]+2-self.pInArray[0]#how far away og pos is to new pos
                else:
                    if self.place==4:#if bottom two pieces
                        displacement = check[0]-self.pInArray[0]#how far away og pos is to new pos
                    elif self.place==3:
                        displacement = check[0]-1-self.pInArray[0]#how far away og pos is to new pos
                    else:
                        displacement = check[0]-2-self.pInArray[0]#how far away og pos is to new pos
            if self.rstate==2:#if in first rotation state
                if check[1]==3 or check[1]==4:
                    if self.place==3 or self.place==2 or self.place==4:#if bottom two pieces
                        displacement = check[0]-self.pInArray[0]#how far away og pos is to new pos
                    else:
                        displacement = check[0]+1-self.pInArray[0]#how far away og pos is to new pos
                else:
                    if self.place==3 or self.place==2 or self.place==4:#if bottom two pieces
                        displacement = check[0]-1-self.pInArray[0]#how far away og pos is to new pos
                    else:
                        displacement = check[0]-self.pInArray[0]#how far away og pos is to new pos
            if self.rstate==3:#if in first rotation state
                if self.place==1 or self.place==2:#if bottom two pieces
                    displacement = check[0]-self.pInArray[0]#how far away og pos is to new pos
                elif self.place==3:
                    displacement = check[0]-1-self.pInArray[0]#how far away og pos is to new pos
                else:
                    displacement = check[0]-2-self.pInArray[0]#how far away og pos is to new pos
            self.pInArray[0]+=displacement#new array position
            self.rect.move_ip(0,displacement*20)#move rect here
            screen.blit(self.img,self.rect)#blit new position

class sL(Piece):
    def __init__(self,img,pnum,pplace,screen):
        super().__init__(img,pnum,pplace,screen)
        if self.place==1:
            self.x = 420
            self.y = 121
            self.bottomPiece=False
            self.leftPiece=True
            self.rightPiece=True
            self.pInArray = [0,6]
        elif self.place==2:
            self.x = 420
            self.y = 141
            self.bottomPiece=True
            self.leftPiece=False
            self.rightPiece=True
            self.pInArray = [1,6]
        elif self.place==3:
            self.x = 400
            self.y = 141
            self.bottomPiece=True
            self.leftPiece=False
            self.rightPiece=False
            self.pInArray = [1,5]
        elif self.place==4:
            self.x = 380
            self.y = 141
            self.bottomPiece=True
            self.leftPiece=True
            self.rightPiece=False
            self.pInArray = [1,4]
        self.rect = self.img.get_rect(topleft=(self.x,self.y))
        self.name="L"
        self.spawnM(screen)

    def spawnM(self,screen):
        screen.blit(self.img, self.rect)
        pygame.display.flip()

    def rotate1(self,screen,newrstate,check):
        if check==0:
            screen.blit(self.tile,self.rect)
        else:
            if newrstate==0:
                if self.place==1:
                    self.bottomPiece=False
                    self.leftPiece=True
                    self.rightPiece=True
                elif self.place==2:
                    self.bottomPiece=True
                    self.leftPiece=False
                    self.rightPiece=True
                elif self.place==3:
                    self.bottomPiece=True
                    self.leftPiece=False
                    self.rightPiece=False
                elif self.place==4:
                    self.bottomPiece=True
                    self.leftPiece=True
                    self.rightPiece=False
            elif newrstate==1:
                if self.place==1:
                    self.bottomPiece=True
                    self.leftPiece=False
                    self.rightPiece=True
                elif self.place==2:
                    self.bottomPiece=True
                    self.leftPiece=True
                    self.rightPiece=False
                elif self.place==3:
                    self.bottomPiece=False
                    self.leftPiece=True
                    self.rightPiece=True
                elif self.place==4:
                    self.bottomPiece=False
                    self.leftPiece=True
                    self.rightPiece=True
            elif newrstate==2:
                if self.place==1:
                    self.bottomPiece=True
                    self.leftPiece=True
                    self.rightPiece=True
                elif self.place==2:
                    self.bottomPiece=False
                    self.leftPiece=True
                    self.rightPiece=False
                elif self.place==3:
                    self.bottomPiece=True
                    self.leftPiece=False
                    self.rightPiece=False
                elif self.place==4:
                    self.bottomPiece=True
                    self.leftPiece=False
                    self.rightPiece=True
            elif newrstate==3:
                if self.place==1:
                    self.bottomPiece=True
                    self.leftPiece=True
                    self.rightPiece=False
                elif self.place==2:
                    self.bottomPiece=False
                    self.leftPiece=False
                    self.rightPiece=True
                elif self.place==3:
                    self.bottomPiece=False
                    self.leftPiece=True
                    self.rightPiece=True
                elif self.place==4:
                    self.bottomPiece=True
                    self.leftPiece=True
                    self.rightPiece=True
            self.rstate = newrstate
            displacement1 = self.newrstate[0]-self.pInArray[0]
            displacement2 = self.newrstate[1]-self.pInArray[1]
            self.rect.move_ip(displacement2*20,displacement1*20)
            self.pInArray = self.newrstate
            screen.blit(self.img,self.rect)
            self.newrstate=[0,0]

    def rotate(self,matrixarray,newrstate):#matrixarray to check if next place is free/newrstate to which pos it is now in
        if self.rstate==0:#if new pos is 0th pos  #testNo to know which test the rotation is now checking.
            if newrstate==1:#if new rstate is 1 (if they rotated clockwise)
                if self.place==1 and matrixarray[self.pInArray[0]+2][self.pInArray[1]]==0:#check if pos where it would be is free
                    self.newrstate = [self.pInArray[0]+2,self.pInArray[1]]#if it is, save this in a variable
                    return True#return true for loop to continue for all pieces
                elif self.place==2 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]-1]
                        return True
                elif self.place==3:
                    self.newrstate = [self.pInArray[0],self.pInArray[1]]
                    return True
                elif self.place==4 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]+1]
                        return True
                else:
                    return False#if untrue, return false for loop to stop
            elif newrstate==3:#if new rstate is 1 (if they rotated clockwise)
                if self.place==1 and self.pInArray[1]-2!=-1 and self.pInArray[1]-2!=-2:#check if pos where it would be is free
                    if matrixarray[self.pInArray[0]][self.pInArray[1]-2]==0:
                        self.newrstate = [self.pInArray[0],self.pInArray[1]-2]#if it is, save this in a variable
                        return True#return true for loop to continue for all pieces
                elif self.place==2 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]-1]
                        return True
                elif self.place==3:
                    self.newrstate = [self.pInArray[0],self.pInArray[1]]
                    return True
                elif self.place==4 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]+1]
                        return True
                else:
                    return False#if untrue, return false for loop to stop
        if self.rstate==1:#if new pos is 0th pos  #testNo to know which test the rotation is now checking.
            if newrstate==0:#if new rstate is 1 (if they rotated clockwise)
                if self.place==1 and matrixarray[self.pInArray[0]-2][self.pInArray[1]]==0:#check if pos where it would be is free
                    self.newrstate = [self.pInArray[0]-2,self.pInArray[1]]#if it is, save this in a variable
                    return True#return true for loop to continue for all pieces
                elif self.place==2 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]+1]
                        return True
                elif self.place==3:
                    self.newrstate = [self.pInArray[0],self.pInArray[1]]
                    return True
                elif self.place==4 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]-1]
                        return True
                else:
                    return False#if untrue, return false for loop to stop
            elif newrstate==2:#if new rstate is 1 (if they rotated clockwise)
                if self.place==1 and self.pInArray[1]-2!=-1 and self.pInArray[1]-2!=-2:#check if pos where it would be is free
                    if matrixarray[self.pInArray[0]][self.pInArray[1]-2]==0:
                        self.newrstate = [self.pInArray[0],self.pInArray[1]-2]#if it is, save this in a variable
                        return True#return true for loop to continue for all pieces
                elif self.place==2 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]-1]
                        return True
                elif self.place==3:
                    self.newrstate = [self.pInArray[0],self.pInArray[1]]
                    return True
                elif self.place==4 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]+1]
                        return True
                else:
                    return False#if untrue, return false for loop to stop
        if self.rstate==2:#if new pos is 0th pos  #testNo to know which test the rotation is now checking.
            if newrstate==1:#if new rstate is 1 (if they rotated clockwise)
                if self.place==1 and self.pInArray[1]+2!=10 and self.pInArray[1]+2!=11:#check if pos where it would be is free
                    if matrixarray[self.pInArray[0]][self.pInArray[1]+2]==0:
                        self.newrstate = [self.pInArray[0],self.pInArray[1]+2]#if it is, save this in a variable
                        return True#return true for loop to continue for all pieces
                elif self.place==2 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]+1]
                        return True
                elif self.place==3:
                    self.newrstate = [self.pInArray[0],self.pInArray[1]]
                    return True
                elif self.place==4 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]-1]
                        return True
                else:
                    return False#if untrue, return false for loop to stop
            elif newrstate==3:#if new rstate is 1 (if they rotated clockwise)
                if self.place==1 and matrixarray[self.pInArray[0]-2][self.pInArray[1]]==0:#check if pos where it would be is free
                        self.newrstate = [self.pInArray[0]-2,self.pInArray[1]]#if it is, save this in a variable
                        return True#return true for loop to continue for all pieces
                elif self.place==2 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]+1]
                        return True
                elif self.place==3:
                    self.newrstate = [self.pInArray[0],self.pInArray[1]]
                    return True
                elif self.place==4 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]-1]
                        return True
                else:
                    return False#if untrue, return false for loop to stop
        if self.rstate==3:#if new pos is 0th pos  #testNo to know which test the rotation is now checking.
            if newrstate==2:#if new rstate is 1 (if they rotated clockwise)
                if self.place==1 and matrixarray[self.pInArray[0]+2][self.pInArray[1]]==0:#check if pos where it would be is free
                    self.newrstate = [self.pInArray[0]+2,self.pInArray[1]]#if it is, save this in a variable
                    return True#return true for loop to continue for all pieces
                elif self.place==2 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]-1]
                        return True
                elif self.place==3:
                    self.newrstate = [self.pInArray[0],self.pInArray[1]]
                    return True
                elif self.place==4 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]+1]
                        return True
                else:
                    return False#if untrue, return false for loop to stop
            elif newrstate==0:#if new rstate is 1 (if they rotated clockwise)
                if self.place==1 and self.pInArray[1]+2!=10 and self.pInArray[1]+2!=11:#check if pos where it would be is free
                    if matrixarray[self.pInArray[0]][self.pInArray[1]+2]==0:
                        self.newrstate = [self.pInArray[0],self.pInArray[1]+2]#if it is, save this in a variable
                        return True#return true for loop to continue for all pieces
                elif self.place==2 and self.pInArray[1]+1!=10:
                    if matrixarray[self.pInArray[0]+1][self.pInArray[1]+1]==0:
                        self.newrstate = [self.pInArray[0]+1,self.pInArray[1]+1]
                        return True
                elif self.place==3:
                    self.newrstate = [self.pInArray[0],self.pInArray[1]]
                    return True
                elif self.place==4 and self.pInArray[1]-1!=-1:
                    if matrixarray[self.pInArray[0]-1][self.pInArray[1]-1]==0:
                        self.newrstate = [self.pInArray[0]-1,self.pInArray[1]-1]
                        return True
                else:
                    return False#if untrue, return false for loop to stop

    def movement1(self, matrixarray, check, screen, hardrop):
        if hardrop==False:#var to check if a hardrop is occurring
            if check==0:
                self.pInArray[0]+=1
                if self.rstate==0:
                    if self.place==1 or self.place==3 or self.place==4:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                if self.rstate==1:
                    if self.place==1 or self.place==4:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                if self.rstate==2:
                    if self.place==2 or self.place==3 or self.place==4:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                if self.rstate==3:
                    if self.place==1 or self.place==2:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                self.rect.move_ip(0,20)#move rect 20 pixels down
                screen.blit(self.img,self.rect)#blit new piece
            elif check==1:
                self.pInArray[1]-=1
                if self.rstate==0:
                    if self.place==1 or self.place==2:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                if self.rstate==1:
                    if self.place==1 or self.place==3 or self.place==4:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                if self.rstate==2:
                    if self.place==1 or self.place==4:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                if self.rstate==3:
                    if self.place==2 or self.place==3 or self.place==4:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                self.rect.move_ip(-20,0)#move rect 20 pixels down
                screen.blit(self.img,self.rect)#blit new piece
            elif check==2:
                self.pInArray[1]+=1
                if self.rstate==2:
                    if self.place==1 or self.place==2:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                if self.rstate==3:
                    if self.place==1 or self.place==3 or self.place==4:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                if self.rstate==0:
                    if self.place==1 or self.place==4:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                if self.rstate==1:
                    if self.place==2 or self.place==3 or self.place==4:
                        screen.blit(self.tile,self.rect)#blit tile to cover previous place
                self.rect.move_ip(20,0)#move rect 20 pixels right
                screen.blit(self.img,self.rect)#blit new piece
        else:
            screen.blit(self.tile,self.rect)#cover up original tiles
            if self.rstate==0:#if in first rotation state
                if self.place==3 or self.place==4 or self.place==2:#if bottom two pieces
                    displacement = check[0]-self.pInArray[0]#how far away og pos is to new pos
                else:
                    displacement = check[0]-1-self.pInArray[0]#how far away og pos is to new pos
            if self.rstate==1:#if in first rotation state
                if self.place==1 or self.place==2:#if bottom two pieces
                    displacement = check[0]-self.pInArray[0]#how far away og pos is to new pos
                elif self.place==3:
                    displacement = check[0]-1-self.pInArray[0]#how far away og pos is to new pos
                else:
                    displacement = check[0]-2-self.pInArray[0]#how far away og pos is to new pos
            if self.rstate==2:#if in first rotation state
                if check[1]==3 or check[1]==4:
                    if self.place==3 or self.place==2 or self.place==4:#if bottom two pieces
                        displacement = check[0]-self.pInArray[0]#how far away og pos is to new pos
                    else:
                        displacement = check[0]+1-self.pInArray[0]#how far away og pos is to new pos
                else:
                    if self.place==3 or self.place==2 or self.place==4:#if bottom two pieces
                        displacement = check[0]-1-self.pInArray[0]#how far away og pos is to new pos
                    else:
                        displacement = check[0]-self.pInArray[0]#how far away og pos is to new pos
            if self.rstate==3:#if in first rotation state
                if check[1]==1:
                    if self.place==1 or self.place==2:#if bottom two pieces
                        displacement = check[0]-self.pInArray[0]#how far away og pos is to new pos
                    elif self.place==3:
                        displacement = check[0]+1-self.pInArray[0]#how far away og pos is to new pos
                    elif self.place==4:
                        displacement = check[0]+2-self.pInArray[0]#how far away og pos is to new pos
                else:
                    if self.place==4:#if bottom two pieces
                        displacement = check[0]-self.pInArray[0]#how far away og pos is to new pos
                    elif self.place==3:
                        displacement = check[0]-1-self.pInArray[0]#how far away og pos is to new pos
                    else:
                        displacement = check[0]-2-self.pInArray[0]#how far away og pos is to new pos
            self.pInArray[0]+=displacement#new array position
            self.rect.move_ip(0,displacement*20)#move rect here
            screen.blit(self.img,self.rect)#blit new position