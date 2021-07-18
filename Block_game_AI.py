import os
import pygame
from pygame.locals import *
from enum import Enum
from collections import namedtuple

#%% Constants

FPS = 7
WINDOWWIDTH = 200
WINDOWHEIGHT = 200
BLOCKSIZE = 20
assert WINDOWWIDTH % BLOCKSIZE == 0, "Window width must be a multiple of block size."
assert WINDOWHEIGHT % BLOCKSIZE == 0, "Window height must be a multiple of block size."
CELLWIDTH = int(WINDOWWIDTH / BLOCKSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / BLOCKSIZE)

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
YELLOW    = (255, 255,   0)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


BGCOLOR = BLACK

 # start Block close to the top of the game window
startx = 2*BLOCKSIZE
starty = 2*BLOCKSIZE

tx = (BLOCKSIZE * 8)
ty = (BLOCKSIZE * 8)


#%% Main Game

Point = namedtuple('Point', 'x, y') 

class blocks:
    def __init__(self):
        global FPSCLOCK, DISPLAYSURF, BASICFONT

        FPSCLOCK = pygame.time.Clock()
        DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
        pygame.display.set_caption('Q_learning_Block_Game')

        # init game state
        
        self.direction = None

        self.head = Point(startx, starty)       # got this code (Point(x,y) from snake_game)
        self.blocks = [self.head, 
                      ]                         #for future I should be able to insert more blocks into this list!
        
        self.t = Point(tx, ty)
        self.target = [self.t]

    def play_step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                os._exit(0)


        DISPLAYSURF.fill(BGCOLOR)

    def drawGrid(self):
        for x in range(0, WINDOWWIDTH, BLOCKSIZE): # draw vertical lines
            pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
        for y in range(0, WINDOWHEIGHT, BLOCKSIZE): # draw horizontal lines
            pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))

    def draw_Block(self):
        for pt in self.blocks:
            pygame.draw.rect(DISPLAYSURF, RED, pygame.Rect(pt.x, pt.y, BLOCKSIZE, BLOCKSIZE))
        # access the x and y coordinates of nametuple using index numbers!!! x = 400 and y = 300. x and y are just the keys to find the values of x and y. Its like a dictionary.


    def draw_target(self):
        for pt in self.target:
            pygame.draw.rect(DISPLAYSURF, GREEN, pygame.Rect(pt.x, pt.y, BLOCKSIZE, BLOCKSIZE))

