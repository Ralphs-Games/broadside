#==============================================
# Broadside - A Naval Battle Game for 2 Players
#==============================================
# 8/27/22, 9:25 PM

'''
stuff to do:

add changes to the rules/instructions at the start of instr?

AI code... (row 1740)

add new tree to check for Red at row 1 & attack, or else cover merchs

add moves to cover the merchant ships: what are the squares? row 0, col 4/6/8/10
    move vertically to cover the merchs if possible


_add moves left/right in a row if nothing else to do

look for moves to make, to avoid, etc.
check rote moves to avoid turning into a T attack
place ships on each row to defend harbor
place ships in front of merchant ships
use 2 mast ships to clog entrances (don't unclog too soon, always from left side first)
use 3 mast ships to defend harbor
use 1 mast ships to shield marchants

_look for T moves
_wait for red to enter harbor to attack


is movecheck working for AI player now? maybe?
false invalid move due to ship self @ start? fixed?
fix ghost ship blue boxes, done?


change moveCheck(ok now?), _moveShip, and _combatCheck to be player & _direction agmostic
    _use ship#, d_col/d_row, direction?
    _fix draw red vs blue
    _fix no combat for AI

_change AI def moves to use list & index counter rather than 1, 2, 3...
check list starting points vs. new AI ship deployment (if no ship, pick another move)


clean up land image drawing code?

rules_menu_user(): pre game screen for rules
    (?): R = rules, X = exit rules, G = game (skip rules), Q = quit game
        _prompt user for rules? type X when done?
        _how to display rules? scans? page thru them?
        update rules to reflect paying vs computer, mines vs buoys, etc.

add user plaecment/setup of red fleet... text instructions?
userDeploymentRules(): click on a piece to move it, click to drop it (swap)
userDeployment()

setup_AI_opponent()
    _change default ship deployment, mix it up? what is best?
    randomize placement of cannons & mines
    randomize AI strategies:
    1. passive - ships on each row to make T attacks?
    2. aggressive - ?
    3. trap? - ships on each row to make T attacks? other?
create new lists of initial moves for each strategy, also 3 sets of moves to mix things up randomly

game_setup(): draw screen, etc.

game_loop()
    moves: click on ship, click on destination
    check each square along the path for land, guns, buoys, other ships
    then resolve final combat at destination (combat if ship before destination?)
    console at bottom for error messages?

game_resolution(): end of game, show winner, fireworks, prompt for new game, etc.


_fixed:

_replay code needs to reset the terrain array!

_why is it moving my ships?? to bad squares... forgot shipnum lookup

_driving over top of other ships!
_taking an extra turn when human move invalid!
_stop all the ringing bells when AI is trying to move!!

_mines (buoys) should be used once, then removed (update needed to remove)

_check on cannon on both sides of entrance, add dual hits in center
    _update terrain to show ++ ; sq array uses R, B

_edit sounds in Audacity

_change default ship deployment, mix it up

_check on losing masts, does it update? refresh screen needed

_separate move checking from actual moving: don't move until checked

clean up land image drawing code
_adjust sizes to cover gaps? check image sizes vs squares, s/b 100x100
_check order of draws, edges should be first to get covered, last is border ship images

_add classes & arrays for squares & pieces (done?)
_class square:
_terrainType(land/sea/port/mine?/battery?), shipType(R/B/merch), shoreBatt(0/1/2), mine(sink/pass)
_class: square (type, ship, shoreb, buoy)
_array of squares
_squaresArray = np.zeros(15,14)
_squaresArray[14,0] = square

#-----------------

Defensive AI:

make initial moves by rote, unless Red fleet enters harbor...
check by quadrants where red fleet is moving
clog up entrances!

# (old)
# Move to block entry on row 6, col 2-4, 9-11
# 1/12 -> 6/12 -> 6/11
# 1/8  -> 6/8  -> 6/9
# 1/11 -> 4/11
# 1/10 -> 4/10
# 1/9  -> 4/9
# 1/5  -> 6/5 -> 6/4
# 1/4  -> 4/4
# 1/3  -> 4/3
# 1/6  -> 2/6 -> 2/2 -> 4/2
# 1/7  -> 2/7 -> 2/1 -> 6/1 -> 6/2

How to search for Red fleet? if any ship in row 6 or less
How to decide on moves? Good Q. Look for adjacent row/col
Look for crossing the T based on direction

Priorities:
1. defend merchant ships (block access? ship across bow of merch)
2. look for T attack
3. avoid being T attacked
4. sink single masted Red ships?



#-----------------
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
    # r c  ter Num
    # 1 2   S  11
    # 1 4   S  12
    # 1 5   S  13
    # 1 6   S  14  #1
    # 1 7   S  15
    # 1 8   S  16
    # 1 9   S  17
    # 1 10  S  18
    # 1 11  S  19
    # 1 12  S  20
    # 0 4   P  21  # merchant ships
    # 0 6   P  22
    # 0 8   P  23
    # 0 10  P  24

#-----------------
rule change ideas:

attack land guns?
combat if ship before destination? alongside during move? or in they path by mistake?
raking from astern destroys the rudder (% chance? 33%?) can't turn?
0 sails = immobile, not dead, can fire one more time? at passing enemies?
wind? blowing into port, hard to sail out, only one space at a time?
boarding & capture?
destroy/capture flagship = all that fleet's ships lose one sail? (unless down to one)

#-----------------

'''

#from distutils.ccompiler import new_compiler
import pygame
import sys
import os
import numpy as np
import time
import random

# must come before pygame.init():
os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

clock = pygame.time.Clock()
random.seed()  # uses system time as a seed
#random.randint(a, b)   #Return a random integer N such that a <= N <= b

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
pygame.mixer.init()
pygame.mixer.music.set_volume(0.05)  # 0.03-0.05

music = pygame.mixer.music.load("sounds/sea_waves_266.wav")
##music = pygame.mixer.music.load("sounds/yoyoma_cello_suite1inG_prelude.mp3")

## To have our music play continuously we do the following directly after defining our variable music:
#pygame.mixer.music.play(-1) # -1 will ensure the song keeps looping
##fadeout(time)  # ms

#pygame.mixer.music.load('sounds/sea_waves_266.wav')
pygame.mixer.music.play(-1)

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
# colors

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
## load images into memory ##

#img = pygame.image.load('bird.png')
#img.convert()    #The method convert() optimizes the image format and makes drawing faster

# The function rotozoom() allows to combine rotation and scaling
# Rotation is counter-clockwise: if 0 = N, 90 = W, 180 = S, 270 = E
#img = pygame.transform.rotozoom(img0, angle, scale)

## background sea image ##
bgScreen_0 = pygame.image.load('images/ocean_1_1440.jpg')
bgScreen_0.convert()

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

## land images around bay ##
# Rotation is counter-clockwise

land_11 = pygame.image.load('images/coast11_100x100_t2.png')  # 1 x 1 transparent *
land_11.convert()

land_11_solid = pygame.image.load('images/coast7_100x100_solid2a.png')  # 1 x 1 solid *
land_11_solid.convert()

land_11_solid_edge = pygame.image.load('images/coast7_100x29_solid.png')  # 1 x 0.3 solid *
land_11_solid_edge.convert()

land_21 = pygame.image.load('images/coast11_200x100_t3.png')  # 2 x 1 transparent *
land_21.convert()

land_21_edge = pygame.image.load('images/coast11_200x50_t2.png')  # 2 x 0.5 transparent *
land_21_edge.convert()

land_41 = pygame.image.load('images/coast11_400x100_t2.png')  # 4 x 1 transparent *
land_41.convert()

land_corner_out = pygame.image.load('images/coast_corner2_out3.png')  # outside corner transparent *
land_corner_out.convert()

land_corner_in = pygame.image.load('images/coast_corner_in4.png')   # inside corner transparent *
land_corner_in.convert()

land_gun = pygame.image.load('images/gun_island3.png')  # 1 x 1 for gun mount *
land_gun.convert()


def drawLandImages():  # ordered for proper layering

    #print("drawLandImages")
    # draw map edges first to let other stuff cover gaps

    # land_1x1_solid - left outside edge of map
    screen.blit(pygame.transform.rotozoom(land_11_solid, 90, 1), ( 426,  19))
    screen.blit(pygame.transform.rotozoom(land_11_solid, 90, 1), ( 426, 119))
    screen.blit(pygame.transform.rotozoom(land_11_solid, 90, 1), ( 426, 619))
    screen.blit(pygame.transform.rotozoom(land_11_solid, 90, 1), ( 426, 719))
    screen.blit(pygame.transform.rotozoom(land_11_solid, 90, 1), ( 426, 819))
    screen.blit(pygame.transform.rotozoom(land_11_solid, 90, 1), ( 426, 919))
    screen.blit(pygame.transform.rotozoom(land_11_solid, 90, 1), ( 426,1019))
    screen.blit(pygame.transform.rotozoom(land_11_solid, 90, 1), ( 426,1119))
    screen.blit(pygame.transform.rotozoom(land_11_solid, 90, 1), ( 426,1219))

    # land_1x1_solid - right outside edge of map
    screen.blit(pygame.transform.rotozoom(land_11_solid, 90, 1), (2026,  19))
    screen.blit(pygame.transform.rotozoom(land_11_solid, 90, 1), (2026, 119))
    screen.blit(pygame.transform.rotozoom(land_11_solid, 90, 1), (2026, 219))
    screen.blit(pygame.transform.rotozoom(land_11_solid, 90, 1), (2026, 519))
    screen.blit(pygame.transform.rotozoom(land_11_solid, 90, 1), (2026, 619))
    #screen.blit(pygame.transform.rotozoom(land_11_solid, 90, 1), (2026, 719))

    # land_11_solid_edge - top outside edge of map
    screen.blit(pygame.transform.rotozoom(land_11_solid_edge,  0, 1), ( 500, 0))
    screen.blit(pygame.transform.rotozoom(land_11_solid_edge,  0, 1), ( 528, 0))  ## to cover gaps
    screen.blit(pygame.transform.rotozoom(land_11_solid_edge,  0, 1), ( 628, 0))  ## to cover gaps
    screen.blit(pygame.transform.rotozoom(land_11_solid_edge,  0, 1), ( 728, 0))  ## to cover gaps
    #screen.blit(pygame.transform.rotozoom(land_11_solid_edge,  0, 1), ( 776, 0))
    #screen.blit(pygame.transform.rotozoom(land_11_solid_edge,  0, 1), ( 826, 0))  # port
    #screen.blit(pygame.transform.rotozoom(land_11_solid_edge,  0,0.95), (1030, 0))  # port
    #screen.blit(pygame.transform.rotozoom(land_11_solid_edge,  0,0.95), (1230, 0))  # port
    #screen.blit(pygame.transform.rotozoom(land_11_solid_edge,  0,0.95), (1430, 0))  # port
    #screen.blit(pygame.transform.rotozoom(land_11_solid_edge,  0, 1), (1630, 0))  # port
    screen.blit(pygame.transform.rotozoom(land_11_solid_edge,  0, 1), (1726, 0))
    screen.blit(pygame.transform.rotozoom(land_11_solid_edge,  0, 1), (1826, 0))
    screen.blit(pygame.transform.rotozoom(land_11_solid_edge,  0, 1), (1926, 0))
    screen.blit(pygame.transform.rotozoom(land_11_solid_edge,  0, 1), (1976, 0))

    # land_21_edge # 2 x 0.5 transparent *
    screen.blit(pygame.transform.rotozoom(land_21_edge,270, 1), ( 480, 219))  # side bars
    screen.blit(pygame.transform.rotozoom(land_21_edge,270, 1), ( 480, 419))  # side bars
    screen.blit(pygame.transform.rotozoom(land_21_edge, 90, 1), (2020, 319))  # side bars
    screen.blit(pygame.transform.rotozoom(land_21_edge, 90, 1), (2025, 819))  # gaps # side bars
    screen.blit(pygame.transform.rotozoom(land_21_edge, 90, 1), (2025,1019))  # gaps # side bars
    #screen.blit(pygame.transform.rotozoom(land_21_edge, 90, 1), (2020,1219))  # side bars

    # end of map edges

    # draw rest of map

    # land_1x1_solid - left side of map
    screen.blit(pygame.transform.rotozoom(land_11_solid, 90, 1), ( 528,  19))  # gaps
    screen.blit(pygame.transform.rotozoom(land_11_solid, 90, 1), ( 526, 818))  # gaps
    screen.blit(pygame.transform.rotozoom(land_11_solid, 90, 1), ( 526, 919))
    screen.blit(pygame.transform.rotozoom(land_11_solid, 90, 1), ( 526,1019))
    screen.blit(pygame.transform.rotozoom(land_11_solid, 90, 1), ( 526,1119))
    screen.blit(pygame.transform.rotozoom(land_11_solid, 90, 1), ( 526,1219))
    screen.blit(pygame.transform.rotozoom(land_11_solid, 90, 1), ( 626,1118))  # gaps
    screen.blit(pygame.transform.rotozoom(land_11_solid, 90, 1), ( 626,1219))
    #screen.blit(pygame.transform.rotozoom(land_11_solid, 90, 1), (1975, 619))  # gaps # exp

    # 1 x 1 transparent
    screen.blit(pygame.transform.rotozoom(land_11,180, 1), ( 526, 119))  # too small??
    screen.blit(pygame.transform.rotozoom(land_11,180, 1), ( 726,  19))  # experiment
    #screen.blit(pygame.transform.rotozoom(land_11,180, 1), (1676,  19))  # experiment
    screen.blit(pygame.transform.rotozoom(land_11,180, 1), (1126, 719))  # center island south coast   
    screen.blit(pygame.transform.rotozoom(land_11,180, 1), (1226, 719))  # center island south coast  
    #screen.blit(pygame.transform.rotozoom(land_11,180, 1), (1126, 722))  ## center island south coast
    #screen.blit(pygame.transform.rotozoom(land_11,180, 1), (1226, 722))  ## center island south coast
    screen.blit(pygame.transform.rotozoom(land_11,270, 1), ( 726,1119))  # too small??
    screen.blit(pygame.transform.rotozoom(land_11, 90, 1), (1927, 119))  # upper right corner-ish
    screen.blit(pygame.transform.rotozoom(land_11,  0, 1), (1926, 521))  # gaps # right side island   
    screen.blit(pygame.transform.rotozoom(land_11, 90, 1), (1825, 621))  # gaps # right side island
    screen.blit(pygame.transform.rotozoom(land_11,270, 1), (1923, 621))  # gaps # right side island  # exp
    screen.blit(pygame.transform.rotozoom(land_11,180, 1), (1826, 719))  # gaps # right side island 
    screen.blit(pygame.transform.rotozoom(land_11,180, 1), (1926, 719))  # gaps # right side island
    screen.blit(pygame.transform.rotozoom(land_11,180, 1), ( 428,1319))  # bottom left corner
    screen.blit(pygame.transform.rotozoom(land_11,180, 1), ( 528,1318))  # bottom left corner
    screen.blit(pygame.transform.rotozoom(land_11, 90, 1), (2020,1219))  ## bottom left outside edge

    screen.blit(pygame.transform.rotozoom(land_11,270, 1), (1973, 621))  # gaps # right side island  # exp
    screen.blit(pygame.transform.rotozoom(land_11_solid, 90, 1), (2025, 619))  # gaps # exp

    # 2 x 1 transparent *
    #screen.blit(pygame.transform.rotozoom(land_21,180, 1), ( 680,  19))  # experiment, too small?
    #screen.blit(pygame.transform.rotozoom(land_21,180, 1), (1676,  19))  # experiment
    screen.blit(pygame.transform.rotozoom(land_21,180, 1), (1726,  19))
    screen.blit(pygame.transform.rotozoom(land_21,270, 1), ( 626, 819))  # too small??
    screen.blit(pygame.transform.rotozoom(land_21,  0, 1), ( 826,1221))  # gaps
    #screen.blit(pygame.transform.rotozoom(land_21, 90, 1), (1826, 619))  # tmp
    #screen.blit(pygame.transform.rotozoom(land_21,180, 1), (1826, 719))
    #screen.blit(pygame.transform.rotozoom(land_21,180, 1), (1126, 719))  # center island south coast

    # 4 x 1 transparent
    #screen.blit(pygame.transform.rotozoom(land_41,180, 1), (1026,718))   # center island south coast
    #screen.blit(pygame.transform.rotozoom(land_41,270, 1), ( 626,818))   # ?
    #screen.blit(pygame.transform.rotozoom(land_41,  0, 1), ( 626,1218))
    screen.blit(pygame.transform.rotozoom(land_41,180, 1), ( 628,1317))   # to cover gap
    screen.blit(pygame.transform.rotozoom(land_41,  0, 1), (1026,1219))   # too small? pos?

    if MsgFlag == 0:
        screen.blit(pygame.transform.rotozoom(land_41,180, 1), (1026,1314))   # to cover gap # bottom center of screen
        #textToDisplay40redCam("BROADSIDE",(1120),(1340))
        #textToDisplay40whiteCam("BROADSIDE",(1122),(1342))
    elif MsgFlag == 1:
        if winner == -1:
            textToDisplay40blueCam(MsgText,(1090),(1336))
            textToDisplay40whiteCam(MsgText,(1092),(1338))
        else:
            textToDisplay40redCam(MsgText,(1100),(1336))  # 1180, 1340
            textToDisplay40whiteCam(MsgText,(1102),(1338))
        #textToDisplay40redCam("Error!",(1180),(1340))
        #textToDisplay40whiteCam("Error!",(1182),(1342))

    #screen.blit(pygame.transform.rotozoom(land_41,180, 1), (1026,1323))   # pushed lower to match corner

    # inside corner
    screen.blit(pygame.transform.rotozoom(land_corner_in,270, 1), ( 628,  21))  # gaps # too small? pos?
    screen.blit(pygame.transform.rotozoom(land_corner_in,180, 1), (1922,  19))  # gaps # too small? pos?
    screen.blit(pygame.transform.rotozoom(land_corner_in,  0, 1), ( 528, 717))  # gaps
    screen.blit(pygame.transform.rotozoom(land_corner_in,  0, 1), ( 628,1017))  # gaps
    screen.blit(pygame.transform.rotozoom(land_corner_in,  0, 1), ( 728,1217))  # gaps
    screen.blit(pygame.transform.rotozoom(land_corner_in,180, 1), (2018, 719))  # outside right edge

    # outside corner transparent
    screen.blit(pygame.transform.rotozoom(land_corner_out,270, 1), ( 826,   0))  # port
    screen.blit(pygame.transform.rotozoom(land_corner_out,180, 1), (1626,  -2))  ##  0))  # port
    screen.blit(pygame.transform.rotozoom(land_corner_out,270, 1), ( 826,  19))  # port
    screen.blit(pygame.transform.rotozoom(land_corner_out,180, 1), (1626,  19))  # port
    screen.blit(pygame.transform.rotozoom(land_corner_out,270, 1), ( 626, 119))
    screen.blit(pygame.transform.rotozoom(land_corner_out,180, 1), (1927, 216))  # pos? too small?
    screen.blit(pygame.transform.rotozoom(land_corner_out,  0, 1), ( 526, 619))
    screen.blit(pygame.transform.rotozoom(land_corner_out,  0, 1), ( 626, 719))
    screen.blit(pygame.transform.rotozoom(land_corner_out, 90, 1), (1126, 621))  # gaps # center island north coast
    screen.blit(pygame.transform.rotozoom(land_corner_out,  0, 1), (1226, 621))  # gaps # center island north coast
    #screen.blit(pygame.transform.rotozoom(land_corner_out,180, 1), (1126, 719))  # center island south coast
    #screen.blit(pygame.transform.rotozoom(land_corner_out,270, 1), (1226, 719))  # center island south coast
    #screen.blit(pygame.transform.rotozoom(land_corner_out,180, 1), (1926, 119))
    #screen.blit(pygame.transform.rotozoom(land_corner_out,180, 1), (1926, 219))
    screen.blit(pygame.transform.rotozoom(land_corner_out,  0, 1), (1426,1219))
    screen.blit(pygame.transform.rotozoom(land_corner_out,270, 1), (1424,1310))  # gaps 
    screen.blit(pygame.transform.rotozoom(land_corner_out,  0, 1), ( 726,1019))  # pos?
    #screen.blit(pygame.transform.rotozoom(land_corner_out,270, 1), ( 726,1119))
#    screen.blit(pygame.transform.rotozoom(land_corner_out,  0, 1), (1926, 519))  # right side island
    screen.blit(pygame.transform.rotozoom(land_corner_out, 90, 1), (1826, 522))  # gaps # right side island
    #screen.blit(pygame.transform.rotozoom(land_corner_out,270, 1), (1926, 619))  # tmp
    #screen.blit(pygame.transform.rotozoom(land_corner_out,180, 1), (1826, 619))  # tmp
#    screen.blit(pygame.transform.rotozoom(land_corner_out,270, 1), (1926, 719))  # right side island
    #screen.blit(pygame.transform.rotozoom(land_corner_out,180, 1), (1826, 719))  # right side island
    screen.blit(pygame.transform.rotozoom(land_corner_out,180, 1), (2020,1316))  # gaps # bottom left outside edge

    # land_gun # gun island
    #screen.blit(pygame.transform.rotozoom(land_gun,180, 1), ( 626, 719))  # center island south coast
    screen.blit(pygame.transform.rotozoom(land_gun,  0, 1), (1028, 716))  # gaps # center island
    screen.blit(pygame.transform.rotozoom(land_gun,180, 1), (1326, 715))  # gaps # center island
    screen.blit(pygame.transform.rotozoom(land_gun,  0, 1), (1728, 716))  # gaps # east side island

    # port square images:
    screen.blit(pygame.transform.rotozoom(land_gun, 90, 1), (1026, 0))  # port
    screen.blit(pygame.transform.rotozoom(land_gun, 90, 1), (1226, 0))  # port
    screen.blit(pygame.transform.rotozoom(land_gun, 90, 1), (1426, 0))  # port
    screen.blit(pygame.transform.rotozoom(land_gun, 90, 1), (1026, 19))  # port
    screen.blit(pygame.transform.rotozoom(land_gun, 90, 1), (1226, 19))  # port
    screen.blit(pygame.transform.rotozoom(land_gun, 90, 1), (1426, 19))  # port

    # cannons picoli single 80x80
    screen.blit(cannons_L, ( 628, 729))  # far left
    screen.blit(cannons_R, (1038, 729))  # left side of island
    screen.blit(cannons_L, (1332, 729))  # right side of island
    screen.blit(cannons_R, (1738, 729))  # far right

    ## cannons # 78x64 original cannon
    #screen.blit(pygame.transform.rotozoom(cannons_L,  0, 1), ( 628, 737))  # far left
    #screen.blit(pygame.transform.rotozoom(cannons_R,  0, 1), (1038, 734))  # left side of island
    #screen.blit(pygame.transform.rotozoom(cannons_L,  0, 1), (1332, 734))  # right side of island
    #screen.blit(pygame.transform.rotozoom(cannons_R,  0, 1), (1738, 734))  # far right

    ## mines # 50x50 (moved to drawTerrain)
    #screen.blit(mines, ( 751, 544))  # 50x50
    #screen.blit(mines, ( 851, 544))  # 50x50
    #screen.blit(mines, ( 951, 544))  # 50x50
    #screen.blit(mines, (1451, 544))  # 50x50
    #screen.blit(mines, (1551, 544))  # 50x50
    #screen.blit(mines, (1651, 544))  # 50x50


# load background sidebar ship images #
# see redrawGameWindow() for blit to screen

bgr_ship_2 = pygame.image.load('images/bgr_ship2a.jpg')
bgr_ship_2.convert()
bgr_ship_4 = pygame.image.load('images/bgr_ship4a.jpg')
bgr_ship_4.convert()
bgr_ship_5 = pygame.image.load('images/bgr_ship5a.jpg')
bgr_ship_5.convert()
bgr_ship_6 = pygame.image.load('images/bgr_ship6a.jpg')
bgr_ship_6.convert()
#bgr_ship_1 = pygame.image.load('images/bgr_ship1.jpg')
#bgr_ship_1.convert()
#bgr_ship_3 = pygame.image.load('images/bgr_ship3.jpg')
#bgr_ship_3.convert()


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

# draw using raw x/y coordinates, not row/col (debug only)
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


#map out valid sea squares, blocked or land squares, the 4 port squares, etc.
# L = land
# P = port (merchant ships)
# Y = mine/mine
# G = shore batteries
# R = sea in range of shore guns
# B = sea in range of both shore guns
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

MsgFlag = 0   # controls console window at bottom
MsgText = "Error!"

boardSquareSize = 100
boardStartX = 526
boardStartY =  19

userDeploymentDone = 0  # 1 = done, game starts

shipNum = 0
shipSelected = 0
sq_row = 0
sq_col = 0
new_sq_row = 0
new_sq_col = 0
pmr = 0  # plus/minus row
pmc = 0  # plus/minus col
direction = 0

moveRange = 0         # d_col or d_row
moveValid = 0         # 1 = valid move
humanPlayerMoved = 0  # 1 = move done   #RH what do I need this for??

numPlayers   = 1   # 1 for human vs. computer, 2 for human vs. human
playerTurn   = 1   # 1 (human) or -1 ? 2 (computer) - computer is always player 2 (blue fleet) if single player mode
turnNum      = 0   # which turn is it? start from zero? or 1?
playCount    = 0   # a play is one round, i.e. computer and human each taking a turn

AImoveIndex  = 0   # used to fetch moves from ai_moves list (until a better approach is developed)
AImoveIndexSize = 0
playColumn   = 12  # ai always picks this on first move
#leftRight    = 0   # for random ai movement

#whoGoesFirst = 1   # red fleet always goes first  # 1 (player #1) or -1 (player #2) if I ever support two human players...
# can be changed at game start: if I ever support two human players...

#colorPlayer1 = red
#colorPlayer2 = blue

winner      = 0   # 1 (human) or -1 ? 2 (computer) - winning player
# stats: num victories by each player/computer
winsPlayer1 = 0   # human
winsPlayer2 = 0   # computer

delay = 200

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
    #def __init__(self, shipNum, fleet?, num_masts, image, moved, direction, shipType):

        self.shipNum = shipNum
        self.color = color
        self.image = image
        self.p_row_num = p_row_num
        self.p_col_num = p_col_num
        self.num_masts = num_masts
        self.moved = moved
        self.direction = direction   # Rotation is counter-clockwise: if 0 = N, 90 = W, 180 = S, 270 = E
        self.shipType = shipType   # 0 = merch?
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
    #   def __init__(self, shipNum, color, image, p_row_num, p_col_num, num_masts, moved, direction, shipType, label)
    #                     Num, color,    image,    row,col,mast,moved,dir,Type, label)
    #pieceArray.append(Piece(1,  'red',  ship_red_4, 12, 10, 1, 0, 0, 1, 'Man of War'))  # British Fleet 
    for i in range(pieceNum+1):
        pieceArray.append(Piece(0,  '',  '', 0, 0, 0, 0, 0, 0, ''))  # dummy data

def resetPieceArray():  # initialize array of class Piece
    print("")
    print("resetPieceArray")    # debug

    pieceArray[1]  = Piece(1,  'red',  ship_red_4, 12, 10, 2, 0, 0, 1, 'Man of War')  # British Fleet 
    pieceArray[2]  = Piece(2,  'red',  ship_red_4, 12, 11, 2, 0, 0, 1, 'Man of War')  # British Fleet 
    pieceArray[3]  = Piece(3,  'red',  ship_red_4, 12, 12, 1, 0, 0, 1, 'Man of War')  # British Fleet 
    pieceArray[4]  = Piece(4,  'red',  ship_red_4, 12, 13, 1, 0, 0, 1, 'Man of War')  # British Fleet 
    pieceArray[5]  = Piece(5,  'red',  ship_red_4, 12, 14, 3, 0, 0, 1, 'Man of War')  # British Fleet 
    pieceArray[6]  = Piece(6,  'red',  ship_red_4, 13, 10, 4, 0, 0, 1, 'Man of War')  # British Fleet 
    pieceArray[7]  = Piece(7,  'red',  ship_red_4, 13, 11, 4, 0, 0, 1, 'Man of War')  # British Fleet 
    pieceArray[8]  = Piece(8,  'red',  ship_red_4, 13, 12, 2, 0, 0, 1, 'Man of War')  # British Fleet 
    pieceArray[9]  = Piece(9,  'red',  ship_red_4, 13, 13, 3, 0, 0, 1, 'Man of War')  # British Fleet 
    pieceArray[10] = Piece(10, 'red',  ship_red_4, 13, 14, 3, 0, 0, 1, 'Man of War')  # British Fleet 

    pieceArray[11] = Piece(11, 'blue', ship_blue_4, 1, 2, 3, 0, 180, 2, 'Man of War')  # American Fleet
    pieceArray[12] = Piece(12, 'blue', ship_blue_4, 1, 4, 1, 0, 180, 2, 'Man of War')  # American Fleet
    pieceArray[13] = Piece(13, 'blue', ship_blue_4, 1, 5, 3, 0, 180, 2, 'Man of War')  # American Fleet
    pieceArray[14] = Piece(14, 'blue', ship_blue_4, 1, 6, 1, 0, 180, 2, 'Man of War')  # American Fleet
    pieceArray[15] = Piece(15, 'blue', ship_blue_4, 1, 7, 1, 0, 180, 2, 'Man of War')  # American Fleet
    pieceArray[16] = Piece(16, 'blue', ship_blue_4, 1, 8, 2, 0, 180, 2, 'Man of War')  # American Fleet
    pieceArray[17] = Piece(17, 'blue', ship_blue_4, 1, 9, 3, 0, 180, 2, 'Man of War')  # American Fleet
    pieceArray[18] = Piece(18, 'blue', ship_blue_4, 1,10, 1, 0, 180, 2, 'Man of War')  # American Fleet
    pieceArray[19] = Piece(19, 'blue', ship_blue_4, 1,11, 3, 0, 180, 2, 'Man of War')  # American Fleet
    pieceArray[20] = Piece(20, 'blue', ship_blue_4, 1,12, 2, 0, 180, 2, 'Man of War')  # American Fleet

    pieceArray[21] = Piece(21, 'blue', ship_merchant, 0, 4, 1, 1, 180, 3, 'Merchant')  # American Merchant Ships
    pieceArray[22] = Piece(22, 'blue', ship_merchant, 0, 6, 1, 1, 180, 3, 'Merchant')  # American Merchant Ships
    pieceArray[23] = Piece(23, 'blue', ship_merchant, 0, 8, 1, 1, 180, 3, 'Merchant')  # American Merchant Ships
    pieceArray[24] = Piece(24, 'blue', ship_merchant, 0,10, 1, 1, 180, 3, 'Merchant')  # American Merchant Ships

    ## debug:
    #print("print pieceArray (debug)")
    #print("shipNum, color, image, p_row_num, p_col_num, num_masts, moved, direction, shipType, label")
    #for i in range(1,pieceNum+1):
    #    print(pieceArray[i].shipNum,pieceArray[i].color,pieceArray[i].image,pieceArray[i].p_row_num,pieceArray[i].p_col_num,pieceArray[i].num_masts,pieceArray[i].moved,pieceArray[i].direction,pieceArray[i].shipType,pieceArray[i].label)
    #print("")


################################################################################################
################################################################################################
# see line 2760...

#game_setup()           # what background for setup & instructions?
    #initTerrain()
    #refreshGameScreen()

#user_instructions()
#userDeploymentRules()  # needed?  just which ships are in which of the 10 locs
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


#########################################################
def drawScreenSetup():
    screen.fill(black)    # erase screen #
    screen.blit(bgScreen_0, (0, 0))    # load background image, loc must be a tuple
    # load sidebar ship images #
    screen.blit(bgr_ship_5, (0,0))      # left margin:   570 - 50 = 520 (500?)
    screen.blit(bgr_ship_4, (0,720))
    screen.blit(bgr_ship_6, (2060,0))   # right margin: 1970 + 50 = 2020 (2040?)
    screen.blit(bgr_ship_2, (2060,720))

def redrawGameWindow():
    #print("redrawGameWindow")
    screen.fill(black)    # erase screen #
    screen.blit(bgScreen_0, (0, 0))    # load background image, loc must be a tuple
    drawLandImages()    # draw land #
    # load sidebar ship images #
    # graphic border image size 500 x 720 (4 images)
    screen.blit(bgr_ship_5, (0,0))      # left margin:   570 - 50 = 520 (500?)
    screen.blit(bgr_ship_4, (0,720))
    screen.blit(bgr_ship_6, (2060,0))   # right margin: 1970 + 50 = 2020 (2040?)
    screen.blit(bgr_ship_2, (2060,720))

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
def moveCheck():
    # check entered move for validity...

    # inputs are: sq_row new_sq_row sq_col new_sq_col
    # outputs are: moveValid

    print("")
    print("##----  moveCheck  ----##")
    print("")

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
        print("## computer's turn (AI) ##")
    elif playerTurn == 1:   # human
        print("## human's turn ##")
    # golden display of row/col move #
    print("sq_row     =",sq_row,"     sq_col =",sq_col)
    print("new_sq_row =",new_sq_row," new_sq_col =",new_sq_col)

    # check move...
    if sq_row != new_sq_row and sq_col != new_sq_col:      # if neither is the same, error!
        print("mistaken input, sound the alarm!!")
        new_sq_row = 0
        new_sq_col = 0
        sq_row = 0     # reset to new click mode
        sq_col = 0
        moveValid  = 0
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
        print("check path along row or column for obstacles")
        # what direction to turn for move? check d_col (+/-), d_row (+/-) (delta row/column)
        # d_row+ = N   (0), d_row- = S (180)
        # d_col+ = E (270), d_col- = W  (90)
        #----------------------------
        d_row = new_sq_row - sq_row
        d_col = new_sq_col - sq_col
        print("d_row =",d_row," d_col =",d_col)
        pmr = 0  # plus/minus row
        pmc = 0  # plus/minus col
        # direction?
        if sq_row == new_sq_row:
            print("# horizontal move: sq_row = new_sq_row")
            if d_col < 0:
                direction = 90   # W
                pmc = -1
            elif d_col > 0:
                direction = 270  # E
                pmc = 1
            moveRange = d_col * pmc
        elif sq_col == new_sq_col:
            print("# vertical move: sq_col = new_sq_col")
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
            print("")
            print("square: irow =",irow," icol =",icol)
            print("i =",i," terrain =",terrain[irow][icol])
            if terrain[irow][icol] != 'S':   # might be an error... maybe
                if terrain[irow][icol] == 'L' or terrain[irow][icol] == 'G':
                    print("land")
                    print("mistaken input, sound the alarm!!")
                    moveValid = 0
                    print("moveValid =",moveValid) 
                    new_sq_row = 0  # to deselect the destination square (mistake)
                    new_sq_col = 0
                    sq_row = 0      # reset to new click mode
                    sq_col = 0
                    refreshGameScreen()   # erase red square?
                    break  # to exit for loop
                elif terrain[irow][icol] == 'R' or terrain[irow][icol] == 'B' or terrain[irow][icol] == 'M':
                    if playerTurn == -1 and terrain[irow][icol] == 'M':   # AI
                        moveValid = 0
                        print("Mine!")
                        print("moveValid =",moveValid) 
                        break  # to exit for loop
                    else:
                        print("R,B,M")
                        print("moveValid =",moveValid) 
            elif terrain[irow][icol] == 'S':
                for j in range(1,pieceNum+1):
                    if pieceArray[j].p_row_num == irow and pieceArray[j].p_col_num == icol:
                        print("There's a ship in the way, sound the alarm!!") 
                        print("ship[row] =",pieceArray[j].p_row_num," ship[col] =",pieceArray[j].p_col_num)
                        moveValid = 0
                        print("moveValid =",moveValid) 

        if moveValid == 0:
            new_sq_row = 0     # to deselect the destination square (mistake)
            new_sq_col = 0
            sq_row = 0     # reset to new click mode
            sq_col = 0
            #alarmBellSound.play()  # error sound
            #if playerTurn == -1:
            #    pygame.time.delay(2000)
            refreshGameScreen()   # erase red square?

        # end moveCheck for loop
        print("")
        print("# end moveCheck For Loop...")
        print("moveValid =",moveValid)  # moveValid = 1  # if it passes move checking
        print("sq_row     =",sq_row,"     sq_col =",sq_col)
        print("new_sq_row =",new_sq_row," new_sq_col =",new_sq_col)
        print("end square: irow =",irow," icol =",icol)

# end moveCheck()


#########################################################
def moveShip():
    # move ship per valid entry to destination, one square at a time
    # check any cannon or mine results along the way...

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
    #global humanPlayerMoved

    global playerTurn   # 1 (human) or -1 (computer)
    global turnNum
    global playCount

    # move ship...
    if moveValid == 1:
        print("")
        print("##----  move ship  ----##")
        print("")
        # debug:
        if playerTurn == -1:   # AI
            print("## computer's turn (AI) ##")
        elif playerTurn == 1:   # human
            print("## human's turn ##")

        twoBellsSound.play()  # good move
        print("shipSelected =",shipSelected)
        print("sq_row     =",sq_row,"     sq_col =",sq_col)
        print("new_sq_row =",new_sq_row," new_sq_col =",new_sq_col)
        print("pmr =",pmr," pmc =",pmc)
        print("moveRange =",moveRange)
        print("direction =",direction)

        pieceArray[shipSelected].direction = direction

        # increment from current sq to new sq:
        for i in range (1,moveRange + 1):                 
            irow = sq_row + pmr*i
            icol = sq_col + pmc*i
            print("")
            print("square: irow =",irow," icol =",icol)
            print("i =",i," terrain =",terrain[irow][icol])
            pieceArray[shipSelected].p_row_num = pieceArray[shipSelected].p_row_num + pmr
            pieceArray[shipSelected].p_col_num = pieceArray[shipSelected].p_col_num + pmc
            refreshGameScreen()
            if i < moveRange:
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
                        boardSquaresArray[irow][icol].mine = 0
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
                print("move ahead 1: move code") 
                refreshGameScreen()
                if i < moveRange:
                    if playerTurn == 1:
                        boardSquaresArray[new_sq_row][new_sq_col].drawRed()  # highlight destination square
                    elif playerTurn == -1:
                        boardSquaresArray[new_sq_row][new_sq_col].drawBlue()  # highlight destination square
                pygame.time.delay(delay)

        # end moveShip For Loop
        print("")
        print("## Arrived at Destination ##")
        print("shipSelected.num_masts =",pieceArray[shipSelected].num_masts)
        print("shipSelected.p_col_num =",pieceArray[shipSelected].p_col_num)
        print("shipSelected.p_row_num =",pieceArray[shipSelected].p_row_num)
        new_sq_row = 0
        new_sq_col = 0
        sq_row = 0     # reset to new click mode
        sq_col = 0
        refreshGameScreen()
        pygame.display.update()   # debug?

    elif moveValid == 0:
        print("movS: mistaken input, moveValid = 0")

# end def moveShip():


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
    #global humanPlayerMoved  # needed?
    global playerTurn   # 1 (human) or -1 (computer)
    global turnNum
    global playCount

    # check for combat...
    if moveValid == 1:
        print("")
        print("##----  combatCheck  ----##")
        print("")
        # debug:
        if playerTurn == -1:   # AI
            print("## computer's turn (AI) ##")
        elif playerTurn == 1:   # human
            print("## human's turn ##")

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
        print("comC: mistaken input, moveValid = 0")

    # clear moveValid for next turn...
    moveValid = 0  # no longer needed, done at moveCheck

# end combatCheck()


#########################################################
def set_AI_Strategy():
    # set strategy (random)
    global boardSquaresArray

    #boardSquaresArray[j][i].shoreBatt = 0/1  #  1-5, 8-12  # must be R squares, not G squares? not yet? 
    #boardSquaresArray[j][i].mine      = 0/1  #  2/3/4, 9/10/11 
    
    print("")
    print("# set_AI_Strategy #")   
    dieRoll = random.randint(1, 6)   # Return a random integer N such that 1 <= N <= 6
    print("dieRoll =",dieRoll)   # debug

    # set strategy & cannon/mine placement:
    if dieRoll <= 2:
        AI_Strategy = 1  # hang back, passive defense (right side full clog)
        print("AI_Strategy =",AI_Strategy)   
        # cannons left:
        boardSquaresArray[7][ 1].shoreBatt = 0  # debug # must be R squares, not G squares
        boardSquaresArray[7][ 2].shoreBatt = 0  # debug # must be R squares, not G squares
        boardSquaresArray[7][ 3].shoreBatt = 0  # debug # must be R squares, not G squares
        boardSquaresArray[7][ 4].shoreBatt = 0  # debug # must be R squares, not G squares
        boardSquaresArray[7][ 5].shoreBatt = 0  # debug # must be R squares, not G squares
        # cannons right:
        boardSquaresArray[7][ 8].shoreBatt = 1  # debug # must be R squares, not G squares 
        boardSquaresArray[7][ 9].shoreBatt = 1  # debug # must be R squares, not G squares
        boardSquaresArray[7][10].shoreBatt = 2  # debug # must be R squares, not G squares
        boardSquaresArray[7][11].shoreBatt = 1  # debug # must be R squares, not G squares
        boardSquaresArray[7][12].shoreBatt = 1  # debug # must be R squares, not G squares 
        # mines (3, can't have three in a row)
        dieRoll = random.randint(1, 6)   # Return a random integer N such that 1 <= N <= 6
        print("2nd dieRoll =",dieRoll)   # debug
        if dieRoll <= 3:
            boardSquaresArray[5][ 2].mine = 1  # debug
            boardSquaresArray[5][ 3].mine = 0  # debug
            boardSquaresArray[5][ 4].mine = 0  # debug
            boardSquaresArray[5][ 9].mine = 1  # debug
            boardSquaresArray[5][10].mine = 0  # debug
            boardSquaresArray[5][11].mine = 1  # debug
        else:
            boardSquaresArray[5][ 2].mine = 0  # debug
            boardSquaresArray[5][ 3].mine = 0  # debug
            boardSquaresArray[5][ 4].mine = 1  # debug
            boardSquaresArray[5][ 9].mine = 0  # debug
            boardSquaresArray[5][10].mine = 1  # debug
            boardSquaresArray[5][11].mine = 1  # debug
    elif dieRoll <= 4:
        AI_Strategy = 2  # hit & run? hit any invaders? Or Agreessive? (both sides even)
        print("AI_Strategy =",AI_Strategy)   
        # cannons left:
        boardSquaresArray[7][ 1].shoreBatt = 0  # debug # must be R squares, not G squares
        boardSquaresArray[7][ 2].shoreBatt = 0  # debug # must be R squares, not G squares
        boardSquaresArray[7][ 3].shoreBatt = 1  # debug # must be R squares, not G squares
        boardSquaresArray[7][ 4].shoreBatt = 1  # debug # must be R squares, not G squares
        boardSquaresArray[7][ 5].shoreBatt = 1  # debug # must be R squares, not G squares
        # cannons right:
        boardSquaresArray[7][ 8].shoreBatt = 0  # debug # must be R squares, not G squares 
        boardSquaresArray[7][ 9].shoreBatt = 0  # debug # must be R squares, not G squares
        boardSquaresArray[7][10].shoreBatt = 1  # debug # must be R squares, not G squares
        boardSquaresArray[7][11].shoreBatt = 1  # debug # must be R squares, not G squares
        boardSquaresArray[7][12].shoreBatt = 1  # debug # must be R squares, not G squares 
        # mines (3, can't have three in a row)
        dieRoll = random.randint(1, 6)   # Return a random integer N such that 1 <= N <= 6
        print("2nd dieRoll =",dieRoll)   # debug
        if dieRoll <= 3:
            boardSquaresArray[5][ 2].mine = 1  # debug
            boardSquaresArray[5][ 3].mine = 0  # debug
            boardSquaresArray[5][ 4].mine = 0  # debug
            boardSquaresArray[5][ 9].mine = 1  # debug
            boardSquaresArray[5][10].mine = 0  # debug
            boardSquaresArray[5][11].mine = 1  # debug
        else:
            boardSquaresArray[5][ 2].mine = 1  # debug
            boardSquaresArray[5][ 3].mine = 0  # debug
            boardSquaresArray[5][ 4].mine = 1  # debug
            boardSquaresArray[5][ 9].mine = 1  # debug
            boardSquaresArray[5][10].mine = 0  # debug
            boardSquaresArray[5][11].mine = 0  # debug
    elif dieRoll <= 6:
        AI_Strategy = 3  # plug entrances to prevent incursion, chase any breaches. Or set a trap? how? (left side full clog?)
        print("AI_Strategy =",AI_Strategy)   
        # cannons left:
        boardSquaresArray[7][ 1].shoreBatt = 1  # debug # must be R squares, not G squares
        boardSquaresArray[7][ 2].shoreBatt = 1  # debug # must be R squares, not G squares
        boardSquaresArray[7][ 3].shoreBatt = 1  # debug # must be R squares, not G squares
        boardSquaresArray[7][ 4].shoreBatt = 0  # debug # must be R squares, not G squares
        boardSquaresArray[7][ 5].shoreBatt = 0  # debug # must be R squares, not G squares
        # cannons right:
        boardSquaresArray[7][ 8].shoreBatt = 0  # debug # must be R squares, not G squares 
        boardSquaresArray[7][ 9].shoreBatt = 0  # debug # must be R squares, not G squares
        boardSquaresArray[7][10].shoreBatt = 1  # debug # must be R squares, not G squares
        boardSquaresArray[7][11].shoreBatt = 1  # debug # must be R squares, not G squares
        boardSquaresArray[7][12].shoreBatt = 1  # debug # must be R squares, not G squares 
        # mines (3, can't have three in a row)
        dieRoll = random.randint(1, 6)   # Return a random integer N such that 1 <= N <= 6
        print("2nd dieRoll =",dieRoll)   # debug
        if dieRoll <= 3:
            boardSquaresArray[5][ 2].mine = 1  # debug
            boardSquaresArray[5][ 3].mine = 0  # debug
            boardSquaresArray[5][ 4].mine = 1  # debug
            boardSquaresArray[5][ 9].mine = 0  # debug
            boardSquaresArray[5][10].mine = 0  # debug
            boardSquaresArray[5][11].mine = 1  # debug
        else:
            boardSquaresArray[5][ 2].mine = 0  # debug
            boardSquaresArray[5][ 3].mine = 0  # debug
            boardSquaresArray[5][ 4].mine = 1  # debug
            boardSquaresArray[5][ 9].mine = 1  # debug
            boardSquaresArray[5][10].mine = 0  # debug
            boardSquaresArray[5][11].mine = 1  # debug

    # debug:
    #print("AI_Strategy =",AI_Strategy)   
    # debug:
    print("")
    print("print boardSquaresArray rows 5 & 7:")
    print("r,c","\t","t,c/m")
    #print("")
    #print(boardSquaresArray)
    j = 5   # rows
    for i in range(15):   # cols
        print(boardSquaresArray[j][i].row_num,boardSquaresArray[j][i].col_num,"\t",boardSquaresArray[j][i].terrain,boardSquaresArray[j][i].mine)
    print("")
    j = 7   # rows
    for i in range(15):   # cols
        print(boardSquaresArray[j][i].row_num,boardSquaresArray[j][i].col_num,"\t",boardSquaresArray[j][i].terrain,boardSquaresArray[j][i].shoreBatt)

    global AImoveIndex
    AImoveIndex  = 0
    global AImoveIndexSize
    AImoveIndexSize = 31

    global ai_moves
    ai_moves = np.zeros((AImoveIndexSize,4))  # rows, columns
    ai_moves = [
    # 0  1  2  3
    [ 1,12, 6,12],  # 0 a  # Move to block entry
    [ 6,12, 6,11],  # 1 b
    [ 1, 8, 6, 8],  # 2 a  # Move to block entry
    [ 6, 8, 6, 9],  # 3 b
    [ 1,11, 4,11],  # 4  # defensive 
    [ 1, 9, 3, 9],  # 5  # defensive
    [ 1, 5, 6, 5],  # 6 a  # Move to block entry
    [ 6, 5, 6, 4],  # 7 b
    [ 1, 2, 2, 2],  # 8  # defensive
    [ 1, 7, 1, 8],  # 9   # merc prot
    [ 4,11, 4,10],  #10  # defensive
    [ 3,10, 3,14],  #11  # defensive
    [ 2, 2, 2, 1],  #12  # defensive
    [ 4,10, 4, 3],  #13  # defensive
    [ 3,14, 3,10],  #14  # defensive
    [ 2, 1, 2, 3],  #15  # defensive
    [ 4, 3, 4,10],  #16  # defensive
    [ 3,10, 3,14],  #17  # defensive
    [ 2, 3, 2, 1],  #18  # defensive
    [ 4,10, 4, 3],  #19  # defensive
    [ 3,14, 3,10],  #20  # defensive
    [ 2, 1, 2, 3],  #21  # defensive
    [ 4, 3, 4,10],  #22  # defensive
    [ 3,10, 3,14],  #23  # defensive
    [ 2, 3, 2, 1],  #24  # defensive
    [ 4,10, 4, 3],  #25  # defensive
    [ 3,14, 3,10],  #26  # defensive
    [ 2, 1, 2, 3],  #27  # defensive
    [ 4, 3, 4,10],  #28  # defensive
    [ 3,10, 3,14],  #29  # defensive
    [ 2, 3, 2, 1]   #30  # defensive
    ]

    # AI ship starting positions:
    # r c  ter Num
    # 1 2   S  11  # 3
    # 1 4   S  12  # 1 merc prot
    # 1 5   S  13  # 3
    # 1 6   S  14  # 1 merc prot
    # 1 7   S  15  # 1 merc prot
    # 1 8   S  16  # 2
    # 1 9   S  17  # 3 
    # 1 10  S  18  # 1 merc prot
    # 1 11  S  19  # 3
    # 1 12  S  20  # 2

    print("")
    for i in range(AImoveIndexSize):    # includes test move 0
        print("ai_moves =",i,"\t",ai_moves[i])


#########################################################
def shipNumLookup():
    # looks up what shipNum is at current location, if any
    print("# shipNumLookup #")
    global shipSelected  # needed for moveShip
    global sq_row   # ship to move
    global sq_col
    shipSelected = 0
    for i in range(1,pieceNum+1):
        if pieceArray[i].p_row_num == sq_row and pieceArray[i].p_col_num == sq_col:
            # what ship is at r/c?
            shipSelected = i
    print("shipSelected =",shipSelected)


#########################################################
def Defensive_AI():
    # AI move & attack
    # return sq_row, sq_col, new_sq_row, new_sq_col, shipSelected
    print("")
    print("##  Defensive_AI  ##")
    #print("")

    # globals:
    #global delay
    global shipNum
    global shipSelected  # needed for moveShip
    global sq_row      # ship to move
    global sq_col
    global new_sq_row  # destination
    global new_sq_col

    global moveValid   # set by moveCheck
    #global humanPlayerMoved    #RH ???
    global playerTurn   # 1 (human) or -1 (computer)
    global turnNum
    global playCount
    global AImoveIndex

    enemy_row = 0
    enemy_col = 0
    harborCheckedforRedScum = 0

    # Defensive AI:
    # make initial moves by rote, unless Red fleet enters harbor...
    # check to make sure rote moves don't subject Blue fleet to T attack (don't move into one)
    # check by quadrants where red fleet is moving?
    # check rote moves to avoid turning into a T attack
    # place ships on each row to defend harbor
    # place ships in front of merchant ships
    # use 2 mast ships to clog entrances
    # use 3 mast ships to defend harbor
    # use 1 mast ships to shield merchants
    #
    # clog up entrances!
    # Move to block entry on row 6, col 2-4, 9-11
    # 
    # How to search for Red fleet? check rows 1-6
    # How to decide on moves?
    # Look for crossing the T
    # use moveCheck to iterate until valid move found?
    # 
    # Priorities:
    # 1. defend merchant ships (block access? ship across bow of merch)
    # 2. look for T attack
    # 3. avoid being T attacked or moving into T attack
    # 4. sink single masted Red ships?
    # 5. defend the harbor, ship on each row at all times!

    #RH what is priority order in code??

    pygame.event.clear()  # clear any pending events
    run_def_AI = True

    while run_def_AI:
        # check for red ships in the harbor... if so, try to attack!
        # if not, use list of rote defensive moves to prepare

        # if harbor already checked, skip this first section to save time...
        if harborCheckedforRedScum == 0:
            print("checking for Red fleet inside the harbor...")

            for i in range (1,11):  # search by ship, check red fleet (1-10)
                print("i =",i)
                if pieceArray[i].p_row_num > 0 and pieceArray[i].p_row_num < 7:  # check for red ships in the harbor
                    print("Red fleet inside the harbor!! Attack!")
                    enemy_row = pieceArray[i].p_row_num
                    enemy_col = pieceArray[i].p_col_num

                    numInRow = [0,0,0,0,0,0,0]  # 7 members for rows 1 - 6
                    print("# check blue fleet (11-20) to find empty rows in the harbor")
                    print(numInRow)
                    for i in range (11,21):  
                        for j in range (1,7):  # for rows 1 - 6
                            if pieceArray[i].p_row_num == j:  # check for blue ships in row 1
                                numInRow[j] = numInRow[j] + 1
                    for j in range (1,7):  # for rows 1 - 6
                        print("numInRow[",j,"] =",numInRow[j])

                    #find a ship & move it to empty row, esp row #1, if any are empty
                    for i in range (1,5):  # for rows 1 - 4
                        if numInRow[i] == 0:
                            for j in range (2,7):  # for rows 2 - 6
                                if numInRow[j] > 0:
                                    for k in range (11,21):  # search blue fleet
                                        if pieceArray[k].p_row_num == j:  # check for blue ships in row j
                                            sq_row = pieceArray[k].p_row_num
                                            sq_col = pieceArray[k].p_col_num
                                            new_sq_row = i
                                            new_sq_col = pieceArray[k].p_col_num
                                            break
                            for j in range (2,7):  # for rows 2 - 6
                                if numInRow[j] > 1:
                                    for k in range (11,21):  # search blue fleet
                                        if pieceArray[k].p_row_num == j:  # check for blue ships in row j
                                            sq_row = pieceArray[k].p_row_num
                                            sq_col = pieceArray[k].p_col_num
                                            new_sq_row = i
                                            new_sq_col = pieceArray[k].p_col_num
                                            break
                            for j in range (1,7):  # for rows 1 - 6
                                if numInRow[j] > 2:
                                    for k in range (11,21):  # search blue fleet
                                        if pieceArray[k].p_row_num == j and pieceArray[k].num_masts > 1:  # check for blue ships in row j
                                            sq_row = pieceArray[k].p_row_num
                                            sq_col = pieceArray[k].p_col_num
                                            new_sq_row = i
                                            new_sq_col = pieceArray[k].p_col_num
                                            break
                            moveCheck()
                            if moveValid == 1:
                                print("moveValid =",moveValid) 
                                print("sq_row     =",sq_row,"     sq_col =",sq_col)
                                print("new_sq_row =",new_sq_row," new_sq_col =",new_sq_col)
                                #boardSquaresArray[sq_row][sq_col].drawBlue()
                                #boardSquaresArray[new_sq_row][new_sq_col].drawBlue()
                                shipNumLookup()
                                #click.play()
                                #run_def_AI = False
                                break

                    #RH try this...
                    if enemy_row == 1:
                        for i in range (11,21):  # search blue fleet
                            if pieceArray[i].p_row_num == 1:   # check for blue ships in row 1 if Red there
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
                                    print("sq_row     =",sq_row,"     sq_col =",sq_col)
                                    print("new_sq_row =",new_sq_row," new_sq_col =",new_sq_col)
                                    #boardSquaresArray[sq_row][sq_col].drawBlue()
                                    #boardSquaresArray[new_sq_row][new_sq_col].drawBlue()
                                    shipNumLookup()
                                    click.play()
                                    #run_def_AI = False
                                    break

                    for j in range (11,21):  # search by ship, check blue fleet (11-20)
                    #    if enemy_row == 1:
                    #        if pieceArray[j].p_row_num == 1:   # check for blue ships in row 1 if Red there
                        # check for crossing the T attacks...
                        if pieceArray[j].p_row_num == enemy_row - 1:  # check for blue ships in adjacent row
                            if pieceArray[i].direction == 0 or pieceArray[i].direction == 180:
                                print("T attack!")
                                new_sq_row = enemy_row - 1
                                new_sq_col = enemy_col
                                sq_row = pieceArray[j].p_row_num
                                sq_col = pieceArray[j].p_col_num
                                moveCheck()
                                print("return to AI...")
                                print("moveValid =",moveValid) 
                                print("sq_row     =",sq_row,"     sq_col =",sq_col)
                                print("new_sq_row =",new_sq_row," new_sq_col =",new_sq_col)
                                if moveValid == 1:
                                    break
                        if pieceArray[j].p_row_num == enemy_row + 1:  # check for blue ships in adjacent row
                            if pieceArray[i].direction == 0 or pieceArray[i].direction == 180:
                                print("T attack!")
                                new_sq_row = enemy_row + 1
                                new_sq_col = enemy_col
                                sq_row = pieceArray[j].p_row_num
                                sq_col = pieceArray[j].p_col_num
                                moveCheck()
                                print("return to AI...")
                                print("moveValid =",moveValid) 
                                print("sq_row     =",sq_row,"     sq_col =",sq_col)
                                print("new_sq_row =",new_sq_row," new_sq_col =",new_sq_col)
                                if moveValid == 1:
                                    break
                        if pieceArray[j].p_col_num == enemy_col - 1:  # check for blue ships in adjacent col
                            if pieceArray[i].direction == 90 or pieceArray[i].direction == 270:
                                print("T attack!")
                                new_sq_row = enemy_row
                                new_sq_col = enemy_col - 1
                                sq_row = pieceArray[j].p_row_num
                                sq_col = pieceArray[j].p_col_num
                                moveCheck()
                                print("return to AI...")
                                print("moveValid =",moveValid) 
                                print("sq_row     =",sq_row,"     sq_col =",sq_col)
                                print("new_sq_row =",new_sq_row," new_sq_col =",new_sq_col)
                                if moveValid == 1:
                                    break
                        if pieceArray[j].p_col_num == enemy_col + 1:  # check for blue ships in adjacent col
                            if pieceArray[i].direction == 90 or pieceArray[i].direction == 270:
                                print("T attack!")
                                new_sq_row = enemy_row
                                new_sq_col = enemy_col + 1
                                sq_row = pieceArray[j].p_row_num
                                sq_col = pieceArray[j].p_col_num
                                moveCheck()
                                print("return to AI...")
                                print("moveValid =",moveValid) 
                                print("sq_row     =",sq_row,"     sq_col =",sq_col)
                                print("new_sq_row =",new_sq_row," new_sq_col =",new_sq_col)
                                if moveValid == 1:
                                    break
                    # end 1st inside for loop
                    if moveValid == 0:
                        for j in range (11,21):  # search by ship, check blue fleet (11-20)
                            # no T attacks, now check for broadside attacks...
                            if pieceArray[j].p_row_num == enemy_row - 1:  # check for blue ships in adjacent row
                                new_sq_row = enemy_row - 1
                                new_sq_col = enemy_col
                                sq_row = pieceArray[j].p_row_num
                                sq_col = pieceArray[j].p_col_num
                                moveCheck()
                                print("return to AI...")
                                print("moveValid =",moveValid) 
                                print("sq_row     =",sq_row,"     sq_col =",sq_col)
                                print("new_sq_row =",new_sq_row," new_sq_col =",new_sq_col)
                                if moveValid == 1:
                                    break
                            if pieceArray[j].p_row_num == enemy_row + 1:  # check for blue ships in adjacent row
                                new_sq_row = enemy_row + 1
                                new_sq_col = enemy_col
                                sq_row = pieceArray[j].p_row_num
                                sq_col = pieceArray[j].p_col_num
                                moveCheck()
                                print("return to AI...")
                                print("moveValid =",moveValid) 
                                print("sq_row     =",sq_row,"     sq_col =",sq_col)
                                print("new_sq_row =",new_sq_row," new_sq_col =",new_sq_col)
                                if moveValid == 1:
                                    break
                            if pieceArray[j].p_col_num == enemy_col - 1:  # check for blue ships in adjacent col
                                new_sq_row = enemy_row
                                new_sq_col = enemy_col - 1
                                sq_row = pieceArray[j].p_row_num
                                sq_col = pieceArray[j].p_col_num
                                moveCheck()
                                print("return to AI...")
                                print("moveValid =",moveValid) 
                                print("sq_row     =",sq_row,"     sq_col =",sq_col)
                                print("new_sq_row =",new_sq_row," new_sq_col =",new_sq_col)
                                if moveValid == 1:
                                    break
                            if pieceArray[j].p_col_num == enemy_col + 1:  # check for blue ships in adjacent col
                                new_sq_row = enemy_row
                                new_sq_col = enemy_col + 1
                                sq_row = pieceArray[j].p_row_num
                                sq_col = pieceArray[j].p_col_num
                                moveCheck()
                                print("return to AI...")
                                print("moveValid =",moveValid) 
                                print("sq_row     =",sq_row,"     sq_col =",sq_col)
                                print("new_sq_row =",new_sq_row," new_sq_col =",new_sq_col)
                                if moveValid == 1:
                                    break
                        # end 2nd inside for loop


                #print("Red fleet inside the harbor, done checking for an attack move:")
                #print("moveValid =",moveValid) 
                #print("sq_row     =",sq_row,"     sq_col =",sq_col)
                #print("new_sq_row =",new_sq_row," new_sq_col =",new_sq_col)

                # AI result?
                if moveValid == 1:
                    #shipNumLookup()
                    #boardSquaresArray[sq_row][sq_col].drawBlue()
                    #boardSquaresArray[new_sq_row][new_sq_col].drawBlue()
                    #print("sq_row     =",sq_row,"     sq_col =",sq_col)
                    #print("new_sq_row =",new_sq_row," new_sq_col =",new_sq_col)
                    #click.play()
                    ##harborCheckedforRedScum = 1
                    ##run_def_AI = False
                    break
                elif moveValid == 0:
                    print("AI can't find an attack move... check next red ship...")
                    print("moveValid =",moveValid) 
                    #harborCheckedforRedScum = 1
                    new_sq_row = 0
                    new_sq_col = 0
                    sq_row = 0     # reset to new click mode
                    sq_col = 0
                    shipNumLookup()  # to clear it
                    #print("try the list instead?")

            # end for loop
            harborCheckedforRedScum = 1
            print("")
            print("harborCheckedforRedScum =",harborCheckedforRedScum)
            print("done checking for Red fleet inside the harbor...")
            #print("moveValid =",moveValid) 
            #print("sq_row     =",sq_row,"     sq_col =",sq_col)
            #print("new_sq_row =",new_sq_row," new_sq_col =",new_sq_col)
            if moveValid == 1:
                print("# AI found an attack move...")
                print("moveValid =",moveValid) 
                shipNumLookup()
                boardSquaresArray[sq_row][sq_col].drawBlue()
                boardSquaresArray[new_sq_row][new_sq_col].drawBlue()
                print("sq_row     =",sq_row,"     sq_col =",sq_col)
                print("new_sq_row =",new_sq_row," new_sq_col =",new_sq_col)
                click.play()
                run_def_AI = False   # ends the while loop! RH
            elif moveValid == 0:
                print("# AI can't find an attack move...")
                print("moveValid =",moveValid) 
                print("trying the list instead...")
                #print("AImoveIndex =",AImoveIndex)
                new_sq_row = 0
                new_sq_col = 0
                sq_row = 0     # reset to new click mode
                sq_col = 0
                shipNumLookup()

        ##################################
        elif harborCheckedforRedScum == 1:
            print("")
            print("skipped checking for Red fleet inside the harbor...")

            #if moveValid == 1:
            #    print("")
            #    print("# AI found an attack move...")
            #    print("moveValid =",moveValid) 
            #    run_def_AI = False
            #elif moveValid == 0:
            #    print("")
            #    print("# AI can't find an attack move...")
            #    print("moveValid =",moveValid) 
            #    print("trying the list instead...")
            #    print("AImoveIndex =",AImoveIndex)

            if AImoveIndex < AImoveIndexSize:   # we have index moves left
                for i in range(AImoveIndex,AImoveIndexSize):
                    sq_row = ai_moves[i][0]
                    sq_col = ai_moves[i][1]
                    shipNumLookup()
                    if shipSelected > 10:
                        AImoveIndex = i
                        # list result:
                        sq_row = ai_moves[AImoveIndex][0]
                        sq_col = ai_moves[AImoveIndex][1]
                        new_sq_row = ai_moves[AImoveIndex][2]
                        new_sq_col = ai_moves[AImoveIndex][3]
                        break  # out of for loop
                #shipNumLookup()
                print("shipSelected =",shipSelected)
                if shipSelected > 10:
                    print("sq_row     =",sq_row,"     sq_col =",sq_col)
                    print("new_sq_row =",new_sq_row," new_sq_col =",new_sq_col)
                    # debug:
                    boardSquaresArray[sq_row][sq_col].drawBlue()
                    boardSquaresArray[new_sq_row][new_sq_col].drawBlue()
                    # use moveCheck to validate here; if no good, try again... new index?
                    moveCheck()
                    if moveValid == 1:
                        boardSquaresArray[sq_row][sq_col].drawBlue()
                        boardSquaresArray[new_sq_row][new_sq_col].drawBlue()
                        print("sq_row     =",sq_row,"     sq_col =",sq_col)
                        print("new_sq_row =",new_sq_row," new_sq_col =",new_sq_col)
                        click.play()
                        AImoveIndex = AImoveIndex + 1
                        run_def_AI = False   # ends the while loop! RH
                    elif moveValid == 0:
                        print("AI mistake, bad input!")
                        print("moveValid =",moveValid) 
                        print("try again...")
                        AImoveIndex = AImoveIndex + 1
                        #if AImoveIndex == (AImoveIndexSize - 1):   # can't increment any further
                        #    print("AImoveIndex =",AImoveIndex)
                        #else:
                        #    AImoveIndex = AImoveIndex + 1
                    if AImoveIndex == (AImoveIndexSize - 1):   # can't increment any further
                        print("AImoveIndex =",AImoveIndex)
                        print("list moves maxxed out... this is the last one")
                    else:
                        print("AImoveIndex =",AImoveIndex)
                elif shipSelected <= 10:
                    print("shipSelected <= 10")
                    AImoveIndex = AImoveIndex + 1
                    print("AImoveIndex =",AImoveIndex)
                    new_sq_row = 0
                    new_sq_col = 0
                    sq_row = 0     # reset to new click mode
                    sq_col = 0
                    shipNumLookup()  # to clear it
                    #print("shipSelected =",shipSelected)
                    #if AImoveIndex == (AImoveIndexSize - 1):   # can't increment any further
                    #    print("AImoveIndex =",AImoveIndex)
                    #    print("list moves maxxed out... this is the last one")

            # list moves maxxed out...
            elif AImoveIndex == AImoveIndexSize:   # can't increment any further
                print("AImoveIndex = AImoveIndexSize")
                print("AImoveIndex =",AImoveIndex)
                print("No more list moves available...")
                # see if there are any other defensive moves we can make...

                # move to cover the merchant ships: row 0, col 4/6/8/10
                print("move to cover the merchant ships...")
#                for i in range (11,21):    # check blue ships
                for j in range (4,12,2):   # for cols 4,6,8,10
                    print("i =",i," j =",j)
                    sq_row = 0
                    sq_col = j
                    shipNumLookup()
                    if pieceArray[shipSelected].shipType == 3:  # merchant in that square (column)
                        sq_row = 1
                        sq_col = j
                        shipNumLookup()
                        if pieceArray[shipSelected].shipType == 0:  # merchant in that square (column)
                            for i in range (11,21):    # check blue ships
                                if pieceArray[shipSelected].p_col_num == j and pieceArray[i].p_row_num != 1:  # move up in same column to cover
                                    sq_row = pieceArray[i].p_row_num
                                    sq_col = pieceArray[i].p_col_num
                                    new_sq_row = 1
                                    new_sq_col = pieceArray[i].p_col_num
                                    moveCheck()
                                    if moveValid == 1:
                                        print("moveValid =",moveValid) 
                                        print("sq_row     =",sq_row,"     sq_col =",sq_col)
                                        print("new_sq_row =",new_sq_row," new_sq_col =",new_sq_col)
                                        boardSquaresArray[sq_row][sq_col].drawBlue()
                                        boardSquaresArray[new_sq_row][new_sq_col].drawBlue()
                                        shipNumLookup()
                                        click.play()
                                        run_def_AI = False   # ends the while loop! RH
                                        break
                                elif pieceArray[shipSelected].p_col_num != j and pieceArray[i].p_row_num == 1:  # move in same row to cover
                                    sq_row = pieceArray[i].p_row_num
                                    sq_col = pieceArray[i].p_col_num
                                    new_sq_row = pieceArray[i].p_row_num
                                    new_sq_col = j
                                    moveCheck()
                                    if moveValid == 1:
                                        print("moveValid =",moveValid) 
                                        print("sq_row     =",sq_row,"     sq_col =",sq_col)
                                        print("new_sq_row =",new_sq_row," new_sq_col =",new_sq_col)
                                        boardSquaresArray[sq_row][sq_col].drawBlue()
                                        boardSquaresArray[new_sq_row][new_sq_col].drawBlue()
                                        shipNumLookup()
                                        click.play()
                                        run_def_AI = False   # ends the while loop! RH
                                        break
#                for i in range (11,21):    # check blue ships
#                        if pieceArray[i].p_col_num == j and pieceArray[i].p_row_num != 1:  # check for blue ships in col j not in front of merch


                # if Red in row 1 check for blue ships there, move to block access to merchants
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
                                print("sq_row     =",sq_row,"     sq_col =",sq_col)
                                print("new_sq_row =",new_sq_row," new_sq_col =",new_sq_col)
                                boardSquaresArray[sq_row][sq_col].drawBlue()
                                boardSquaresArray[new_sq_row][new_sq_col].drawBlue()
                                shipNumLookup()
                                click.play()
                                run_def_AI = False   # ends the while loop! RH
                                break

                # fold this into a loop? yes
                numInRow = [0,0,0,0,0,0,0]  # 7 members for rows 1 - 6
                print("# check blue fleet (11-20) to find empty rows in the harbor")
                for i in range (11,21):  
                    for j in range (1,7):  # for rows 1 - 6
                        if pieceArray[i].p_row_num == j:  # check for blue ships in row 1
                            numInRow[j] = numInRow[j] + 1
                for j in range (1,7):  # for rows 1 - 6
                    print("numInRow[",j,"] =",numInRow[j])

                #find a ship & move it to empty row, esp row #1, if any are empty
                for i in range (1,5):  # for rows 1 - 4
                    if numInRow[i] == 0:
                        for j in range (2,7):  # for rows 5 - 6
                            if numInRow[j] > 0:
                                for k in range (11,21):  # search blue fleet
                                    if pieceArray[k].p_row_num == j:  # check for blue ships in row j
                                        sq_row = pieceArray[k].p_row_num
                                        sq_col = pieceArray[k].p_col_num
                                        new_sq_row = i
                                        new_sq_col = pieceArray[k].p_col_num
                                        break
                        for j in range (2,7):  # for rows 1 - 6
                            if numInRow[j] > 1:
                                for k in range (11,21):  # search blue fleet
                                    if pieceArray[k].p_row_num == j:  # check for blue ships in row j
                                        sq_row = pieceArray[k].p_row_num
                                        sq_col = pieceArray[k].p_col_num
                                        new_sq_row = i
                                        new_sq_col = pieceArray[k].p_col_num
                                        break
                        for j in range (1,7):  # for rows 1 - 6
                            if numInRow[j] > 2:
                                for k in range (11,21):  # search blue fleet
                                    if pieceArray[k].p_row_num == j and pieceArray[k].num_masts > 1:  # check for blue ships in row j
                                        sq_row = pieceArray[k].p_row_num
                                        sq_col = pieceArray[k].p_col_num
                                        new_sq_row = i
                                        new_sq_col = pieceArray[k].p_col_num
                                        break
                        moveCheck()
                        if moveValid == 1:
                            print("moveValid =",moveValid) 
                            print("sq_row     =",sq_row,"     sq_col =",sq_col)
                            print("new_sq_row =",new_sq_row," new_sq_col =",new_sq_col)
                            boardSquaresArray[sq_row][sq_col].drawBlue()
                            boardSquaresArray[new_sq_row][new_sq_col].drawBlue()
                            shipNumLookup()
                            #print("shipSelected =",shipSelected)
                            click.play()
                            run_def_AI = False   # ends the while loop! RH
                            break
                        elif moveValid == 0:
                            print("AI can't find a move yet...")
                            print("moveValid =",moveValid) 
                            print("trying again...")
                            new_sq_row = 0
                            new_sq_col = 0
                            sq_row = 0     # reset to new click mode
                            sq_col = 0
                            shipNumLookup()  # to clear it
                            #print("shipSelected =",shipSelected)

                # should not get to this if moveValid = 1:
                #moveCheck()
                #if moveValid == 1:
                #    boardSquaresArray[sq_row][sq_col].drawBlue()
                #    boardSquaresArray[new_sq_row][new_sq_col].drawBlue()
                #    print("sq_row     =",sq_row,"     sq_col =",sq_col)
                #    print("new_sq_row =",new_sq_row," new_sq_col =",new_sq_col)
                #    click.play()
                #    run_def_AI = False
                #elif moveValid == 0:
                #    #print("AI can't find a move yet...")
                #    print("AI is all out of ideas...")
                #    print("moveValid =",moveValid) 
                #    #print("trying again...")
                #    new_sq_row = 0
                #    new_sq_col = 0
                #    sq_row = 0     # reset to new click mode
                #    sq_col = 0
                #    run_def_AI = False

                # free up defenders in entrances...
                if moveValid == 0:
                    sq_row = 6
                    sq_col = 4
                    shipNumLookup()
                    if shipSelected > 10:
                        new_sq_row = 6
                        new_sq_col = 5
                    else: 
                        sq_row = 6
                        sq_col = 9
                        shipNumLookup()
                        if shipSelected > 10:
                            new_sq_row = 6
                            new_sq_col = 8
                        else: 
                            sq_row = 6
                            sq_col = 11
                            shipNumLookup()
                            if shipSelected > 10:
                                new_sq_row = 6
                                new_sq_col = 12
                moveCheck()
                if moveValid == 1:
                    print("sq_row     =",sq_row,"     sq_col =",sq_col)
                    print("new_sq_row =",new_sq_row," new_sq_col =",new_sq_col)
                    boardSquaresArray[sq_row][sq_col].drawBlue()
                    boardSquaresArray[new_sq_row][new_sq_col].drawBlue()
                    shipNumLookup()
                    #print("shipSelected =",shipSelected)
                    click.play()
                    run_def_AI = False   # ends the while loop! RH
                elif moveValid == 0:
                    # time killing moves...
                    #[ 2, 1, 2, 3],
                    #[ 4, 3, 4,10],
#                    if moveValid == 0:
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
                    moveCheck()
                    if moveValid == 1:
                        print("sq_row     =",sq_row,"     sq_col =",sq_col)
                        print("new_sq_row =",new_sq_row," new_sq_col =",new_sq_col)
                        boardSquaresArray[sq_row][sq_col].drawBlue()
                        boardSquaresArray[new_sq_row][new_sq_col].drawBlue()
                        shipNumLookup()
                        #print("shipSelected =",shipSelected)
                        click.play()
                        run_def_AI = False   # ends the while loop! RH
                    elif moveValid == 0:
                        print("AI is all out of ideas...")
                        print("moveValid =",moveValid) 
                        new_sq_row = 0
                        new_sq_col = 0
                        sq_row = 0     # reset to new click mode
                        sq_col = 0
                        shipNumLookup()
                        #print("shipSelected =",shipSelected)
                        run_def_AI = False   # ends the while loop! RH  # let it go back around again? or is that an infinite loop?


                ## reset to new click mode if no move found
                #new_sq_row = 0
                #new_sq_col = 0
                #sq_row = 0     
                #sq_col = 0
                #run_def_AI = False

    # end while run_def_AI
# end Defensive_AI():


#########################################################
def game_loop():
    print("")
    print("# game_loop #")
    print("")
    print("## enter next move ##")
    print("")

    # globals:
    global delay
    global sq_row
    global sq_col
    global new_sq_row
    global new_sq_col

    global shipSelected
    global moveValid
    global numPlayers
    global humanPlayerMoved    #RH ???
    global playerTurn   # 1 (human) or -1 (computer)
    global turnNum
    global playCount
    global winner    # here?

    #numPlayers   = 1   # here? or in setup_game? # 1 for human vs. computer, 2 for human vs. human
    #winner       = 0   # here? or in victory_check? # 1 (human) or 2 (computer) - winning player

    shipSelected = 0
    humanPlayerMoved = 0   # 1 = move done # RH needed??
    playerTurn = 1
    turnNum    = 0
    playCount  = 0
    #MsgFlag = 0   # controls console window at bottom # RH do this here??

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

            # who's turn is it?
                # if AI, go to AI move function, then moveCheck, moveShip, combatCheck?
                # else proceed below for human

            if playerTurn == -1:   # AI
                print("")
                print("##-------- computer's turn (AI) --------##")
                #print("")
                # if AI, go to AI move function, return sq_row, sq_col, new_sq_row, new_sq_col
                Defensive_AI()
                print("")
                print("# AI done, going to moveCheck... #")
                moveCheck()  # already checked in def_AI?
                if moveValid == 0:
                    alarmBellSound.play()  # error sound
                    print("AI moveValid = 0, failed moveCheck...  ??")
                    pygame.time.delay(1000)  # 2000? lower?
                elif moveValid == 1:
                    moveShip()
                    combatCheck()
                    victoryCheck()
                #
                #if playerTurn == -1:
                turnNum    = turnNum + 1
                playCount  = playCount + 1   # needed?
                playerTurn = playerTurn * -1    # 1 (human) or -1 (computer)
                print("")
                print("# AI turn done #")
                print("turnNum    =",turnNum)
                print("playCount  =",playCount)   # needed?
                print("playerTurn =",playerTurn)  # 1 (human) or -1 (computer)
                print("moveValid =",moveValid) 
                pygame.display.update()   # debug? needed??

            elif playerTurn == 1:   # human
                if event.type == pygame.MOUSEBUTTONDOWN:   
                    print("")
                    print("## human's turn ##")
                    print("## enter next move ##")
                    print("")
                    print("mouse clicked")
                    print("pos[0] =",pos[0]," pos[1] =",pos[1])
                    click.play()
                    #for i in range (squareNum):
                    for j in range(14):   # rows
                        for i in range(15):   # cols
                            if boardSquaresArray[j][i].isOver(pos):
                                new_sq_row = j
                                new_sq_col = i
                                print("sq_row     =",sq_row,"     sq_col =",sq_col)
                                print("new_sq_row =",new_sq_row," new_sq_col =",new_sq_col)
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
                                    print("playCount  =",playCount)   # needed?
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

                pygame.display.update()   # debug?



#########################################################
def game_setup():   # what background music?

    print("")
    print("#=========== Welcome to Broadside ===========#")
    print("")

    global MsgFlag
    global winner
    MsgFlag = 0   # controls console window at bottom
    winner = 0

    drawScreenSetup()
    text2dispCenter50("Do You Need Instructions? (Y/N)",display_width/2,1380, white)
    pygame.display.update()
    run_setup = True

    while run_setup:
        for event in pygame.event.get():
            #pos = pygame.mouse.get_pos()
            #if event.type == pygame.QUIT:
            #    run_setup = False
            #    pygame.quit()
            #    sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    drawScreenSetup()
                    text2dispCenter50("Use Left/Right arrow to turn pages, X to exit", display_width/2, 1380, white)
                    pygame.display.update()
                    displayInstructions()
                    print("instructions done")
                    run_setup = False
            #if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    print("chose no instructions")
                    run_setup = False
                if event.key == pygame.K_q or event.key == pygame.K_x:
                    run_setup = False
                    pygame.quit()
                    sys.exit()
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

    #RH add user setup of red fleet...

    ## debug:
    #print("")
    #print("print piece array board locations")
    #print("row, col, x, y, terrain, shipNum, shoreBatt, mine, size")
    #print("")
    #for j in range(14):   # rows
    #    for i in range(15):   # cols
    #        if boardSquaresArray[j][i].shipNum > 0:
    #            print(boardSquaresArray[j][i].row_num,boardSquaresArray[j][i].col_num,"\t",boardSquaresArray[j][i].x,boardSquaresArray[j][i].y,"\t",boardSquaresArray[j][i].terrain,boardSquaresArray[j][i].shipNum,boardSquaresArray[j][i].shoreBatt,boardSquaresArray[j][i].mine,boardSquaresArray[j][i].size)

    #showKybdInputs()     # debug only
    #drawSquares()        # debug only
    #drawBoardPiecesXY()  # debug


#########################################################
def displayInstructions():
    print("")
    print("# displayInstructions #")

    i = 0

    #RH use different background?
    #blitScreenBkgnd(titleScreenM5)
    pygame.display.update()
    pygame.time.wait(2000)

    #RH fix:
    #text2dispCenter50("Use Left/Right arrow to turn pages, X to exit", display_width/2, 1380, white)
    pygame.display.update()

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
    
            print("i =",i)
    
        # copy instructions scans to the screen:
        screen.blit(instructions[i], (820, 100))   # 2560x1440
        #screen.blit(instructions[i], (345, 0))   #  1920x1080
        #screen.blit(instructions[i], (display_width/2, 0))
        pygame.display.update() 

    # end def displayInstructions():





#########################################################
# Everything above this line works...
#########################################################


################################################################################################
# stuff still in process...
################################################################################################



#RH need to add prompt for replay...
#########################################################
def victoryCheck():
    print("## victory check ##")

    # did anyone win yet?
    # if merch = 0, red wins
    # if red fleet = 0, blue wins
    # if both, tie!  # hard to imagine, but possible?

    global MsgFlag
    global MsgText
    global winner
    global winsPlayer1
    global winsPlayer2

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
        pygame.time.delay(3000)  # 2 secs
        #run_game = False  # needed?
        #pygame.time.delay(3000)  # secs
        promptForReplay()

        ## prompt For Replay
        #MsgText = "Replay? (Y/N)"
        #refreshGameScreen()
        #run_victory = True

        #while run_victory:
        #    for event in pygame.event.get():
        #        if event.type == pygame.QUIT:
        #            run_victory = False
        #            pygame.quit()
        #            sys.exit()
        #        if event.type == pygame.KEYDOWN:
        #            if event.key == pygame.K_q or event.key == pygame.K_x or event.key == pygame.K_n:  # q or x to quit, n for no replay
        #                print("")
        #                print("Q or X or N entered, exiting...")
        #                print("")
        #                run_victory = False
        #                pygame.quit()
        #                sys.exit()
        #            elif event.key == pygame.K_y:  # y to play again
        #                print("")
        #                print("Y entered, play again!")
        #                print("")
        #                game_setup()               # just blue ocean & side ships
        #                    #user_instructions()
        #                #userDeployment()          # just which ships are in which of the 10 locs
        #                    #userDeploymentRules()     # needed?
        #                set_AI_Strategy()          # to set cannons, mines, etc. 
        #                    #AI_ship_placement()       # done in initPieceArray for now
        #                run_victory = False
        #                game_loop()             # does this work?
        #                #promptForReplay()
    # end victoryCheck()



#RH no longer needed?
#########################################################
def promptForReplay():

    print("Play again?")
    global MsgFlag
    global MsgText
    MsgFlag = 1   # controls console window at bottom
    MsgText = "Replay? (Y/N)"

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
                    print("Q or or X N entered, exiting...")
                    print("")
                    run_newgame = False
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_y:
                    print("")
                    print("Y entered, restarting...")
                    print("")
                    game_setup()               # just blue ocean & side ships
                        #user_instructions()
                    #userDeployment()          # just which ships are in which of the 10 locs
                        #userDeploymentRules()     # needed?
                    set_AI_Strategy()          # to set cannons, mines, etc. 
                        #AI_ship_placement()       # done in initPieceArray for now
                    run_newgame = False
                    game_loop()             # does this work?
    # end promptForReplay()




#########################################################
#RH do I need this??
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



#########################################################
def userFleetDeployment():   
    # adjust default ship placement as needed by clicking on ship, then destination (swap ships)
    # just swap r/c locations of the two ships
    # update pieceArray after user input
    # how to know when done? click on a ship, then a valid destination square. click on a cannon? noise?
    print("")
    print("# userFleetDeployment #")

    global userDeploymentDone

    userDeploymentDone = 0

    #RH needed?
    redrawGameWindow()   # blit game board
    # text2scr("User Fleet Deployment",gmenuX1,gmenuY)
    # text2scr("Click to move ships if needed",gmenuX1,gmenuY+gmenuYinc*4)
    # text2scr("Hit D or X when done...",gmenuX1,gmenuY)

    drawBoardPieces()   # debug
    pygame.display.update() 

    pygame.event.clear()  # clear any pending events
    run_dep = True

    while run_dep:
        #clock.tick(60)

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run_dep = False
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

            # exit for any key...
            #if event.type == pygame.KEYDOWN:
            #    run_dep = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    print("X entered, exiting deployment...")
                    run_dep = False
                if event.key == pygame.K_d:
                    print("D entered, exiting deployment...")
                    run_dep = False

#RH:   use code from move ship...

'''

            if event.type == pygame.MOUSEBUTTONDOWN:
                print("MOUSEBUTTONDOWN pos[0] =",pos[0]," pos[1] =",pos[1])   # debug
                isOverUnit = False

                # erase yellow border around previous hex:
                print("isOverHex =",isOverHex)   # debug
                hexArray[isOverHex].drawBlack()

                # off screen?
                if pos[0] > 2150:
                    isOverUnit = False
                else:
                    for i in range (hexNum):
                        if hexArray[i].isOver(pos):
                            print("isOver hex =",i)   # debug
                            #hexArray[i].draw()
                            isOverUnit = True
                            isOverHex = i
                            #displayUnitStatus()
                            text2dispTopLeft("Hex #: " + str(i),gmenuX1,gmenuY+gmenuYinc*10)
                            # debug:
                            if pos[0] < 30:    # 630:
                                text2dispTopLeft("No units in red zone! Try again...",gmenuX1,gmenuY+gmenuYinc*11)
                            elif hexArray[i].terrain == 0:
                                if hexArray[i].unit == 0:
                                    text2dispTopLeft("Clear Hex",gmenuX1,gmenuY+gmenuYinc*11)
                                    pieceArray[unitNum].hexLoc = i
                                    hexArray[i].unit = unitNum
                                    run_dep = False
                                elif hexArray[i].unit != 0:
                                    text2dispTopLeft("Hex occupied! Try again...",gmenuX1,gmenuY+gmenuYinc*11)
                                    print("hex: ",i," unit: ",hexArray[i].unit)
                                    #for j in range(hexNum):
                                    #    print("hex: ",j," unit: ",hexArray[j].unit)
                            elif hexArray[i].terrain == 1:
                                text2dispTopLeft("Blocked Hex! Try again...",gmenuX1,gmenuY+gmenuYinc*11)

                if isOverUnit == False:
                    print("isOverUnit =",isOverUnit)   # debug
                    #refreshGameScreen()
                pygame.display.update()

    # end userFleetDeployment() #
'''


'''


#########################################################

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

    global playPhase
    playPhase = 0   # a play is one round, i.e., computer and human each taking a turn

    #instructionsDone = 0

    #RH needed??
    #yesButton = ButtonCir((255,255,0), 1200,70,25,'Y')
    #noButton  = ButtonCir((255,255,0), 1270,70,25,'N')
    #yesButton = Button((255,255,0), 1180,50,40,40,'Y')
    #noButton  = Button((255,255,0), 1250,50,40,40,'N')

    #redrawGameWindow()
    #pygame.display.update()

    #blitScreenBkgnd...

    blitScreenBkgnd(titleScreenM3)

    pygame.display.update()
    #pygame.time.wait(2000)

    initHexArray()   # is this ok here or do at end of setup?
    initPieceTypeArray()
    initPieceArray()
    #updatePieceArrayTest()   # debug only, do this after unit purchase

    initOgreTypeArray()
    #initOgreArray()    # later in deployment
    #updateOgreArray()

    #Show Credits
    text2dispCenter50("OGRE: Tactical Ground Combat in the 22nd Century",display_width/2,1240, white)
    text2dispCenter50("based on OGRE, by Steve Jackson, c1977",display_width/2,1310, white)
    #text2dispCenter50("OGRE: Tactical Ground Combat",display_width/2,1380, white)
    #text2dispCenter50("in the 21st Century",display_width/2,1380, white)
#    pygame.display.update()

    text2dispCenter50("Do You Need Instructions? (Y/N)",display_width/2,1380, white)
    ##text = font.render(textmsg,0,(0,255,0))
    #font = pygame.font.SysFont('arial', 40)  # comicsansms arial
    #text = "Do you need instructions?"
    #textr = font.render(text,1,white)
    #screen.blit(textr, (display_width/2 - len(text)/2,1300))   # len(textr)?

    #yesButton.draw(screen,(0,0,0))  #surface, black outline
    #noButton.draw(screen,(0,0,0))   #surface, black outline

    pygame.display.update()

    print("")
    print("game_setup => while run_setup")

    while run_setup:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run_setup = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    displayInstructions()
                    print("instructions done")
                    run_setup = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    print("chose no instructions")
                    run_setup = False
#            if event.type == pygame.MOUSEBUTTONDOWN:
#                if yesButton.isOver(pos):
#                    displayInstructions()
#                    print("instructions Done")
#                    #instructionsDone = 1
#                    run_setup = False
#            if event.type == pygame.MOUSEMOTION:
#                if yesButton.isOver(pos):
#                    yesButton.color = (0,255,0)
#                else:
#                    yesButton.color = (255,255,0)

#   end def game_setup():

'''


    #        #for i in range (1,shipNum + 1):  # to search by ship, check red fleet?
    #        for j in range(14):   # rows
    #            for i in range(15):   # cols
    #                    new_sq_row = j
    #                    new_sq_col = i
    #                    print("new_sq_row =",new_sq_row," new_sq_col =",new_sq_col)
    #                    print("sq_row     =",sq_row,"     sq_col =",sq_col)



#######################################################
# game function calls...

game_setup()               # just blue ocean & side ships
    #user_instructions()
#userDeployment()          # just which ships are in which of the 10 locs
    #userDeploymentRules()     # needed?
set_AI_Strategy()          # to set cannons, mines, etc. 
    #AI_ship_placement()       # done in initPieceArray for now
game_loop()
    # AI move & attack
    # moveCheck
    # moveShip
    # checkCombat
    # victoryCheck

#######################################################



# to hold display for debug rather than exiting...

run_wait = True

while run_wait:

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            run_wait = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                print("")
                print("Q entered, exiting...")
                print("")
                run_wait = False
                pygame.quit()
                sys.exit()


pygame.quit()
sys.exit()
