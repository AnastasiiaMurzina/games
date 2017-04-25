__author__="Anestezia"
import random, pygame, sys
from pygame.locals import *

FPS = 30 # frames per second, the general speed of the program
WINDOWWIDTH = 640 # size of window's width in pixels
WINDOWHEIGHT = 480 # size of windows' height in pixels
REVEALSPEED = 8 # speed boxes' sliding reveals and covers
BOXSIZE = 40 # size of box height & width in pixels
GAPSIZE = 10 # size of gap between boxes in pixels
BOARDWIDTH = 5# number of columns of icons
BOARDHEIGHT = 5 # number of rows of icons
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)
LVL=0
#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

map_colors = ['RED','YELLOW', 'PURPLE','GRAY', 'NAVYBLUE','GREEN','CYAN','WHITE']
k_colors=2
RAND=False
def leftTopCoordsOfBox(boxx, boxy):
    # Convert board coordinates to pixel coordinates
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)

def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)

def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(BOARDWIDTH):
        revealedBoxes.append([val] * BOARDHEIGHT)
    return revealedBoxes

def change_col(points):
    return map_colors[(map_colors.index(points)+1)%k_colors]

def getBoxAtPixel(x, y):  #get the cursor place
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)
def drawPoints(points):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            pygame.draw.rect(DISPLAYSURF, eval(points[boxx][boxy]), (left, top, BOXSIZE, BOXSIZE))

def check_won(points):
    for i in range(len(points)):
        str = points[i]
        if ('RED' in str)==True:
            return False
    return True

def field_generate():
    field = []  # np.zeros((BOARDWIDTH,BOARDHEIGHT))
    if RAND==False:
        for i in range(0, BOARDWIDTH):
            field.append(['RED' for j in range(BOARDHEIGHT)])
    else:
        for i in range(0, BOARDWIDTH):
            field.append([random.choice(map_colors[:k_colors]) for j in range(BOARDHEIGHT)])
    return field

def next_lvl():
    my_field = field_generate()  # np.zeros((BOARDWIDTH,BOARDHEIGHT))
    drawPoints(my_field)
    return my_field

def win_animation():
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR
    for i in range(13):
        DISPLAYSURF.fill(color1)
        pygame.display.update()
        DISPLAYSURF.fill(color2)
        pygame.display.update()
        pygame.time.wait(300)
    pygame.quit()
    sys.exit()

global FPSCLOCK, DISPLAYSURF
pygame.init()
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
mousex = 0  # used to store x coordinate of mouse event
mousey = 0  # used to store y coordinate of mouse event
pygame.display.set_caption('Change all')
DISPLAYSURF.fill(BGCOLOR)
my_field = field_generate()
while True:  # main game loop
    mouseClicked = False
    DISPLAYSURF.fill(BGCOLOR)  # drawing the window
    drawPoints(my_field)
    revealedBoxes = generateRevealedBoxesData(False)
    pygame.display.update()
    for event in pygame.event.get():  # event handling loop
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            mousex, mousey = event.pos
        elif event.type == MOUSEBUTTONUP:
            mousex, mousey = event.pos
            mouseClicked = True
    boxx, boxy = getBoxAtPixel(mousex, mousey)
    if boxx != None and boxy != None:
        if not revealedBoxes[boxx][boxy]:
            drawHighlightBox(boxx, boxy)
        if not revealedBoxes[boxx][boxy] and mouseClicked:
            for i in range(BOARDWIDTH):
                my_field[i][boxy] = change_col(my_field[i][boxy])
            for i in range(BOARDHEIGHT):
                my_field[boxx][i] = change_col(my_field[boxx][i])
            for i in range(k_colors-2):
                my_field[boxx][boxy]=change_col(my_field[boxx][boxy])
            my_field[boxx][boxy] = change_col(my_field[boxx][boxy])
            drawPoints(my_field)
            pygame.display.update()
            if check_won(my_field):
                # win_animation()
                LVL+=1
                if LVL==1:
                    BOARDWIDTH += 1
                    BOARDHEIGHT += 1
                if LVL==2:
                    k_colors+=1
                    BOARDHEIGHT=5
                    BOARDWIDTH=5
                if LVL==3:
                    k_colors-=1
                    BOARDWIDTH=4
                    BOARDHEIGHT=4
                    RAND=True
                if 3<LVL<10:
                    RAND=False
                    BOARDHEIGHT = random.randint(3,7)
                    BOARDWIDTH = random.randint(3,7)
                if 10<=LVL<15:
                    RAND=True
                    BOARDHEIGHT = random.randint(3, 7)
                    BOARDWIDTH = random.randint(3, 7)
                if LVL==15 or LVL==16:
                    RAND=True
                    k_colors=random.randint(2,len(map_colors)-1)
                    BOARDHEIGHT=4
                    BOARDWIDTH=4
                if 16<LVL<19:
                    RAND=True
                    k_colors=random.randint(2,4)
                    BOARDHEIGHT=random.randint(3,7)
                    BOARDWIDTH=random.randint(3,7)
                if 19<=LVL<21:
                    RAND = True
                    k_colors = random.randint(2, 6)
                    BOARDHEIGHT = random.randint(3, 7)
                    BOARDWIDTH = random.randint(3, 7)
                if LVL ==21:
                    win_animation()
                    pygame.display.update()
                    FPSCLOCK.tick(FPS)
                my_field = next_lvl()
    pygame.display.update()
    FPSCLOCK.tick(FPS)
