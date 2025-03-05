#-------------------------------------------------------------------------------
# Name:        aspectratio
# Purpose:
#
# Author:      17Mota
#
# Created:     28/04/2023
# Copyright:   (c) CoderBox 2023
# Licence:     <your licence>
#-------------------------------------------------------------------------------
'''
This module 'main.py' uses the classes from the other modules to implement
the corresponding features of the game
It has all the main code needed to display and run the game as well as the logic
behind general gameplay
'''
from button import Button
from pieces import *
import pygame, sys, csv,os,pandas as pd, numpy as np, random,time
pygame.init()

size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Catris!")
icon = pygame.image.load("cat_icon.jpg")
pygame.display.set_icon(icon)


#initialising controls
controls = ["right","left","up","z","down","space","c"]
#what the controls control
controlsfunc = ["Right","Left","Clockwise","Anti-Clockwise","Soft Drop","Hard Drop","Hold"]

#initialise sfx and music vol
vols = [1,1]
buttonSound = pygame.mixer.Sound('sounds/button.wav')
meowSound = pygame.mixer.Sound('sounds/catmeow2.wav')
meowSound1 = pygame.mixer.Sound('sounds/catmeow1.wav')
openMenu = pygame.mixer.Sound('sounds/open_menu.wav')
closeMenu = pygame.mixer.Sound('sounds/close_menu.wav')
sfxChange = pygame.mixer.Sound('sounds/SFX_change.wav')
musicChange = pygame.mixer.Sound('sounds/music_change.wav')
pieceMove = pygame.mixer.Sound('sounds/piece_move.wav')
pieceNoMove = pygame.mixer.Sound('sounds/piece_nomove.wav')
rotateSound = pygame.mixer.Sound('sounds/rotate_sound.wav')
levelUpSound= pygame.mixer.Sound('sounds/level_up.wav')
hurrySound = pygame.mixer.Sound('sounds/hurry.wav')
noRotateSound = pygame.mixer.Sound('sounds/no_rotate.wav')
linesSound = pygame.mixer.Sound('sounds/lines.wav')
allClearSound = pygame.mixer.Sound('sounds/all_clear.wav')
hardDropSound = pygame.mixer.Sound('sounds/hard_drop.wav')

buttonSound.set_volume(vols[1]/5)
meowSound.set_volume(vols[1]/5)
meowSound1.set_volume(vols[1]/5)
openMenu.set_volume(vols[1]/5)
closeMenu.set_volume(vols[1]/5)
sfxChange.set_volume(vols[1]/5)
musicChange.set_volume(vols[1]/5)
pieceMove.set_volume(vols[1]/5)
pieceNoMove.set_volume(vols[1]/5)
rotateSound.set_volume(vols[1]/5)
levelUpSound.set_volume(vols[1]/5)
hurrySound.set_volume(vols[1]/5)
noRotateSound.set_volume(vols[1]/5)
linesSound.set_volume(vols[1]/5)
allClearSound.set_volume(vols[1]/5)
hardDropSound.set_volume(vols[1]/5)

#button sprite initialisation
buttonimg = pygame.image.load("button.png")
buttonBorder = pygame.image.load("button_border.png")
buttonimg2 = pygame.image.load("button2.png")
buttonBorder2 = pygame.image.load("button_border2.png")

music_buttons = pygame.sprite.Group()
sfx_buttons = pygame.sprite.Group()
all_buttons = pygame.sprite.Group()

for i in range(0,6):#to create 5 buttons
    x=279+(i*78)#x coord of each
    t = i+1
    if i==0:#to make it so the first button is automatically selected
        button_obj = Button(x, 189, str(t), buttonimg, buttonBorder, t, 1)#passing parameters
    elif i==5:
        button_obj = Button(x-18, 189, "OFF", buttonimg2, buttonBorder2, 0, 0)#passing parameters
    else:
        button_obj = Button(x, 189, str(t), buttonimg, buttonBorder, t, 0)#passing parameters
    music_buttons.add(button_obj)#adding object to music group
    all_buttons.add(button_obj)# adding object to all buttons group

for i in range(0,6):
    x=279+(i*78)
    t = i+1
    if i==0:
        button_obj = Button(x, 280, str(t), buttonimg, buttonBorder, t, 1)
    elif i==5:
        button_obj = Button(x-18, 280, "OFF", buttonimg2, buttonBorder2, 0, 0)#passing parameters
    else:
        button_obj = Button(x, 280, str(t), buttonimg, buttonBorder, t, 0)
    sfx_buttons.add(button_obj)
    all_buttons.add(button_obj)

earray = []
marray = []
harray = []

names = ["eleaderboards","mleaderboards","hleaderboards"]

for filename in names:#for each filename earray, marray, harray
    fields = []#all fields
    rows = []#all rows
    if os.path.isfile(filename):#if the file already exists in folder directory
        with open(filename, 'r') as csvfile:#open this file in read mode
            empt = pd.DataFrame(columns = ['Names','Scores'])#using pandas module to check if empty
            empty = empt.empty
            if empty:#if not empty, read the file
                csvreader = csv.reader(csvfile)#converting csv into readable format
                fields = next(csvreader)#move to first line
                for row in csvreader:#for each row in the file
                    if row!=[]:#if the row is not empty
                        rows.append(row)#add row in file to row array

                for row in rows[:5]:#for first five rows
                    if filename == "eleaderboards":#append to correct array based on which leaderboard it is
                        earray.append(row)
                    elif filename == "mleaderboards":
                        marray.append(row)
                    elif filename == "hleaderboards":
                        harray.append(row)
            else:#if file is empty
                fields = ["Names", "Scores"]#add title of names and scores
                with open(filename, 'w') as csvfile:#write this into files
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(fields)
    else:#if file does not already exist
        fields = ["Names", "Scores"]#add title of names and scores
        with open(filename, 'w') as csvfile:#write this into files
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(fields)

newscore=0
score=0
name = ""
ups=[]
downs=[]

num = 0

spng = pygame.image.load('Snew.png').convert()#load images for pieces
zpng = pygame.image.load('Znew-1.png.png').convert()
ipng = pygame.image.load('Inew.png').convert()
opng = pygame.image.load('Onew1-1.png.png').convert()
jpng = pygame.image.load('Jnew.png').convert()
lpng = pygame.image.load('Lnew1-1.png.png').convert()
tpng = pygame.image.load('Tnew1-1.png.png').convert()

piece_objs = pygame.sprite.Group()#group to store all piece objects
locked_piece_objs = pygame.sprite.Group()#group to store all locked piece objects

def changeLeaderboards(gamemode, newscore, name, array):#function to change leaderboards when high schore achieved
    if gamemode=="easy":#ammend respective file for which gamemode a high score was reached.
        filename = "eleaderboards"
    elif gamemode=="medium":
        filename = "mleaderboards"
    elif gamemode=="hard":
        filename = "hleaderboards"
    array.append([name, newscore])#append this new score and name to array
    if array!=[]:#if array (earray, marray, or harray) not already empty
        done = False#var to check algorithm's completion
        check = 0
        while not done:#apply BUBBLE sort for descending ordered list
          done = True#declare alg is finished
          for i in range(0,len(array)-1):#for length of array
            tmp = array[i][0]#temporary variables to be able to change values
            tmp1 = array[i][1]
            if int(array[i][1])<int(array[i+1][1]):#if the next value is larger than previous
              array[i][0]=array[i+1][0]
              array[i+1][0]=tmp#swap the name and score position of the entries
              array[i][1]=array[i+1][1]
              array[i+1][1]=tmp1
              done = False#done is false as must check again if another entry in wrong place
        if len(array)==6:
            array.pop(5)#if final array ends with more than 5 entries, remove the last one
    rows = array#make rows var the now sorted list

    fields = ["Names", "Scores"]

    with open(filename, 'w') as csvfile:#overwrite file to show new scores.
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)

    return(array)

def gameOver(array, score, gamemode,num,piece_objs,locked_piece_objs,earray,marray,harray,vols):
    alpha = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    white = (248,248,248)
    font = pygame.font.SysFont("lucidaconsole", 35)#load font
    print (array)
    check10=0
    if array!=[]:
        if score>int(array[len(array)-1][1]) or len(array)<5:
          check10=1#change check variable so program can only let player enter name if have achieved high score
          gohs = pygame.image.load('game_over_hs1.png').convert()#if high score, display high score game over screen
          screen.blit(gohs, (0, 0))
          pygame.display.flip()
          au = pygame.image.load('arrow_up.png').convert()#also display arrows to be used to change name values
          ad = pygame.image.load('arrow_down.png').convert()
          for i in range(0,3):
            ups.append(screen.blit(au,(384+(i*46),287)))
          for i in range(0,3):
            downs.append(screen.blit(ad,(384+(i*46),335)))
        else:
          go = pygame.image.load('game_over2.png').convert()#if not high score, display normal game over screen
          screen.blit(go, (0, 0))
          pygame.display.flip()
    else:
          check10=1#change check variable so program can only let player enter name if have achieved high score
          gohs = pygame.image.load('game_over_hs1.png').convert()#if high score, display high score game over screen
          screen.blit(gohs, (0, 0))
          pygame.display.flip()
          au = pygame.image.load('arrow_up.png').convert()#also display arrows to be used to change name values
          ad = pygame.image.load('arrow_down.png').convert()
          for i in range(0,3):
            ups.append(screen.blit(au,(384+(i*46),287)))
          for i in range(0,3):
            downs.append(screen.blit(ad,(384+(i*46),335)))

    scoretxt = font.render(str(score), False, white)#load and display score text
    scoretxtRect = scoretxt.get_rect(topleft=(390,243))#create rect for text
    screen.blit(scoretxt, scoretxtRect)
    pygame.display.flip()

    buttonSound.set_volume(vols[1]/5)
    closeMenu.set_volume(vols[1]/5)

    check=1
    check1=1
    check2=1
    check3=1
    check4=1

    namenum = [0,0,0]#array to store name

    square =pygame.image.load('square.png').convert()#to cover original letter

    true1 = True
    if check10==1:
        initname = font.render("A", False, white)#load and display initial AAA
        for i in range(0,3):
            screen.blit(initname,(378+(i*46),298))
    pygame.display.flip()
    while true1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                changeLeaderboards(gamemode, score, name, array)#change leaderboards before game exits
                true1 = False
            if event.type == pygame.MOUSEBUTTONDOWN and check10==1:#only runs code if high score
                pos = pygame.mouse.get_pos()
                for i in ups:
                    if i.collidepoint(pos):#checks if arrows were clicked
                        buttonSound.play()
                        idx = ups.index(i)
                        screen.blit(square, (i[0]-7, i[1]+17))#blit sqaure to cover original letter
                        if namenum[idx]==25:#changes letter shown and saved
                            namenum[idx] = 0#if letter originally z, it is now a
                        else:
                            namenum[idx]+=1
                        txt = font.render(alpha[namenum[idx]], False, white)#loads and displays new letter
                        screen.blit(txt,(378+(idx*46),298))
                        pygame.display.flip()
                for j in downs:
                    if j.collidepoint(pos):
                        buttonSound.play()
                        idx = downs.index(j)
                        screen.blit(square, (j[0]-9, j[1]-33))#blit sqaure to cover original letter
                        if namenum[idx]==0:#changes letter shown and saved
                            namenum[idx] = 25#if letter originally a, it is now z
                        else:
                            namenum[idx]-=1
                        txt = font.render(alpha[namenum[idx]], False, white)#loads and displays new letter
                        screen.blit(txt,(378+(idx*46),298))
                        pygame.display.flip()
            if (event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP) and (263 < event.pos[0] < 536 and 361 < event.pos[1] < 438):#if user hovering on button
                if check1==1:
                   buttonSound.play()
                   tad = pygame.image.load('try_again_down.png').convert()
                   screen.blit(tad, (263, 361))
                   pygame.display.flip()#loads and displays pushed button img^^
                   check=1
                   check1=2
                if event.type == pygame.MOUSEBUTTONUP:
                    name = str(alpha[namenum[0]]+alpha[namenum[1]]+alpha[namenum[2]])
                    if check10==1:
                        changeLeaderboards(gamemode, score, name, array)#leaderboards are changed
                    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
                    pygame.mixer.music.load('sounds/main_menu_music.mp3')
                    pygame.mixer.music.set_volume(vols[0]/5)
                    pygame.mixer.music.play(-1,0,2500)
                    gameScreen(num,piece_objs,locked_piece_objs,earray,marray,harray,vols)
            else:
                if check==1:
                   ta = pygame.image.load('try_again.png').convert()
                   screen.blit(ta, (263, 361))
                   pygame.display.flip()#loads and displays original button img^
                   check=2
                   check1=1
            if (event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP) and (191 < event.pos[0] < 608 and 466 < event.pos[1] < 543):#if user hovering on button
                if check4==1:
                   buttonSound.play()
                   emmd = pygame.image.load('exitmm_down.png').convert()
                   screen.blit(emmd, (191, 466))
                   pygame.display.flip()#loads and displays pushed button img^^
                   check3=1
                   check4=2
                if event.type == pygame.MOUSEBUTTONUP:
                    name = str(alpha[namenum[0]]+alpha[namenum[1]]+alpha[namenum[2]])
                    if check10==1:
                        changeLeaderboards(gamemode, score, name, array)#leaderboards are changed
                    closeMenu.play()
                    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
                    pygame.mixer.music.load('sounds/main_menu_music.mp3')
                    pygame.mixer.music.set_volume(vols[0]/5)
                    pygame.mixer.music.play(-1,0,2500)
                    main(num,piece_objs,locked_piece_objs,earray,marray,harray,vols)
            else:
                if check3==1:
                   emm = pygame.image.load('exitmm.png').convert()
                   screen.blit(emm, (191, 466))
                   pygame.display.flip()#loads and displays original button img^
                   check3=2
                   check4=1
    pygame.quit()

def displayLeaderboards(earray,marray,harray,num,piece_objs,locked_piece_objs,vols):
    lb = pygame.image.load('leaderboards2.png').convert()
    screen.blit(lb, (0, 0))
    pygame.display.flip()
    white = (248,248,248)
    font = pygame.font.SysFont("lucidaconsole", 35)#load font

    buttonSound.set_volume(vols[1]/5)
    closeMenu.set_volume(vols[1]/5)

    true1 = True

    check=1
    check2=1
    check3=1
    check4=1
    check5=1
    check6=1
    check7=0#check variables so images are only blitted once
    check8=0
    check9=0

    gamemode1 = ""

    square1 = pygame.image.load('squarenew.png').convert()

    while true1:
        for event in pygame.event.get():
            if event.type== pygame.MOUSEBUTTONUP and (688 < event.pos[0] < 753 and 29 < event.pos[1] < 93):
                closeMenu.play()
                main(num,piece_objs,locked_piece_objs,earray,marray,harray,vols)
            if (event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP) and (99 < event.pos[0] < 218 and 130 < event.pos[1] < 208):#if user hovering on button
                if check2==1 and gamemode1=="easy":#button is selected
                    buttonSound.play()
                    ezbd = pygame.image.load('easy_border_down2.png').convert()
                    screen.blit(ezbd, (99, 130))
                    pygame.display.flip()#loads and displays pushed button img^^
                    check=1
                    check2=2
                elif check2==1:#button is not selected
                    buttonSound.play()
                    ezd = pygame.image.load('easy_down2.png').convert()
                    screen.blit(ezd, (99, 130))
                    pygame.display.flip()#loads and displays pushed button img^^
                    check=1
                    check2=2
                if event.type == pygame.MOUSEBUTTONUP and gamemode1!="easy":#button is selected
                    gamemode1="easy"
                    ezb = pygame.image.load('easy_border2.png').convert()
                    m = pygame.image.load('medium2.png').convert()
                    h = pygame.image.load('hard2.png').convert()#other buttons are flipped to be deselected
                    screen.blit(ezb, (99, 130))
                    screen.blit(m, (307, 131))
                    screen.blit(h, (563, 127))
                    add=0
                    for i in range(0,5):#clears every single line
                        screen.blit(square1,(192,239+(add*70)))
                        pygame.display.flip()
                        add+=1
                    add=0
                    place = 1
                    if earray!=[]:#if earray isnt empty
                        for namescore in earray:
                            if earray.index(namescore)!=0:#make sure not first item in list
                                if earray[earray.index(namescore)-1][1]==namescore[1]:#if last value same as previous
                                    place-=1#make same place on leaderboard
                            scoredisplay = font.render(str(place)+". "+(str(namescore[0])+" - "+str(namescore[1])), False, white)
                            screen.blit(scoredisplay,(192,240+(add*70)))#blit text with score
                            if earray.index(namescore)!=0:#make sure not first item in list
                                if earray[earray.index(namescore)-1][1]==namescore[1]:
                                    place+=2#add 2 for next item's place to be 2 away
                                else:
                                    place+=1#add one for next item's place to be 1 away
                            else:
                                place+=1
                            add+=1
                    pygame.display.flip()#loads and displays original button img^
            else:
                if check==1 and gamemode1=="easy":#button is selected
                    ezb = pygame.image.load('easy_border2.png').convert()
                    screen.blit(ezb, (99, 130))
                    pygame.display.flip()#loads and displays original button img^
                    check=2
                    check2=1
                elif check==1:#button is not selected
                    ez = pygame.image.load('easy2.png').convert()
                    screen.blit(ez, (99, 130))
                    pygame.display.flip()#loads and displays original button img^
                    check=2
                    check2=1
#################################
            if (event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP) and (307 < event.pos[0] < 493 and 131 < event.pos[1] < 209):#if user hovering on button
                if check4==1 and gamemode1=="medium":#button is selected
                    buttonSound.play()
                    mbd = pygame.image.load('medium_border_down2.png').convert()
                    screen.blit(mbd, (307, 131))
                    pygame.display.flip()#loads and displays pushed button img^^
                    check3=1
                    check4=2
                elif check4==1:#button is not selected
                    buttonSound.play()
                    md = pygame.image.load('medium_down2.png').convert()
                    screen.blit(md, (307, 131))
                    pygame.display.flip()#loads and displays pushed button img^^
                    check3=1
                    check4=2
                if event.type == pygame.MOUSEBUTTONUP and gamemode1!="medium":#button is selected
                    gamemode1="medium"
                    mb = pygame.image.load('medium_border2.png').convert()
                    ez = pygame.image.load('easy2.png').convert()
                    h = pygame.image.load('hard2.png').convert()#other buttons are flipped to be deselected
                    screen.blit(ez, (99, 130))
                    screen.blit(mb, (307, 131))
                    screen.blit(h, (563, 127))
                    add=0
                    for i in range(0,5):#clears every single line
                        screen.blit(square1,(192,239+(add*70)))
                        pygame.display.flip()
                        add+=1
                    add=0
                    place = 1
                    if marray!=[]:#if earray isnt empty
                        for namescore in marray:
                            if marray.index(namescore)!=0:#make sure not first item in list
                                if marray[marray.index(namescore)-1][1]==namescore[1]:#if last value same as previous
                                    place-=1#make same place on leaderboard
                            scoredisplay = font.render(str(place)+". "+(str(namescore[0])+" - "+str(namescore[1])), False, white)
                            screen.blit(scoredisplay,(192,240+(add*70)))#blit text with score
                            if marray.index(namescore)!=0:#make sure not first item in list
                                if marray[marray.index(namescore)-1][1]==namescore[1]:
                                    place+=2#add 2 for next item's place to be 2 away
                                else:
                                    place+=1#add one for next item's place to be 1 away
                            else:
                                place+=1
                            add+=1
                    pygame.display.flip()#loads and displays original button img^
            else:
                if check3==1 and gamemode1=="medium":#button is selected
                    mb = pygame.image.load('medium_border2.png').convert()
                    screen.blit(mb, (307, 131))
                    pygame.display.flip()#loads and displays original button img^
                    check3=2
                    check4=1
                elif check3==1:#button is not selected
                    m = pygame.image.load('medium2.png').convert()
                    screen.blit(m, (307, 131))
                    pygame.display.flip()#loads and displays original button img^
                    check3=2
                    check4=1
#################################
            if (event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP) and (563 < event.pos[0] < 693 and 127 < event.pos[1] < 210):#if user hovering on button
                if check6==1 and gamemode1=="hard":#button is selected
                    buttonSound.play()
                    hbd = pygame.image.load('hard_border_down2.png').convert()
                    screen.blit(hbd, (563, 127))
                    pygame.display.flip()#loads and displays pushed button img^^
                    check5=1
                    check6=2
                elif check6==1:#button is not selected
                    buttonSound.play()
                    hd = pygame.image.load('hard_down2.png').convert()
                    screen.blit(hd, (563, 127))
                    pygame.display.flip()#loads and displays pushed button img^^
                    check5=1
                    check6=2
                if event.type == pygame.MOUSEBUTTONUP and gamemode1!="hard":#button is selected
                    gamemode1="hard"
                    hb = pygame.image.load('hard_border2.png').convert()
                    m = pygame.image.load('medium2.png').convert()
                    ez = pygame.image.load('easy2.png').convert()#other buttons are flipped to be deselected
                    screen.blit(ez, (99, 130))
                    screen.blit(m, (307, 131))
                    screen.blit(hb, (563, 127))
                    add=0#must declare add=0
                    for i in range(0,5):#clears every single line
                        screen.blit(square1,(192,239+(add*70)))
                        pygame.display.flip()
                        add+=1
                    add=0
                    place = 1
                    if harray!=[]:#if earray isnt empty
                        for namescore in harray:
                            if harray.index(namescore)!=0:#make sure not first item in list
                                if harray[harray.index(namescore)-1][1]==namescore[1]:#if last value same as previous
                                    place-=1#make same place on leaderboard
                            scoredisplay = font.render(str(place)+". "+(str(namescore[0])+" - "+str(namescore[1])), False, white)
                            screen.blit(scoredisplay,(192,240+(add*70)))#blit text with score
                            if harray.index(namescore)!=0:#make sure not first item in list
                                if harray[harray.index(namescore)-1][1]==namescore[1]:
                                    place+=2#add 2 for next item's place to be 2 away
                                else:
                                    place+=1#add one for next item's place to be 1 away
                            else:
                                place+=1
                            add+=1
                    pygame.display.flip()#loads and displays original button img^
            else:
                if check5==1 and gamemode1=="hard":#button is selected
                    hb = pygame.image.load('hard_border2.png').convert()
                    screen.blit(hb, (563, 127))
                    pygame.display.flip()#loads and displays original button img^
                    check5=2
                    check6=1
                elif check5==1:#button is not selected
                    h = pygame.image.load('hard2.png').convert()
                    screen.blit(h, (563, 127))
                    pygame.display.flip()#loads and displays original button img^
                    check5=2
                    check6=1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    closeMenu.play()
                    main(num,piece_objs,locked_piece_objs,earray,marray,harray,vols)
            if event.type == pygame.QUIT:
                true1 = False
    pygame.quit()

def settings(check,controls,controlsfunc,num,piece_objs,locked_piece_objs,earray,marray,harray,vols):
    if check==1:
        s = pygame.image.load('settings2.png').convert()
    else:
        s = pygame.image.load('pause_menu3.png').convert()

    screen.blit(s, (0, 0))
    pygame.display.flip()

    closeMenu.set_volume(vols[1]/5)
    buttonSound.set_volume(vols[1]/5)
    sfxChange.set_volume(vols[1]/5)
    musicChange.set_volume(vols[1]/5)

    square3 = pygame.image.load('square3.png').convert()
    square4 = pygame.image.load('square4.png').convert()

    white = (248,248,248)
    green = (117,192,106)
    font = pygame.font.SysFont("lucidaconsole", 35)
    font2 = pygame.font.SysFont("lucidaconsole", 17)
    set2d = font.render("Set to Default", False, white)#load set to default text
    set2drect = set2d.get_rect(topleft=(280,430))#give rect to allow collisions
    screen.blit(set2d, set2drect)#blit to screen
    controltxt = font2.render((controls[0]).title(), False, white)#load control texts
    cname = font2.render(controlsfunc[0], False, white)
    controltxtrect = controltxt.get_rect(topleft=(595,388))#give x y coords
    cnamerect = cname.get_rect(topleft=(350,388))
    screen.blit(controltxt, controltxtrect)#blit to screen
    screen.blit(cname, cnamerect)
    pygame.display.flip()#update screen

    musicVal = vols[0]
    sfxVal = vols[1]

    status=0#var to remember which control is being displayed

    true1 = True

    check2=1
    check3=1
    check4=0
    check5=0

    while true1:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:#if user presses key
                #pygame.key.key_code() to go the other way
                #print(pygame.key.name(event.key))
                controls[status] =pygame.key.name(event.key)#new control for function
                screen.blit(square4, (586,379))#cover up previous text
                controltxt = font2.render((controls[status]).title(), False, white)#define new text
                screen.blit(controltxt, controltxtrect)#blit to screen
                pygame.display.flip()#update display
            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                if set2drect.collidepoint(pos):
                    if check4==0:
                        font = pygame.font.SysFont("lucidaconsole", 35)
                        set2d = font.render("Set to Default", False, green)
                        screen.blit(set2d, set2drect)
                        check5=0
                        check4=1
                else:
                    if check5==0:
                        font = pygame.font.SysFont("lucidaconsole", 35)
                        set2d = font.render("Set to Default", False, white)
                        screen.blit(set2d, set2drect)
                        check4=0
                        check5=1
                #pygame.display.flip()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()#get current mouse position
                if set2drect.collidepoint(pos):#if user clicked on text rect
                    screen.blit(square3, (345,380))
                    screen.blit(square4, (586,379))#cover previous text
                    buttonSound.play()
                    controls = ["right","left","up","z","down","space","c"]#controls to default
                    controltxt = font2.render((controls[0]).title(), False, white)
                    cname = font2.render(controlsfunc[0], False, white)#display original text
                    screen.blit(controltxt, controltxtrect)
                    screen.blit(cname, cnamerect)
                    pygame.display.flip()
                    status=0#status back to 0
            if (event.type == pygame.MOUSEBUTTONUP) and (298 < event.pos[0] < 328 and 378 < event.pos[1] < 410):#if user clicks on left arrow
                buttonSound.play()
                screen.blit(square3, (345,380))#covers up control and control name from before
                screen.blit(square4, (586,379))
                if status==0:#changes which control is shown
                    status = 6
                else:
                    status-=1
                controltxt = font2.render((controls[status]).title(), False, white)#loads new control text
                cname = font2.render(controlsfunc[status], False, white)#loads new control name text
                screen.blit(controltxt, controltxtrect)
                screen.blit(cname, cnamerect)#displays new texts
                pygame.display.flip()
            if (event.type == event.type == pygame.MOUSEBUTTONUP) and (518 < event.pos[0] < 543 and 378 < event.pos[1] < 410):#if user clicks on right arrow
                buttonSound.play()
                screen.blit(square3, (345,380))
                screen.blit(square4, (586,379))#displays new texts
                if status==6:#changes which control is shown
                    status = 0
                else:
                    status+=1
                controltxt = font2.render((controls[status]).title(), False, white)#loads new control text
                cname = font2.render(controlsfunc[status], False, white)#loads new control name text
                screen.blit(controltxt, controltxtrect)
                screen.blit(cname, cnamerect)
                pygame.display.flip()
            if event.type == pygame.MOUSEBUTTONUP:
                for button in music_buttons:
                    musicVal, check1 = button.input(pygame.mouse.get_pos(), musicVal, screen,musicChange)
                    if check1 == 1:
                        for button1 in music_buttons:
                            button1.display(screen)
                            if button != button1:
                                vols[0] = musicVal
                                pygame.mixer.music.set_volume(vols[0]/5)
                                button1.check1 = 0
                for button in sfx_buttons:
                    sfxVal, check1 = button.input(pygame.mouse.get_pos(), sfxVal, screen,sfxChange)
                    if check1 == 1:
                        for button1 in sfx_buttons:
                            button1.display(screen)
                            if button != button1:
                                vols[1] = sfxVal
                                closeMenu.set_volume(vols[1]/5)
                                buttonSound.set_volume(vols[1]/5)
                                sfxChange.set_volume(vols[1]/5)
                                musicChange.set_volume(vols[1]/5)
                                button1.check1 = 0
            if event.type== pygame.MOUSEBUTTONUP and (688 < event.pos[0] < 753 and 29 < event.pos[1] < 93):
                closeMenu.play()
                if check==1:
                    return vols
                else:
                    x = "x"
                    return x,vols
            if (event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP) and (191 < event.pos[0] < 608 and 472 < event.pos[1] < 549) and check==2:#if user hovering on button
                if check3==1:
                    buttonSound.play()
                    emmd = pygame.image.load('exitmm_down.png').convert()
                    screen.blit(emmd, (191, 472))
                    pygame.display.flip()#loads and displays pushed button img^^
                    check2=1
                    check3=2
                if event.type == pygame.MOUSEBUTTONUP:
                    piece_objs.empty()
                    locked_piece_objs.empty()
                    closeMenu.play()
                    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
                    pygame.mixer.music.load('sounds/main_menu_music.mp3')
                    pygame.mixer.music.set_volume(vols[0]/5)
                    pygame.mixer.music.play(-1,0,2500)
                    main(num,piece_objs,locked_piece_objs,earray,marray,harray,vols)#takes back to main menu
            else:
                if check==2:
                    if check2==1:
                        emm = pygame.image.load('exitmm.png').convert()
                        screen.blit(emm, (191, 472))
                        pygame.display.flip()#loads and displays original button img^
                        check2=2
                        check3=1
            if event.type == pygame.QUIT:
                true1 = False

        for button in all_buttons:
            button.display(screen)
            button.hover(pygame.mouse.get_pos())

        pygame.display.flip()
    pygame.quit()

def spawn(ps,num,piece_objs):
    newPiece = ps[0]
    if newPiece == "S":
        for i in range(1,5):
            num+=1
            piece_obj = sS(spng,num,i,screen)
            piece_objs.add(piece_obj)#add objects to group
    if newPiece == "Z":
        for i in range(1,5):
            num+=1
            piece_obj = sZ(zpng,num,i,screen)
            piece_objs.add(piece_obj)#add objects to group
    if newPiece == "I":
        for i in range(1,5):
            num+=1
            piece_obj = sI(ipng,num,i,screen)
            piece_objs.add(piece_obj)#add objects to group
    if newPiece == "O":
        for i in range(1,5):
            num+=1
            piece_obj = sO(opng,num,i,screen)
            piece_objs.add(piece_obj)#add objects to group
    if newPiece == "J":
        for i in range(1,5):
            num+=1
            piece_obj = sJ(jpng,num,i,screen)
            piece_objs.add(piece_obj)#add objects to group
    if newPiece == "L":
        for i in range(1,5):
            num+=1
            piece_obj = sL(lpng,num,i,screen)
            piece_objs.add(piece_obj)#add objects to group
    if newPiece == "T":
        for i in range(1,5):
            num+=1
            piece_obj = sT(tpng,num,i,screen)
            piece_objs.add(piece_obj)#add objects to group
    return num,piece_objs


def sevenBag(ps, check, psq2,num,piece_objs):#sevenBag function to decide next piece
    """
    function that shuffles order of pieces
    """
    def shuffle(pieces):
        random.shuffle(pieces)
        return pieces
    """
    #function to remove used pieces from the piece sequence
    and append new values back to piece sequence
    """
    def add(ps, psq2, c):
        check = False
        ps.pop(0)#this value will actually be taken onto matrix to be used
        if c==1:
            ps.append(psq2[0])
            psq2.pop(0)
        return ps, psq2

    def main1():#function to initialise piece sequences
        pieces1 = ["S","Z","I","O","J","L","T"]
        pieces2 = ["S","Z","I","O","J","L","T"]
        psq1 = random.choice(pieces1)
        psq2 = shuffle(pieces2)
        return psq1, psq2

    """
    selection statements to check where the sequences
    are in their iterations.
    """
    if check == True:
        psq1, psq2 = main1()
        ps.append(psq1)
        check = False
    elif len(psq2)==4 or len(psq2)==3:
        ps, psq2 = add(ps, psq2, 1)
        none, psq2, = main1()
    elif len(ps)==1:
        ps, psq2 = add(ps, psq2, 1)
    else:
        ps, psq2 = add(ps, psq2, 2)

    display(psq2[0],"next")#display next piece
    nextPiece = psq2[0]#define next piece
    num,piece_objs = spawn(ps,num,piece_objs)#spawn the new piece
    return ps, check, psq2, nextPiece,num,piece_objs#return to gameplay

def display(piece,place):#display function to show pieces
    gc = pygame.image.load('green_cover.png').convert()#green image to cover original piece in holding/new piece position
    if place=="held":#if displaying new held piece, x coord different to if it was a new piece to cover original piece
        x1 = 80
    else:
        x1 = 637
    screen.blit(gc, (x1,114))
    '''
    as O and I pieces have different image dimensions to others, they must be defined differently to display in centre of boxes.
    '''
    if piece=="O":
        if place=="held":
            x =102#if O piece, it has a different x coord to siplay in middle for hold/new piece, etc.
        else:
            x = 658
        o = pygame.image.load('O1-1.png.png').convert()
        screen.blit(o, (x, 116))
        pygame.display.flip()#load and display the whole piece img^^
    elif piece=="I":
        if place=="held":
            x = 83
        else:
            x = 639
        iP = pygame.image.load('I.png.png').convert()
        screen.blit(iP, (x, 126))
        pygame.display.flip()#load and display the whole piece img^^
    else:
        if place=="held":
            x = 93
        else:
            x = 649
        if piece=="J":
            pc = pygame.image.load('J6.png.png').convert_alpha()#using alpha function to allow for transparency in the images
        elif piece=="L":
            pc = pygame.image.load('L1-1.png.png').convert_alpha()
        elif piece=="S":
            pc = pygame.image.load('S.png.png').convert_alpha()
        elif piece=="Z":
            pc = pygame.image.load('Z1-1.png.png').convert_alpha()
        elif piece=="T":
            pc = pygame.image.load('T1-1.png.png').convert_alpha()
        screen.blit(pc, (x, 116))
        pygame.display.flip()#load and display the whole piece img^^

def hold(ps,psq2,held,nextPiece,num,piece_objs):#hold function
    if held==[]:#if no original held piece
        held = ps#new held piece is one currently using
        ps = []#declare ps is array again
        ps.append(psq2[0])#ps is now next piece in piece sequence
        psq2.pop(0)#get rid of this piece from the piece sequence as is being used
        nextPiece = []#next piece empty again
        nextPiece.append(psq2[0])#next piece now the next piece in piece sequence array
    else:#if already piece held
        temp = held#use temporary vars to swap the currently used piece and held piece
        held = ps
        ps = temp

    for i in range(0,2):#to iterate twice
        if i==0:#on first iteration, change displayed held piece
            piece = held[0]
            display(piece,"held")#using display function
        else:#on second iteration, change displayed next piece
            piece = nextPiece[0]
            display(piece,"next")#using display function

    num,piece_objs = spawn(ps,num,piece_objs)#spawn the new piece

    return ps,psq2,held,nextPiece,num#return to gameplay with piece variables

def lineClears(score, matrixarray,locked_piece_objs,screen,totalclearcount,level,b2b,text2display):
    '''
    function that calculates scores when clearing lines and fixes
    overall matrix depending on how many lines were cleared
    '''
    linesSound.set_volume(vols[1]/5)
    allClearSound.set_volume(vols[1]/5)

    white = (248,248,248)
    font = pygame.font.SysFont("lucidaconsole", 35)#load font

    def repair(l,matrixarray):
        for i in range(l,-1,-1):
            print(i)
            if i!=0:
                count3=0
                count4=-1
                for value in matrixarray[i-1]:
                    for piece in locked_piece_objs:
                        if piece.num==value:
                            piece.hold(screen)
                            piece.movement1(matrixarray, 0, screen, False)
                    count4+=1
                    if value!=0:
                        matrixarray[i][count4] = matrixarray[i-1][count4]
                        matrixarray[i-1][count4] = 0
                    elif value==0:
                        count3+=1
                    else:
                      pass
                    if count3==10:

                        print(matrixarray)
                        return

    clearcount=0
    line=-1

    for row in matrixarray:
        line+=1
        count2 = 0
        for value in row:
            if value!=0:
                count2+=1
            else:
                break
        if count2==10:
            clearcount+=1 #to check how many overall line clears methinks
            for i in range(0,10):
                for piece in locked_piece_objs:
                    if piece.num==matrixarray[line][i]:
                        piece.hold(screen)
                matrixarray[line][i] = 0
            repair(line,matrixarray)

    allClear=True
    for row in matrixarray:
        for value in row:
            if value!=0:
                allClear=False

    if clearcount==1 and allClear==True:
        allClearSound.play()
        add2score=800*level#score is 800pts * level for perfect single clear
        b2b=False
        combo=True
        ticks = pygame.time.get_ticks()
        text2display[ticks] = "single_a"
    elif clearcount==1:
        linesSound.play()
        add2score=100*level#score is 100pts * level for single clear
        b2b=False
        combo=True
        ticks = pygame.time.get_ticks()
        text2display[ticks] = "single"
    elif clearcount==2 and allClear==True:
        allClearSound.play()
        add2score=1200*level#score is 120000pts * level for perfect double clear
        b2b=False
        combo=True
        ticks = pygame.time.get_ticks()
        text2display[ticks] = "double_a"
    elif clearcount==2:
        linesSound.play()
        add2score=200*level#score is 200pts * level for double clear
        b2b=False
        combo=True
        ticks = pygame.time.get_ticks()
        text2display[ticks] = "double"
    elif clearcount==3 and allClear==True:
        allClearSound.play()
        add2score=1800*level#score is 500pts * level for perfect triple clear
        b2b=False
        combo=True
        ticks = pygame.time.get_ticks()
        text2display[ticks] = "triple_a"
    elif clearcount==3:
        linesSound.play()
        add2score=500*level#score is 500pts * level for triple clear
        b2b=False
        combo=True
        ticks = pygame.time.get_ticks()
        text2display[ticks] = "triple"
    elif clearcount==4 and b2b==True and allClear==True:
        allClearSound.play()
        add2score=(3200*level)#back to back tetris scores extra points
        combo=True
        ticks = pygame.time.get_ticks()
        text2display[ticks] = "tetris_ab"
    elif clearcount==4 and allClear==True:
        allClearSound.play()
        add2score=2000*level
        b2b=True
        combo=True
        ticks = pygame.time.get_ticks()
        text2display[ticks] = "tetris_a"
    elif clearcount==4 and b2b==True:
        linesSound.play()
        add2score=round((800*level)*1.5)#back to back tetris scores extra points
        combo=True
        ticks = pygame.time.get_ticks()
        text2display[ticks] = "tetris_b"
    elif clearcount==4:
        linesSound.play()
        add2score=800*level
        print("meow")
        print(add2score)
        b2b=True
        combo=True
        ticks = pygame.time.get_ticks()
        text2display[ticks] = "tetris"
    elif clearcount==0:
        add2score=0
        b2b=False
        combo=False

    score+=add2score

    totalclearcount+=clearcount
    if totalclearcount!=0:
        greencover = pygame.image.load('greencover.png').convert()
        screen.blit(greencover,(624,391))
        linedisplay = font.render(str(totalclearcount), False, white)
        if totalclearcount<10:
            screen.blit(linedisplay,(668,391))
        elif totalclearcount>9 and totalclearcount<100:
            screen.blit(linedisplay,(658,391))
        elif totalclearcount>99 and totalclearcount<1000:
            screen.blit(linedisplay,(645,391))
        elif totalclearcount>999 and totalclearcount<10000:
            screen.blit(linedisplay,(636,391))

    return score,matrixarray,totalclearcount,level,b2b,text2display

def steal(screen,matrixarray,locked_piece_objs,vols):
    '''
    function for paws to move and grab piece from matrix
    to create difficulty for player as a debuff
    '''

    pl = pygame.image.load('paw_left.png').convert_alpha()#load paw images
    pr = pygame.image.load('paw_right.png').convert_alpha()
    surface1 = pygame.Surface((107,56))#create 2 new surfaces for paws
    surface1 = surface1.convert_alpha()
    surface2 = pygame.Surface((107,56))
    surface2 = surface2.convert_alpha()
    surface1.fill((0,0,0,0))#create transpaency
    surface2.fill((0,0,0,0))
    onerect = pl.get_rect(topleft=(222,261))#get rect to alter coordinates for paws to move
    tworect = pr.get_rect(topleft=(470,261))

    surface3 = pygame.Surface((400,600))#create 2 more surfaces to create illusion of paws moving
    surface4 = pygame.Surface((400,600))

    pygame.image.save(screen,"surface1_bg.png")#save background to use on surface

    def movePaw(yDisp,xDisp,xDisp_2,surface,block,rect,check,surface3,surface4,finished):
        '''
        function within steal function to use in program
        to move move paw and cover up previous instance
        '''
        if check:#if moving left paw
            p = pygame.image.load('paw_left.png').convert_alpha()
        else:#if moving right paw
            p = pygame.image.load('paw_right.png').convert_alpha()

        if yDisp!=0 and yDisp!=1000:#checking if yDisp has not changed to 0
            if check:#if moving left paw
                surface4.blit(pygame.image.load('surface1_bg.png').convert(),(0,0))
                screen.blit(surface4,(0,0))#^^load background to display to cover previous paw
            else:#if moving right paw
                surface3.blit(pygame.image.load('surface1_bg.png').convert(),(0,0),(400,0,400,600))#width height https://stackoverflow.com/questions/6239769/how-can-i-crop-an-image-with-pygame
                screen.blit(surface3,(400,0))#^^load CROPPED background to right side of screen
            pygame.display.flip()#display
            surface.blit(p,(0,0))#blit paw image to surface
            if yDisp>0:
                rect.move_ip(0,10)#move surface rect 10 px up
                yDisp-=1
            else:
                rect.move_ip(0,-10)#move surface rect 10 px down
                yDisp+=1
            screen.blit(surface,rect)#blit paw at new rect pos
            pygame.display.flip()#flip
            time.sleep(0.05)#delay
            return(yDisp, xDisp, xDisp_2,False)

        elif xDisp_2!=xDisp and yDisp!=1000:
            if check:#if moving left paw
                surface4.blit(pygame.image.load('surface1_bg.png').convert(),(0,0))
                screen.blit(surface4,(0,0))#^^load background to display to cover previous paw
            else:#if moving right paw
                surface3.blit(pygame.image.load('surface1_bg.png').convert(),(0,0),(400,0,400,600))
                screen.blit(surface3,(400,0))#^^load CROPPED background to right side of screen
            pygame.display.flip()#display
            surface.blit(p,(0,0))#blit paw image to surface
            if check:#if left paw must be moving right
                rect.move_ip(10,0)#move surface rect 10 px right
            else:#if right paw must be moving left
                rect.move_ip(-10,0)#move surface rect 10 px left
            screen.blit(surface,rect)#blit paw at new rect pos
            pygame.display.flip()#flip
            time.sleep(0.05)#delay
            xDisp_2-=1
            return(yDisp, xDisp, xDisp_2,False)
        elif xDisp_2==xDisp and yDisp!=1000:
            yDisp=1000
            return(yDisp, xDisp, xDisp_2,False)
        elif (xDisp!=0) and yDisp==1000:
            if check:#if moving left paw
                surface4.blit(pygame.image.load('surface2_bg.png').convert(),(0,0))
                screen.blit(surface4,(0,0))#^^load background to display to cover previous paw
            else:#if moving right paw
                surface3.blit(pygame.image.load('surface2_bg.png').convert(),(0,0),(400,0,400,600))
                screen.blit(surface3,(400,0))#^^load CROPPED background to right side of screen
            pygame.display.flip()#display
            surface.blit(p,(0,0))#blit paw image to surface
            if check:#if left paw must be moving left
                rect.move_ip(-10,0)#move surface rect 10 px left
            else:#if right paw must be moving right
                rect.move_ip(10,0)#move surface rect 10 px right
            screen.blit(surface,rect)#blit paw at new rect pos
            pygame.display.flip()#flip
            time.sleep(0.1)#delay
            xDisp-=1
            return(yDisp, xDisp, xDisp_2,False)
        elif xDisp==0:
            return(yDisp, xDisp, xDisp_2,True)

    ticksForBlocks=pygame.time.get_ticks()

    block1 = random.randint(0,len(locked_piece_objs)-1)#block index to be removed
    counter=0
    for piece in locked_piece_objs:#small loop to find block actual object
        if counter==block1:
            block1=piece#if counter==block index then it is correct block
            block1y = 121+(block1.pInArray[0])*20
            block1x = 300+(block1.pInArray[1])*20
            break
        else:
            counter+=1
    while block1x>=380:#if block on right side of matrix
        ticksForBlocks2=pygame.time.get_ticks()
        block1 = random.randint(0,len(locked_piece_objs)-1)#find new one
        counter=0
        for piece in locked_piece_objs:
            if counter==block1:
                block1=piece
                block1y = 121+(block1.pInArray[0])*20
                block1x = 300+(block1.pInArray[1])*20
                break
            else:
                counter+=1
        if ticksForBlocks2-ticksForBlocks>500:
            block1x=-1
    ticksForBlocks=pygame.time.get_ticks()
    block2 = random.randint(0,len(locked_piece_objs)-1)#same process but for a block on right side
    counter=0
    for piece in locked_piece_objs:
        if counter==block2:
            block2=piece
            block2y = 121+(block2.pInArray[0])*20
            block2x = 300+(block2.pInArray[1])*20
            break
        else:
            counter+=1
    while block2x<=400:#if block on left side of matrix
        ticksForBlocks2=pygame.time.get_ticks()
        block2 = random.randint(0,len(locked_piece_objs)-1)
        counter=0
        for piece in locked_piece_objs:
            if counter==block2:
                block2=piece
                block2y = 121+(block2.pInArray[0])*20
                block2x = 300+(block2.pInArray[1])*20
                break
            else:
                counter+=1
        if ticksForBlocks2-ticksForBlocks>500:
            block2x=504

    yDisp1 = (block1y-281)//10#if +ve moves up
    yDisp2 = (block2y-281)//10#if -ve moves down
    xDisp1 = (block1x-300)//10
    xDisp2 = (block2x-490)//10#these values probably the problem
    if block1x==-1:
        xDisp1=0
        yDisp1=0
    else:
        block1.hold(screen)
    if block2x==504:
        xDisp2=0
        yDisp2=0
    else:
        block2.hold(screen)

    print(block1.num)
    print(block2.num)
    for i in range(0,19):
      for j in range(0,9):
        if matrixarray[i][j]==(block1.num) and block1x!=-1:
            matrixarray[i][j]=0
        if matrixarray[i][j]==(block2.num) and block2x!=504:
            matrixarray[i][j]=0
    print(matrixarray)
    pygame.image.save(screen,"surface2_bg.png")#save background to use on surface
    screen.blit(pygame.image.load('surface1_bg.png').convert(),(0,0))
    pygame.display.flip()

    time.sleep(0.1)

    surface1.blit(pl,(0,0))#blit paws on surface at rect pos
    surface2.blit(pr,(0,0))
    screen.blit(surface1,onerect)#blit to screen
    screen.blit(surface2,tworect)
    pygame.display.flip()#display

    pygame.event.clear(eventtype=[pygame.KEYDOWN,pygame.KEYUP,pygame.MOUSEBUTTONUP,pygame.MOUSEBUTTONDOWN])#clear events

    finished1=False
    finished2=False

    xDisp1 = abs(xDisp1)
    xDisp2 = abs(xDisp2)

    xDisp1_2 = xDisp1*2
    xDisp2_2 = xDisp2*2
    checkticks=pygame.time.get_ticks()
    checktick2 =pygame.time.get_ticks()

    while (finished1==False or finished2==False) and (checktick2-checkticks<9000):
        yDisp1, xDisp1, xDisp1_2,finished1 = movePaw(yDisp1,xDisp1,xDisp1_2,surface1,block1,onerect,True,surface3,surface4,finished1)
        yDisp2, xDisp2, xDisp2_2,finished2 = movePaw(yDisp2,xDisp2,xDisp2_2,surface2,block2,tworect,False,surface3,surface4,finished2)
        checktick2 =pygame.time.get_ticks()

    surface4.blit(pygame.image.load('surface2_bg.png').convert(),(0,0))
    screen.blit(surface4,(0,0))#^^load background to display to cover previous paw
    surface3.blit(pygame.image.load('surface2_bg.png').convert(),(0,0),(400,0,400,600))
    screen.blit(surface3,(400,0))#^^load CROPPED background to right side of screen
    pygame.display.flip()#display

    x = "hey"
    pygame.event.clear(eventtype=[pygame.KEYDOWN,pygame.KEYUP,pygame.MOUSEBUTTONUP,pygame.MOUSEBUTTONDOWN])
    return x

    true=True
    while true:
        for event in pygame.event.get():
            if event.type== pygame.MOUSEBUTTONUP and (39 < event.pos[0] < 107 and 452 < event.pos[1] < 520):
                pygame.image.save(screen,"current_gameplay.png")
                x,vols = settings(2,controls,controlsfunc,num,piece_objs,locked_piece_objs,earray,marray,harray,vols)
                screen.blit(pygame.image.load('current_gameplay.png').convert(),(0,0))
                pygame.display.flip()
            if event.type == pygame.QUIT:
                true = False
    pygame.quit()

def gameplay(gamemode,num,piece_objs,locked_piece_objs,earray,marray,harray,vols):
    '''
    function controlling gameplay. includes control of time, checking of pieces, and end conditions
    '''
    gp = pygame.image.load('gameplay12.png').convert()
    gp1 = pygame.image.load('1_gameplay.png').convert()
    gp2 = pygame.image.load('2_gameplay.png').convert()
    gp3 = pygame.image.load('3_gameplay.png').convert()

    meowSound.set_volume(vols[1]/5)
    meowSound1.set_volume(vols[1]/5)
    openMenu.set_volume(vols[1]/5)
    pieceMove.set_volume(vols[1]/5)
    pieceNoMove.set_volume(vols[1]/5)
    rotateSound.set_volume(vols[1]/5)
    levelUpSound.set_volume(vols[1]/5)
    hurrySound.set_volume(vols[1]/5)
    noRotateSound.set_volume(vols[1]/5)
    hardDropSound.set_volume(vols[1]/5)

    screen.blit(gp3,(0,0))
    pygame.display.flip()
    time.sleep(1)
    screen.blit(gp2,(0,0))
    pygame.display.flip()
    time.sleep(1)
    screen.blit(gp1,(0,0))
    pygame.display.flip()
    time.sleep(1)
    screen.blit(gp, (0, 0))
    pygame.display.flip()
    pygame.event.clear(eventtype=[pygame.KEYDOWN,pygame.KEYUP,pygame.MOUSEBUTTONUP,pygame.MOUSEBUTTONDOWN])

    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
    pygame.mixer.music.load('sounds/gameplay_music.mp3')
    pygame.mixer.music.set_volume(vols[0]/5)
    pygame.mixer.music.play(-1,0,0)

    #596,200

    ps = []
    psq2 = []
    held = []
    canHold = True
    nextPiece = []

    #displaying text
    text2display = {}
    ac = pygame.image.load('all clear.png').convert()
    d = pygame.image.load('double.png').convert()
    t = pygame.image.load('triple.png').convert()
    te = pygame.image.load('tetris.png').convert()
    s = pygame.image.load('single.png').convert()
    wc1 = pygame.image.load('word_cover1.png').convert()
    wc2 = pygame.image.load('word_cover2.png').convert()
    b2bt = pygame.image.load('b2b.png').convert()
    wordlist=[]

    check2001=0

    b2b=False

    clock = pygame.time.Clock()

    white = (248,248,248)
    font = pygame.font.SysFont("lucidaconsole", 30)#load font

    if gamemode=="easy":
        level=1
        increment = 15
        timing=20
        levelfont = font.render(str(level), False, white)
        screen.blit(levelfont,(668,293))
    elif gamemode=="medium":
        level=5
        increment = 5
        timing=10
        levelfont = font.render(str(level), False, white)
        screen.blit(levelfont,(668,293))
    elif gamemode=="hard":
        level=10
        increment = 3
        timing=6
        levelfont = font.render(str(level), False, white)
        screen.blit(levelfont,(658,293))

    pnumber = 0
    score = 0
    num=1

    #debuffs
    noRotate = False
    speedUp = False
    debuffCheck=True

    nr = pygame.image.load('no_rotate-1.png.png').convert()
    fm = pygame.image.load('fast_moving-2.png.png').convert()
    sp = pygame.image.load('steal_piece-3.png.png').convert()
    og = pygame.image.load('blank_debuff-3.png.png').convert()
    qm = pygame.image.load('questionmark-3.png.png').convert()

    true1 = True
    check = True
    check1998=False
    check1999 = False
    check2000 = False

    ps, check, psq2, nextPiece,num,piece_objs = sevenBag(ps, check, psq2,num,piece_objs)

    display(psq2[0],"next")

    matrixarray = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]] #19
    frameCounter = 0
    totalclearcount = 0

    font2 = pygame.font.SysFont("lucidaconsole", 35)#load font
    linedisplay = font2.render(str(totalclearcount), False, white)
    screen.blit(linedisplay,(668,391))

    debuffCounter=0

    hasRotated=False
    firstcheck=False
    while true1:
        counter1=0
        counter2=0
        counter3=0
        for event in pygame.event.get():
            if event.type== pygame.MOUSEBUTTONUP and (39 < event.pos[0] < 107 and 452 < event.pos[1] < 520):
                pygame.image.save(screen,"current_gameplay.png")
                pygame.mixer.music.pause()
                openMenu.play()
                x,vols = settings(2,controls,controlsfunc,num,piece_objs,locked_piece_objs,earray,marray,harray,vols)
                meowSound.set_volume(vols[1]/5)
                meowSound1.set_volume(vols[1]/5)
                pieceMove.set_volume(vols[1]/5)
                pieceNoMove.set_volume(vols[1]/5)
                rotateSound.set_volume(vols[1]/5)
                levelUpSound.set_volume(vols[1]/5)
                hurrySound.set_volume(vols[1]/5)
                noRotateSound.set_volume(vols[1]/5)
                hardDropSound.set_volume(vols[1]/5)
                pygame.mixer.music.unpause()
                screen.blit(pygame.image.load('current_gameplay.png').convert(),(0,0))
                pygame.display.flip()
            if event.type == pygame.QUIT:
                true1 = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.image.save(screen,"current_gameplay.png")
                    pygame.mixer.music.pause()
                    openMenu.play()
                    x, vols = settings(2,controls,controlsfunc,num,piece_objs,locked_piece_objs,earray,marray,harray,vols)
                    meowSound.set_volume(vols[1]/5)
                    meowSound1.set_volume(vols[1]/5)
                    pieceMove.set_volume(vols[1]/5)
                    pieceNoMove.set_volume(vols[1]/5)
                    rotateSound.set_volume(vols[1]/5)
                    levelUpSound.set_volume(vols[1]/5)
                    hurrySound.set_volume(vols[1]/5)
                    noRotateSound.set_volume(vols[1]/5)
                    hardDropSound.set_volume(vols[1]/5)
                    pygame.mixer.music.unpause()
                    screen.blit(pygame.image.load('current_gameplay.png').convert(),(0,0))
                    pygame.display.flip()
                counter1=0
                counter2=0
                counter3=0
                if event.key == pygame.key.key_code(controls[4]):#if soft drop
                    check1998=True
                    for piece in piece_objs:#for objects in matrix
                        if piece.bottomPiece==True:
                            if piece.locked==False:#if piece falling
                                counter1+=1
                                canMove = piece.movement(matrixarray, 0, screen)#move once down
                                if canMove==True:
                                    counter2+=1
                            if piece.locked==True:
                                counter3+=1
                    if counter3!=0:
                        for piece in piece_objs:
                            piece.lock()
                    if counter1==counter2:#selection checking variable value
                        score+=1
                        pieceMove.play()
                        for piece in piece_objs:#for objects in matrix
                            if piece.locked==False:#if piece falling
                                piece.movement1(matrixarray, 0, screen,False)
                        pygame.display.flip()#flip screen for all blocks to move together
                    pygame.display.flip()
                counter1=0
                counter2=0
                counter3=0
                if event.key == pygame.key.key_code(controls[1]):#if moving left
                    check1999=True
                    for piece in piece_objs:#for objects in matrix
                        if piece.leftPiece==True:
                            if piece.locked==False:#if piece falling
                                counter1+=1
                                canMove = piece.movement(matrixarray, 1, screen)#move once to left
                                if canMove==True:
                                    counter2+=1
                    if counter1==counter2:#selection checking variable value
                        for piece in piece_objs:#for objects in matrix
                            if piece.locked==False:#if piece falling
                                counter3+=1#counter to make sure all pieces are unlocked
                        if counter3==len(piece_objs):#if all are unlocked
                            pieceMove.play()
                            for piece in piece_objs:
                                piece.movement1(matrixarray, 1, screen,False)#move piece to left
                    else:
                        pieceNoMove.play()
                        pygame.display.flip()#flip screen for all blocks to move together
                    pygame.display.flip()
                counter1=0
                counter2=0
                counter3=0
                if event.key == pygame.key.key_code(controls[0]):#if moving right
                    check2000=True
                    pygame.event.clear(eventtype=[pygame.KEYDOWN,pygame.KEYUP])
                    for piece in piece_objs:#for objects in matrix
                        if piece.rightPiece==True:#if piece is on the right
                            if piece.locked==False:#if piece falling
                                counter1+=1
                                canMove = piece.movement(matrixarray, 2, screen)#check if can move right
                                if canMove==True:
                                    counter2+=1
                    if counter1==counter2:#selection checking variable value
                        for piece in piece_objs:#for objects in matrix
                            if piece.locked==False:#if piece falling
                                counter3+=1#counter to make sure all pieces are unlocked
                        if counter3==len(piece_objs):#if all are unlocked
                            pieceMove.play()
                            for piece in piece_objs:
                                piece.movement1(matrixarray, 2, screen,False)#move piece to right
                    else:
                        pieceNoMove.play()
                        pygame.display.flip()#flip screen for all blocks to move together
                    pygame.display.flip()
                if event.key == pygame.key.key_code(controls[5]):#if hard drop
                    #code of the piece being dropped to the bottom
                    matrixrow = []
                    for piece in piece_objs:
                        if piece.bottomPiece==True:
                            matrixrow.append([piece.hardDrop(matrixarray,screen),piece.place])
                    if(([matrixrow[0][0]]*len(matrixrow)) == matrixrow):#check if all the rows are the same
                        if piece.name=="S":
                            smallest=matrixrow[1]
                        else:
                            smallest=matrixrow[0]
                    else:
                        smallest = [20,0]
                        for i in matrixrow:#small loop to check for the smallest value
                            print(i[0])
                            print(matrixrow)
                            if i[0]<=smallest[0]:
                                smallest = i
                                print(str(smallest)+" this is the smallest")
                        if (piece.name=="S" or piece.name=="Z") and (piece.rstate==0):
                            if 19 in matrixrow:
                                smallest = [19,3]
                            if matrixrow[0][0]==matrixrow[1][0]-1 and matrixrow[0][0]==matrixrow[2][0]-1:
                                smallest = matrixrow[1]
                        if (piece.name=="Z" and piece.rstate==3):
                            for i in matrixrow:
                                if i[0]==19:
                                    smallest = [19,1]
                        checkvar = 0
                        counter=0
                        if (piece.name=="J" or piece.name=="L") and piece.rstate==2:
                            checkvar=matrixrow[0][0]
                            for i in matrixrow:
                                if i[0]!=checkvar:
                                    counter+=1
                            if counter==0:
                                smallest = [checkvar,1]
                            if matrixrow[0][0]==matrixrow[1][0] or matrixrow[0][0]==matrixrow[2][0]:
                                smallest = matrixrow[0]
                            if matrixrow[0][0]==matrixrow[1][0]+1 and matrixrow[0][0]==matrixrow[2][0]+1:
                                smallest = matrixrow[0]
                        if (piece.name=="S" or piece.name=="Z") and (piece.rstate==2):
                            if matrixrow[2][0]==matrixrow[1][0]-1 and matrixrow[2][0]==matrixrow[0][0]-1:
                                smallest = matrixrow[1]
                            for i in matrixrow:
                                if i[0]==19 and matrixrow[2][0]==19:
                                    smallest = [19,2]
                        checkvar = 0
                        counter=0
                        if (piece.name=="S" or piece.name=="Z") and (piece.rstate==1 or piece.rstate==3):
                            checkvar=matrixrow[0][0]
                            for i in matrixrow:
                                if i[0]!=checkvar:
                                    counter+=1
                            if counter==0 and checkvar==19:
                                if (piece.rstate==1 and piece.name=="S") or (piece.rstate==3 and piece.name=="Z"):
                                    smallest = [19,1]
                                else:
                                    smallest = [19,4]
                            elif counter==0:
                                if (piece.rstate==1 and piece.name=="S") or (piece.rstate==3 and piece.name=="Z"):
                                    smallest = matrixrow[0]
                                else:
                                    smallest = matrixrow[1]
                        if (piece.name=="T" and piece.rstate==2):
                            for i in matrixrow:
                                if i[0]==19:
                                    smallest = [19,1]
                        checkvar=0
                        if (piece.name=="J" and piece.rstate==1) or (piece.name=="L" and piece.rstate==3):
                            checkvar=matrixrow[0][0]-matrixrow[1][0]
                            if abs(checkvar)==1:
                                smallest = matrixrow[1]
                            if abs(checkvar)==2:
                                print(smallest)
                                if checkvar==-2:
                                    smallest = matrixrow[0]
                                else:
                                    smallest = matrixrow[1]

                        if piece.name=="I" and piece.rstate==1 or piece.rstate==3:
                            if matrixrow[0]==19:
                                if piece.rstate==1:
                                    smallest = [19,4]
                                else:
                                    smallest = [19,1]
                    counter4=0
                    for piece in piece_objs:
                        if piece.bottomPiece==True:#if a bottompiece
                            if smallest[0]==piece.pInArray[0]:#if its value where should be dropped
                                counter4+=1#add to counter
                    if counter4==0:#if counter added to, skip moving piece to bottom
                        hardDropSound.play()
                        score+=(smallest[0]-piece.pInArray[0])*2
                        debuffCounter+=1
                        for piece in piece_objs:
                            print(piece.name)
                            print(piece.rstate)
                            piece.movement1(matrixarray, smallest, screen,True)#move piece to this row
                            pygame.display.flip()
                    for piece in piece_objs:
                        if piece.locked==False:
                            piece.lock()#lock all pieces
                    for piece in piece_objs:#for each of these pieces
                        matrixarray = piece.save2matrix(matrixarray)#save new matrix array
                        locked_piece_objs.add(piece)
                    print(matrixarray)
                    piece_objs.empty()
                    score, matrixarray,totalclearcount,level,b2b,text2display = lineClears(score, matrixarray,locked_piece_objs,screen,totalclearcount,level,b2b,text2display)
                    print(matrixarray)
                    print(ps)
                    print(psq2)
                    ps, check, psq2, nextPiece,num,piece_objs = sevenBag(ps, check, psq2,num,piece_objs)
                    pygame.display.flip()
                    canHold=True#anytime piece reaches bottom make this true
                if event.key == pygame.key.key_code(controls[6]) and canHold==True:#if piece is held
                    for piece in piece_objs:
                        piece.hold(screen)
                    pygame.display.flip()
                    piece_objs.empty()#empty group
                    ps,psq2,held,nextPiece,num = hold(ps,psq2,held,nextPiece,num,piece_objs)#new piece
                    canHold=False
                if event.key == pygame.key.key_code(controls[2]) and noRotate==False:#if player rotating clockwise
                    pygame.event.clear(eventtype=[pygame.KEYDOWN,pygame.KEYUP])
                    for piece in piece_objs:#for each piece
                        if piece.rstate==3:#change rotation state, 'rstate' based on input
                            newrstate=0
                        else:
                            newrstate=piece.rstate+1
                    if piece.name!="O":#Os do not rotate
                        true=True#validation making sure rotation is valid
                        for piece in piece_objs:#for each piece
                            if true==True:
                                canRotate = piece.rotate(matrixarray,newrstate)#check if can rotate
                                if canRotate==True and piece.place==4:#if rotation can happen and has reached last piece
                                    rotateSound.play()
                                    for j in range(0,2):#for each piece in array
                                        for piece in piece_objs:
                                            piece.rotate1(screen,newrstate,j)#actually rotate the piece
                                        true=False#come out of second loop
                                    pygame.display.flip()
                                elif canRotate==False:#if any piece fails rotation test
                                    pieceNoMove.play()
                                    for piece in piece_objs:
                                        piece.newrstate = [0,0]#change all new rotation states back to 0
                                    true=False
                if event.key == pygame.key.key_code(controls[3]) and noRotate==False:#if player rotating anticlockwise
                    pygame.event.clear(eventtype=[pygame.KEYDOWN,pygame.KEYUP])
                    for piece in piece_objs:#for each piece
                        if piece.rstate==0:#change rotation state, 'rstate' based on input
                            newrstate=3
                        else:
                            newrstate=piece.rstate-1
                    if piece.name!="O":#Os do not rotate
                        true=True#validation making sure rotation is valid
                        for piece in piece_objs:#for each piece
                            if true==True:
                                canRotate = piece.rotate(matrixarray,newrstate)#check if can rotate
                                if canRotate==True and piece.place==4:#if rotation can happen and has reached last piece
                                    rotateSound.play()
                                    for j in range(0,2):#for each piece in array
                                        for piece in piece_objs:
                                            piece.rotate1(screen,newrstate,j)#actually rotate the piece
                                        true=False#come out of second loop
                                    pygame.display.flip()
                                elif canRotate==False:#if any piece fails rotation test
                                    pieceNoMove.play()
                                    for piece in piece_objs:
                                        piece.newrstate = [0,0]#change all new rotation states back to 0
                                    true=False
                if (event.key == pygame.key.key_code(controls[2]) or event.key == pygame.key.key_code(controls[3])) and noRotate==True:
                    pieceNoMove.play()

        if text2display!={}:
            displaytext = text2display[list(text2display)[0]]
            print(displaytext)
            if check2001==0:
                screen.blit(wc1,(596,200))
                screen.blit(wc2,(550,527))
                screen.blit(wc1,(363,25))
                pygame.display.flip()
                check2001=1
                if displaytext=="single":
                    screen.blit(s,(596,200))
                elif displaytext=="single_a":
                    screen.blit(s,(596,200))
                    screen.blit(ac,(550,527))
                elif displaytext=="double":
                    screen.blit(d,(596,200))
                elif displaytext=="double_a":
                    screen.blit(d,(596,200))
                    screen.blit(ac,(550,527))
                elif displaytext=="triple":
                    screen.blit(t,(596,200))
                elif displaytext=="triple_a":
                    screen.blit(t,(596,200))
                    screen.blit(ac,(550,527))
                elif displaytext=="tetris":
                    screen.blit(te,(596,200))
                elif displaytext=="tetris_a":
                    screen.blit(te,(596,200))
                    screen.blit(ac,(550,527))
                elif displaytext=="tetris_ab":
                    screen.blit(te,(596,200))
                    screen.blit(ac,(550,527))
                    screen.blit(b2bt,(363,25))
                elif displaytext=="tetris_b":
                    screen.blit(te,(596,200))
                    screen.blit(b2bt,(363,25))
                pygame.display.flip()
                wordlist.append(list(text2display)[0])
                text2display.pop(list(text2display)[0])
        if wordlist!=[]:
            ticks1 = pygame.time.get_ticks()
            if (ticks1-(wordlist[0]))>1500:
                if wordlist[0]=="single" or wordlist[0]=="double" or wordlist[0]=="triple" or wordlist[0]=="tetris":
                    screen.blit(wc1,(596,200))
                elif wordlist[0]=="single_a" or wordlist[0]=="double_a" or wordlist[0]=="triple_a" or wordlist[0]=="tetris_a":
                    screen.blit(wc1,(596,200))
                    screen.blit(wc2,(550,527))
                elif wordlist[0]=="tetris_ab":
                    screen.blit(wc1,(596,200))
                    screen.blit(wc1,(363,25))
                    screen.blit(wc2,(550,527))
                else:
                    screen.blit(wc1,(596,200))
                    screen.blit(wc1,(363,25))

                wordlist.pop(0)
                check2001=0
                pygame.display.flip()

        keys = pygame.key.get_pressed()#which keys pressed

        counter1=0
        counter2=0
        counter4=0

        for piece in piece_objs:#for objects in matrix
            if piece.bottomPiece==True:
                if piece.locked==False:#if piece falling
                    counter1+=1
                    canMove = piece.movement(matrixarray, 0, screen)#check if can move once down
                    if canMove==True:
                        counter2+=1#if piece can move

        if keys[pygame.key.key_code(controls[4])]:
            if piece.locked==False and counter1==counter2 and check1998==False:#if piece falling
                pieceMove.play()
                for piece in piece_objs:#for objects in matrix
                    piece.movement1(matrixarray, 0, screen,False)#move once down
        time.sleep(0.1)
        pygame.display.flip()

        counter1=0
        counter2=0
        counter3=0
        counter4=0
        if keys[pygame.key.key_code(controls[1])]:#if moving left
            for piece in piece_objs:#for objects in matrix
                if piece.leftPiece==True:
                    if piece.locked==False:#if piece falling
                        counter1+=1
                        canMove = piece.movement(matrixarray, 1, screen)#move once to left
                        if canMove==True:
                            counter2+=1
            if counter1==counter2 and check1999==False:#selection checking variable value
                for piece in piece_objs:#for objects in matrix
                    if piece.locked==False:#if piece falling
                        counter3+=1#counter to make sure all pieces are unlocked

        for piece in piece_objs:#for objects in matrix
            if piece.locked==False and counter3==len(piece_objs):#if piece falling
                piece.movement1(matrixarray, 1, screen,False)#move once down
        time.sleep(0.025)
        pygame.display.flip()

        counter1=0
        counter2=0
        counter3=0
        counter4=0

        if keys[pygame.key.key_code(controls[0])]:#if moving right
            for piece in piece_objs:#for objects in matrix
                if piece.rightPiece==True:
                    if piece.locked==False:#if piece falling
                        counter1+=1
                        canMove = piece.movement(matrixarray, 2, screen)#move once to left
                        if canMove==True:
                            counter2+=1
            if counter1==counter2 and check2000==False:#selection checking variable value
                for piece in piece_objs:#for objects in matrix
                    if piece.locked==False:#if piece falling
                        counter3+=1#counter to make sure all pieces are unlocked

        if piece.locked==False and counter3==len(piece_objs):#if piece falling
            pieceMove.play()
            for piece in piece_objs:#for objects in matrix
                piece.movement1(matrixarray, 2, screen,False)#move once down
        time.sleep(0.025)
        pygame.display.flip()

        counter1=0
        counter2=0
        counter3=0
        counter4=0

        for piece in piece_objs:
            isGameOver =piece.movement(matrixarray,-1,screen)
            if isGameOver:
                pygame.mixer.music.stop()
                pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
                pygame.mixer.music.load('sounds/top_out.mp3')
                pygame.mixer.music.set_volume(vols[0]/5)
                pygame.mixer.music.play(0)
                pygame.event.clear(eventtype=[pygame.KEYDOWN,pygame.KEYUP,pygame.MOUSEBUTTONUP,pygame.MOUSEBUTTONDOWN])
                piece_objs.empty()
                locked_piece_objs.empty()
                num=1
                tile = pygame.image.load('tile.png').convert()
                for i in range(0,20):
                    pygame.event.clear(eventtype=[pygame.KEYDOWN,pygame.KEYUP,pygame.MOUSEBUTTONUP,pygame.MOUSEBUTTONDOWN])
                    for j in range(0,10):
                        pygame.event.clear(eventtype=[pygame.KEYDOWN,pygame.KEYUP,pygame.MOUSEBUTTONUP,pygame.MOUSEBUTTONDOWN])
                        screen.blit(tile,((300+(j*20)),(121+(i*20))))
                    pygame.display.flip()
                    time.sleep(0.1)
                time.sleep(1)
                if gamemode=="easy":
                    score = 19888
                    gameOver(earray, score, gamemode,num,piece_objs,locked_piece_objs,earray,marray,harray,vols)
                elif gamemode=="medium":
                    gameOver(marray, score, gamemode,num,piece_objs,locked_piece_objs,earray,marray,harray,vols)
                elif gamemode=="hard":
                    gameOver(harray, score, gamemode,num,piece_objs,locked_piece_objs,earray,marray,harray,vols)
        for piece in piece_objs:#for objects in matrix
            if piece.bottomPiece==True:
                if piece.locked==False:#if piece falling
                    counter1+=1
                    canMove = piece.movement(matrixarray, 0, screen)#check if can move once down
                    if canMove==True:
                        counter2+=1#if piece can move
            if piece.locked==True:
                counter4+=1#if any piece locked

        if counter4!=0:#if one of any pieces are locked
            hardDropSound.play()
            for piece in piece_objs:
                if piece.locked==False:
                    piece.lock()#lock all pieces

        if totalclearcount>=increment*level:
            if timing==2 or timing==3:
                timing=1
            elif timing>2:
                timing-=2
            level+=1
            levelUpSound.play()
            greencover = pygame.image.load('greencover.png').convert()
            screen.blit(greencover,(624,290))
            levelfont = font.render(str(level), False, white)
            if level<10:
                screen.blit(levelfont,(668,293))
            elif level>9 and level<100:
                screen.blit(levelfont,(658,293))
            elif level>99 and level<1000:
                screen.blit(levelfont,(645,293))
            elif level>999 and level<10000:
                screen.blit(levelfont,(636,293))
            pygame.display.flip()
            increment+=2

        if frameCounter==timing and speedUp==False:
            if counter1==counter2:#selection checking variable value
                for piece in piece_objs:#for objects in matrix
                    if piece.locked==False:#if piece falling
                        piece.movement1(matrixarray, 0, screen,False)
                pygame.display.flip()#flip screen for all blocks to move together
                pieceMove.play()
            elif counter1!=counter2:
                for piece in piece_objs:#must check through list again
                    piece.update(matrixarray,screen)#update piece
            frameCounter = 0#reset counter to increment again
        elif speedUp==True:
            if counter1==counter2:#selection checking variable value
                for piece in piece_objs:#for objects in matrix
                    if piece.locked==False:#if piece falling
                        piece.movement1(matrixarray, 0, screen,False)
                pygame.display.flip()#flip screen for all blocks to move together
                pieceMove.play()
            elif counter1!=counter2:
                for piece in piece_objs:#must check through list again
                    piece.update(matrixarray,screen)#update piece
        elif speedUp==False:
            if frameCounter>=timing:
                frameCounter = 0
            frameCounter += 1#increment frame counter so movement can be reached
        counter=0
        for piece in piece_objs:#check list
            if piece.first==False and piece.locked==False:
                piece.update(matrixarray,screen)
            if piece.locked==True:
                counter+=1
        if counter==len(piece_objs):#if all pieces locked
            for piece in piece_objs:#for each of these pieces
                matrixarray = piece.save2matrix(matrixarray)#save new matrix array
                locked_piece_objs.add(piece)
            debuffCounter+=1
            print(matrixarray)
            piece_objs.empty()#empty group
            score, matrixarray,totalclearcount,level,b2b,text2display = lineClears(score, matrixarray,locked_piece_objs,screen,totalclearcount,level,b2b,text2display)
            print(matrixarray)
            print(ps)
            print(psq2)
            ps, check, psq2, nextPiece,num,piece_objs = sevenBag(ps, check, psq2,num,piece_objs)#get new piece
            canHold=True#pieces can be held again
        counter=0
        counter1=0
        counter2=0
        counter4=0

        greencover = pygame.image.load('greencover.png').convert()
        screen.blit(greencover,(624,464))
        scorefont = font.render(str(score), False, white)
        if score<10:
            screen.blit(scorefont,(668,467))
        elif score>9 and score<100:
            screen.blit(scorefont,(658,467))
        elif score>99 and score<1000:
            screen.blit(scorefont,(650,467))
        elif score>999 and score<10000:
            screen.blit(scorefont,(640,467))
        elif score>9999 and score<100000:
            screen.blit(scorefont,(631,467))
        elif score>99999 and score<1000000:
            screen.blit(scorefont,(623,467))

        if debuffCounter==7:
            screen.blit(qm,(40,243))
        if debuffCounter==10 and debuffCheck==True:
            debuffCheck=False
            if gamemode=="easy":
                choicerandom = random.randint(0,1)
                if choicerandom==0:
                    choicerandom="steal"
                else:
                    choicerandom="hurry"
            elif gamemode=="medium":
                choicerandom= random.randint(0,11)
                if choicerandom>-1 and choicerandom<5:
                    choicerandom="steal"
                elif choicerandom>4 and choicerandom<9:
                    choicerandom="hurry"
                else:
                    choicerandom="no rotate"
            else:
                choicerandom = random.randint(0,2)
                if choicerandom==0:
                    choicerandom="steal"
                elif choicerandom==1:
                    choicerandom="hurry"
                elif choicerandom==2:
                    choicerandom="no rotate"
            if choicerandom=="no rotate":
                screen.blit(nr,(40,243))
                noRotateSound.play()
                noRotate=True
            elif choicerandom=="steal":
                screen.blit(sp,(40,243))
                pygame.event.clear(eventtype=[pygame.KEYDOWN,pygame.KEYUP,pygame.MOUSEBUTTONUP,pygame.MOUSEBUTTONDOWN])
                meowSound1.play()
                x = steal(screen,matrixarray,locked_piece_objs,vols)
                meowSound.play()
                screen.blit(og,(40,243))
                speedUp=False
                noRotate=False
                debuffCheck=True
                debuffCounter=0
            elif choicerandom=="hurry":
                hurrySound.play()
                pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
                pygame.mixer.music.load('sounds/gameplay_spedUp.mp3')
                pygame.mixer.music.set_volume(vols[0]/5)
                pygame.mixer.music.play(-1,0,0)
                screen.blit(fm,(40,243))
                speedUp=True
        elif debuffCounter==20:
            if choicerandom=="hurry":
                pygame.mixer.music.stop()
                pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
                pygame.mixer.music.load('sounds/gameplay_music.mp3')
                pygame.mixer.music.set_volume(vols[0]/5)
                pygame.mixer.music.play(-1,0,0)
            screen.blit(og,(40,243))
            speedUp=False
            noRotate=False
            debuffCheck=True
            debuffCounter=0
        pygame.display.flip()

        check1998=False
        check1999 = False
        check2000 = False
        clock.tick(60)
    pygame.quit()

def gameScreen(num,piece_objs,locked_piece_objs,earray,marray,harray,vols):
    '''
    function controlling game screen features
    '''
    gs = pygame.image.load('game_screen4.png').convert()
    screen.blit(gs, (0, 0))
    pygame.display.flip()

    buttonSound.set_volume(vols[1]/5)
    closeMenu.set_volume(vols[1]/5)

    true1=True

    check=1
    check2=1
    check3=1
    check4=1
    check5=1
    check6=1
    check7=1
    check8=1

    gamemode=""

    while true1:
        for event in pygame.event.get():
            if (event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP) and (99 < event.pos[0] < 218 and 296 < event.pos[1] < 374):#if user hovering on button
                if check2==1 and gamemode=="easy":#button is selected
                    buttonSound.play()
                    ezbd = pygame.image.load('easy_border_down2.png').convert()
                    screen.blit(ezbd, (99, 296))
                    pygame.display.flip()#loads and displays pushed button img^^
                    check=1
                    check2=2
                elif check2==1:#button is not selected
                    buttonSound.play()
                    ezd = pygame.image.load('easy_down2.png').convert()
                    screen.blit(ezd, (99, 296))
                    pygame.display.flip()#loads and displays pushed button img^^
                    check=1
                    check2=2
                if event.type == pygame.MOUSEBUTTONUP and gamemode!="easy":#button is selected
                    gamemode="easy"
                    ezb = pygame.image.load('easy_border2.png').convert()
                    m = pygame.image.load('medium2.png').convert()
                    h = pygame.image.load('hard2.png').convert()#other buttons are flipped to be deselected
                    g = pygame.image.load('green1.png')
                    screen.blit(ezb, (99, 296))
                    screen.blit(m, (307, 297))
                    screen.blit(h, (563, 293))
                    screen.blit(g, (44, 392))
                    pygame.display.flip()#loads and displays original button img^
            else:
                if check==1 and gamemode=="easy":#button is selected
                    ezb = pygame.image.load('easy_border2.png').convert()
                    screen.blit(ezb, (99, 296))
                    pygame.display.flip()#loads and displays original button img^
                    check=2
                    check2=1
                elif check==1:#button is not selected
                    ez = pygame.image.load('easy2.png').convert()
                    screen.blit(ez, (99, 296))
                    pygame.display.flip()#loads and displays original button img^
                    check=2
                    check2=1
#################################
            if (event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP) and (307 < event.pos[0] < 493 and 297 < event.pos[1] < 375):#if user hovering on button
                if check4==1 and gamemode=="medium":#button is selected
                    buttonSound.play()
                    mbd = pygame.image.load('medium_border_down2.png').convert()
                    screen.blit(mbd, (307, 297))
                    pygame.display.flip()#loads and displays pushed button img^^
                    check3=1
                    check4=2
                elif check4==1:#button is not selected
                    buttonSound.play()
                    md = pygame.image.load('medium_down2.png').convert()
                    screen.blit(md, (307, 297))
                    pygame.display.flip()#loads and displays pushed button img^^
                    check3=1
                    check4=2
                if event.type == pygame.MOUSEBUTTONUP and gamemode!="medium":#button is selected
                    gamemode="medium"
                    mb = pygame.image.load('medium_border2.png').convert()
                    ez = pygame.image.load('easy2.png').convert()
                    h = pygame.image.load('hard2.png').convert()#other buttons are flipped to be deselected
                    g = pygame.image.load('green1.png')
                    screen.blit(ez, (99, 296))
                    screen.blit(mb, (307, 297))
                    screen.blit(h, (563, 293))
                    screen.blit(g, (44, 392))
                    pygame.display.flip()#loads and displays original button img^
            else:
                if check3==1 and gamemode=="medium":#button is selected
                    mb = pygame.image.load('medium_border2.png').convert()
                    screen.blit(mb, (307, 297))
                    pygame.display.flip()#loads and displays original button img^
                    check3=2
                    check4=1
                elif check3==1:#button is not selected
                    m = pygame.image.load('medium2.png').convert()
                    screen.blit(m, (307, 297))
                    pygame.display.flip()#loads and displays original button img^
                    check3=2
                    check4=1
#################################
            if (event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP) and (563 < event.pos[0] < 693 and 293 < event.pos[1] < 376):#if user hovering on button
                if check6==1 and gamemode=="hard":#button is selected
                    buttonSound.play()
                    hbd = pygame.image.load('hard_border_down2.png').convert()
                    screen.blit(hbd, (563, 293))
                    pygame.display.flip()#loads and displays pushed button img^^
                    check5=1
                    check6=2
                elif check6==1:#button is not selected
                    buttonSound.play()
                    hd = pygame.image.load('hard_down2.png').convert()
                    screen.blit(hd, (563, 293))
                    pygame.display.flip()#loads and displays pushed button img^^
                    check5=1
                    check6=2
                if event.type == pygame.MOUSEBUTTONUP and gamemode!="hard":#button is selected
                    gamemode="hard"
                    hb = pygame.image.load('hard_border2.png').convert()
                    m = pygame.image.load('medium2.png').convert()
                    ez = pygame.image.load('easy2.png').convert()#other buttons are flipped to be deselected
                    g = pygame.image.load('green1.png')
                    screen.blit(ez, (99, 296))
                    screen.blit(m, (307, 297))
                    screen.blit(hb, (563, 293))
                    screen.blit(g, (44, 392))
                    pygame.display.flip()#loads and displays original button img^
            else:
                if check5==1 and gamemode=="hard":#button is selected
                    hb = pygame.image.load('hard_border2.png').convert()
                    screen.blit(hb, (563, 293))
                    pygame.display.flip()#loads and displays original button img^
                    check5=2
                    check6=1
                elif check5==1:#button is not selected
                    h = pygame.image.load('hard2.png').convert()
                    screen.blit(h, (563, 293))
                    pygame.display.flip()#loads and displays original button img^
                    check5=2
                    check6=1
####################
            if (event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP) and (283 < event.pos[0] < 516 and 440 < event.pos[1] < 517):#if user hovering on button
                if check8==1:
                    buttonSound.play()
                    pd2 = pygame.image.load('play2_down.png').convert()
                    screen.blit(pd2, (283, 440))
                    pygame.display.flip()#loads and displays pushed button img^^
                    check7=1
                    check8=2
                if event.type == pygame.MOUSEBUTTONUP and gamemode=="":
                    pls = pygame.image.load('pls_select.png')
                    screen.blit(pls, (44, 392))
                    pygame.display.flip()
                elif event.type == pygame.MOUSEBUTTONUP:
                    pygame.mixer.music.fadeout(1500)
                    gameplay(gamemode,num,piece_objs,locked_piece_objs,earray,marray,harray,vols)
            else:
                if check7==1:
                    p2 = pygame.image.load('play2.png').convert()
                    screen.blit(p2, (283, 440))
                    pygame.display.flip()#loads and displays original button img^
                    check7=2
                    check8=1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    closeMenu.play()
                    main(num,piece_objs,locked_piece_objs,earray,marray,harray,vols)
            if event.type== pygame.MOUSEBUTTONUP and (688 < event.pos[0] < 753 and 29 < event.pos[1] < 93):
                closeMenu.play()
                main(num,piece_objs,locked_piece_objs,earray,marray,harray,vols)
            if event.type == pygame.QUIT:
                true1 = False
    pygame.quit()

def helpMenu():
    '''
    function controlling help menu features
    '''
    hm = pygame.image.load('help_menu_img.png').convert()
    screen.blit(hm, (0, 0))
    pygame.display.flip()

    true1=True
    while true1:
        for event in pygame.event.get():#check events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    closeMenu.play()
                    main(num,piece_objs,locked_piece_objs,earray,marray,harray,vols)
            if event.type== pygame.MOUSEBUTTONUP and (688 < event.pos[0] < 753 and 29 < event.pos[1] < 93):
                closeMenu.play()
                main(num,piece_objs,locked_piece_objs,earray,marray,harray,vols)
            if event.type == pygame.QUIT:#quits
                true1 = False
    closeMenu.play()
    pygame.quit()

def main(num,piece_objs,locked_piece_objs,earray,marray,harray,vols):
    '''
    function controlling main menu of game to load buttons and selection
    '''
    mm = pygame.image.load('Main_Menu7.png').convert()
    screen.blit(mm, (0, 0))
    pygame.display.flip()

    pygame.mixer.music.set_volume(vols[0]/5)
    buttonSound.set_volume(vols[1]/5)
    openMenu.set_volume(vols[1]/5)
    closeMenu.set_volume(vols[1]/5)

    true1 = True

    check=1#checks if original button has already been redisplayed
    check2=1#checks if pushed button has already been redisplayed
    check3=1
    check4=1
    check5=1
    check6=1
    check7=1
    check8=1
    check9=1
    check10=1
    while true1:
        for event in pygame.event.get():#check events
            if (event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP) and (284 < event.pos[0] < 518 and 173 < event.pos[1] < 250):#if user hovering on button
                if check2==1:
                    buttonSound.play()
                    pd = pygame.image.load('play_down.png').convert()
                    screen.blit(pd, (284, 173))
                    pygame.display.flip()#loads and displays pushed button img^^
                    check=1
                    check2=2
                if event.type == pygame.MOUSEBUTTONUP:
                    openMenu.play()
                    gameScreen(num,piece_objs,locked_piece_objs,earray,marray,harray,vols)#takes to game screen
            else:
                if check==1:
                    p = pygame.image.load('play.png').convert()
                    screen.blit(p, (284, 173))
                    pygame.display.flip()#loads and displays original button img^
                    check=2
                    check2=1
            if (event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP) and (192 < event.pos[0] < 608 and 257 < event.pos[1] < 330):#if user hovering on button
                if check4==1:
                    buttonSound.play()
                    lbd = pygame.image.load('leaderboards_down.png').convert()
                    screen.blit(lbd, (192, 257))
                    pygame.display.flip()#loads and displays pushed button img^^
                    check3=1
                    check4=2
                if event.type == pygame.MOUSEBUTTONUP:
                    openMenu.play()
                    displayLeaderboards(earray,marray,harray,num,piece_objs,locked_piece_objs,vols)#takes to leaderboards
            else:
                if check3==1:
                    lb = pygame.image.load('leaderboards.png').convert()
                    screen.blit(lb, (192, 257))
                    pygame.display.flip()#loads and displays original button img^
                    check3=2
                    check4=1
            if (event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP) and (192 < event.pos[0] < 608 and 337 < event.pos[1] < 410):#if user hovering on button
                if check6==1:
                    buttonSound.play()
                    sd = pygame.image.load('settings_down.png').convert()
                    screen.blit(sd, (192, 337))
                    pygame.display.flip()#loads and displays pushed button img^^
                    check5=1
                    check6=2
                if event.type==pygame.MOUSEBUTTONUP:
                    pygame.mixer.music.pause()
                    openMenu.play()
                    p = settings(1,controls,controlsfunc,num,piece_objs,locked_piece_objs,earray,marray,harray,vols)
                    pygame.mixer.music.unpause()
                    screen.blit(mm, (0, 0))
                    pygame.display.flip()
                    buttonSound.set_volume(vols[1]/5)
                    openMenu.set_volume(vols[1]/5)
            else:
                if check5==1:
                    s = pygame.image.load('settings1.png').convert()
                    screen.blit(s, (192, 337))
                    pygame.display.flip()#loads and displays original button img^
                    check5=2
                    check6=1
            if (event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP) and (192 < event.pos[0] < 608 and 417 < event.pos[1] < 490):#if user hovering on button
                if check8==1:
                    buttonSound.play()
                    hmd = pygame.image.load('help_menu_down.png').convert()
                    screen.blit(hmd, (192, 417))
                    pygame.display.flip()#loads and displays pushed button img^^
                    check7=1
                    check8=2
                if event.type==pygame.MOUSEBUTTONUP:
                    openMenu.play()
                    helpMenu()
            else:
                if check7==1:
                    hm = pygame.image.load('help_menu.png').convert()
                    screen.blit(hm, (192, 417))
                    pygame.display.flip()#loads and displays original button img^
                    check7=2
                    check8=1
            if (event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP) and (308 < event.pos[0] < 504 and 497 < event.pos[1] < 570):#if user hovering on button
                if check10==1:
                    buttonSound.play()
                    ed = pygame.image.load('exit_down.png').convert()
                    screen.blit(ed, (308, 497))
                    pygame.display.flip()#loads and displays pushed button img^^
                    check9=1
                    check10=2
            else:
                if check9==1:
                    e = pygame.image.load('exit.png').convert()
                    screen.blit(e, (308, 497))
                    pygame.display.flip()#loads and displays original button img^
                    check9=2
                    check10=1
            if event.type == pygame.QUIT or (event.type == pygame.MOUSEBUTTONUP and 308 < event.pos[0] < 505 and 497 < event.pos[1] < 564):#quits
                true1 = False
    closeMenu.play()
    pygame.quit()

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
pygame.mixer.music.load('sounds/main_menu_music.mp3')
pygame.mixer.music.set_volume(vols[0]/5)
pygame.mixer.music.play(-1,0,2500)

main(num,piece_objs,locked_piece_objs,earray,marray,harray,vols)
true = True

while true:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            true = False
pygame.quit()

