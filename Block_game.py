
import random
import os
import pygame
from pygame.locals import *
from enum import Enum
from collections import namedtuple

# # code to ignore depreciation warnings
# import warnings
# warnings.filterwarnings("ignore", category=DeprecationWarning)
# # Ideally this won't be needed



#%% Constants

FPS = 7
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
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

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


BGCOLOR = BLACK

 # start Block close to the top of the game window
startx = 2*BLOCKSIZE
starty = 2*BLOCKSIZE


tx = WINDOWWIDTH - 4*BLOCKSIZE
ty = WINDOWHEIGHT - 2*BLOCKSIZE

#%% Main Game

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y') 

pygame.init()

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
                      ] #for future I should be able to insert more blocks into this list!
        self.t = Point(tx, ty)
        self.target = [self.t]

    def play_step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                os._exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN

            # To make every press of the keys move once.
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.direction = None
                elif event.key == pygame.K_RIGHT:
                    self.direction = None
                elif event.key == pygame.K_UP:
                    self.direction = None
                elif event.key == pygame.K_DOWN:
                    self.direction = None

        # move
        self._move(self.direction) # update the head

        # update block with new x and y coordinates
        self.blocks.insert(0, self.head)

        # collisions
        game_over = False
        if self.collision(self.direction):
            game_over = True
            return game_over

        DISPLAYSURF.fill(BGCOLOR)
        self.drawGrid()
        self.draw_Block()
        self.draw_target()
        pygame.display.flip()
        FPSCLOCK.tick(FPS)

#%% Functions
    
    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCKSIZE
        elif direction == Direction.LEFT:
            x -= BLOCKSIZE
        elif direction == Direction.DOWN:
            y += BLOCKSIZE
        elif direction == Direction.UP:
            y -= BLOCKSIZE
            
        self.head = Point(x, y)
        # to not leave a trail behind need to delete the previous blocks
        del self.blocks[-1]
    
    def collision(self, direction):
       # hits boundary
        if self.head.x > WINDOWWIDTH - BLOCKSIZE or self.head.x < 0 or self.head.y > WINDOWHEIGHT - BLOCKSIZE or self.head.y < 0:
            return True
        
    def reset(self):
        self.head = Point(startx, starty)       # got this code (Point(x,y) from snake_game)
        self.blocks = [self.head,] 

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


if __name__ == '__main__':
    game = blocks()

    while True:
        game_over = game.play_step()

        if game_over == True:
           game.reset()
