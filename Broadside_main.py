#===============================================
# Broadside - A Naval Battle Game vs. Computer
#===============================================
# 5/1/24, 4:50 PM

'''
to do:

_(works?) add timeout for red loss via infinite moves... if blue is winning, red can't delay forever, 20 moves?

keep track of max ai movelist index (largest so far: 56, 92, 127...) sorting blows out max #

add beginner 'easyMode' ??



Computer AI code... 

line 2209: moveScore()
line 2414: Computer_AI()

---> improve merchant protection late in the game, add blockers, cover mercs, etc.

add merc coverage, esp if ship < 5
cover entrance columns, esp if mines gone. c1, c5, c2-4 (mines),c8, c12, c9-11 (mines) 
col coverage can be in R2-R4, just don't leave a straight shot to R1
find a way to reshuffle merc coverage if needed, use idle ships
why killing time along R2? stop it!

checkMoveIntoT forbids it, but maybe should be a scoring thing instead?

#-----------------
rule change ideas:

attack land guns?
combat if ship before destination? alongside during move? or in they path by mistake?
raking from astern destroys the rudder (% chance? 33%?) can't turn?
0 sails = immobile, not dead, can fire one more time? at passing enemies?
wind? blowing into port, hard to sail out, only one space at a time?
boarding & capture?
destroy/capture flagship = all that fleet's ships lose one sail? (unless down to one)


_add scoring system for attacks & moves! (not just dumb first valid move) in process...

new flow: 
scoring: (see scores starting on line 2533)
find & prioritize targets first
then look for moves to attack them
target priority: based on row for now, +2 for only one mast (sink it!)
add target priority to move score for averall score (consolidation)
move score: check row 1, row 2, for merchant coverage or blocking moves!
place ships on each row to defend harbor
avoid moving into a T attack (subtract score?)
else rote list
check rote moves to avoid moving into a T attack

attacks:
check for Red at row 1 & attack, or else cover merchs
if red has one mast, can it be attacked? (killed)
if > 1 mast, are merch blocked from access? if no, block. If yes, attack red ship if possible
if red @ row 2, can destroy ships covering merchants! must attack or block!

moves:
_update flow to prioritize merchant protection!!
_add non-attack moves to list that protect merchants
_reduce score for entrance blocking, esp left side and esp later in the game!!

let R1C8 move to entrance? cover from R1C7?

no entrance blockers? or fewer of them?
check entrance blockers for moves later on, what are the squares?
covering empty rows should be more important? scoring?

# clog up entrances! esp col 9/10/11
# Move to block entry on row 6, col 2-4, 9-11
# use 2 mast ships to clog entrances
# use 3 mast ships to defend harbor
# use 1 mast ships to shield merchants
#? add code to prep defenses based on red moves outside harbor?
#? check for red fleet left side entrance strategy?

_improved code to cover merchant ships 2/11/23:
_add moves to cover the merchant ships: port squares: row 0, cols 4/6/8/10
move vertically to cover the merchs if possible
how to keep them covered and not move ships away? (fixed?)
don't move blue ships in squares: row 1, cols 4/6/8/10 (fixed?)

remove movecheck on line 3007? redundant?

test play_again code

_add check for moving into T attacks (fixed?)

_fix dumb moves: time killing across R1 (fixed?)

setup_AI_opponent()
randomize AI strategies:
1. passive - ships on each row to make T attacks?
2. aggressive - ?
3. trap? - ships on each row to make T attacks? other?
_randomize placement of cannons & mines
??change default ship deployment, mix it up? what is best? (updated, good for now...)

init_AI_RoteMoveList()
??    create new lists of initial moves for each strategy, also 3 sets of moves to mix things up randomly (?)
??    create another set of ai rote moves for 'laid back' defenseive strategy??


other stuff:

Rules:
add changes to the rules/instructions at the start of instr?
update rules to reflect paying vs computer, mines vs buoys, etc.
_prompt user for rules? type X when done?
_how to display rules? scans? page thru them?
add mouse buttons for rules prompts?

_remove import of time? (seems ok so far...)

_remove unneeded image files from images folder (done)

fix no algo move found, check time killing, back row, etc. (using scoring system seems to fix this)

Add code to prep defenses based on red moves outside harbor??

check various gui bugboos, glitching, freezing, etc. (reduced # of images loaded during refresh)

_add moves left/right in a row if nothing else to do ??
** but keep lanes from harbor entrances blocked! also all rows & mercs covered!

_look for T attacks on red fleet
_wait for red to enter harbor to attack

_add user plaecment/setup of red fleet... text instructions? userDeployment()

_clean up land image drawing code? (loaded with background and sidebars as one image)

fixed stuff:

_fix extra blue squares & clicks when no attack found, esp back row moves (done?)

_edit sounds in Audacity

_separate move checking from actual moving: don't move until checked

_clean up land image drawing code
_adjust sizes to cover gaps? check image sizes vs squares, s/b 100x100
_check order of draws, edges should be first to get covered, last is border ship images

_array of squares
_squaresArray = np.zeros(15,14)
_squaresArray[14,0] = square

#----------------------------------------------------------------------------------------
setup stuff:

class: piece (ship) (color, num_masts, moved, direction, type="man of war"("merchant"?))
array of class piece (ship) instances for each side
num of sails (life left) (0-4) 0 = dead, removed
location, direction (NSEW) (angles?) if 0 = N, 90 = W, 180 = S, 270 = E

RED FLEET
The RED fleet totals 10 ships with 25 Removable Masts
2 Ships of the Line -- 4 Masts Each - 1 Jib, 1 Fore, 1 Main and 1 Mizzen (man of war?)
3 Frigates          -- 3 masts Each - 1 Fore, 1 Main, and 1 Mizzen
3 Brigs             -- 2 Masts Each - Fore and 1 Mizzen
2 Cutters           -- 1 Mast Each  - 1 Cutter Mast

BLUE FLEET
The BLUE fleet totals 10 Ships with 20 Removable Masts
4 Frigates -- 3 Masts Each - 1 Fore, 1 Main, and 1 Mizzen
2 Brigs    -- 2 Masts Each - 1 Fore and 1 Mizzen
4 Cutters  -- 1 Mast Each  - 1 Cutter Mast

turn only in 90/180/270 degree increments
turn & move, fire if alongside enemy ship
if passing a land battery, may take a hit (50%)
if passing over a mine, may be a decoy or may sink ship (50%)

    # AI Blue fleet starting positions:
    # r c   Num
    # 1 2   11   # 3
    # 1 4   12   # 1 merc prot
    # 1 5   13   # 3
    # 1 6   14   # 1 merc prot
    # 1 7   15   # 1 merc prot
    # 1 8   16   # 2
    # 1 9   17   # 3 
    # 1 10  18   # 1 merc prot
    # 1 11  19   # 3
    # 1 12  20   # 2
    # merchant ships
    # 0 4   21
    # 0 6   22
    # 0 8   23
    # 0 10  24

#-----------------

'''

#from distutils.ccompiler import new_compiler
import pygame
import sys
import os
import numpy as np
#import time
import random

# must come before pygame.init():
os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

clock = pygame.time.Clock()
random.seed()  # uses system time as a seed
#random.randint(a, b)   #Return a random integer N such that a <= N <= b

pygame.font.init()

#---------------------------
# display setup #

screen = pygame.display.set_mode((0,0))   # full screen
display_width = 2560
display_height = 1440
#screen = pygame.display.set_mode((display_width,display_height))

# 14 rows * 15 columns

# left margin:  570 - 50 = 520 (500?)
# right margin: 1970 + 50 = 2020 (2040?)
# graphic border image size 500 x 720 (4 images) or 500 x 1440 (2 images)

# convert square to x/y: square x/y plus offset
# sq_x.append(i*100+526)   # left edge x value
# sq_y.append(j*100+19)    #  top edge y value

# ship offsets: x = 26, y = -1
# screen.blit(ship_red_4,    (i*100+1552,j*100+1220))   # 1570 - 18 = 1552, 1270 - 40 = 1230, 1270 - 55 = 1215
# screen.blit(ship_blue_4,   (i*100+852,120))           # 1570 - 18 = 1552, 1270 - 40 = 1230
# screen.blit(ship_merchant, (i*200+952,20))            # 1570 - 18 = 1552, 1270 - 40 = 1230

#---------------------------
# music #

pygame.mixer.init()
pygame.mixer.music.set_volume(0.05)  # 0.03-0.05

music = pygame.mixer.music.load("sounds/sea_waves_13sec.wav")
#music = pygame.mixer.music.load("sounds/sea_waves_266.wav")
#music = pygame.mixer.music.load("sounds/yoyoma_cello_suite1inG_prelude.mp3")

## To have our music play continuously we do the following directly after defining our variable music:
pygame.mixer.music.play(-1) # -1 will ensure the song keeps looping
#fadeout(time)  # ms

#---------------------------
# sounds #

#To play a sound we type:
#bulletSound.play()

click = pygame.mixer.Sound('./sounds/click.ogg')

alarmBellSound = pygame.mixer.Sound('./sounds/alarm-bell.wav')  # error sound
shipsBellSound = pygame.mixer.Sound('./sounds/ships_bell.wav')
twoBellsSound = pygame.mixer.Sound('./sounds/ship-bell-two-chimes.wav')  # acknowledge sound (ok)

explosion0 = pygame.mixer.Sound('./sounds/explosion_destroy0.ogg')
explosion1 = pygame.mixer.Sound('./sounds/explosion_big_2s.ogg')
explosion2 = pygame.mixer.Sound('./sounds/explosion_big_3s.mp3')

#---------------------------
# colors #

black     = (0,0,0)
gray      = (127,127,127)
white     = (255,255,255)
red       = (255,0,0)
green     = (0,255,0)
blue      = (0,0,255)
lightblue = (0,255,255)
yellow    = (255,255,0)
pink      = (255,0,255)
ocean     = (0,40,50)

#---------------------------
# load images into memory #

#img = pygame.image.load('bird.png')
#img.convert()    #The method convert() optimizes the image format and makes drawing faster

# The function rotozoom() allows to combine rotation and scaling
# Rotation is counter-clockwise: if 0 = N, 90 = W, 180 = S, 270 = E
#img = pygame.transform.rotozoom(img0, angle, scale)

# background sea image
#bgScreen_0 = pygame.image.load('images/ocean_1_1440.jpg')
#bgScreen_0.convert()

# background sea image with sidebar ships (for instructions only)
bgScreen_1 = pygame.image.load('images/background_combined_ships.jpg')
bgScreen_1.convert()

# background sea image with sidebar ships & most land images
bgScreen_2 = pygame.image.load('images/background_combined_ships_land2.jpg')
bgScreen_2.convert()

# screen captures of original rules:
instructions = [pygame.image.load('images/rules_orig_0.jpg'), pygame.image.load('images/rules_orig_1.jpg'), pygame.image.load('images/rules_orig_2.jpg'), pygame.image.load('images/rules_orig_3.jpg'), pygame.image.load('images/rules_orig_4.jpg')]

# mines & cannons
cannons_L = pygame.image.load('images/cannoni_piccoli_single_L.png')
#cannons_L = pygame.image.load('images/original_cannon_2bL.png')
cannons_L.convert()
cannons_R = pygame.image.load('images/cannoni_piccoli_single_R.png')
#cannons_R = pygame.image.load('images/original_cannon_2bR.png')
cannons_R.convert()

mines = pygame.image.load('images/mine_1_50.png')
mines.convert()


land_41 = pygame.image.load('images/coast11_400x100_t2.png')  # 4 x 1 transparent *
land_41.convert()

def drawLandMessage():
    if MsgFlag == 0:
        #print("dummy")
        screen.blit(pygame.transform.rotozoom(land_41,180, 1), (1026,1314))   # to cover gap # bottom center of screen
    elif MsgFlag == 1:
        if winner == -1:
            #textToDisplay40blueCam(MsgText,(1092),(1338))
            #textToDisplay40whiteCam(MsgText,(1090),(1336))
            textToDisplay40blueCam(MsgText,(1090),(1336))
            textToDisplay40whiteCam(MsgText,(1092),(1338))
        else:
            #textToDisplay40redCam(MsgText,(1102),(1338))
            #textToDisplay40whiteCam(MsgText,(1100),(1336))
            textToDisplay40redCam(MsgText,(1100),(1336))  # 1180, 1340
            textToDisplay40whiteCam(MsgText,(1102),(1338))
    elif MsgFlag == 2:
        textToDisplay40redCam("BROADSIDE",(1120),(1340))
        textToDisplay40whiteCam("BROADSIDE",(1122),(1342))


# load gamepiece ship images #
# merchant ships
ship_merchant = pygame.image.load('images/ship_merchant.png')
ship_merchant.convert()

# blue fleet
ship_blue_1 = pygame.image.load('images/ship_blue_1.png')
ship_blue_1.convert()
ship_blue_2 = pygame.image.load('images/ship_blue_2.png')
ship_blue_2.convert()
ship_blue_3 = pygame.image.load('images/ship_blue_3.png')
ship_blue_3.convert()
ship_blue_4 = pygame.image.load('images/ship_blue_4.png')
ship_blue_4.convert()

# red fleet
ship_red_1 = pygame.image.load('images/ship_red_1.png')
ship_red_1.convert()
ship_red_2 = pygame.image.load('images/ship_red_2.png')
ship_red_2.convert()
ship_red_3 = pygame.image.load('images/ship_red_3.png')
ship_red_3.convert()
ship_red_4 = pygame.image.load('images/ship_red_4.png')
ship_red_4.convert()

# draw using raw x/y coordinates, not row/col (debug only, not currently used)
def drawBoardPiecesXY():   
    #RH: what are x/y offsets for drawing the ships in a square?
    # place red fleet
    for i in range(5):
        print("i =",i)
        for j in range(2):
            screen.blit(ship_red_4, (i*100+1552,j*100+1220))   # 1570 - 18 = 1552, 1270 - 40 = 1230, 1270 - 55 = 1215
    # place blue fleet
    for i in range(10):
        print("i =",i)
        screen.blit(ship_blue_4, (i*100+852,120))   # 1570 - 18 = 1552, 1270 - 40 = 1230
    # place merchant fleet
    for i in range(4):
        print("i =",i)
        screen.blit(ship_merchant, (i*200+952,20))   # 1570 - 18 = 1552, 1270 - 40 = 1230

# function which rotates image around its center, and .blit to screen:
def blitRotateCenter(surf, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)
    surf.blit(rotated_image, new_rect.topleft)
    # example:     blitRotateCenter(screen, image, pos, angle)  # pos is a tuple

# text drawing functions

gmenuX1 = 2200   # 1440
gmenuY1 = 600    # 1440
gmenuYinc = 50
gmenuY1inc = 33  # 

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def text2dCtr30gray(text, x, y, color=gray):
    largeText = pygame.font.SysFont('arial',30)
    TextSurf, TextRect = text_objects(text, largeText, color)
    TextRect.center = ((display_width/2),y)
    screen.blit(TextSurf, TextRect)

def textToDisplay30gray(text, x, y):
    font = pygame.font.SysFont('arial', 30)
    text = font.render(text,1,gray)
    screen.blit(text,(x,y))

def textToDisplay40red(text, x, y):
    font = pygame.font.SysFont('arial', 40)
    text = font.render(text,1,red)
    screen.blit(text,(x,y))

def textToDisplay40redCam(text, x, y):
    font = pygame.font.SysFont('cambria', 40)
    text = font.render(text,1,red)
    screen.blit(text,(x,y))

def textToDisplay40blueCam(text, x, y):
    font = pygame.font.SysFont('cambria', 40)
    text = font.render(text,1,blue)
    screen.blit(text,(x,y))

def textToDisplay40whiteCam(text, x, y):
    font = pygame.font.SysFont('cambria', 40)
    text = font.render(text,1,white)
    screen.blit(text,(x,y))

def text2dispCenter50(text, x, y, color=white):
    largeText = pygame.font.SysFont('arial',50)
    TextSurf, TextRect = text_objects(text, largeText, color)
    #TextRect.topleft = (x,y)
    TextRect.center = ((display_width/2),y)
    screen.blit(TextSurf, TextRect)


# array of valid sea squares, blocked or land squares, the 4 port squares, etc.
# L = land
# P = port (merchant ships)
# M = mine/mine
# G = shore batteries
# R = sea in range of shore guns (red cross)
# B = sea in range of both shore guns (double red cross)
# S = sea

# 14 rows * 15 columns
# create 2D array for map squares
#squareNum = 210

terrain = np.zeros((14,15))

def initTerrain():
    print("initTerrain()")
    global terrain
    terrain = [
    #                                         1               1
    # 0   1   2   3   4   5   6   7   8   9   0   1   2   3   4
    ["L","L","L","L","P","L","P","L","P","L","P","L","L","L","L"], # 0 
    ["L","L","S","S","S","S","S","S","S","S","S","S","S","S","L"], # 1 
    ["S","S","S","S","S","S","S","S","S","S","S","S","S","S","L"], # 2 
    ["S","S","S","S","S","S","S","S","S","S","S","S","S","S","S"], # 3 
    ["S","S","S","S","S","S","S","S","S","S","S","S","S","S","S"], # 4 
    ["S","S","M","M","M","S","S","S","S","M","M","M","S","L","L"], # 5 
    ["L","S","S","S","S","S","L","L","S","S","S","S","S","L","L"], # 6 
    ["L","G","R","B","R","G","L","L","G","R","B","R","G","L","L"], # 7 
    ["L","L","S","S","S","S","S","S","S","S","S","S","S","S","S"], # 8 
    ["L","L","S","S","S","S","S","S","S","S","S","S","S","S","S"], # 9 
    ["L","L","L","S","S","S","S","S","S","S","S","S","S","S","S"], #10 
    ["L","L","L","S","S","S","S","S","S","S","S","S","S","S","S"], #11 
    ["L","L","L","L","L","L","L","L","L","L","S","S","S","S","S"], #12 
    ["L","L","L","L","L","L","L","L","L","L","S","S","S","S","S"]] #13 

# port squares: row 0, cols 4/6/8/10

# game screen drawing functions:

def drawTerrain():  # draw letter for each square type for debug, but keep '+' later
    #print("drawTerrain")
    #terrain = np.zeros((14,15))  # 14 rows * 15 columns
    for i in range(15):
        for j in range(14):
            if terrain[j][i] == "S":
                textToDisplay30gray("+",(i*100+570),(j*100+50))
            elif terrain[j][i] == "R":
                textToDisplay40red("+",(i*100+567),(j*100+44))
            elif terrain[j][i] == "B":
                textToDisplay40red("+",(i*100+561),(j*100+44))  # side by side +
                textToDisplay40red("+",(i*100+573),(j*100+44))  # side by side +
            #    textToDisplay40red("+",(i*100+567),(j*100+44))
            #    textToDisplay40red("o",(i*100+567),(j*100+44))
            elif terrain[j][i] == "M":
                screen.blit(mines, ((i*100+553),(j*100+48)))  # ( 751, 544))  # 50x50
            #else:
            #    textToDisplay30gray(terrain[j][i],(i*100+570),(j*100+50))  # other letters, debug only
            #    if terrain[j][i] == "L":
            #        pygame.draw.rect(screen, (0,127,0), (1026,720,100,100))   # dumb green box for land


#---------------------------
### gameplay variables ###

MsgFlag = 2   # controls console window at bottom
MsgText = "Error!"

boardSquareSize = 100
boardStartX = 526
boardStartY =  19

#userDeploymentDone = 0  # 1 = done, game starts
userDeploymentMode = 0    # 1 = in user arrangement mode, 0 = done

shipNum = 0
shipSelected = 0
sq_row = 0
sq_col = 0
new_sq_row = 0
new_sq_col = 0
pmr = 0             # plus/minus row
pmc = 0             # plus/minus col
direction = 0

moveRange = 0       # d_col or d_row
moveValid = 0       # 1 = valid move

easyMode     = 0    # 1 for easy mode, 0 for normal (tougher) mode
numPlayers   = 1    # 1 for human vs. computer, 2 for human vs. human
playerTurn   = 1    # 1 (human) or -1 ? 2 (computer) - computer is always player 2 (blue fleet) if single player mode
turnNum      = 0    # a play is one round, i.e. computer and human each taking a turn
turnTimeout  = 0    # if blue is winning, red can't delay forever, 20 moves? if red is down to 1 ship, start counting...

# if I ever support two human players...
#whoGoesFirst = 1   # red fleet always goes first  # 1 (player #1) or -1 (player #2) if I ever support two human players...
# can be changed at game start
#colorPlayer1 = red
#colorPlayer2 = blue

winner      = 0   # 1 (human) or -1 ? 2 (computer) - winning player

# stats: num victories by each player/computer
winsPlayer1 = 0   # human
winsPlayer2 = 0   # computer

delay = 200

leftRight = 1   # for random ai movement

# AI related variables:

AIroteMoveIndex     = 0   # used to fetch 'rote' moves from ai_moves list (until a better approach is developed)
AIroteMoveIndexSize = 0

AImoveScore     = 0   # used to find best move based on 'score' for various attributes (used?)

AImoveScoreListIndex     = 0
AImoveScoreListIndexSize = 0    # see AImoveScoreListSetup() for assignment value
AImoveScoreListIndexMax  = 0

numShipsBlue = 0
#mercCovered = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]  # 3 = empty, 2 = not a port, 1 = merc covered, 0 = merc uncovered!, -1 = red ship in front of merc


#---------------------------

sq_x = []  # column left edge x value
sq_y = []  # row top edge y value

def defineRowsColumns():
    print("define sq_x columns")
    for i in range(15):   # cols
        sq_x.append(i*100+526)   # left edge x value
        print("i =",i," sq_x[i] =",sq_x[i])
    print("define sq_y rows")
    for j in range(14):   # rows
        sq_y.append(j*100+19)   # top edge y value
        print("j =",j," sq_y[j] =",sq_y[j])

def drawSquares():    
    print("draw a yellow border around each square")   # debug only
    for i in range(15):
        for j in range(14):
            pygame.draw.polygon(screen, yellow, [(sq_x[i],sq_y[j]), (sq_x[i]+boardSquareSize,sq_y[j]), (sq_x[i]+boardSquareSize,sq_y[j]+boardSquareSize), (sq_x[i],sq_y[j]+boardSquareSize), (sq_x[i],sq_y[j])], width=1)


#---------------------------
# Classes & Arrays:

#########################################################
# Class boardSquare, and array class instances
# Used to draw/update screen, track position of units
# Row/Col, terrain, unit #, etc.

class boardSquare():
    #class square: terrainType(land/sea/port/mine/battery), shipNum, shoreBatt(0/1/2? or just 0/1?), mine(sink/pass = 1/0)

    def __init__(self, row_num, col_num, x, y, terrain, shipNum=0, shoreBatt=0, mine=0, size=boardSquareSize):
        self.row_num = row_num
        self.col_num = col_num
    #    self.num = num
        self.x = sq_x[col_num]
        self.y = sq_y[row_num]
        self.terrain = terrain
        self.shipNum = shipNum
        self.shoreBatt = shoreBatt
        self.mine = mine
        self.size = size

    # call this method to draw a red square border on the screen: boardSquaresArray[j][i].drawRed()
    def drawRed(self):
        #print("boardsquare.drawRed")
        pygame.draw.polygon(screen, red, [(self.x,self.y), (self.x+self.size,self.y), (self.x+self.size,self.y+self.size), (self.x,self.y+self.size), (self.x,self.y)], width=1)
        pygame.display.update()   # debug?

    # call this method to draw a blue square border on the screen: boardSquaresArray[j][i].drawBlue()
    def drawBlue(self):
        #print("boardsquare.drawBlue")
        pygame.draw.polygon(screen, blue, [(self.x,self.y), (self.x+self.size,self.y), (self.x+self.size,self.y+self.size), (self.x,self.y+self.size), (self.x,self.y)], width=2)
        pygame.display.update()   # debug?

    # Class boardsquare # pos is the mouse position or a tuple of (x,y) coordinates
    def isOver(self, pos):
        if pos[0] > (self.x) and pos[0] < (self.x+self.size):
            if pos[1] > (self.y) and pos[1] < (self.y+self.size):
            #    self.drawRed()  # call this method to draw a red square border
                #displayUnitStatus()    # if there's a ship in the square. Move to piece class display? or better here?
            #    pygame.display.update()   # debug?
                return True


#########################################################
# create 2D array of class boardsquare for map squares
# 14 rows * 15 columns

# terrain = np.zeros((14,15))  # rows,cols
#squaresArray = np.zeros(15,14)  # ??

# create a 2D nested list for map squares: rows[cols] aka [[cols]rows]
boardSquaresArray = [[0 for x in range(15)] for x in range(14)]

def initBoardSquaresArray():    # initialize array

    print("")
    print("initBoardSquaresArray")   # debug
    for j in range(14):   # rows
        for i in range(15):   # cols (nested within each row list)
            boardSquaresArray[j][i] = boardSquare(j,i,sq_x[i],sq_y[j],terrain[j][i])
            #def __init__(self, row_num, col_num, x, y, terrain, shipNum=0, shoreBatt=0, mine=0, size=boardSquareSize):

    ## debug:
    #print("")
    #print("print boardSquaresArray")
    #print("row, col, x, y, terrain, shipNum, shoreBatt, mine, size")
    #print("")
    ##print(boardSquaresArray)
    #for j in range(14):   # rows
    #    for i in range(15):   # cols
    #        print(boardSquaresArray[j][i].row_num,boardSquaresArray[j][i].col_num,"\t",boardSquaresArray[j][i].x,boardSquaresArray[j][i].y,"\t",boardSquaresArray[j][i].terrain,boardSquaresArray[j][i].shipNum,boardSquaresArray[j][i].shoreBatt,boardSquaresArray[j][i].mine,boardSquaresArray[j][i].size)


#########################################################
# Class: Piece, and array of class instances

class Piece():
    def __init__(self, shipNum, color, image, p_row_num, p_col_num, num_masts, moved, direction, shipType, label):

        self.shipNum = shipNum
        self.color = color
        self.image = image
        self.p_row_num = p_row_num
        self.p_col_num = p_col_num
        self.num_masts = num_masts
        self.moved = moved
        self.direction = direction   # Rotation is counter-clockwise: if 0 = N, 90 = W, 180 = S, 270 = E
        self.shipType = shipType     # 1 = red, 2 = blue, 3 = merchant
        self.label = label   # needed?

    ##RH do I need this?
    ## pos is the mouse position or a tuple of (x,y) coordinates
    #def isOver(self, pos):
    #    # change to square row/col? is there a ship there?
    #    if pos[0] > (self.x) and pos[0] < (self.x+self.size):
    #        if pos[1] > (self.y) and pos[1] < (self.y+self.size):
    #            #displayUnitStatus()    # move to piece class display?
    #            #self.drawOcean()  # call this method to draw a ocean square border
    #            self.drawRed()    # call this method to draw a red square border
    #            #self.drawYellow() # call this method to draw a yellow square border
    #            return True


#########################################################
#array of class Piece (ship) instances

    # Red Fleet  (shipType = 1)
    # 2 Man of War -- 4 Masts Each (Ships of the Line)
    # 3 Frigates   -- 3 masts Each
    # 3 Brigs      -- 2 Masts Each
    # 2 Cutters    -- 1 Mast  Each
    
    # Blue Fleet  (shipType = 2)
    # 4 Frigates   -- 3 Masts Each
    # 2 Brigs      -- 2 Masts Each
    # 4 Cutters    -- 1 Mast  Each
    # 4 Merchants  -- 1? or no masts?  (shipType = 3)

pieceArray = []   # create array of Piece class instances
pieceNum = 24     # more realistic number?

def initPieceArray():  # initialize array of class Piece
    print("")
    print("initPieceArray")    # debug
    #   def __init__(self, shipNum, color, image, p_row_num, p_col_num, num_masts, moved, direction, shipType, label)  # add target_priority?
    for i in range(pieceNum+1):
        pieceArray.append(Piece(0,  '',  '', 0, 0, 0, 0, 0, 0, ''))  # dummy data  # add target_priority?

def resetPieceArray():  # initialize array of class Piece
    print("")
    print("resetPieceArray")    # debug
                    #  shipNum, color, image,    row, col, masts, moved, dir, Type, label  # add target_priority?
    pieceArray[1]  = Piece(1,  'red',  ship_red_4, 12, 10, 2, 0, 0, 1, 'Man of War')  # British Fleet 
    pieceArray[2]  = Piece(2,  'red',  ship_red_4, 12, 11, 2, 0, 0, 1, 'Man of War')  # British Fleet 
    pieceArray[3]  = Piece(3,  'red',  ship_red_4, 12, 12, 4, 0, 0, 1, 'Man of War')  # British Fleet 
    pieceArray[4]  = Piece(4,  'red',  ship_red_4, 12, 13, 1, 0, 0, 1, 'Man of War')  # British Fleet 
    pieceArray[5]  = Piece(5,  'red',  ship_red_4, 12, 14, 3, 0, 0, 1, 'Man of War')  # British Fleet 
    pieceArray[6]  = Piece(6,  'red',  ship_red_4, 13, 10, 1, 0, 0, 1, 'Man of War')  # British Fleet 
    pieceArray[7]  = Piece(7,  'red',  ship_red_4, 13, 11, 2, 0, 0, 1, 'Man of War')  # British Fleet 
    pieceArray[8]  = Piece(8,  'red',  ship_red_4, 13, 12, 4, 0, 0, 1, 'Man of War')  # British Fleet 
    pieceArray[9]  = Piece(9,  'red',  ship_red_4, 13, 13, 3, 0, 0, 1, 'Man of War')  # British Fleet 
    pieceArray[10] = Piece(10, 'red',  ship_red_4, 13, 14, 3, 0, 0, 1, 'Man of War')  # British Fleet 

    pieceArray[11] = Piece(11, 'blue', ship_blue_4, 1, 2, 3, 0, 180, 2, 'Man of War')  # American Fleet
    pieceArray[12] = Piece(12, 'blue', ship_blue_4, 1, 4, 1, 0, 180, 2, 'Man of War')  # American Fleet
    pieceArray[13] = Piece(13, 'blue', ship_blue_4, 1, 5, 3, 0, 180, 2, 'Man of War')  # American Fleet
    pieceArray[14] = Piece(14, 'blue', ship_blue_4, 1, 6, 1, 0, 180, 2, 'Man of War')  # American Fleet
    pieceArray[15] = Piece(15, 'blue', ship_blue_4, 1, 7, 3, 0, 180, 2, 'Man of War')  # American Fleet
    pieceArray[16] = Piece(16, 'blue', ship_blue_4, 1, 8, 2, 0, 180, 2, 'Man of War')  # American Fleet
    pieceArray[17] = Piece(17, 'blue', ship_blue_4, 1, 9, 1, 0, 180, 2, 'Man of War')  # American Fleet
    pieceArray[18] = Piece(18, 'blue', ship_blue_4, 1,10, 1, 0, 180, 2, 'Man of War')  # American Fleet
    pieceArray[19] = Piece(19, 'blue', ship_blue_4, 1,11, 3, 0, 180, 2, 'Man of War')  # American Fleet
    pieceArray[20] = Piece(20, 'blue', ship_blue_4, 1,12, 2, 0, 180, 2, 'Man of War')  # American Fleet

    pieceArray[21] = Piece(21, 'blue', ship_merchant, 0, 4, 1, 1, 180, 3, 'Merchant')  # American Merchant Ships
    pieceArray[22] = Piece(22, 'blue', ship_merchant, 0, 6, 1, 1, 180, 3, 'Merchant')  # American Merchant Ships
    pieceArray[23] = Piece(23, 'blue', ship_merchant, 0, 8, 1, 1, 180, 3, 'Merchant')  # American Merchant Ships
    pieceArray[24] = Piece(24, 'blue', ship_merchant, 0,10, 1, 1, 180, 3, 'Merchant')  # American Merchant Ships

    ## debug:
    #print("print pieceArray (debug)")
    #print("shipNum, color, image, p_row_num, p_col_num, num_masts, moved, direction, shipType, label")  # add target_priority?
    #for i in range(1,pieceNum+1):
    #    print(pieceArray[i].shipNum,pieceArray[i].color,pieceArray[i].image,pieceArray[i].p_row_num,pieceArray[i].p_col_num,pieceArray[i].num_masts,pieceArray[i].moved,pieceArray[i].direction,pieceArray[i].shipType,pieceArray[i].label)
    #print("")


################################################################################################
################################################################################################
# see line 3325...

#game_setup()           # what background for setup & instructions?
    #initTerrain()
    #refreshGameScreen()
    #displayInstructions()

#userDeployment()       # just which ships are in which of the 10 locs

#set_AI_Strategy()
#AI_ship_placement()
#setup_opponent()       # computer AI for now...

#game_loop()
    #moveCheck()
    #moveShip()
    #combatCheck()
    #victoryCheck()

################################################################################################
################################################################################################


#########################################################
def game_setup():   
    print("")
    print("#=========== Welcome to Broadside ===========#")
    print("")
    # what background music? ocean waves, see line 267

    global MsgFlag
    global winner
    MsgFlag = 0   # controls console window at bottom
    winner = 0

    #redrawGameWindow()
    drawScreenSetup()
    text2dispCenter50("Do You Need Instructions? (Y/n)",display_width/2,1380, white)

    pygame.display.update()
    pygame.event.clear()  # clear any pending events
    run_setup = True

    while run_setup:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_setup = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y or event.key == pygame.K_RETURN:
                    drawScreenSetup()
                    text2dispCenter50("Use Left/Right arrow to turn pages, X to exit", display_width/2, 1380, white)
                    pygame.display.update()
                    displayInstructions()
                    print("instructions done")
                    run_setup = False
                if event.key == pygame.K_n:
                    print("chose no instructions")
                    run_setup = False
                if event.key == pygame.K_q or event.key == pygame.K_x:
                    run_setup = False
                    pygame.quit()
                    sys.exit()

    # user setup of red fleet...
    displayInstructionsUserFleetSetup()
    #inits
    defineRowsColumns()
    initBoardSquaresArray()
    initPieceArray()
    resetPieceArray()
    initTerrain()
    #draw stuff
    redrawGameWindow()    # blit game board
    print("redrawGameWindow")
    drawTerrain()         # draw land, gun emplacements, mines
    print("drawTerrain")
    drawBoardPieces()
    print("drawBoardPieces")
    pygame.display.update()   # needed? maybe...


#########################################################
def displayInstructions():
    #print("")
    print("# displayInstructions #")

    i = 0
    pygame.event.clear()  # clear any pending events
    run_di = True

    while run_di:
        pygame.event.clear()
        clock.tick(2)
        #clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_di = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    i += 1
                if event.key == pygame.K_LEFT:
                    i += -1
                if event.key == pygame.K_x:
                    run_di = False
                if event.key == pygame.K_q:
                    run_di = False
                    pygame.quit()
                    sys.exit()
            if i == 5:
                i = 0
            elif i < 0:
                i = 4
            #print("i =",i)
    
        # copy instructions scans to the screen:
        screen.blit(instructions[i], (820, 100))   # 2560x1440
        #screen.blit(instructions[i], (345, 0))   #  1920x1080
        #screen.blit(instructions[i], (display_width/2, 0))
        pygame.display.update() 


#########################################################
def displayInstructionsUserFleetSetup():   
 
    print("")
    print("# displayInstructionsUserFleetSetup #")

    global MsgFlag
    global MsgText
    global userDeploymentMode
    userDeploymentMode = 0

    drawScreenSetup()
    text2dispCenter50("Hit Q at any time to quit the game.",display_width/2,980, white)
    text2dispCenter50("User Fleet Arrangement Instructions (next screen):",display_width/2,1140, white)
    text2dispCenter50("Adjust default ship placement as needed by",display_width/2,1230, white)    # moved these 2 lines closer together
    text2dispCenter50("clicking on a ship, then click new location.",display_width/2,1290, white)    # moved these 2 lines closer together
    text2dispCenter50("Do you want to adjust your Fleet Arrangement? (Y/n)",display_width/2,1380, white)

    pygame.display.update() 
    pygame.event.clear()  # clear any pending events
    run_diufs = True

    while run_diufs:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_diufs = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y or event.key == pygame.K_RETURN:
                    userDeploymentMode = 1
                    MsgText = "hit X when done"
                    MsgFlag = 1   # controls console window at bottom
                    print("Arrangement selected")
                    run_diufs = False
                if event.key == pygame.K_n:
                    userDeploymentMode = 0
                    MsgFlag = 2   # controls console window at bottom
                    print("chose no Arrangement")
                    run_diufs = False
                if event.key == pygame.K_q or event.key == pygame.K_x:
                    print("")
                    print("Q entered, exiting...")
                    print("")
                    run_diufs = False
                    pygame.quit()
                    sys.exit()


#########################################################
def userFleetArrangement():
    # adjust default ship placement as needed by clicking on ship, then destination (swap ships)
    # just swap r/c locations of the two ships, update pieceArray after user input

    print("")
    print("# userFleetArrangement #")

    global sq_row
    global sq_col
    global new_sq_row
    global new_sq_col
    global moveValid
    global userDeploymentMode
    global MsgFlag
    global MsgText

    # see displayInstructionsUserFleetSetup()
    #MsgFlag = 1   # controls console window at bottom
    #MsgText = "hit X when done"
    #refreshGameScreen()

    shipSelectedFrom = 0
    shipSelectedTo = 0

    pygame.display.update() 
    pygame.event.clear()  # clear any pending events
    run_ufa = True

    while run_ufa:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()    # needed here?
            if event.type == pygame.QUIT:
                run_ufa = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    print("")
                    print("Q entered, exiting...")
                    print("")
                    run_ufa = False
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_x:
                    userDeploymentMode = 0
                    new_sq_row = 0
                    new_sq_col = 0
                    sq_row = 0         # reset to new click mode
                    sq_col = 0
                    MsgFlag = 2   # controls console window at bottom
                    refreshGameScreen()
                    print("")
                    print("exiting userFleetArrangement mode...")
                    run_ufa = False
            elif event.type == pygame.MOUSEBUTTONDOWN:   
                print("")
                print("mouse clicked")
                #print("pos[0] =",pos[0]," pos[1] =",pos[1])
                click.play()
                for j in range(14):   # rows
                    for i in range(15):   # cols
                        if boardSquaresArray[j][i].isOver(pos):
                            new_sq_row = j
                            new_sq_col = i
                            print("sq_row =",sq_row," new_sq_row =",new_sq_row)    
                            print("sq_col =",sq_col," new_sq_col =",new_sq_col)
                # what did we click on?
                if terrain[new_sq_row][new_sq_col] == 'S':   # must be S
                    print("sea square selected")
                    # new selection?
                    if sq_row == 0 and sq_col == 0:
                        print("new selection - check for a red ship...")
                        shipSelectedFrom = 0
                        for i in range(1,11):
                            if pieceArray[i].p_row_num == new_sq_row and pieceArray[i].p_col_num == new_sq_col:
                                shipSelectedFrom = i
                                print("shipSelectedFrom =",shipSelectedFrom)
                        if pieceArray[shipSelectedFrom].shipType == 1:    # British fleet, ok!
                            print("British ship selected")
                            # save selection
                            sq_row = new_sq_row
                            sq_col = new_sq_col
                            print("sq_row =",sq_row," sq_col =",sq_col)
                            boardSquaresArray[sq_row][sq_col].drawRed()  # highlight square
                            pygame.display.update()
                        elif pieceArray[shipSelectedFrom].shipType != 1:    # not a British ship, anything else is an error
                            print("mistaken input, sound the alarm!!")
                            alarmBellSound.play()  # error sound
                    else:
                        print("# destination clicked")
                        shipSelectedTo = 0
                        if sq_row == new_sq_row and sq_col == new_sq_col:    # both are same, deselect ship (remove red box)
                            print("both are same, deselect ship")
                            new_sq_row = 0
                            new_sq_col = 0
                            sq_row = 0     # reset to new click mode
                            sq_col = 0
                            refreshGameScreen()
                        elif new_sq_row == 12 or new_sq_row == 13:    # check for valid rows (12, 13)
                            if new_sq_col >= 10 and new_sq_col <= 14:    # check for valid columns (10-14)
                                #moveValid = 1    # RH ?
                                #for i in range(1,11):
                                #    if pieceArray[i].p_row_num == sq_row and pieceArray[i].p_col_num == sq_col:
                                #        shipSelectedFrom = i
                                #        print("shipSelectedFrom =",shipSelectedFrom)
                                #        print("British ship selected")
                                for i in range(1,11):
                                    if pieceArray[i].p_row_num == new_sq_row and pieceArray[i].p_col_num == new_sq_col:
                                        shipSelectedTo = i
                                        boardSquaresArray[new_sq_row][new_sq_col].drawRed()  # highlight square
                                        print("shipSelectedTo =",shipSelectedTo)
                                        print("British ship selected")
                                        pygame.time.delay(delay)
                                # swap locations
                                print("swap ship locations...")
                                pieceArray[shipSelectedFrom].p_row_num = new_sq_row
                                pieceArray[shipSelectedFrom].p_col_num = new_sq_col
                                pieceArray[shipSelectedTo].p_row_num = sq_row
                                pieceArray[shipSelectedTo].p_col_num = sq_col
                                print("pieceArray[shipSelectedFrom].p_row_num =", new_sq_row)
                                print("pieceArray[shipSelectedFrom].p_col_num =", new_sq_col)
                                print("pieceArray[shipSelectedTo].p_row_num =", sq_row)
                                print("pieceArray[shipSelectedTo].p_col_num =", sq_col)
                                pygame.display.update() 
                                new_sq_row = 0
                                new_sq_col = 0
                                sq_row = 0     # reset to new click mode
                                sq_col = 0
                                refreshGameScreen()
                        else:
                            print("mistaken input, try again...")
                            new_sq_row = 0
                            new_sq_col = 0
                            sq_row = 0     # reset to new click mode
                            sq_col = 0
                            #moveValid = 0    # RH ?
                            #moveValid = 1
                            #print("moveValid =",moveValid) 
                            alarmBellSound.play()  # error sound
                else:
                    # error (or else show status if applicable?) 
                    print("clicked on a non-Sea square...")
                    new_sq_row = 0
                    new_sq_col = 0
                    sq_row = 0     # reset to new click mode
                    sq_col = 0
                    #shipSelectedFrom = 0    # needed?
                    #shipSelectedTo = 0
                    refreshGameScreen()
                    alarmBellSound.play()  # error sound
# end userFleetArrangement() #


#########################################################
def drawScreenSetup():
    screen.blit(bgScreen_1, (0, 0))    # load background image, loc must be a tuple

    # screen.fill(black)    # erase screen #
    # screen.blit(bgScreen_0, (0, 0))    # load background image, loc must be a tuple
    # # load sidebar ship images #
    # screen.blit(bgr_ship_5, (0,0))      # left margin:   570 - 50 = 520 (500?)
    # screen.blit(bgr_ship_4, (0,720))
    # screen.blit(bgr_ship_6, (2060,0))   # right margin: 1970 + 50 = 2020 (2040?)
    # screen.blit(bgr_ship_2, (2060,720))


#########################################################
def redrawGameWindow():
    screen.blit(bgScreen_2, (0, 0))    # load background image, loc must be a tuple
    drawLandMessage()

    #screen.fill(black)    # erase screen #
    #screen.blit(bgScreen_0, (0, 0))    # load background image, loc must be a tuple
    #drawLandImages()    # draw land #
    # load sidebar ship images #
    # graphic border image size 500 x 720 (4 images)
    #screen.blit(bgr_ship_5, (0,0))      # left margin:   570 - 50 = 520 (500?)
    #screen.blit(bgr_ship_4, (0,720))
    #screen.blit(bgr_ship_6, (2060,0))   # right margin: 1970 + 50 = 2020 (2040?)
    #screen.blit(bgr_ship_2, (2060,720))

#########################################################
def refreshGameScreen():
    print("# refreshGameScreen #")
    redrawGameWindow()   # blit game board (background, draw land, sidebar ships)
    drawTerrain()        # gun emplacements, mines, "+" crosses
    drawBoardPieces()    # also updates boardSquaresArray for ship positions
    #showKybdInputs()     # debug only
    #drawSquares()        # debug only
    #drawBoardPiecesXY()  # debug
    pygame.display.update()  # keep!



#########################################################
def drawBoardPieces():
    # draw pieces on board in loop from pieceArray
    #RH:
    # also update boardSquaresArray for ship positions (no longer neeeded?)
    #print("clear shipNum in BoardSquaresArray")   # debug
    for j in range(14):   # rows
        for i in range(15):   # cols (nested within each row list)
                boardSquaresArray[j][i].shipNum = 0
    #print("drawBoardPieces")
    for i in range(1,pieceNum+1):
        if pieceArray[i].num_masts > 0:
            # screen.blit(image, (x,y))   # offsets: x = 26, y = -1
            # img = pygame.transform.rotozoom(img0, angle, scale)
            # Rotation is counter-clockwise: if 0 = N, 90 = W, 180 = S, 270 = E
            if pieceArray[i].shipType == 1:
                if pieceArray[i].num_masts == 4:
                    pieceArray[i].image = ship_red_4
                if pieceArray[i].num_masts == 3:
                    pieceArray[i].image = ship_red_3
                if pieceArray[i].num_masts == 2:
                    pieceArray[i].image = ship_red_2
                if pieceArray[i].num_masts == 1:
                    pieceArray[i].image = ship_red_1
                #print("i =",i," x =",(pieceArray[i].p_col_num*100+526+26)," y =",(pieceArray[i].p_row_num*100+19-1))   # debug only
                #screen.blit(pygame.transform.rotozoom(pieceArray[i].image, pieceArray[i].direction, 0.15), ((pieceArray[i].p_col_num*100+526+26), (pieceArray[i].p_row_num*100+19-1)))
                blitRotateCenter(screen, pygame.transform.rotozoom(pieceArray[i].image, 0, 0.15), ((pieceArray[i].p_col_num*100+526+26), (pieceArray[i].p_row_num*100+19-1)), pieceArray[i].direction)
                boardSquaresArray[pieceArray[i].p_row_num][pieceArray[i].p_col_num].shipNum = i
            elif pieceArray[i].shipType == 2:
                if pieceArray[i].num_masts == 4:
                    pieceArray[i].image = ship_blue_4
                if pieceArray[i].num_masts == 3:
                    pieceArray[i].image = ship_blue_3
                if pieceArray[i].num_masts == 2:
                    pieceArray[i].image = ship_blue_2
                if pieceArray[i].num_masts == 1:
                    pieceArray[i].image = ship_blue_1
                #print("i =",i," x =",(pieceArray[i].p_col_num*100+526+26)," y =",(pieceArray[i].p_row_num*100+19-1))   # debug only
                #screen.blit(pygame.transform.rotozoom(pieceArray[i].image, pieceArray[i].direction, 0.15), ((pieceArray[i].p_col_num*100+526+26), (pieceArray[i].p_row_num*100+19-1)))
                blitRotateCenter(screen, pygame.transform.rotozoom(pieceArray[i].image, 0, 0.15), ((pieceArray[i].p_col_num*100+526+26), (pieceArray[i].p_row_num*100+19-1)), pieceArray[i].direction)
                boardSquaresArray[pieceArray[i].p_row_num][pieceArray[i].p_col_num].shipNum = i
            else:
                #print("i =",i," x =",(pieceArray[i].p_col_num*100+526+26)," y =",(pieceArray[i].p_row_num*100+19-14))   # debug only
                #screen.blit(pygame.transform.rotozoom(pieceArray[i].image, pieceArray[i].direction, 0.15), ((pieceArray[i].p_col_num*100+526+26), (pieceArray[i].p_row_num*100+19-14)))
                blitRotateCenter(screen, pygame.transform.rotozoom(pieceArray[i].image, 0, 0.15), ((pieceArray[i].p_col_num*100+526+26), (pieceArray[i].p_row_num*100+19-1)), pieceArray[i].direction)
                boardSquaresArray[pieceArray[i].p_row_num][pieceArray[i].p_col_num].shipNum = i



################################################################################################
################################################################################################


#########################################################
def shipNumLookup():
    # looks up what shipNum is at current location, if any
    #print("# shipNumLookup #")
    global shipSelected    # needed for moveShip
    global sq_row    # ship to move
    global sq_col
    shipSelected = 0
    for i in range (1,pieceNum+1):
        if pieceArray[i].p_row_num == sq_row and pieceArray[i].p_col_num == sq_col:
            shipSelected = i    # what ship is at r/c?
    #print("shipNumLookup =",shipSelected)    # debug
    if sq_row == 0 and sq_col == 0:
        shipSelected = 0
    print("shipNumLookup =",shipSelected)    # debug


#########################################################
def moveCheck():
    # check entered move for validity...
    # add checkMoveIntoT for T attacks for AI player...
    # inputs are: sq_row new_sq_row sq_col new_sq_col
    # outputs are: moveValid

    print("")
    print("##----  moveCheck  ----##")

    global pmr
    global pmc
    global sq_row
    global sq_col
    global new_sq_row
    global new_sq_col
    global direction
    global moveRange
    global moveValid

    pmr = 0  # plus/minus row
    pmc = 0  # plus/minus col
    moveRange = 0
    moveValid = 1  #RH go back to this, and only set to 1 here and nowhere else!!
    #moveValid = 0   # this is too tricky, prone to error

    # debug:
    if playerTurn == -1:   # AI
        print("# computer's turn...")
    elif playerTurn == 1:   # human
        print("# human's turn...")
    # golden display of row/col move #
    print("sq_row     =",sq_row,"\t","    sq_col =",sq_col)
    print("new_sq_row =",new_sq_row,"\t","new_sq_col =",new_sq_col)

    # check move...
    if sq_row != new_sq_row and sq_col != new_sq_col:      # if neither is the same, error!
        print("mistaken input, sound the alarm!!")
        new_sq_row = 0
        new_sq_col = 0
        sq_row = 0     # reset to new click mode
        sq_col = 0
        moveValid  = 0
        if playerTurn == 1:   # human
            alarmBellSound.play()  # error sound
        refreshGameScreen()   # erase red square?
    elif sq_row == new_sq_row and sq_col == new_sq_col:    # both are same, deselect ship (remove red box)
        print("both are same, deselect ship")
        new_sq_row = 0
        new_sq_col = 0
        sq_row = 0     # reset to new click mode
        sq_col = 0
        moveValid  = 0
        refreshGameScreen()   # erase red square?
    else:
        print("# check path along row or column for obstacles")
        # what direction to turn for move? check d_col (+/-), d_row (+/-) (delta row/column)
        # d_row+ = N   (0), d_row- = S (180)
        # d_col+ = E (270), d_col- = W  (90)
        #----------------------------
        d_row = new_sq_row - sq_row
        d_col = new_sq_col - sq_col
        print("d_row =",d_row," d_col =",d_col)
        pmr = 0    # plus/minus row
        pmc = 0    # plus/minus col
        # direction?
        if sq_row == new_sq_row:
            print("horizontal move: sq_row = new_sq_row")
            if d_col < 0:
                direction = 90   # W
                pmc = -1
            elif d_col > 0:
                direction = 270  # E
                pmc = 1
            moveRange = d_col * pmc
        elif sq_col == new_sq_col:
            print("vertical move: sq_col = new_sq_col")
            if d_row < 0:
                direction =   0  # N
                pmr = -1
            elif d_row > 0:
                direction = 180  # S
                pmr = 1
            moveRange = d_row * pmr
        print("direction =",direction)
        print("pmr =",pmr," pmc =",pmc)
        print("moveRange =",moveRange)

        #----------------------------
        # increment from current sq to new sq:
        for i in range (1,moveRange + 1):                 
            irow = sq_row + pmr*i
            icol = sq_col + pmc*i
            #print("")
            #print("square: irow =",irow," icol =",icol)
            #print("i =",i," terrain =",terrain[irow][icol])
            if terrain[irow][icol] != 'S':   # might be an error... maybe
                if terrain[irow][icol] == 'L' or terrain[irow][icol] == 'G':
                    print("There's land in the way, sound the alarm!!")
                    moveValid = 0
                    print("moveValid =",moveValid) 
                    new_sq_row = 0  # to deselect the destination square (mistake)
                    new_sq_col = 0
                    sq_row = 0      # reset to new click mode
                    sq_col = 0
                    #refreshGameScreen()   # erase red square?
                    break  # to exit for loop
                elif terrain[irow][icol] == 'R' or terrain[irow][icol] == 'B' or terrain[irow][icol] == 'M':
                    if playerTurn == -1 and terrain[irow][icol] == 'M':   # AI
                        print("There's a Mine in the way, sound the alarm!!")   # RH ??
                        moveValid = 0
                        print("moveValid =",moveValid) 
                        break  # to exit for loop
                    else:
                        # No need to do anything here, this is handled elsewhere (shore guns not an obstacle)
                        print("R,B,M")
                        print("moveValid =",moveValid) 
            elif terrain[irow][icol] == 'S':
                for j in range(1,pieceNum+1):
                    if pieceArray[j].p_row_num == irow and pieceArray[j].p_col_num == icol:
                        print("There's a ship in the way, sound the alarm!!") 
                        print("ship[row] =",pieceArray[j].p_row_num," ship[col] =",pieceArray[j].p_col_num)
                        moveValid = 0
                        print("moveValid =",moveValid)
                        break  # to exit for loop
                if moveValid == 0:
                    break  # to exit outer for loop
        # end for loop

        # add checkMoveIntoT for T attacks for AI player...
        if playerTurn == -1 and moveValid == 1:   # AI
            #print("")
            print("# checkMoveIntoT for AI...")
            irow = sq_row + pmr*(moveRange + 1)
            icol = sq_col + pmc*(moveRange + 1)
            print("T ck square: irow =",irow," icol =",icol)
            if irow >= 1 and irow <= 13 and icol >= 0 and icol <= 14:
                print("terrain =",terrain[irow][icol])
                if terrain[irow][icol] == 'S':
                    for k in range(1,11):    # check red fleet
                        if pieceArray[k].p_row_num == irow and pieceArray[k].p_col_num == icol:
                            print("There's a red ship at end of move...") 
                            print("red ship =",k)
                            print("ship[row] =",pieceArray[k].p_row_num," ship[col] =",pieceArray[k].p_col_num)
                            print("checking red ship direction...") 
                            if sq_row == new_sq_row:
                                # horizontal move: sq_row = new_sq_row
                                if pieceArray[k].direction == 0 or pieceArray[k].direction == 180:
                                    print("T attack! Danger Will Robinson!")
                                    moveValid = 0
                                    print("T ck moveValid =",moveValid) 
                            elif sq_col == new_sq_col:
                                # vertical move: sq_col = new_sq_col
                                if pieceArray[k].direction == 90 or pieceArray[k].direction == 270:
                                    print("T attack! Danger Will Robinson!")
                                    moveValid = 0
                                    print("T ck moveValid =",moveValid) 
                            else:
                                print("no T attack, safe move")
            else:
                print("False: if irow >= 1 and irow <= 13 and icol >= 0 and icol <= 14")
        
        # to deselect the destination square (mistake)
        if moveValid == 0:
            new_sq_row = 0     
            new_sq_col = 0
            sq_row = 0         # reset to new click mode
            sq_col = 0
            refreshGameScreen()   # erase red square?

        # end moveCheck for loop
        # RH keep this summary for debug...
        #print("")
        print("# moveCheck summary...")
        print("moveValid =",moveValid)  # moveValid = 1  # if it passes move checking
        #print("sq_row     =",sq_row,"\t","    sq_col =",sq_col)
        #print("new_sq_row =",new_sq_row,"\t","new_sq_col =",new_sq_col)
        #print("end square: irow =",irow," icol =",icol)
        print("## end moveCheck For Loop ##")
        #print("")
# end moveCheck()


#########################################################
def moveShip():
    # move ship per valid entry to destination, one square at a time
    # check for any cannon or mine results along the way...
    # inputs are: shipSelected, sq_row, new_sq_row, sq_col, new_sq_col, pmr, pmc, direction, moveRange
    # outputs are: shipSelect(newRow)(newColum) and attack resolution if any: cannons, mines, enemy fleet

    global delay
    global shipSelected
    global pmr
    global pmc
    global sq_row
    global sq_col
    global new_sq_row
    global new_sq_col
    global direction
    global moveRange
    global moveValid

    global playerTurn   # 1 (human) or -1 (computer)
    global turnNum

    if moveValid == 1:
        print("")
        print("##----  moveShip  ----##")
        # debug:
        if playerTurn == -1:   # AI
            print("## computer's turn...")
            # RH testing... does this fix blue fleet first move highliting?
            # RH do this again at the end??
            boardSquaresArray[sq_row][sq_col].drawBlue()  # highlight starting square
            pygame.time.delay(delay)

        elif playerTurn == 1:   # human
            print("## human's turn...")

        twoBellsSound.play()  # good move
        print("shipSelected =",shipSelected)
        print("sq_row     =",sq_row," sq_col =",sq_col)
        print("new_sq_row =",new_sq_row," new_sq_col =",new_sq_col)
        print("pmr =",pmr," pmc =",pmc)
        print("moveRange =",moveRange)
        print("direction =",direction)

        pieceArray[shipSelected].direction = direction

        # increment from current sq to new sq:
        for i in range (1,moveRange + 1):                 
            irow = sq_row + pmr*i
            icol = sq_col + pmc*i
            #print("")
            #print("square: irow =",irow," icol =",icol)
            #print("i =",i," terrain =",terrain[irow][icol])
            pieceArray[shipSelected].p_row_num = pieceArray[shipSelected].p_row_num + pmr
            pieceArray[shipSelected].p_col_num = pieceArray[shipSelected].p_col_num + pmc
            refreshGameScreen()

            if i <= moveRange:
            #if i < moveRange:    # RH < or <= ??
                if playerTurn == 1:
                    boardSquaresArray[new_sq_row][new_sq_col].drawRed()  # highlight destination square
                elif playerTurn == -1:
                    boardSquaresArray[new_sq_row][new_sq_col].drawBlue()  # highlight destination square

            if terrain[irow][icol] != 'S':       # check for cannon or mine results
                if terrain[irow][icol] == 'R' or terrain[irow][icol] == 'B':  # check cannon
                    print("cannon")
                    # check cannon for hit/miss, if still alive:
                    if boardSquaresArray[irow][icol].shoreBatt >= 1:   # hit
                        print("shoreBatt =",boardSquaresArray[irow][icol].shoreBatt)
                        print("# explosion sound #")
                        explosion0.play()  # small expl
                        pygame.time.delay(delay*2)
                        pieceArray[shipSelected].num_masts = pieceArray[shipSelected].num_masts - boardSquaresArray[irow][icol].shoreBatt  # was 1
                        print("num_masts =",pieceArray[shipSelected].num_masts)
                        if pieceArray[shipSelected].num_masts == 0:
                            pieceArray[shipSelected].p_col_num = 0
                            pieceArray[shipSelected].p_row_num = 0
                            break  # to exit for loop
                    elif boardSquaresArray[irow][icol].shoreBatt == 0:   # miss
                        print("miss")
                    refreshGameScreen()
                    if playerTurn == 1:
                        boardSquaresArray[new_sq_row][new_sq_col].drawRed()  # highlight destination square
                    elif playerTurn == -1:
                        boardSquaresArray[new_sq_row][new_sq_col].drawBlue()  # highlight destination square
                    pygame.time.delay(delay)

                elif terrain[irow][icol] == 'M':  # check mine
                    print("mine")
                    print("terrain =",terrain[irow][icol])
                    print("boardSA.mine =",boardSquaresArray[irow][icol].mine)
                    # check mine for sink/pass, if still alive:
                    if boardSquaresArray[irow][icol].mine == 1:  # sink
                        print("# explosion sound #")
                        print("ship sunk!")
                        explosion2.play()  # big expl
                        pygame.time.delay(delay*2)
                        pieceArray[shipSelected].num_masts = 0
                        pieceArray[shipSelected].p_col_num = 0
                        pieceArray[shipSelected].p_row_num = 0
                        boardSquaresArray[irow][icol].mine = 0
                        terrain[irow][icol] = "S"
                        print("terrain =",terrain[irow][icol])
                        print("boardSA.mine =",boardSquaresArray[irow][icol].mine)
                        refreshGameScreen()
                        if playerTurn == 1:
                            boardSquaresArray[new_sq_row][new_sq_col].drawRed()  # highlight destination square
                        elif playerTurn == -1:
                            boardSquaresArray[new_sq_row][new_sq_col].drawBlue()  # highlight destination square
                        break  # to exit for loop
                    elif boardSquaresArray[irow][icol].mine == 0:  # pass
                        # keep going
                        #boardSquaresArray[irow][icol].mine = 0
                        terrain[irow][icol] = "S"
                        print("terrain =",terrain[irow][icol])
                        print("boardSA.mine =",boardSquaresArray[irow][icol].mine)
                        refreshGameScreen()
                        if playerTurn == 1:
                            boardSquaresArray[new_sq_row][new_sq_col].drawRed()  # highlight destination square
                        elif playerTurn == -1:
                            boardSquaresArray[new_sq_row][new_sq_col].drawBlue()  # highlight destination square
                        pygame.time.delay(delay)
            elif terrain[irow][icol] == 'S':   # sea square
                # keep going
                pygame.time.delay(delay)
                #print("moveShip(): move ahead 1") 
                #refreshGameScreen()

                # RH remove this? see same code above...
                #if i <= moveRange:
                ##if i < moveRange:    # RH < or <= ??
                #    if playerTurn == 1:
                #        boardSquaresArray[new_sq_row][new_sq_col].drawRed()  # highlight destination square
                #    elif playerTurn == -1:
                #        boardSquaresArray[new_sq_row][new_sq_col].drawBlue()  # highlight destination square

        # end moveShip For Loop
        #print("")
        print("## Arrived at Destination ##")
        #print("shipSelected.num_masts =",pieceArray[shipSelected].num_masts)
        print("shipSelected.p_col_num =",pieceArray[shipSelected].p_col_num)
        print("shipSelected.p_row_num =",pieceArray[shipSelected].p_row_num)
        new_sq_row = 0
        new_sq_col = 0
        sq_row = 0     # reset to new click mode
        sq_col = 0
        refreshGameScreen()        #RH removed, ok? No, keep this!
        #pygame.display.update()   # debug?

    elif moveValid == 0:
        print("moveShip: bad input, moveValid = 0")

    print("## end moveShip() ##")
    #print("")

# end moveShip()


#########################################################
def combatCheck():
    # at end of move, check for available broadsides to fire (both sides)
    # also check for incoming fire
    # adjust mast count on both fleets as needed

    #global delay
    global shipSelected
    global sq_row
    global sq_col
    global new_sq_row
    global new_sq_col
    global moveValid
    global playerTurn   # 1 (human) or -1 (computer)
    global turnNum

    # check for combat...
    if moveValid == 1:
        print("")
        print("##----  combatCheck  ----##")
        #print("")
        # debug:
        if playerTurn == -1:   # AI
            print("## computer's turn...")
        elif playerTurn == 1:   # human
            print("## human's turn...")

        print("shipSelected.p_row_num =",pieceArray[shipSelected].p_row_num)  # debug
        print("shipSelected.p_col_num =",pieceArray[shipSelected].p_col_num)  # debug
        attacker_row = pieceArray[shipSelected].p_row_num
        attacker_col = pieceArray[shipSelected].p_col_num
        print("attacker_row =",attacker_row," attacker_col =",attacker_col)  # debug

        # check sides, i.e., +90, -90 from current direction for enemy ships, shoot them!
        # d_row+ = N   (0), d_row- = S (180)
        # d_col+ = E (270), d_col- = W  (90)

        if pieceArray[shipSelected].direction == 0 or pieceArray[shipSelected].direction == 180:
            target_row_num1 = attacker_row
            target_col_num1 = attacker_col - 1
            target_row_num2 = attacker_row
            target_col_num2 = attacker_col + 1
            print("target_row_num1 =",target_row_num1," target_col_num1 =",target_col_num1)
            print("target_row_num2 =",target_row_num2," target_col_num2 =",target_col_num2)

        elif pieceArray[shipSelected].direction == 90 or pieceArray[shipSelected].direction == 270:
            target_row_num1 = attacker_row - 1
            target_col_num1 = attacker_col
            target_row_num2 = attacker_row + 1
            target_col_num2 = attacker_col
            print("target_row_num1 =",target_row_num1," target_col_num1 =",target_col_num1)
            print("target_row_num2 =",target_row_num2," target_col_num2 =",target_col_num2)

        #RH also need to check for enemies off my bow that are crossing my T!
        if pieceArray[shipSelected].direction == 0:
            target_row_num3 = attacker_row - 1
            target_col_num3 = attacker_col
        elif pieceArray[shipSelected].direction == 180:
            target_row_num3 = attacker_row + 1
            target_col_num3 = attacker_col
        elif pieceArray[shipSelected].direction == 90:
            target_row_num3 = attacker_row
            target_col_num3 = attacker_col - 1
        elif pieceArray[shipSelected].direction == 270:
            target_row_num3 = attacker_row
            target_col_num3 = attacker_col + 1

        # are there any ships there?
        targetShip1 = -1
        targetShip2 = -1
        targetShip3 = -1
        for i in range(1,pieceNum+1):
            if pieceArray[i].p_row_num == target_row_num1 and pieceArray[i].p_col_num == target_col_num1:
                targetShip1 = i
                print("targetShip1 =",targetShip1)
            if pieceArray[i].p_row_num == target_row_num2 and pieceArray[i].p_col_num == target_col_num2:
                targetShip2 = i
                print("targetShip2 =",targetShip2)
            if pieceArray[i].p_row_num == target_row_num3 and pieceArray[i].p_col_num == target_col_num3:
                targetShip3 = i
                print("targetShip2 =",targetShip3)
        if targetShip1 == -1 and targetShip2 == -1 and targetShip3 == -1:
            print("# no target ships detected #")

        # check for available broadsides to fire

        #RH change this to look at playerTurn instead...
        # if player == 1: atk type 2 or 3
        # elif player == -1: atk type 1

        if targetShip1 >= 0:
            if (playerTurn == 1 and pieceArray[targetShip1].shipType == 1) or (playerTurn == -1 and pieceArray[targetShip1].shipType > 1):    # friendly fleet, don't shoot!
                print("targetShip1 is friendly, dont shoot!")
            elif (playerTurn == 1 and pieceArray[targetShip1].shipType > 1) or (playerTurn == -1 and pieceArray[targetShip1].shipType == 1):    # enemy fleet, fire!
                print("targetShip1 is enemy, fire!")
                explosion0.play()  # small expl
                pieceArray[targetShip1].num_masts = pieceArray[targetShip1].num_masts - 1
                print("targetShip1.num_masts =",pieceArray[targetShip1].num_masts)
                if pieceArray[targetShip1].num_masts == 0:
                    pieceArray[targetShip1].p_col_num = 0
                    pieceArray[targetShip1].p_row_num = 0
                # resolve incoming fire
                if pieceArray[targetShip1].shipType < 3:  # need to check direction of enemy ship
                    if pieceArray[shipSelected].direction == 0 or pieceArray[shipSelected].direction == 180:
                        if pieceArray[targetShip1].direction == 0 or pieceArray[targetShip1].direction == 180:
                            pieceArray[shipSelected].num_masts = pieceArray[shipSelected].num_masts - 1
                            print("shipSelected.num_masts =",pieceArray[shipSelected].num_masts)
                    elif pieceArray[shipSelected].direction == 90 or pieceArray[shipSelected].direction == 270:
                        if pieceArray[targetShip1].direction == 90 or pieceArray[targetShip1].direction == 270:
                            pieceArray[shipSelected].num_masts = pieceArray[shipSelected].num_masts - 1
                            print("shipSelected.num_masts =",pieceArray[shipSelected].num_masts)
                refreshGameScreen()

        # check for available broadsides to fire
        if targetShip2 >= 0:
            if (playerTurn == 1 and pieceArray[targetShip2].shipType == 1) or (playerTurn == -1 and pieceArray[targetShip2].shipType > 1):    # friendly fleet, don't shoot!
                print("targetShip2 is friendly, dont shoot!")
            elif (playerTurn == 1 and pieceArray[targetShip2].shipType > 1) or (playerTurn == -1 and pieceArray[targetShip2].shipType == 1):    # enemy fleet, fire!
                print("targetShip2 is enemy, fire!")
                explosion0.play()  # small expl
                pieceArray[targetShip2].num_masts = pieceArray[targetShip2].num_masts - 1
                print("targetShip2.num_masts =",pieceArray[targetShip2].num_masts)
                if pieceArray[targetShip2].num_masts == 0:
                    pieceArray[targetShip2].p_col_num = 0
                    pieceArray[targetShip2].p_row_num = 0
                # resolve incoming fire
                if pieceArray[targetShip2].shipType < 3:  # need to check direction of enemy ship
                    if pieceArray[shipSelected].direction == 0 or pieceArray[shipSelected].direction == 180:
                        if pieceArray[targetShip2].direction == 0 or pieceArray[targetShip2].direction == 180:
                            pieceArray[shipSelected].num_masts = pieceArray[shipSelected].num_masts - 1
                            print("shipSelected.num_masts =",pieceArray[shipSelected].num_masts)
                    elif pieceArray[shipSelected].direction == 90 or pieceArray[shipSelected].direction == 270:
                        if pieceArray[targetShip2].direction == 90 or pieceArray[targetShip2].direction == 270:
                            pieceArray[shipSelected].num_masts = pieceArray[shipSelected].num_masts - 1
                            print("shipSelected.num_masts =",pieceArray[shipSelected].num_masts)
                refreshGameScreen()

        #RH also need to check for enemies off my bow that are crossing my T!
        if targetShip3 >= 0:
            if (playerTurn == 1 and pieceArray[targetShip3].shipType == 1) or (playerTurn == -1 and pieceArray[targetShip3].shipType > 1):    # friendly fleet, don't shoot!
                print("targetShip3 is friendly, dont shoot!")
            elif (playerTurn == 1 and pieceArray[targetShip3].shipType > 1) or (playerTurn == -1 and pieceArray[targetShip3].shipType == 1):    # enemy fleet, fire!
                print("targetShip3 is enemy, fire!")
                # resolve incoming fire from enemies off my bow that are crossing my T!
                if pieceArray[targetShip3].shipType < 3:  # need to check direction of enemy ship
                    if pieceArray[shipSelected].direction == 0 or pieceArray[shipSelected].direction == 180:
                        if pieceArray[targetShip3].direction == 90 or pieceArray[targetShip3].direction == 270:
                            pieceArray[shipSelected].num_masts = pieceArray[shipSelected].num_masts - 1
                            print("shipSelected.num_masts =",pieceArray[shipSelected].num_masts)
                            explosion0.play()  # small expl
                    elif pieceArray[shipSelected].direction == 90 or pieceArray[shipSelected].direction == 270:
                        if pieceArray[targetShip3].direction == 0 or pieceArray[targetShip3].direction == 180:
                            pieceArray[shipSelected].num_masts = pieceArray[shipSelected].num_masts - 1
                            print("shipSelected.num_masts =",pieceArray[shipSelected].num_masts)
                            explosion0.play()  # small expl
                refreshGameScreen()

        # resolve incoming fire results
        if pieceArray[shipSelected].num_masts <= 0:
            pieceArray[shipSelected].num_masts = 0
            pieceArray[shipSelected].p_col_num = 0
            pieceArray[shipSelected].p_row_num = 0
            print("shipSelected.num_masts =",pieceArray[shipSelected].num_masts)
            print("shipSelected.p_col_num =",pieceArray[shipSelected].p_col_num)
            print("shipSelected.p_row_num =",pieceArray[shipSelected].p_row_num)
            refreshGameScreen()
            #break  # ? to exit for loop

    elif moveValid == 0:
        print("combatCheck: mistaken input, moveValid = 0")

    # clear moveValid for next turn...
    moveValid = 0  # no longer needed, done at moveCheck

    print("## end combatCheck ##")
# end combatCheck()


#########################################################
def set_AI_Strategy():
    print("")
    print("# set_AI_Strategy #")   

    global boardSquaresArray

    # set strategy (random)
    dieRoll = random.randint(1, 6)   # Return a random integer N such that 1 <= N <= 6
    print("dieRoll =",dieRoll)   # debug

    # strategy based cannon/mine placement:
    if dieRoll <= 2:
        AI_Strategy = 1  # hang back, passive defense (right side full clog)
        print("AI_Strategy =",AI_Strategy)   
        # cannons left:
        boardSquaresArray[7][ 1].shoreBatt = 0  # must be R squares, not G squares
        boardSquaresArray[7][ 2].shoreBatt = 0  # must be R squares, not G squares
        boardSquaresArray[7][ 3].shoreBatt = 0  # must be R squares, not G squares
        boardSquaresArray[7][ 4].shoreBatt = 0  # must be R squares, not G squares
        boardSquaresArray[7][ 5].shoreBatt = 0  # must be R squares, not G squares
        #boardSquaresArray[5][ 2].mine = 1
        #boardSquaresArray[5][ 3].mine = 0
        #boardSquaresArray[5][ 4].mine = 1
        # cannons right:
        boardSquaresArray[7][ 8].shoreBatt = 1  # must be R squares, not G squares 
        boardSquaresArray[7][ 9].shoreBatt = 1  # must be R squares, not G squares
        boardSquaresArray[7][10].shoreBatt = 2  # must be R squares, not G squares
        boardSquaresArray[7][11].shoreBatt = 1  # must be R squares, not G squares
        boardSquaresArray[7][12].shoreBatt = 1  # must be R squares, not G squares 
        #boardSquaresArray[5][ 9].mine = 0
        #boardSquaresArray[5][10].mine = 0
        #boardSquaresArray[5][11].mine = 1
        # mines (3, can't have three in a row)
        dieRoll = random.randint(1, 6)   # Return a random integer N such that 1 <= N <= 6
        print("2nd dieRoll =",dieRoll)   # debug
        if dieRoll <= 2:    # was 3
            boardSquaresArray[5][ 2].mine = 1  
            boardSquaresArray[5][ 3].mine = 0  
            boardSquaresArray[5][ 4].mine = 0  
            boardSquaresArray[5][ 9].mine = 1  
            boardSquaresArray[5][10].mine = 0  
            boardSquaresArray[5][11].mine = 1  
        else:
            boardSquaresArray[5][ 2].mine = 1  
            boardSquaresArray[5][ 3].mine = 0  
            boardSquaresArray[5][ 4].mine = 1  
            boardSquaresArray[5][ 9].mine = 0  
            boardSquaresArray[5][10].mine = 0  
            boardSquaresArray[5][11].mine = 1  
    elif dieRoll <= 4:
        AI_Strategy = 2  # hit & run? hit any invaders? Or Agreessive? (both sides even)
        print("AI_Strategy =",AI_Strategy)   
        # cannons left:
        boardSquaresArray[7][ 1].shoreBatt = 0  # must be R squares, not G squares
        boardSquaresArray[7][ 2].shoreBatt = 0  # must be R squares, not G squares
        boardSquaresArray[7][ 3].shoreBatt = 1  # must be R squares, not G squares
        boardSquaresArray[7][ 4].shoreBatt = 1  # must be R squares, not G squares
        boardSquaresArray[7][ 5].shoreBatt = 1  # must be R squares, not G squares
        # cannons right:
        boardSquaresArray[7][ 8].shoreBatt = 0  # must be R squares, not G squares 
        boardSquaresArray[7][ 9].shoreBatt = 0  # must be R squares, not G squares
        boardSquaresArray[7][10].shoreBatt = 1  # must be R squares, not G squares
        boardSquaresArray[7][11].shoreBatt = 1  # must be R squares, not G squares
        boardSquaresArray[7][12].shoreBatt = 1  # must be R squares, not G squares 
        # mines (3, can't have three in a row)
        dieRoll = random.randint(1, 6)   # Return a random integer N such that 1 <= N <= 6
        print("2nd dieRoll =",dieRoll)   # debug
        if dieRoll <= 3:
            boardSquaresArray[5][ 2].mine = 1  
            boardSquaresArray[5][ 3].mine = 0  
            boardSquaresArray[5][ 4].mine = 0  
            boardSquaresArray[5][ 9].mine = 1  
            boardSquaresArray[5][10].mine = 0  
            boardSquaresArray[5][11].mine = 1  
        else:
            boardSquaresArray[5][ 2].mine = 1  
            boardSquaresArray[5][ 3].mine = 0  
            boardSquaresArray[5][ 4].mine = 0  
            boardSquaresArray[5][ 9].mine = 0  
            boardSquaresArray[5][10].mine = 1  
            boardSquaresArray[5][11].mine = 1  
    elif dieRoll <= 6:
        AI_Strategy = 3  # plug entrances to prevent incursion, chase any breaches. Or set a trap? how? (left side full clog?)
        print("AI_Strategy =",AI_Strategy)   
        # cannons left:
        boardSquaresArray[7][ 1].shoreBatt = 1  # must be R squares, not G squares
        boardSquaresArray[7][ 2].shoreBatt = 1  # must be R squares, not G squares
        boardSquaresArray[7][ 3].shoreBatt = 1  # must be R squares, not G squares
        boardSquaresArray[7][ 4].shoreBatt = 0  # must be R squares, not G squares
        boardSquaresArray[7][ 5].shoreBatt = 0  # must be R squares, not G squares
        # cannons right:
        boardSquaresArray[7][ 8].shoreBatt = 0  # must be R squares, not G squares 
        boardSquaresArray[7][ 9].shoreBatt = 0  # must be R squares, not G squares
        boardSquaresArray[7][10].shoreBatt = 1  # must be R squares, not G squares
        boardSquaresArray[7][11].shoreBatt = 1  # must be R squares, not G squares
        boardSquaresArray[7][12].shoreBatt = 1  # must be R squares, not G squares 
        # mines (3, can't have three in a row)
        dieRoll = random.randint(1, 6)   # Return a random integer N such that 1 <= N <= 6
        print("2nd dieRoll =",dieRoll)   # debug
        if dieRoll <= 3:
            boardSquaresArray[5][ 2].mine = 0  
            boardSquaresArray[5][ 3].mine = 0  
            boardSquaresArray[5][ 4].mine = 1  
            boardSquaresArray[5][ 9].mine = 0  
            boardSquaresArray[5][10].mine = 1  
            boardSquaresArray[5][11].mine = 1  
        else:
            boardSquaresArray[5][ 2].mine = 0  
            boardSquaresArray[5][ 3].mine = 0  
            boardSquaresArray[5][ 4].mine = 1  
            boardSquaresArray[5][ 9].mine = 1  
            boardSquaresArray[5][10].mine = 0  
            boardSquaresArray[5][11].mine = 1  

    print("")
    print("print boardSquaresArray rows 5 & 7:")
    print("r,c","\t","t,c/m")
    j = 5   # rows
    for i in range(15):   # cols
        print(boardSquaresArray[j][i].row_num,boardSquaresArray[j][i].col_num,"\t",boardSquaresArray[j][i].terrain,boardSquaresArray[j][i].mine)
    print("")
    j = 7   # rows
    for i in range(15):   # cols
        print(boardSquaresArray[j][i].row_num,boardSquaresArray[j][i].col_num,"\t",boardSquaresArray[j][i].terrain,boardSquaresArray[j][i].shoreBatt)


#########################################################
def init_AI_RoteMoveList():
    print("")
    print("# init_AI_RoteMoveList #")   
    # RH create another set of moves for 'laid back' defenseive strategy?

    # AI ship starting positions:
    # r c   Num
    # 1 2   11   # 3
    # 1 4   12   # 1 merc prot
    # 1 5   13   # 3
    # 1 6   14   # 1 merc prot
    # 1 7   15   # 1 merc prot
    # 1 8   16   # 2
    # 1 9   17   # 3 
    # 1 10  18   # 1 merc prot
    # 1 11  19   # 3
    # 1 12  20   # 2

    global AIroteMoveIndex
    global AIroteMoveIndexSize
    AIroteMoveIndex  = 0
    AIroteMoveIndexSize = 41

    global ai_moves
    ai_moves = np.zeros((AIroteMoveIndexSize,4))  # rows, columns
    ai_moves = [
    ## 0  1  2  3
    #[ 1,11, 6,11],  # 0  # defensive
    #[ 1,11, 4,11],  # 1  # defensive, in case 6,11 doesn't work 
    #[ 1,12, 4,12],  # 2  # Move to block entry
    #[ 1, 8, 6, 8],  # 3  # Move to block entry
    #[ 1, 5, 6, 5],  # 4  # Move to block entry
    #[ 1, 9, 3, 9],  # 5  # defensive row coverage
    #[ 1, 2, 2, 2],  # 6  # defensive
    #[ 1, 7, 1, 8],  # 7  # merch protect
    #[ 1, 6, 1, 7],  # 8  # merch protect ????
    #[ 1, 7, 1, 6],  # 9  # merch protect (to align facing out)
    #[ 3, 9, 3, 4],  #10  # defensive ??
    #[ 2, 2, 2, 4],  #11  # defensive
    #[ 4,12, 4, 5],  #12  # defensive
    #[ 3, 4, 3, 9],  #13  # defensive
    #[ 2, 4, 2, 2],  #14  # defensive
    #[ 4, 5, 4,12],  #15  # defensive
    #[ 3, 9, 3, 4],  #16  # defensive
    #[ 2, 2, 2, 4],  #17  # defensive
    #[ 4,12, 4, 5],  #18  # defensive
    #[ 3, 4, 3, 9],  #19  # defensive
    #[ 2, 4, 2, 2],  #20  # defensive
    #[ 4, 5, 4,12],  #21  # defensive
    #[ 3, 9, 3, 4],  #22  # defensive
    #[ 2, 2, 2, 4],  #23  # defensive
    #[ 4,12, 4, 5],  #24  # defensive
    #[ 3, 4, 3, 9],  #25  # defensive
    #[ 2, 4, 2, 2],  #26  # defensive
    #[ 4, 5, 4,12],  #27  # defensive
    #[ 3, 9, 3, 4],  #28  # defensive
    #[ 2, 4, 2, 2],  #29  # defensive
    #[ 4,12, 4, 5]   #30  # defensive
    #]

    #global ai_moves2
    #ai_moves2 = np.zeros((AIroteMoveIndexSize,4))  # rows, columns
    #ai_moves2 = [
    # 0  1  2  3
    [ 1,12, 6,12],  # 1  # Move to block entry
    [ 6,12, 6,11],  # 2  # Move to block entry 2
    [ 1,11, 4,11],  # 3  # defensive row coverage (4)
    [ 1, 8, 6, 8],  # 4  # Move to block entry
    [ 6, 8, 6, 9],  # 5  # Move to block entry 2
    [ 1, 5, 6, 5],  # 6  # Move to block entry
    [ 6, 5, 6, 4],  # 7  # Move to block entry 2
    [ 1, 2, 6, 2],  # 8  # Move to block entry
    [ 1, 2, 2, 2],  # 9  # defensive row coverage (2)
    [ 1, 9, 1, 8],  #10  # merch protect
    [ 1, 7, 3, 7],  #11  # defensive row coverage (3)
    [ 2, 2, 6, 2],  #12  # Move to block entry
    [ 2, 2, 2, 1],  #13  # defensive
    [ 2, 1, 6, 1],  #14  # Move to block entry
    [ 6, 1, 6, 2],  #15  # Move to block entry 2
    [ 1, 6, 1, 7],  #16  # merch protect ?
    [ 1, 7, 1, 6],  #17  # merch protect (to align facing out)
    [ 1,10, 1, 9],  #18  # merch protect ?
    [ 1, 9, 1,10],  #19  # merch protect (to align facing out)
    [ 1, 4, 1, 5],  #20  # merch protect ?
    [ 1, 5, 1, 4],  #21  # merch protect (to align facing out)
    [ 4,11, 4, 2],  #22  # defensive time kill
    [ 3, 9, 3,11],  #23  # defensive time kill
    [ 4, 2, 4, 4],  #24  # defensive time kill
    [ 3,11, 3, 9],  #25  # defensive time kill
    [ 4, 4, 4,11],  #26  # defensive time kill
    [ 3, 9, 3, 4],  #27  # defensive time kill
    [ 4,11, 4, 2],  #28  # defensive time kill
    [ 3, 4, 3, 9],  #29  # defensive time kill
    [ 4, 2, 4, 4],  #30  # defensive time kill
    [ 3, 9, 3,11],  #31  # defensive time kill
    [ 4, 4, 4, 9],  #32  # defensive time kill
    [ 3,11, 3, 2],  #33  # defensive time kill
    [ 4, 9, 4,11],  #34  # defensive time kill
    [ 3, 2, 3, 4],  #35  # defensive time kill
    [ 4,11, 4, 9],  #36  # defensive time kill
    [ 3, 4, 3,11],  #37  # defensive time kill
    [ 4, 9, 4, 2],  #38  # defensive time kill
    [ 3,11, 3, 9],  #39  # defensive time kill
    [ 4, 2, 4, 4],  #40  # defensive time kill
    [ 3, 9, 3,11]   #40  # defensive time kill
    ]

    print("")
    print("# ai_moves list (defensive)")
    for i in range(AIroteMoveIndexSize):    # includes test move 0
        print("ai_moves =",i,"\t",ai_moves[i])
    #print("")
    #print("# ai_moves2 list (defensive)")
    #for i in range(AIroteMoveIndexSize):    # includes test move 0
    #    print("ai_moves2 =",i,"\t",ai_moves2[i])

    AIroteMoveIndex  = 0

# end init_AI_RoteMoveList()


#########################################################
def AItargetPriorityListSetup():
    ## AItargetPriorityList array creation
    print("")
    print("# AItargetPriorityListSetup...")
    global AItargetPriorityListIndex
    global AItargetPriorityListIndexSize
    global AItargetPriorityList
    AItargetPriorityListIndex  = 1
    AItargetPriorityListIndexSize = 11   # 10?  use 0 for swap space during sorting (or use AItargetPriorityListTemp?)
    AItargetPriorityList = np.zeros((AItargetPriorityListIndexSize,2), dtype=int)    # ship_num, priority level
    # debug
    print("")
    for i in range (AItargetPriorityListIndexSize):
        print("AItargetPriorityList =",i,"\t",AItargetPriorityList[i])
    print("")


#########################################################
def AItargetPriorityListInit():
    # clears the list to all zeros
    print("")
    print("# AItargetPriorityListInit...")
    global AItargetPriorityListIndex
    global AItargetPriorityListIndexSize
    global AItargetPriorityList
    for i in range (AItargetPriorityListIndexSize):
        AItargetPriorityList[i] = [0,0]    # ship_num, priority level

    AItargetPriorityListIndex  = 1
    print("AItargetPriorityListIndex =",AItargetPriorityListIndex)
    #for i in range (AItargetPriorityListIndexSize):
    #    print("AItargetPriorityList =",i,"\t",AItargetPriorityList[i])


#########################################################
def AImoveScoreListSetup():
    ## AImoveScoreList array creation
    print("")
    print("# AImoveScoreListSetup...")
    global AImoveScoreList
    global AImoveScoreListIndex
    global AImoveScoreListIndexSize
    global AIattackScoreList

    AImoveScoreListIndex  = 1
    AImoveScoreListIndexSize = 200    # was 512, 41, 128. Is this large enough? 700? 100 ok? so far: 56, 92, 128...
    AImoveScoreList = np.zeros((AImoveScoreListIndexSize,5), dtype=int)  # starting row, column, dest row, column, score
    AIattackScoreList = np.zeros((AImoveScoreListIndexSize,5), dtype=int)  # starting row, column, dest row, column, score
    #print("")
    #for i in range (AImoveScoreListIndexSize):
    #    print("AImoveScoreList =",i,"\t",AImoveScoreList[i])
    #print("")

#########################################################
def AImoveScoreListInit():
    # clears the list to all zeros
    print("")
    print("# AImoveScoreListInit...")
    global AImoveScoreList
    global AImoveScoreListIndex
    global AImoveScoreListIndexSize
    global AImoveScoreListIndexMax
    global AIattackScoreList

    AImoveScoreListIndexMax  = 1
    print("AImoveScoreListIndexMax =",AImoveScoreListIndexMax)

    for i in range (AImoveScoreListIndexSize):
        AImoveScoreList[i] = [0,0,0,0,0]
        AIattackScoreList[i] = [0,0,0,0,0]
    # debug
    #for i in range (AImoveScoreListIndexSize):
    #    print("AImoveScoreList =",i,"\t",AImoveScoreList[i])
    #print("")


#########################################################
def moveScore():    # various inputs, returns AImoveScore
    print("")
    print("##--- moveScore ---##")

    global sq_row      # ship to move
    global sq_col
    global new_sq_row  # destination
    global new_sq_col
    global enemy_row
    global enemy_col
    global numInRow
    global numShipsBlue

    global mercCovered    # set in Computer_AI()

    global moveValid   # set by moveCheck

    global AImoveScore
    global AImoveScoreList
    global AImoveScoreListIndex
    global AImoveScoreListIndexSize
    global AImoveScoreListIndexMax

    global AIattackScoreList

    global score_block_R1
    global score_block_R2
    global score_cover_open_row
    global score_cover_merch
    global score_uncover_merch
    global score_uncover_R1
    global score_move_into_T
    global score_block_entrance

    # handled in Computer_AI() for now...
    #AImoveScore = 0   # used to find best move based on 'score' for various attributes

    # handled in Computer_AI()
    # see line 2380:
    # move scoring:
    #score_block_R1 = 2
    #score_block_R2 = 1
    #score_uncover_R1 = -1
    #score_cover_open_row = 1
    #score_cover_merch = 6
    #score_uncover_merch = -6
    #score_move_into_T = -1
    #score_block_entrance = 2

    ## how to score moves? criteria?
    # blocking access to mercs
    # covering mercs
    # blocking lanes at entrances
    # free up defenders in entrances
    # move toward red ship if on R1, esp if unguarded merc in between
    # move next to red ship row/column to attack later
    # covering open rows in harbor R1-R4, esp within C2-13
    # moving into attack position, R1 vs R2?
    # time killing moves, safe ones
    # make any move at all if nothing left

    #AImoveScoreList[i][0, 1, 2, 3] = [sq_row, sq_col, new_sq_row, new_sq_col]
    #AImoveScoreList[i][4] = AImoveScore

    # RH debug
    print("sq_row     =",sq_row,"\t","    sq_col =",sq_col)
    print("new_sq_row =",new_sq_row,"\t","new_sq_col =",new_sq_col)

    print("numShipsBlue =",numShipsBlue)
    print("numInRow =",numInRow)
    print("mercCovered[] =",mercCovered)
    #print("mercCovered[sq_col] =",mercCovered[sq_col])
    #print("mercCovered[new_sq_row] =",mercCovered[new_sq_row])
    print("enemy_row =",enemy_row)    # debug

    AImoveScore = AImoveScore + 1    # any valid move gets at least 1 pt
    #print("AImoveScore_1 =",AImoveScore)    # result

    ##RH
    # add merc coverage, esp if ship < 5
    # cover entrance columns, esp if mines gone. c1, c5, c2-4 (mines),c8, c12, c9-11 (mines) 
    # col coverage can be in R2-R4, just don't leave a straight shot to R1
    # find a way to reshuffle merc coverage if needed, use idle ships
    # why killing time along R2? stop it!

    # covering open rows in harbor R1-R4, esp within C2-13
    if numInRow[new_sq_row] == 0 and numInRow[sq_row] > 1 and new_sq_row <= 4:
        AImoveScore = AImoveScore + score_cover_open_row    # +1 pts for covering empty row
        if new_sq_col >= 2 or new_sq_col <= 5:              # esp within C2-5
            AImoveScore = AImoveScore + 1     
        if new_sq_col >= 8 or new_sq_col <= 12:             # esp within C8-12
            AImoveScore = AImoveScore + 1      
        if numInRow[1] >= 5 and sq_row == 1:
            AImoveScore = AImoveScore - score_cover_open_row * 2    # to encourage development of ships more evenly
    print("AImoveScore_0 =",AImoveScore)    # result

    # to encourage development of ships more evenly
    # enemy row = 0 means not in the harbor
    if enemy_row == 0 and numShipsBlue > 7 and numInRow[1] >= 5 and sq_row == 1 and new_sq_row > 1:
        AImoveScore = AImoveScore + score_cover_open_row * 2    # to encourage development of ships more evenly
    print("AImoveScore_1 =",AImoveScore)    # result

    # uncovering a row in harbor R1-R4 (bad)
    if sq_row <= 4 and numInRow[sq_row] == 1 and new_sq_row != sq_row:
        AImoveScore = AImoveScore - score_cover_open_row        # -1 pts for uncovering a row
        if numInRow[new_sq_row] >= 1:
            AImoveScore = AImoveScore - score_cover_open_row    # -1 pts for moving to a row that is already covered
    print("AImoveScore_2 =",AImoveScore)    # result

    # moving a ship on row 1 to a different row & uncovering a merchant ship (very bad)
    if sq_row == 1 and new_sq_row > 1 and mercCovered[sq_col] == 1:
        #AImoveScore = AImoveScore + score_uncover_R1
        AImoveScore = AImoveScore + score_uncover_merch    # -6
        if numShipsBlue < 6:
            AImoveScore = AImoveScore + score_uncover_merch    # -6
            print("numShipsBlue < 6 move score adjustment")
    print("AImoveScore_3 =",AImoveScore)    # result

    # moving a ship on row 1 to a different column & uncovering a merchant ship (very bad)
    if sq_row == 1 and new_sq_row == 1:
        if mercCovered[sq_col] == 1 and mercCovered[new_sq_col] != 0:    # 0 = uncovered merc
            AImoveScore = AImoveScore + score_uncover_merch    # -6
            if numShipsBlue < 6:
                AImoveScore = AImoveScore + score_uncover_merch    # -6
                print("numShipsBlue < 6 move score adjustment")
    print("AImoveScore_4 =",AImoveScore)    # result

    # moving a ship on row 1 to a different row if Red @ R1 (very bad)
    if enemy_row == 1 and sq_row == 1 and new_sq_row > 1 and numInRow[1] < 5:
        AImoveScore = AImoveScore + score_uncover_R1 * 4
    # moving to row 2 from another row if red @ R1 (block?)
    elif enemy_row == 1 and new_sq_row == 2 and numInRow[1] >= 5:
        AImoveScore = AImoveScore + score_block_R2
    print("AImoveScore_5 =",AImoveScore)    # result

    # moving to row 1 from another row if red @ R1 (good)
    if enemy_row == 1 and sq_row > 1 and new_sq_row == 1:
        AImoveScore = AImoveScore + score_block_R1 * 2       # +2 * 2 = 4, update score?
        if new_sq_col <= enemy_col + 2 and new_sq_col >= enemy_col - 2:
            AImoveScore = AImoveScore + score_block_R1       # new score value? 
        # merc covering code:
        if mercCovered[new_sq_col] == 0:
            AImoveScore = AImoveScore + score_cover_merch    # +6 for covering merchant ships if red on row 1
    print("AImoveScore_6 =",AImoveScore)    # result

    # moving to row 2 from another row if red @ R2 (block?)
    if enemy_row == 2 and numInRow[1] >= 5 and sq_row != 2 and new_sq_row == 2:
        AImoveScore = AImoveScore + score_block_R2        # +1 pts for covering row 2
        if new_sq_col <= enemy_col + 2 and new_sq_col >= enemy_col - 2:
            AImoveScore = AImoveScore + score_block_R2
    elif enemy_row == 2 and sq_row > 2 and new_sq_row == 2:
        AImoveScore = AImoveScore + score_block_R2 * 2    # +2 pts for covering row 2
        if new_sq_col <= enemy_col + 2 and new_sq_col >= enemy_col - 2:
            AImoveScore = AImoveScore + score_block_R2    # new score value? 
    print("AImoveScore_7 =",AImoveScore)    # result

    # move toward red ship if on R1, esp if unguarded merc in between, mercCovered[i] ??
    # move in between red & merc
    if enemy_row == 1 and sq_row == 1 and new_sq_row == 1:
    #if enemy_row == 1 and new_sq_row == 1:
        if new_sq_col <= enemy_col + 2 and new_sq_col >= enemy_col - 2:
            AImoveScore = AImoveScore + score_block_R1    # new score value? 
        if mercCovered[new_sq_col] == 0:
            AImoveScore = AImoveScore + score_cover_merch    # +6 pts for covering merchant ships
    print("AImoveScore_8 =",AImoveScore)    # result

    # check for entrance blocking
    # if no red ships are in the harbor (row = 0)
    if enemy_row == 0 and numShipsBlue > 6 and sq_row < 6 and new_sq_row == 6:
        if new_sq_col >= 2 and new_sq_col <= 4 and terrain[5][new_sq_col] != 'M':
            AImoveScore = AImoveScore + score_block_entrance * 2    # 2 * 2 pts
        elif new_sq_col >= 1 and new_sq_col <= 5:
            AImoveScore = AImoveScore + score_block_entrance
        if new_sq_col >= 9 and new_sq_col <= 11 and terrain[5][new_sq_col] != 'M':
            AImoveScore = AImoveScore + score_block_entrance * 5
        elif new_sq_col >= 8 and new_sq_col <= 12:
            AImoveScore = AImoveScore + score_block_entrance * 2
        if numInRow[sq_row] == 1 or numInRow[new_sq_row] > 1:    # would uncover the row, or ship already in dest row
            AImoveScore = AImoveScore - score_cover_open_row * 2
    elif enemy_row == 0 and numShipsBlue > 6 and sq_row < 4 and new_sq_row == 4:
        if new_sq_col >= 2 and new_sq_col <= 4 and terrain[5][new_sq_col] != 'M':
            AImoveScore = AImoveScore + score_block_entrance * 2
        elif new_sq_col >= 1 and new_sq_col <= 5:
            AImoveScore = AImoveScore + score_block_entrance
        if new_sq_col >= 9 and new_sq_col <= 11 and terrain[5][new_sq_col] != 'M':
            AImoveScore = AImoveScore + score_block_entrance * 2
        elif new_sq_col >= 8 and new_sq_col <= 12:
            AImoveScore = AImoveScore + score_block_entrance + 1
        if numInRow[sq_row] == 1 or numInRow[new_sq_row] > 1:    # would uncover the row, or ship already in dest row
            AImoveScore = AImoveScore - score_cover_open_row * 2
    elif enemy_row == 0 and new_sq_row >= 2 and new_sq_row <= 4:
        if new_sq_col >= 2 and new_sq_col <= 4 and terrain[5][new_sq_col] != 'M':
            AImoveScore = AImoveScore + score_block_entrance + 1
        elif new_sq_col >= 1 and new_sq_col <= 5:
            AImoveScore = AImoveScore + score_block_entrance
        if new_sq_col >= 9 and new_sq_col <= 11 and terrain[5][new_sq_col] != 'M':
            AImoveScore = AImoveScore + score_block_entrance + 1
        elif new_sq_col >= 8 and new_sq_col <= 12:
            AImoveScore = AImoveScore + score_block_entrance
        if numInRow[sq_row] == 1:                                # would uncover the row
            AImoveScore = AImoveScore - score_cover_open_row * 2
    # check for entrance blocking even if red in harbor
    elif enemy_row > 0 and numShipsBlue > 6 and new_sq_row == 6:
        if new_sq_col >= 2 and new_sq_col <= 4 and terrain[5][new_sq_col] != 'M':
            AImoveScore = AImoveScore + score_block_entrance * 2    # 2 * 2 = 4 pts
        elif sq_row < 6 and new_sq_col >= 1 and new_sq_col <= 5:
            AImoveScore = AImoveScore + score_block_entrance
        elif new_sq_col >= 9 and new_sq_col <= 11 and terrain[5][new_sq_col] != 'M':
            AImoveScore = AImoveScore + score_block_entrance * 2
        elif sq_row < 6 and new_sq_col >= 8 and new_sq_col <= 12:
            AImoveScore = AImoveScore + score_block_entrance
    # check for entrance blocking ships to recover for defense in R1-R4
    elif enemy_row > 0 and numShipsBlue <= 6 and sq_row == 6:
        if new_sq_col == 1 or new_sq_col == 5:
            AImoveScore = AImoveScore + score_block_entrance
        if new_sq_col == 8 or new_sq_col == 12:
            AImoveScore = AImoveScore + score_block_entrance
    print("AImoveScore_9 =",AImoveScore)    # result

    # moving a ship to cover a merchant ship column (or ship)
    if sq_row < 6 and mercCovered[new_sq_col] == 0:         # merchant ship uncovered in column, move to that column
        AImoveScore = AImoveScore + score_cover_merch       # +6
    if new_sq_row == 1 and mercCovered[new_sq_col] == 0:    # cover merc
        AImoveScore = AImoveScore + score_cover_merch       # +6
        if mercCovered[sq_col] == 1 and sq_col >= 6 and sq_col <= 8:
            AImoveScore = AImoveScore + 1    # encourage moving from center columns
    print("AImoveScore_10 =",AImoveScore)    # result

    print("AImoveScore_Final =",AImoveScore)    # result
    #print("")

    # max AImoveScoreListIndexMax:
    #print("")  # debug
    #print("AImoveScoreListIndex =",AImoveScoreListIndex)
    if AImoveScoreListIndex > AImoveScoreListIndexMax:
        AImoveScoreListIndexMax = AImoveScoreListIndex    # to debug max move list size needed
    print("AImoveScoreListIndexMax =",AImoveScoreListIndexMax)



#########################################################
def Computer_AI():                    # AI move & attack
    # return sq_row, sq_col, new_sq_row, new_sq_col, shipSelected
    print("")
    print("##--- Computer_AI ---##")

    #global delay
    global shipNum
    global targetShipNum # used by priority list approach
    global shipSelected  # needed for moveShip
    global sq_row      # ship to move
    global sq_col
    global new_sq_row  # destination
    global new_sq_col
    global enemy_row
    global enemy_col
    global numInRow
    global numShipsBlue
    global leftRight

    global mercCovered

    global allMercsCovered

    global moveValid   # set by moveCheck
    global playerTurn   # 1 (human) or -1 (computer)
    global turnNum

    global AItargetPriorityList
    global AItargetPriorityListIndex
    global AItargetPriorityListIndexSize

    global AImoveScoreList
    global AImoveScoreListIndex
    global AImoveScoreListIndexSize
    global AImoveScoreListIndexMax

    global AIattackScoreList

    global AIroteMoveIndex    # used by rote move list if no other moves found

    global AImoveScore

    # RH move this to ai moveScore?
    global score_block_R1
    global score_block_R2
    global score_cover_open_row
    global score_cover_merch
    global score_uncover_merch
    global score_uncover_R1
    global score_move_into_T
    global score_block_entrance

    # RH debug only:
    global MsgFlag
    global MsgText


    # target scoring:
    # +5 for row 1 red ships
    # +3 for row 2 red ships
    # +1 for red ships in the harbor (rows 3 to 6)
    # +1 if only one mast on red ship

    # move scoring:
    # raise these scores?
    # +5 for blocking red ships on row 1, i.e. moving in between red & merchant

    # target scoring:
    score_R1 = 5
    score_R2 = 3
    score_harbor = 1    # row_num > 2
    score_1_mast = 2
    score_T_atk  = 1

    # move scoring:
    score_block_R1 = 2
    score_block_R2 = 1
    score_uncover_R1 = -1
    score_cover_open_row = 1
    score_cover_merch = 6
    score_uncover_merch = -6
    score_move_into_T = -1
    score_block_entrance = 2

    enemy_row = 0
    enemy_col = 0

    #harborCheckedforRedScum = 0
    RedScuminHarbor = 0
    targetShipNum = 0
    algoMoveChecked = 0

    allMercsCovered = 1    # set to 0 if any found uncovered (keep this or find a way to remove?) mercCovered[]

    # Computer_AI:
    # make initial moves by rote, unless Red fleet enters harbor...
    # place a ship on each row to defend harbor
    # place ships in front of merchant ships
    # check moves to avoid turning into a T attack (if red in harbor)

    # Priorities:
    # 1. defend merchant ships (block access? ship across bow of merch) esp col 8/10
    # 2. look for T attack
    # 3. avoid being T attacked or moving into T attack
    # 4. sink single masted Red ships
    # 5. defend the harbor, ship on each row at all times! steal from entrance blockers if needed

    # Computer_AI new:

    # update flow to prioritize merchant protection!! Add new section to check all moves

    # find & prioritize targets first(??), then look for moves to attack them, else use rote list
    # target priority 'score': based on row for now, +1 for only one mast (sink it!)
    # add move scoring system to find better moves
    # add target priority score to move score for overall score (test for now...)

    # move score: also check row 1, row 2, for merchant coverage or blocking moves
    # P1, R1/2, P2, P3, rote moves ?
    # What is priority order in code? change flow to score based?

    # check for attacks on red ship? esp if only one mast (already covered in target priority)
    # don't uncover a merchant ship if possible
    # check if mercs are covered or not, attack red ship if covered? from a different row?
    # if all else fails, put a ship on row 1 from col 9 or any other column just to block part of the row
    # block row 2 when red in harbor

    # add new tree to check for Red at row 1 & attack, or else cover merchs
    # if red has one mast, can it be attacked? (killed)
    # if > 1 mast, are merch blocked from access? if no, block. If yes, attack red ship if possible
    # if red @ row 2, can destroy ships covering merchants! must attack or block!

    AImoveScore = 0   # used to find best move based on 'score' for various attributes

    AItargetPriorityListInit()   # clear list for new turn
    AItargetPriorityListIndex  = 1

    AImoveScoreListInit()   # clear list for new turn
    AImoveScoreListIndex  = 1

    # how many blue ships left?
    #print("")
    print("# Computer_AI: check for how many blue ships left...")
    numShipsBlue = 0              
    for i in range (11,21):       # check pieceArray from 11 to 20
        if pieceArray[i].shipType == 2 and pieceArray[i].p_row_num > 0:
            numShipsBlue = numShipsBlue + 1
            #print("numShipsBlue =",numShipsBlue)
    print("  numShipsBlue final =",numShipsBlue)

    # check for empty rows (blue) 
    print("# Computer_AI: check for empty rows in the harbor...")
    numInRow = [0,0,0,0,0,0,0]    # 7 members for rows 1 - 6
    for i in range (11,21):       # check pieceArray from 11 to 20
        for j in range (1,7):     # for rows 1 - 6
            if pieceArray[i].p_row_num == j:
                numInRow[j] = numInRow[j] + 1
    print("  numInRow[] =",numInRow)

    # are merchant ships covered? change to list by column # (0 thru 14)
    print("")
    print("# Computer_AI: are merchant ships covered?")
    mercCovered = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]    # declare list
    for i in range (15):          # check terrain in all columns
        if terrain[0][i] == "L":
            mercCovered[i] = 2    # 3 = empty, 2 = not a port
        elif terrain[0][i] == "P":
            mercCovered[i] = 3    # 3 = empty, 2 = not a port
    print("mercCovered[] init =",mercCovered)
    for i in range (4,12,2):    # for cols 4,6,8,10
        #print("i =",i)
        # check port for merchant
        if boardSquaresArray[0][i].shipNum == 0:      # no merchant in that port square, empty port
            mercCovered[i] = 3                        # 3 = empty
        # check square in front of port for ship type
        elif boardSquaresArray[1][i].shipNum == 0:    # no ship in fron of that port square
            mercCovered[i] = 0                        # 0 = merc uncovered!
        elif boardSquaresArray[1][i].shipNum <= 10:   # red ship in fron of that port square
            mercCovered[i] = -1                       # -1 = red ship in front of merc
        elif boardSquaresArray[1][i].shipNum <= 20:   # blue ship in fron of that port square
            mercCovered[i] = 1                        # 1 = merc covered
    print("mercCovered[] =",mercCovered)

    ##RH safe to remove?
    #print("")
    #print("# Computer_AI: are merchant ships covered?")
    #mercCovered = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]  # 3 = empty, 2 = not a port, 1 = merc covered, 0 = merc uncovered!, -1 = red ship in front of merc
    #for i in range (15):   # all columns
    #    mercCovered[i] = 2    # 3 = empty, 2 = not a port, 1 = merc covered, 0 = merc uncovered!, -1 = red ship in front of merc
    ##print("mercCovered[] =",mercCovered)
    #for i in range (4,12,2):    # for cols 4,6,8,10
    #    for j in range (1,pieceNum + 1):
    #        if pieceArray[j].p_row_num == 0 and pieceArray[j].p_col_num == i:
    #            if pieceArray[j].shipType == 0:      # no merchant in that port square, empty port
    #                mercCovered[i] = 3               ##RH experimental, empty = 3
    #                #mercCovered[i] = 1
    #            elif pieceArray[j].shipType == 3:    # merchant in that port square, covered?
    #                for k in range (1,pieceNum + 1):
    #                    if pieceArray[k].p_row_num == 1 and pieceArray[k].p_col_num == i:    # check row 1
    #                        if pieceArray[k].shipType == 0:     # row 1 empty square, merc uncovered!
    #                            mercCovered[i] = 0
    #                        elif pieceArray[k].shipType == 1:   # row 1 red ship in front of merchant!
    #                            mercCovered[i] = -1
    #                        elif pieceArray[k].shipType == 2:   # row 1 blue ship covering merchant
    #                            mercCovered[i] = 1              # we're good, not to worry!
    #print("mercCovered[] =",mercCovered)

    # create AItargetPriorityList with scores
    print("")
    print("# Computer_AI: fill in AItargetPriorityList...")    ## fill in based on red ship positions, masts
    print("# checking for Red scum in the harbor...")
    for n in range (1,11):  # search by ship, check red fleet (1-10)
        if pieceArray[n].p_row_num > 0 and pieceArray[n].p_row_num < 7:  # check for red ships in the harbor
            RedScuminHarbor = 1
            print("# Red fleet found in the harbor!!")
            if pieceArray[n].p_row_num == 1:
                AItargetPriorityList[n] = [n,score_R1]
            elif pieceArray[n].p_row_num == 2:
                AItargetPriorityList[n] = [n,score_R2]
            elif pieceArray[n].p_row_num > 2:
                AItargetPriorityList[n] = [n,score_harbor]
            #print("AItargetPriorityList[n] =",n,"\t",AItargetPriorityList[n])
            if pieceArray[n].num_masts == 1:
                AItargetPriorityList[n][1] = AItargetPriorityList[n][1] + score_1_mast
                #print("one mast: AItargetPriorityList[n] =",n,"\t",AItargetPriorityList[n])
    #print("")
    #print("print AItargetPriorityList...")
    #for i in range (AItargetPriorityListIndexSize):
    #    print("AItargetPriorityList =",i,"\t",AItargetPriorityList[i])
    #print("")
    print("sort AItargetPriorityList...")
    for i in range (1,AItargetPriorityListIndexSize):     # use index 1 since 0 used for sorting (swap space)
        for n in range (1,AItargetPriorityListIndexSize-1):  # use 1-9 since 10 covered by that range. check red fleet (1-10)
                if  AItargetPriorityList[n][1]  < AItargetPriorityList[n + 1][1]:
                    AItargetPriorityList[0]     = AItargetPriorityList[n]
                    AItargetPriorityList[n]     = AItargetPriorityList[n + 1]
                    AItargetPriorityList[n + 1] = AItargetPriorityList[0]     # copy of n
    #print("")
    print("print AItargetPriorityList...")
    for i in range (AItargetPriorityListIndexSize):
        print("AItargetPriorityList =",i,"\t",AItargetPriorityList[i])


    #-------------------

    pygame.event.clear()  # clear any pending events
    run_def_AI = True
    print("")

    while run_def_AI:

        #run_def_AI = False   # ends the while loop! RH
        #break    # exit for loop

        if RedScuminHarbor == 1 or algoMoveChecked == 1:    # no valid algo move or Red fleet found in the harbor!! can we attack?

        #if harborCheckedforRedScum == 0:    # if harbor already checked, skip this first section to save time...
            #print("# checking for Red fleet inside the harbor...")

            ## use AItargetPriorityList to check for attack moves against top priority targets
            #print("")
            print("# Checking AItargetPriorityList...")
            for n in range (1,11):
                if AItargetPriorityList[n][1] > 0:
                    print("")
                    print("found a Red scum ship inside the harbor!")
                    targetShipNum   = AItargetPriorityList[n][0]
                    enemy_row       = pieceArray[targetShipNum].p_row_num
                    enemy_col       = pieceArray[targetShipNum].p_col_num
                    print("targetShipNum =",targetShipNum)
                    print("shipSelected.num_masts =",pieceArray[targetShipNum].num_masts)
                    print("shipSelected.p_row_num =",pieceArray[targetShipNum].p_row_num)
                    print("shipSelected.p_col_num =",pieceArray[targetShipNum].p_col_num)

                    print("")
                    print("# checking for attacks against Red scum...")
                    print("targetShipNum =",targetShipNum)
                    for j in range (11,21):  # search by ship, check blue fleet (11-20)
                        print("blue ship =",j)   # debug for break
                        print("pieceArray[j].p_row_num =",pieceArray[j].p_row_num)
                        print("pieceArray[j].p_col_num =",pieceArray[j].p_col_num)
                        if pieceArray[j].p_row_num > 0:    # skip dead ships...
                            if pieceArray[j].p_row_num == enemy_row - 1 or pieceArray[j].p_row_num == enemy_row + 1:  # check for blue ships in adjacent row
                                new_sq_row = pieceArray[j].p_row_num    # experimental
                                new_sq_col = enemy_col
                                sq_row = pieceArray[j].p_row_num
                                sq_col = pieceArray[j].p_col_num
                                moveCheck()
                                if moveValid == 1:
                                    AImoveScoreList[AImoveScoreListIndex] = [sq_row,sq_col,new_sq_row,new_sq_col,AItargetPriorityList[n][1]]   # ,1 ?
                                    AIattackScoreList[AImoveScoreListIndex] = [sq_row,sq_col,new_sq_row,new_sq_col,AItargetPriorityList[n][1]]   # ,1 ?
                                    if pieceArray[targetShipNum].direction == 0 or pieceArray[targetShipNum].direction == 180:   # was n
                                        AImoveScoreList[AImoveScoreListIndex][4] = AImoveScoreList[AImoveScoreListIndex][4] + score_T_atk    # +1
                                        AIattackScoreList[AImoveScoreListIndex][4] = AImoveScoreList[AImoveScoreListIndex][4] + score_T_atk
                                    print("")
                                    print("AImoveScoreListIndex =",AImoveScoreListIndex)
                                    print("AImoveScoreList[j] =",AImoveScoreList[AImoveScoreListIndex])
                                    AImoveScoreListIndex = AImoveScoreListIndex + 1
                                    #print("")
                                    #print("print AImoveScoreList...")
                                    #for i in range (AImoveScoreListIndexSize):
                                    #    print("AImoveScoreList =",i,"\t",AImoveScoreList[i])
                            if pieceArray[j].p_col_num == enemy_col - 1 or pieceArray[j].p_col_num == enemy_col + 1:  # check for blue ships in adjacent col
                                new_sq_row = enemy_row
                                new_sq_col = pieceArray[j].p_col_num
                                sq_row = pieceArray[j].p_row_num
                                sq_col = pieceArray[j].p_col_num
                                moveCheck()
                                if moveValid == 1:
                                    AImoveScoreList[AImoveScoreListIndex] = [sq_row,sq_col,new_sq_row,new_sq_col,AItargetPriorityList[n][1]]   # ,1 ?
                                    AIattackScoreList[AImoveScoreListIndex] = [sq_row,sq_col,new_sq_row,new_sq_col,AItargetPriorityList[n][1]]   # ,1 ?
                                    if pieceArray[targetShipNum].direction == 90 or pieceArray[targetShipNum].direction == 270:
                                        AImoveScoreList[AImoveScoreListIndex][4] = AImoveScoreList[AImoveScoreListIndex][4] + score_T_atk    # +1
                                        AIattackScoreList[AImoveScoreListIndex][4] = AImoveScoreList[AImoveScoreListIndex][4] + score_T_atk
                                    print("")
                                    print("AImoveScoreListIndex =",AImoveScoreListIndex)
                                    print("AImoveScoreList[j] =",AImoveScoreList[AImoveScoreListIndex])
                                    AImoveScoreListIndex = AImoveScoreListIndex + 1
                                    #print("")
                                    #print("print AImoveScoreList...")
                                    #for i in range (AImoveScoreListIndexSize):
                                    #    print("AImoveScoreList =",i,"\t",AImoveScoreList[i])

                    # end for loop checking for attacks against Red scum

                    #-------------------------------
                    ##  Merchant Ship Protection  ##
                    #-------------------------------
                    # modify attack scores based on effect on merchant protection...   
                    # this needs work...

                    #AImoveScoreList[i][0, 1, 2, 3] = [sq_row, sq_col, new_sq_row, new_sq_col]
                    print("")
                    print("# modify attack scores for merchant protection...")
                    for i in range (1,AImoveScoreListIndexSize):
                        if AImoveScoreList[i][0] == 1 and AImoveScoreList[i][2] == 1:    # moving a ship along row 1
                            if mercCovered[AImoveScoreList[i][1]] == 1 and mercCovered[AImoveScoreList[i][3]] == 0:
                                AImoveScoreList[i][4] = AImoveScoreList[i][4] + score_uncover_merch    # -6 
                                AIattackScoreList[i][4] = AIattackScoreList[i][4] + score_uncover_merch    # -6 
                                if numShipsBlue < 6:
                                    AImoveScoreList[i][4] = AImoveScoreList[i][4] + score_uncover_merch    # -6 
                                    AIattackScoreList[i][4] = AIattackScoreList[i][4] + score_uncover_merch    # -6 
                                    print("numShipsBlue < 6 move score adjustment")

                        if AImoveScoreList[i][0] == 1 and AImoveScoreList[i][2] > 1:    # moving a ship on row 1 to a different row -1
                            AImoveScoreList[i][4] = AImoveScoreList[i][4] + score_uncover_R1    # -1 for uncovering row 1
                            AIattackScoreList[i][4] = AIattackScoreList[i][4] + score_uncover_R1    # -1 for uncovering row 1
                            if mercCovered[AImoveScoreList[i][1]] == 1:
                                AImoveScoreList[i][4] = AImoveScoreList[i][4] + score_uncover_merch    # -6
                                AIattackScoreList[i][4] = AIattackScoreList[i][4] + score_uncover_merch    # -6 
                                if numShipsBlue < 6:
                                    AImoveScoreList[i][4] = AImoveScoreList[i][4] + score_uncover_merch    # -6 
                                    AIattackScoreList[i][4] = AIattackScoreList[i][4] + score_uncover_merch    # -6 
                                    print("numShipsBlue < 6 move score adjustment")

                        if enemy_row == 1 and AImoveScoreList[i][0] > 1 and AImoveScoreList[i][2] == 1:    # moving to row 1 from another row +2
                            AImoveScoreList[i][4] = AImoveScoreList[i][4] + score_block_R1    # +2
                            AIattackScoreList[i][4] = AIattackScoreList[i][4] + score_block_R1
                            if mercCovered[AImoveScoreList[i][3]] == 0:
                                AImoveScoreList[i][4] = AImoveScoreList[i][4] + score_cover_merch    # +6 for covering merchant ships if red on row 1
                                AIattackScoreList[i][4] = AIattackScoreList[i][4] + score_cover_merch    # +6 for covering merchant ships if red on row 1

                        if enemy_row == 2 and AImoveScoreList[i][0] > 2 and AImoveScoreList[i][2] == 2:    # moving to row 2 from another row +1
                            AImoveScoreList[i][4] = AImoveScoreList[i][4] + score_block_R2    # +1 for covering row 2
                            AIattackScoreList[i][4] = AIattackScoreList[i][4] + score_block_R2    # +1 for covering row 2
                            # bonus for moving to >= col 2? so can access R1

                    # end for loop to cover merchant ships
                    print("score adjustments complete!")

                    # debug
                    #print("")
                    #print("print AImoveScoreList...")
                    #for i in range (AImoveScoreListIndexSize):
                    #    #print("AImoveScoreList =",i,"\t",AImoveScoreList[i])
                    #    if AImoveScoreList[i][0] > 0:
                    #        print("AImoveScoreList =",i,"\t",AImoveScoreList[i])

                # end: if target_priority > 0:
            print("## end checking AItargetPriorityList For Loop ##")


            # #-------------------------------
            # # RH debug "atk debug N/y"
            # # do I need this anymore?
            # #if AImoveScoreListIndex > 1:    # valid attack move found
            #   #if moveValid == 1:
            #     MsgFlag = 1   # controls console window at bottom
            #     MsgText = "atk debug N/y"
            #     refreshGameScreen()
            #     #pygame.time.delay(delay*10)
            #     run_debug = True
            #     while run_debug:
            #         for event in pygame.event.get():
            #             if event.type == pygame.QUIT:
            #                 run_debug = False
            #                 pygame.quit()
            #                 sys.exit()
            #             if event.type == pygame.KEYDOWN:
            #                 if event.key == pygame.K_y:
            #                     print("")
            #                     print("debug = Y entered, exiting...")
            #                     print("")
            #                     run_debug = False
            #                     pygame.quit()
            #                     sys.exit()
            #                 if event.key == pygame.K_n or event.key == pygame.K_RETURN:
            #                     print("debug = n entered, continuing...")
            #                     MsgFlag = 0   # controls console window at bottom
            #                     run_debug = False


            ##-----------------------------------------------##
            ##--- Add non-attack moves to AImoveScoreList ---##
            ##-----------------------------------------------##

            print("")
            print("# Add non-attack moves to AImoveScoreList...")

            # update flow to prioritize merchant protection!!
            # add routine to add non-attack moves to list that protect merchants
            # stop looking once you hit an obstacle to not waste time
            # what impact on move list arry? 5 x 14 poss moves? x10 ships? 700??

            # for all blue ships, what possible moves can I make? if valid, run moveScore
            for j in range (11,21):    # check blue fleet (11-20)
                if pieceArray[j].p_row_num > 0:    # skip dead ships
                    sq_row = pieceArray[j].p_row_num    # 0
                    sq_col = pieceArray[j].p_col_num    # 1
                    AImoveScore = 0

                    # RH check moves from one row to another
                    for k in range (sq_row + 1,7):    # up to row 6
                        new_sq_row = k         # 2
                        new_sq_col = sq_col    # 3
                        print("")
                        print("# next move: j=",j,"k=",k," new_sq_row =",new_sq_row,"new_sq_col =",new_sq_col)
                        moveCheck()
                        if moveValid == 1:
                            AImoveScore = 0    # 4
                            moveScore()
                            AImoveScoreList[AImoveScoreListIndex] = [sq_row,sq_col,new_sq_row,new_sq_col,AImoveScore]
                            print("AImoveScoreList[",AImoveScoreListIndex,"] =",AImoveScoreList[AImoveScoreListIndex])
                            AImoveScoreListIndex = AImoveScoreListIndex + 1
                        elif moveValid == 0:
                            sq_row = pieceArray[j].p_row_num    # 0
                            sq_col = pieceArray[j].p_col_num    # 1
                            break    # exit for loop
                    for k in range (sq_row - 1,0,-1):
                        new_sq_row = k
                        new_sq_col = sq_col
                        print("")
                        print("# next move: j=",j,"k=",k," new_sq_row =",new_sq_row,"new_sq_col =",new_sq_col)
                        #print("j=",j,"k=",k,"new_sq_row =",new_sq_row,"\t","new_sq_col =",new_sq_col)
                        moveCheck()
                        if moveValid == 1:
                            AImoveScore = 0
                            moveScore()
                            AImoveScoreList[AImoveScoreListIndex] = [sq_row,sq_col,new_sq_row,new_sq_col,AImoveScore]
                            print("AImoveScoreList[",AImoveScoreListIndex,"] =",AImoveScoreList[AImoveScoreListIndex])
                            AImoveScoreListIndex = AImoveScoreListIndex + 1
                        elif moveValid == 0:
                            sq_row = pieceArray[j].p_row_num    # 0
                            sq_col = pieceArray[j].p_col_num    # 1
                            break    # exit for loop

                    # RH check moves from one column to another
                    for k in range (sq_col + 1,15):    # up to col 14
                        new_sq_row = sq_row
                        new_sq_col = k
                        print("")
                        print("# next move: j=",j,"k=",k," new_sq_row =",new_sq_row,"new_sq_col =",new_sq_col)
                        #print("j=",j,"k=",k,"new_sq_row =",new_sq_row,"\t","new_sq_col =",new_sq_col)
                        moveCheck()
                        if moveValid == 1:
                            AImoveScore = 0
                            moveScore()
                            AImoveScoreList[AImoveScoreListIndex] = [sq_row,sq_col,new_sq_row,new_sq_col,AImoveScore]
                            print("AImoveScoreList[",AImoveScoreListIndex,"] =",AImoveScoreList[AImoveScoreListIndex])
                            AImoveScoreListIndex = AImoveScoreListIndex + 1
                        elif moveValid == 0:
                            sq_row = pieceArray[j].p_row_num    # 0
                            sq_col = pieceArray[j].p_col_num    # 1
                            break    # exit for loop
                    for k in range (sq_col - 1,-1,-1):
                        new_sq_row = sq_row
                        new_sq_col = k
                        print("")
                        print("# next move: j=",j,"k=",k," new_sq_row =",new_sq_row,"new_sq_col =",new_sq_col)
                        #print("j=",j,"k=",k,"new_sq_row =",new_sq_row,"\t","new_sq_col =",new_sq_col)
                        moveCheck()
                        if moveValid == 1:
                            AImoveScore = 0
                            moveScore()
                            AImoveScoreList[AImoveScoreListIndex] = [sq_row,sq_col,new_sq_row,new_sq_col,AImoveScore]
                            print("AImoveScoreList[",AImoveScoreListIndex,"] =",AImoveScoreList[AImoveScoreListIndex])
                            AImoveScoreListIndex = AImoveScoreListIndex + 1
                        elif moveValid == 0:
                            sq_row = pieceArray[j].p_row_num    # 0
                            sq_col = pieceArray[j].p_col_num    # 1
                            break    # exit for loop

            # max AImoveScoreListIndexMax:
            print("")  # debug
            print("AImoveScoreListIndex =",AImoveScoreListIndex)
            if AImoveScoreListIndex > AImoveScoreListIndexMax:
                AImoveScoreListIndexMax = AImoveScoreListIndex    # to debug max move list size needed
            print("AImoveScoreListIndexMax =",AImoveScoreListIndexMax)

            # print AImoveScoreList after non-attack move search & moveScore
            print("")  # debug
            print("# print AImoveScoreList...")
            print("#   after non-attack move search & moveScore #")
            for i in range (AImoveScoreListIndexSize):
                if AImoveScoreList[i][0] > 0:
                    print("AImoveScoreList =",i,"\t",AImoveScoreList[i])

            ##------------------------------------##
            ##--- consolidate AImoveScoreList ---##
            ##------------------------------------##
            print("")
            print("# consolidate AImoveScoreList...")
            for i in range (1,AImoveScoreListIndexSize-1):        # use index 1 since 0 used for sorting (swap space)
                for n in range (i+1,AImoveScoreListIndexSize):    # use range of valid moves
                    if AImoveScoreList[i][0] == AImoveScoreList[n][0] and AImoveScoreList[i][1] == AImoveScoreList[n][1] and AImoveScoreList[i][2] == AImoveScoreList[n][2] and AImoveScoreList[i][3] == AImoveScoreList[n][3]:
                    #if AImoveScoreList[i][0][1][2][3] == AImoveScoreList[n][0][1][2][3]:    ##RH does this work?
                        AImoveScoreList[i][4] = AImoveScoreList[i][4] + AImoveScoreList[n][4]    ##RH is this a good idea??
                        AImoveScoreList[n] = [0,0,0,0,0]
            # debug
            for i in range (AImoveScoreListIndexSize):
                if AImoveScoreList[i][0] > 0:
                    print("AImoveScoreList =",i,"\t",AImoveScoreList[i])

            ##------------------------------------##
            ##--- sort AImoveScoreList         ---##
            ##------------------------------------##
            print("")
            print("# sort AImoveScoreList...")
            for i in range (1,AImoveScoreListIndexSize):        # use index 1 since 0 used for sorting (swap space)
                AImoveScoreListIndexMax
                for n in range (1,AImoveScoreListIndexMax):  # use range of valid moves - 1
                #for n in range (1,AImoveScoreListIndexSize-1):  # use range of valid moves - 1
                    if  AImoveScoreList[n][4]  < AImoveScoreList[n + 1][4]:
                        AImoveScoreList[0]     = AImoveScoreList[n]
                        AImoveScoreList[n]     = AImoveScoreList[n + 1]
                        AImoveScoreList[n + 1] = AImoveScoreList[0]     # copy of n
            print("# print AImoveScoreList...")
            for i in range (1,AImoveScoreListIndexSize):
                if AImoveScoreList[i][0] > 0:
                    print("AImoveScoreList =",i,"\t",AImoveScoreList[i])

            ##RH debug
            print("")
            print("# print AIattackScoreList...")
            for i in range (1,AImoveScoreListIndexSize):
                if AIattackScoreList[i][0] > 0:
                    print("AIattackScoreList =",i,"\t",AIattackScoreList[i])

            ##------------------------------------##
            # check best move from AImoveScoreList #
            ##------------------------------------##
            # top score move used to set new_sq_row/col
            # RH keep this!! sets moveValid & updates new_sq, etc.

            print("")
            print("# checking AImoveScoreList (top entry only)...")
            moveValid = 0    # keep this to make sure only set by move list check
            for i in range (1,AImoveScoreListIndexSize):    # use starting index 1 since 0 used for sorting (swap space)
                if AImoveScoreList[i][4] > 0:
                    new_sq_row = AImoveScoreList[i][2]
                    new_sq_col = AImoveScoreList[i][3]
                    sq_row = AImoveScoreList[i][0]
                    sq_col = AImoveScoreList[i][1]
                    moveCheck()    # RH redundant? already checked, yes? # keep this to make sure only set by move list check
                    #print("")
                    #print("moveValid =",moveValid) 
                    #print("AImoveScoreList[i][4] =",AImoveScoreList[i][4])
                    #print("i =",i)     # debug
                    if moveValid == 1:
                        #print("moveValid =",moveValid) 
                        #print("AImoveScoreList[i][4] =",AImoveScoreList[i][4])
                        #print("i =",i)     # debug
                        break    # exits the For loop, only top score move should be used
                    #elif moveValid == 0:
                        #print("moveValid =",moveValid) 
                        #print("AImoveScoreList[i][4] =",AImoveScoreList[i][4])
                        #print("i =",i)     # debug
            print("")
            #print("# done checking AImoveScoreList #")
            print("#--- summary of AImoveScoreList check:")
            print("")
            if moveValid == 1:
                print("# AI found a scorelist move...")
                print("moveValid =",moveValid) 
                print("AImoveScoreList moveScore =",AImoveScoreList[1][4])
                #print("AImoveScore =",AImoveScore)
                new_sq_row = AImoveScoreList[1][2]
                new_sq_col = AImoveScoreList[1][3]
                sq_row = AImoveScoreList[1][0]
                sq_col = AImoveScoreList[1][1]
                shipNumLookup()
                boardSquaresArray[sq_row][sq_col].drawBlue()
                boardSquaresArray[new_sq_row][new_sq_col].drawBlue()
                print("sq_row     =",sq_row,"\t","sq_col =",sq_col)
                print("new_sq_row =",new_sq_row,"\t","new_sq_col =",new_sq_col)
                ##RH debug stuff:
                print("numShipsBlue =",numShipsBlue)
                print("numInRow[] =",numInRow)
                print("mercCovered[] =",mercCovered)
                ##RH debug:
                #print("")
                #print("print AItargetPriorityList...")
                #for i in range (AItargetPriorityListIndexSize):
                #    print("AItargetPriorityList =",i,"\t",AItargetPriorityList[i])
                click.play()
                run_def_AI = False   # ends the while loop! RH
                #break    # exits the For loop   ##RH is this required to skip algo stuff?
            elif moveValid == 0:
                print("# AI can't find a scorelist move...")
                print("moveValid =",moveValid) 
                print("AImoveScoreList[1][4] =",AImoveScoreList[1][4])
                #print("AImoveScoreList[2][4] =",AImoveScoreList[2][4])    # debug
                #print("AImoveScore =",AImoveScore)
                print("clear shipNumLookup")
                new_sq_row = 0
                new_sq_col = 0
                sq_row = 0     # reset to new click mode
                sq_col = 0
                shipNumLookup()  # to clear it
                print("# will try the 'rote move list' instead...")

            #harborCheckedforRedScum = 1
            print("")
            #print("set harborCheckedforRedScum =",harborCheckedforRedScum)
            #print("## end: if harborCheckedforRedScum == 0 ##")
            print("## end of scoring based move code ##")
        # end: if RedScuminHarbor == 1 or algoMoveChecked == 1 #


        ################################################################################
        elif RedScuminHarbor == 0 and algoMoveChecked == 0:  # no Red fleet in the harbor, find algo move
        #elif harborCheckedforRedScum == 1:
        ################################################################################


            #print("")
            print("# trying to find a good algo move...")
            # keep this to make sure not set accidentally (???) Or rely on moveCheck to clear it?
            moveValid == 0    
            print("moveValid =",moveValid) 
            print("AImoveScore =",AImoveScore)
            print("AIroteMoveIndex =",AIroteMoveIndex)
            print("")

            if AIroteMoveIndex < (AIroteMoveIndexSize):   # we have index moves left (AIroteMoveIndexSize = 31)
                print("# AIroteMoveList: we have moves left...")
                for i in range(AIroteMoveIndex,AIroteMoveIndexSize):
                    print("i =",i)    # debug
                    sq_row = ai_moves[i][0]
                    sq_col = ai_moves[i][1]
                    print("sq_row     =",sq_row," sq_col =",sq_col)    # debug
                    shipNumLookup()
                    #print("rote list shipSelected =",shipSelected)
                    if shipSelected > 10 and shipSelected <= 20:    # blue ship?
                        AIroteMoveIndex = i
                        # list result:
                        sq_row = ai_moves[AIroteMoveIndex][0]
                        sq_col = ai_moves[AIroteMoveIndex][1]
                        new_sq_row = ai_moves[AIroteMoveIndex][2]
                        new_sq_col = ai_moves[AIroteMoveIndex][3]
                        # found a ship, check move...
                        print("sq_row     =",sq_row," sq_col =",sq_col)
                        print("new_sq_row =",new_sq_row," new_sq_col =",new_sq_col)
                        moveCheck()
                        if moveValid == 1:
                            print("sq_row     =",sq_row," sq_col =",sq_col)
                            print("new_sq_row =",new_sq_row," new_sq_col =",new_sq_col)
                            #AIroteMoveIndex = AIroteMoveIndex + 1
                            break  # out of for loop
                        elif moveValid == 0:
                            print("AI mistake, bad input!")
                            print("moveValid =",moveValid) 
                            print("try again...")
                            #AIroteMoveIndex = AIroteMoveIndex + 1
                        if AIroteMoveIndex == (AIroteMoveIndexSize - 1):   # can't increment any further
                            print("AIroteMoveIndex =",AIroteMoveIndex)
                            print("list moves maxxed out... this is the last one")
                        else:
                            print("AIroteMoveIndex =",AIroteMoveIndex)
                    elif shipSelected <= 10:
                        print("shipSelected <= 10")
                        AIroteMoveIndex = AIroteMoveIndex + 1    ##RH does this work to kill loop?
                        print("AIroteMoveIndex =",AIroteMoveIndex)
                        print("clear shipNumLookup")
                        new_sq_row = 0
                        new_sq_col = 0
                        sq_row = 0
                        sq_col = 0
                        shipNumLookup()  # to clear it
                        print("try again...")
                        print("")

            # list moves maxxed out?
            if AIroteMoveIndex == AIroteMoveIndexSize:   # can't increment any further
            #elif AIroteMoveIndex == AIroteMoveIndexSize:   # can't increment any further
                print("AIroteMoveList: no more list moves available...")
                print("AIroteMoveIndex = AIroteMoveIndexSize")
                print("AIroteMoveIndex =",AIroteMoveIndex)

            # move on from rote list, try other approaches... (add to scoring system?)
            if moveValid == 0:
                print("moveValid =",moveValid) 
                print("# see if there are any other defensive moves we can make...")


            # ---------------------------------------------
            # move to cover the merchant ships: row 0, col 4/6/8/10
            # place blue ships in front of mercs, esp col 9 (why??)
            if moveValid == 0:
                print("")
                print("# move to cover the merchant ships...")
                allMercsCovered = 1

                for j in range (4,12,2):   # for cols 4,6,8,10
                    if mercCovered[j] == 0:    # 3 = empty, 2 = not a port, 1 = merc covered, 0 = merc uncovered!
                        allMercsCovered = 0    ##RH remove if this approach doesn't work

                        ##RH indent this again if this approach doesn't work:
                        print("move up in same column to cover merchant?")
                        for i in range (11,21):    # check blue ships
                            if pieceArray[i].p_col_num == j and pieceArray[i].p_row_num != 1:  # move up in same column to cover
                                sq_row = pieceArray[i].p_row_num
                                sq_col = pieceArray[i].p_col_num
                                new_sq_row = 1
                                new_sq_col = pieceArray[i].p_col_num
                                moveCheck()
                                if moveValid == 1:
                                    print("moveValid =",moveValid) 
                                    print("sq_row     =",sq_row," sq_col =",sq_col)
                                    print("new_sq_row =",new_sq_row," new_sq_col =",new_sq_col)
                                    shipNumLookup()
                                    break
                                elif moveValid == 0:
                                    print("moveValid =",moveValid) 
                                    print("clear shipNumLookup")
                                    new_sq_row = 0
                                    new_sq_col = 0
                                    sq_row = 0
                                    sq_col = 0
                                    shipNumLookup()  # to clear it
                                    print("trying again...")
                        if moveValid == 0:
                            print("move in row 1 to cover merchant?")
                            for i in range (11,21):    # check blue ships
                                for k in range (4,12,2):   # for cols 4,6,8,10
                                    if pieceArray[i].p_col_num == k and pieceArray[i].p_row_num == 1:
                                        print("ship already covering a merchant")
                                        i = i + 1   # RH is this legal?
                                        print("i = i + 1 # RH is this legal?")
                                if pieceArray[i].p_col_num > j and pieceArray[i].p_row_num == 1:  # move in same row to cover
                                    sq_row = pieceArray[i].p_row_num
                                    sq_col = pieceArray[i].p_col_num
                                    new_sq_row = pieceArray[i].p_row_num
                                    new_sq_col = j
                                    moveCheck()
                                    if moveValid == 1:
                                        print("moveValid =",moveValid) 
                                        print("sq_row     =",sq_row," sq_col =",sq_col)
                                        print("new_sq_row =",new_sq_row," new_sq_col =",new_sq_col)
                                        shipNumLookup()
                                        break
                                    elif moveValid == 0:
                                        print("moveValid =",moveValid) 
                                        print("clear shipNumLookup")
                                        new_sq_row = 0
                                        new_sq_col = 0
                                        sq_row = 0
                                        sq_col = 0
                                        shipNumLookup()  # to clear it
                                        print("trying again...")

                    if moveValid == 1:
                        break    # to exit loop: for j in range (4,12,2): # RH is this a good idea?
                if moveValid == 0:
                    print("")
                    print("# unable to cover the merchant ships!!")


            # ---------------------------------------------
            if moveValid == 0:
                # RH eventually remove this? cover in ai moveScore code?
                print("")
                print("# check for empty rows in the harbor, can blue fleet cover it?")
                numInRow = [0,0,0,0,0,0,0]  # 7 members for rows 1 - 6
                for i in range (11,21):  
                    for j in range (1,7):  # for rows 1 - 6
                        if pieceArray[i].p_row_num == j:     # check for blue ships in row j
                            numInRow[j] = numInRow[j] + 1
                #for j in range (1,7):  # for rows 1 - 6
                #    print("numInRow[",j,"] =",numInRow[j])
                print("numInRow =",numInRow)    ##RH does this work?

                #find a ship & move it to empty row, esp row #1, if any are empty
                for i in range (1,5):  # for rows 1 - 4
                    if numInRow[i] == 0:
                        for j in range (1,7):  # for rows 1 - 6
                            if numInRow[j] > 2:
                                for k in range (11,21):  # search blue fleet
                                    if pieceArray[k].p_row_num == j and pieceArray[k].num_masts > 1:  # check for blue ships in row j
                                        sq_row = pieceArray[k].p_row_num
                                        sq_col = pieceArray[k].p_col_num
                                        new_sq_row = i
                                        new_sq_col = pieceArray[k].p_col_num
                                        #break
                        for j in range (2,7):  # for rows 2 - 6
                            if numInRow[j] > 1:
                                for k in range (11,21):  # search blue fleet
                                    if pieceArray[k].p_row_num == j:  # check for blue ships in row j
                                        sq_row = pieceArray[k].p_row_num
                                        sq_col = pieceArray[k].p_col_num
                                        new_sq_row = i
                                        new_sq_col = pieceArray[k].p_col_num
                                        #break
                        for j in range (2,7):  # for rows 2 - 6
                            if numInRow[j] > 0:
                                for k in range (11,21):  # search blue fleet
                                    if pieceArray[k].p_row_num == j:  # check for blue ships in row j
                                        sq_row = pieceArray[k].p_row_num
                                        sq_col = pieceArray[k].p_col_num
                                        new_sq_row = i
                                        new_sq_col = pieceArray[k].p_col_num
                                        #break
                        moveCheck()
                        if moveValid == 1:
                            print("# covering empty rows in the harbor")
                            print("moveValid =",moveValid) 
                            print("sq_row     =",sq_row," sq_col =",sq_col)
                            print("new_sq_row =",new_sq_row," new_sq_col =",new_sq_col)
                            shipNumLookup()
                            break    # exits for loop?
                        elif moveValid == 0:
                            #RH add move ships from entrances here?
                            print("AI can't find a move yet...")
                            print("moveValid =",moveValid) 
                            print("clear shipNumLookup")
                            new_sq_row = 0
                            new_sq_col = 0
                            sq_row = 0     # reset to new click mode
                            sq_col = 0
                            shipNumLookup()  # to clear it
                            print("trying again...")


            # ---------------------------------------------
            ## Merchant Ship Protection ##
            print("moveValid =",moveValid) 
            print("allMercsCovered =",allMercsCovered)
            if moveValid == 0 and allMercsCovered == 0:
                # this needs work...
                ## Merchant Ship Protection ##
                # if Red in row 1 check for blue ships there, move to block access to merchants
                #RH this is just a dumb blocking routine, need to do much better!!
                print("# dumb blocking routine...")
                if enemy_row == 1:
                    for i in range (11,21):  # search blue fleet
                        if pieceArray[i].p_row_num == 1:   
                            if pieceArray[i].p_col_num > enemy_col:
                                sq_row = pieceArray[i].p_row_num
                                sq_col = pieceArray[i].p_col_num
                                new_sq_row = 1
                                new_sq_col = enemy_col + 2
                            elif pieceArray[i].p_col_num < enemy_col:
                                sq_row = pieceArray[i].p_row_num
                                sq_col = pieceArray[i].p_col_num
                                new_sq_row = 1
                                new_sq_col = enemy_col - 2
                            moveCheck()
                            if moveValid == 1:
                                print("moveValid =",moveValid) 
                                print("sq_row     =",sq_row," sq_col =",sq_col)
                                print("new_sq_row =",new_sq_row," new_sq_col =",new_sq_col)
                                shipNumLookup()
                                break
                            elif moveValid == 0:
                                print("moveValid =",moveValid) 
                                print("clear shipNumLookup")
                                new_sq_row = 0
                                new_sq_col = 0
                                sq_row = 0
                                sq_col = 0
                                shipNumLookup()  # to clear it
                                print("trying again...")


            print("# nothing found yet, free up defenders in entrances?")
            if moveValid == 0:
                sq_row = 6
                sq_col = 4
                shipNumLookup()
                if shipSelected > 10:
                    new_sq_row = 6
                    new_sq_col = 5
                else:     # added
                    sq_row = 6
                    sq_col = 5
                    shipNumLookup()
                    if shipSelected > 10:
                        new_sq_row = 4
                        new_sq_col = 5
                    else: 
                        sq_row = 6
                        sq_col = 9
                        shipNumLookup()
                        if shipSelected > 10:
                            new_sq_row = 6
                            new_sq_col = 8
                        else:     # added
                            sq_row = 6
                            sq_col = 8
                            shipNumLookup()
                            if shipSelected > 10:
                                new_sq_row = 4
                                new_sq_col = 8
                            else: 
                                sq_row = 6
                                sq_col = 11
                                shipNumLookup()
                                if shipSelected > 10:
                                    new_sq_row = 6
                                    new_sq_col = 12
                                else:     # added
                                    sq_row = 6
                                    sq_col = 12
                                    shipNumLookup()
                                    if shipSelected > 10:
                                        new_sq_row = 4
                                        new_sq_col = 12
                moveCheck()
                if moveValid == 1:
                    print("# free up defenders in entrances move found")
                    print("sq_row     =",sq_row," sq_col =",sq_col)
                    print("new_sq_row =",new_sq_row," new_sq_col =",new_sq_col)
                    shipNumLookup()
                elif moveValid == 0:
                    print("# nothing found yet, trying time killing moves...")
                    #RH add more? move a ship along any row other than row 1?
                    #[ 2, 1, 2, 3],
                    #[ 4, 3, 4,10],
                    sq_row = 4
                    sq_col = 3
                    shipNumLookup()
                    if shipSelected > 10:
                        new_sq_row = 4
                        new_sq_col = 10
                    else: 
                        sq_row = 4
                        sq_col = 10
                        shipNumLookup()
                        if shipSelected > 10:
                            new_sq_row = 4
                            new_sq_col = 3
                        else: 
                            sq_row = 2
                            sq_col = 1
                            shipNumLookup()
                            if shipSelected > 10:
                                new_sq_row = 2
                                new_sq_col = 3
                            else: 
                                sq_row = 2
                                sq_col = 3
                                shipNumLookup()
                                if shipSelected > 10:
                                    new_sq_row = 2
                                    new_sq_col = 1
                                else: 
                                    for i in range (1,7):  # for rows 1 - 6
                                        print("numInRow[",i,"] =",numInRow[i])
                                    for i in range (6,0,-1):  # for rows 6 - 1
                                        print("numInRow[",i,"] =",numInRow[i])
                                        if numInRow[i] >= 1:
                                            for k in range (11,21):  # search blue fleet
                                                if pieceArray[k].p_row_num == i:  # check for blue ships in row i
                                                    sq_row = pieceArray[k].p_row_num
                                                    sq_col = pieceArray[k].p_col_num
                                                    new_sq_row = i    # pieceArray[k].p_row_num should be same
                                                    new_sq_col = pieceArray[k].p_col_num + leftRight
                                                    leftRight = leftRight * -1    # to toggle leftRight
                                                    moveCheck()
                                                    if moveValid == 1:
                                                        break
                                        if moveValid == 1:
                                            break
                    moveCheck()
                    if moveValid == 1:
                        print("# time killing move found")
                        print("sq_row     =",sq_row," sq_col =",sq_col)
                        print("new_sq_row =",new_sq_row," new_sq_col =",new_sq_col)
                        shipNumLookup()
                    elif moveValid == 0:
                        print("")
                        print("moveValid =",moveValid) 
                        print("clear shipNumLookup")
                        new_sq_row = 0
                        new_sq_col = 0
                        sq_row = 0
                        sq_col = 0
                        shipNumLookup()
                        print("AI is all out of ideas...")
                # end nothing found yet, trying time killing moves...
            # end "see if there are any other defensive moves we can make..."

            ## RH final resolution of move algo...
            print("")
            print("#--- final resolution of AI move algo ---#")
            #moveCheck()    # debug?
            #print("")
            if moveValid == 1:
                print("## AI algo found a move!")
                print("moveValid =",moveValid) 
                algoMoveChecked == 1  # experimental, commented out line below to use scoring code
                # debug only, correct? this is not the move...
                #print("AImoveScoreList[1][4] =",AImoveScoreList[1][4])    # move score???
                #print("AImoveScoreList[2][4] =",AImoveScoreList[2][4])    # debug
                # debug, this is the move, correct?
                shipNumLookup()
                boardSquaresArray[sq_row][sq_col].drawBlue()
                boardSquaresArray[new_sq_row][new_sq_col].drawBlue()
                print("sq_row     =",sq_row,"\t","   sq_col =",sq_col)
                print("new_sq_row =",new_sq_row,"\t","new_sq_col =",new_sq_col)

                ##RH debug stuff:
                print("numShipsBlue =",numShipsBlue)
                print("numInRow[] =",numInRow)
                print("mercCovered[] =",mercCovered)

                click.play()
                run_def_AI = False   # ends the while loop! RH
            elif moveValid == 0:
                print("## AI algo can't find a move...")
                print("moveValid =",moveValid) 
                algoMoveChecked == 1  # experimental, commented out line below to use scoring code
                # debug only, correct? this is not the move...
                #print("AImoveScoreList[1][4] =",AImoveScoreList[1][4])    # move score???
                #print("AImoveScoreList[2][4] =",AImoveScoreList[2][4])    # debug
                print("clear shipNumLookup")
                new_sq_row = 0
                new_sq_col = 0
                sq_row = 0     # reset to new click mode
                sq_col = 0
                shipNumLookup()  # to clear it
                #run_def_AI = False   # ends the while loop! RH

        # end elif RedScuminHarbor == 0 and algoMoveChecked == 0
    # end while run_def_AI
# end Computer_AI()



#########################################################
def game_loop():

    print("")
    print("#-------- Game_Loop --------#")
    print("")

    # globals:
    global delay
    global sq_row
    global sq_col
    global new_sq_row
    global new_sq_col

    global AImoveScoreListIndex    # debug
    global AImoveScoreListIndexMax    # debug
    global mercCovered

    global userDeploymentMode
    global shipSelected
    global moveValid
    global numPlayers
    global playerTurn   # 1 (human) or -1 (computer)
    global turnNum
    global turnTimeout
    global MsgFlag   # controls console window at bottom
    global MsgText

    shipSelected = 0
    playerTurn   = 1    # 1 (human) or -1 (computer)
    turnNum      = 0
    turnTimeout  = 0    # if blue is winning, red can't delay forever, 20 moves? if red is down to 1 ship, start counting...

    #MsgFlag = 0    # RH ok here?

    #if turnNum == 0 and playerTurn == 1:
    #    MsgFlag = 2   # controls console window at bottom

    refreshGameScreen()
    pygame.event.clear()  # clear any pending events
    run_game = True

    while run_game:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run_game = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    print("")
                    print("Q entered, exiting...")
                    print("")
                    run_game = False
                    pygame.quit()
                    sys.exit()

            if userDeploymentMode == 1:
                userFleetArrangement()

            #if turnNum == 0 and playerTurn == 1:
            #    MsgFlag = 2   # controls console window at bottom
            #    refreshGameScreen()

            # who's turn is it?
            # if AI, go to Computer_AI function, then moveCheck, moveShip, combatCheck
            if playerTurn == -1:   # AI
                print("")
                print("##---------- Computer's turn ----------##")
                Computer_AI()    # returns sq_row, sq_col, new_sq_row, new_sq_col
                print("")
                print("# returned to game_loop() from Computer_AI()...")
                # debug only...
                #print("debug moveCheck()...")
                #moveCheck()  # already checked in def_AI? yes, remove? RH
                # keep this:
                print("")
                print("moveValid  =",moveValid) 
                if moveValid == 0:
                    print("# AI done... moveValid = 0 !!!")
                    print("## AI can't find a move...")
                    MsgFlag = 1   # controls console window at bottom
                    MsgText = "Your Move..."
                    refreshGameScreen()
                    alarmBellSound.play()  # error sound
                    pygame.time.delay(1000)  # 2000? lower?
                elif moveValid == 1:
                    print("# AI done... going to moveShip, etc.")
                    moveShip()
                    combatCheck()
                    victoryCheck()
                # update counters, show summary
                turnNum    = turnNum + 1
                playerTurn = playerTurn * -1    # 1 (human) or -1 (computer)
                print("")
                print("# AI turn summary...")
                print("turnNum    =",turnNum)
                print("playerTurn =",playerTurn)  # 1 (human) or -1 (computer)
                #print("moveValid  =",moveValid) 
                print("AImoveScoreListIndex =",AImoveScoreListIndex)    # debug
                print("AImoveScoreListIndexMax =",AImoveScoreListIndexMax)    # debug

                ##RH debug stuff:
                #print("numShipsBlue =",numShipsBlue)
                #print("numInRow[] =",numInRow)
                #print("mercCovered[] =",mercCovered)

                print("##---- Computer's turn done ----##")
                print("")
                pygame.display.update()   # debug? needed?

            elif playerTurn == 1:   # human player's turn
                if event.type == pygame.MOUSEBUTTONDOWN:   
                    print("")
                    print("##----------- Human's turn -----------##")
                    #print("## enter next move...")
                    print("")
                    print("mouse clicked")
                    print("pos[0] =",pos[0]," pos[1] =",pos[1])
                    click.play()
                    MsgFlag = 0   # controls console window at bottom
                    #for i in range (squareNum):
                    for j in range(14):   # rows
                        for i in range(15):   # cols
                            if boardSquaresArray[j][i].isOver(pos):
                                new_sq_row = j
                                new_sq_col = i
                                print("sq_row     =",sq_row,"\t","    sq_col =",sq_col)
                                print("new_sq_row =",new_sq_row,"\t","new_sq_col =",new_sq_col)
                                #pygame.display.update()   # debug?
                    # what did we click on?
                    if terrain[new_sq_row][new_sq_col] == 'S' or terrain[new_sq_row][new_sq_col] == 'R' or terrain[new_sq_row][new_sq_col] == 'B' or terrain[new_sq_row][new_sq_col] == 'M':   # if not, show status? debug readout?
                        print("Sea square (or gun/mine) selected")
                        # new click?
                        if sq_row == 0 and sq_col == 0:
                            print("new click - check for move start")
                            # is there a ship there?
                            shipSelected = 0
                            for i in range(1,pieceNum+1):
                                if pieceArray[i].p_row_num == new_sq_row and pieceArray[i].p_col_num == new_sq_col:
                                    # what ship is at r/c?
                                    shipSelected = i
                                    print("shipSelected =",shipSelected)
                            if shipSelected > 0:
                                if pieceArray[shipSelected].shipType == 1:    # British fleet, ok!
                                    print("British ship selected")
                                    # save selection
                                    sq_row = new_sq_row
                                    sq_col = new_sq_col
                                    print("sq_row =",sq_row," sq_col =",sq_col)
                                    boardSquaresArray[sq_row][sq_col].drawRed()  # highlight square
                                    pygame.display.update()   # debug?
                                elif pieceArray[shipSelected].shipType > 1:    # American fleet, error!
                                    print("mistaken input, sound the alarm!!")
                                    alarmBellSound.play()  # error sound
                            # end of new click
                        # destination clicked?
                        else:
                            print("# destination clicked")
                            if sq_row != new_sq_row and sq_col != new_sq_col:      # if neither is the same, error!
                                print("diagnonal input (mistake), sound the alarm!!")
                                new_sq_row = 0
                                new_sq_col = 0
                                sq_row = 0     # reset to new click mode
                                sq_col = 0
                                alarmBellSound.play()  # error sound
                                refreshGameScreen()
                            elif sq_row == new_sq_row and sq_col == new_sq_col:    # both are same, deselect ship (remove red box)
                                print("both are same, deselect ship")
                                new_sq_row = 0
                                new_sq_col = 0
                                sq_row = 0     # reset to new click mode
                                sq_col = 0
                                refreshGameScreen()
                            else:
                                print("# go to moveCheck...")
                                moveCheck()
                                if moveValid == 0:
                                    alarmBellSound.play()  # error sound
                                elif moveValid == 1:
                                    moveShip()
                                    combatCheck()
                                    victoryCheck()
                                    playerTurn = playerTurn * -1    # 1 (human) or -1 (computer)
                                    print("")
                                    print("# human turn done #")
                                    print("turnNum    =",turnNum)
                                    print("playerTurn =",playerTurn)  # 1 (human) or -1 (computer)
                                    print("moveValid =",moveValid) 
                    else:
                        # error (or else show status if applicable?) 
                        print("clicked on a non-Sea square...")
                        new_sq_row = 0
                        new_sq_col = 0
                        sq_row = 0     # reset to new click mode
                        sq_col = 0
                        refreshGameScreen()
                        alarmBellSound.play()  # error sound

                pygame.display.update()   # debug? needed?

# end game_loop()


#########################################################
def victoryCheck():
    print("")
    print("##--- victory check ---##")

    # did anyone win yet?
    # if merch = 0, red wins
    # if red fleet = 0, blue wins
    # if both, tie!  # hard to imagine, but possible?
    # if red is down to 1 ship, start counting,... 20 moves?

    global MsgFlag
    global MsgText
    global winner
    global winsPlayer1
    global winsPlayer2
    global playerTurn   # 1 (human) or -1 (computer)
    global turnTimeout

    MsgFlag = 0   # controls console window at bottom
    winner = 0
    redShipCount = 0
    blueShipCount = 0
    merchShipCount = 0

    for i in range (1,11):  # check red fleet (1-10)
        if pieceArray[i].num_masts > 0:
            redShipCount = redShipCount + 1
    for i in range (11,21):  # check merchant fleet (11-20)
        if pieceArray[i].num_masts > 0:
            blueShipCount = blueShipCount + 1
    for i in range (21,25):  # check merchant fleet (21-24)
        if pieceArray[i].num_masts > 0:
            merchShipCount = merchShipCount + 1

    if redShipCount == 0 and merchShipCount == 0:
        print("")
        print("It's a tie!!")
        print("")
        winner = 2   # 1 (human) or -1 (computer) or 2 for a tie
        MsgText = "It's a tie!"
    elif merchShipCount == 0 or blueShipCount == 0:
        print("")
        print("Red fleet victory!!")
        print("")
        winner = 1   # 1 (human) or -1 (computer) or 2 for a tie
        MsgText = "Red fleet wins!"
        winsPlayer1 = winsPlayer1 + 1   # human
    elif redShipCount == 0:
        print("")
        print("Blue fleet victory!!")
        print("")
        winner = -1   # 1 (human) or -1 (computer) or 2 for a tie
        MsgText = "Blue fleet wins!"
        winsPlayer2 = winsPlayer2 + 1   # computer
    elif redShipCount == 1:
        if playerTurn == 1:
            turnTimeout = turnTimeout + 1    # to increment timer
        if turnTimeout == 20:
            print("")
            print("Blue fleet victory by timeout!!")
            print("")
            winner = -1   # 1 (human) or -1 (computer) or 2 for a tie
            MsgText = "Blue fleet wins!"
            winsPlayer2 = winsPlayer2 + 1   # computer

    print("winner =",winner)
    print("winsPlayer1 =",winsPlayer1)
    print("winsPlayer2 =",winsPlayer2)

    if winner != 0:
        MsgFlag = 1   # controls console window at bottom
        refreshGameScreen()
        #pygame.display.update() 

        explosion2.play()  # big expl
        if winner == -1:
            alarmBellSound.play()  # error sound
        else:
            twoBellsSound.play()  # good move
        pygame.time.delay(3000)   # 3 secs
        pygame.event.clear()  # clear any pending events
        promptForReplay()

# end victoryCheck()


#########################################################
def promptForReplay():

    print("Play again?")
    global MsgFlag
    global MsgText
    MsgFlag = 1   # controls console window at bottom
    MsgText = "Replay? (Y/n)"

    refreshGameScreen()

    #pygame.display.update() 
    pygame.event.clear()  # clear any pending events
    run_newgame = True

    while run_newgame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_newgame = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or event.key == pygame.K_x or event.key == pygame.K_n:
                    print("")
                    print("Q or X N entered, exiting...")
                    print("")
                    run_newgame = False
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_y or event.key == pygame.K_RETURN:
                    print("")
                    print("Y entered, restarting...")
                    print("")
                    game_setup()               # just blue ocean & side ships
                        #displayInstructions()
                        #displayInstructionsUserFleetSetup()          # just which ships are in which of the 10 locs
                    set_AI_Strategy()          # to set cannons, mines, etc. 
                        #AI_ship_placement()       # done in initPieceArray for now
                    AImoveScoreListInit()      # can move to AI move code later (debug) RH
                    run_newgame = False
                    game_loop()                # does this work? so far, yes...

# end promptForReplay()




# stuff still in process...

#########################################################
#RH do I need this?? only for human defender vs ai attacker
def AI_ship_placement():
    print("")
    print("# AI_ship_placement #")

    # adjust default ship placement as needed - any changes needed?
    # adjust placement for each strategy? left/right/balanced
    # update pieceArray after input
    #global pieceArray

    #for i in range(1,pieceNum+1)):
    for i in range(1,11):
        print("?")
        #pieceArray[i].hexLoc = hexLocDebug[i]
        #hexArray[hexLocDebug[i]].unit = i
    #updatePieceArray()


'''
#########################################################
# use this for 2 player mode?

# =========== game_setup =========== #

def game_setup():

    print("#=========== Welcome to Broadside ===========#")
    pygame.event.clear()
    run_setup = True

    # reset game variables:
    global numPlayers
    numPlayers = 1  # 1 for human vs. computer, 2 for human vs. human
    numPlayersDone = 0

    global turnPlayer
    turnPlayer = 1  # 1 or 2. Computer is player 1 if single player mode
    print("game_setup: turnPlayer = ",turnPlayer)

    global winner
    winner = 0      # 1 or 2, winning player

    #instructionsDone = 0

    text2dispCenter50("Do You Need Instructions? (Y/N)",display_width/2,1380, white)
    pygame.display.update()

'''



#######################################################
# High level game function calls here...
#######################################################

game_setup()                    # just blue ocean & side ships
    # drawScreenSetup()
    # displayInstructions()
    # displayInstructionsUserFleetSetup()
        # drawScreenSetup()
    # defineRowsColumns()
    # initBoardSquaresArray()
    # initPieceArray()
    # resetPieceArray()
    # initTerrain()
    # redrawGameWindow()    # blit game board
    # drawTerrain()         # draw land, gun emplacements, mines
    # drawBoardPieces()     # draw pieces on board in loop from pieceArray

set_AI_Strategy()               # to set cannons, mines, red ships, etc. 
init_AI_RoteMoveList()
    # AI_ship_placement()            # done in initPieceArray for now...

AImoveScoreListSetup()
AImoveScoreListInit()           # keep here
AItargetPriorityListSetup()
AItargetPriorityListInit()      # keep here

game_loop()
    # userFleetArrangement()         # adjust red ships in the 10 starting locs
    # human player or AI move entry
    # Computer_AI()
        # AImoveScoreListInit()
        # AItargetPriorityListInit()
    # moveCheck()
    # moveShip()
    # checkCombat()
    # victoryCheck()
    # refreshGameScreen()
    # promptForReplay()
#######################################################



#######################################################
# keep this (global exit)
pygame.quit()
sys.exit()
