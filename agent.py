import pygame
from pygame.locals import *
from collections import namedtuple
import numpy as np
from Block_game_AI import blocks

# Bugs:
# The starting location of the block is constantly on the game window... Need to figure out how to get that removed


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

BGCOLOR = BLACK

 # start Block close to the top of the game window
 # Note: if I change the starting location, I will have to also change it in Block_game_AI
 
startx = 2*BLOCKSIZE
starty = 2*BLOCKSIZE

# if this gets changed, you also need to change tx and ty in Block_gam_AI.py
# This tx and ty are specifically for the pysical location, those in Block_gam_AI.py are for the drawing of the target
# tx and ty are the x and y coordinates of the target
tx = (BLOCKSIZE * 8)
ty = (BLOCKSIZE * 8)

# states:
environment_rows = WINDOWWIDTH 
environment_columns = WINDOWHEIGHT
# 400 pxls total in environment

# actions
actions = ['up', 'right', 'down', 'left']

UP = 'up'
RIGHT = 'right'
DOWN = 'down'
LEFT = 'left'

#Q-table
Q_table = np.zeros((environment_rows, environment_columns, len(actions)))     # environment_rows = 200 environment_collumns = 200 len(actions) = 4

# rewards = empty list []
# rewards around the game environment = -1
rewards = np.full((environment_rows, environment_columns), -2.)
# rewards when touching target = +1000
rewards[tx, ty] = 1000

RowandColumn = []

n_iterations = 5000
# LS stands for last stretch and it is our testing phase
LS = 100


#%% functions

# define an --epsilon-- greedy algorithm that will choose which action to take next (i.e., where to move next)
def action(current_row_index, current_column_index, epsilon):
    #if a randomly chosen value between 0 and 1 is less than epsilon, 
    #then choose the most promising value from the Q-table for this state.
    if np.random.random() < epsilon:        # Return random floats in the half-open interval [0.0, 1.0). Results are from the "continuous uniform" distribution over the stated interval.
        return np.argmax(Q_table[current_row_index, current_column_index])
    else: 
        return np.random.randint(4) # if the random number is a 0, return Up, if 1, return right, if 2... etc. See above action={., ., ., .}


def next_move(current_row_index, current_column_index, action_index):
    # defines different state if the AI hits the walls
    new_row_index = current_row_index
    new_column_index = current_column_index
    if actions[action_index] ==  UP and current_row_index > 0:
        new_row_index -= BLOCKSIZE

    elif actions[action_index] == RIGHT and current_column_index < environment_columns - BLOCKSIZE:
        new_column_index += BLOCKSIZE

    elif actions[action_index] == DOWN and current_row_index < environment_rows - BLOCKSIZE:
        new_row_index += BLOCKSIZE

    elif actions[action_index] == LEFT and current_column_index > 0:
        new_column_index -= BLOCKSIZE

    # Attempt to prevent agent from going off grid
    elif current_row_index >= environment_rows - BLOCKSIZE or current_column_index >= environment_columns - BLOCKSIZE:
        print('WALL danger')
        current_row_index -= 3*BLOCKSIZE
        current_column_index -= 3*BLOCKSIZE
        
    
    elif current_row_index <= BLOCKSIZE or current_column_index <= BLOCKSIZE:
        print('WALL danger')
        current_row_index += 3*BLOCKSIZE
        current_column_index += 3*BLOCKSIZE
        

    return new_row_index, new_column_index

def get_starting_location():
    if episode == 0:    # This will only be the index for the start of the game
        #get a random row and column index
        current_row_index = startx 
        current_column_index = starty 
    else:
        # The idea is that the first number appended to this list will be the next row and column
        # the appending happens below under the class Agent
        current_row_index, current_column_index = RowandColumn[0], RowandColumn[1]
    return current_row_index, current_column_index

def reset():
    current_row_index = startx 
    current_column_index = starty 
    return current_row_index, current_column_index

#%% Agent

Point = namedtuple('Point', 'x, y') 

pygame.init()

class Agent:
    def __init__(self):
        global FPSCLOCK, DISPLAYSURF, BASICFONT

        
        FPSCLOCK = pygame.time.Clock()
        DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        BASICFONT = pygame.font.Font('freesansbold.ttf', 18)

        DISPLAYSURF.fill(BGCOLOR)

        self.n_games = 0   
        
        #define training parameters
        self.epsilon = 0.9 #the percentage of time when we should take the best action (instead of a random action)
        self.discount_factor = 0.9 #discount factor for future rewards
        self.learning_rate = 0.9 #the rate at which the agent should learn
    

def train():
    agent = Agent()
    game = blocks()
    
    #get the starting location for this episode
    row_index, column_index = get_starting_location()

    # Get the block to reset if it hit the target
    if (row_index, column_index) == (tx, ty):
        print(f'\n hit target at {row_index, column_index}')
        row_index, column_index = reset()
    # Testing AI after training
    # elif n_iterations - LS == episode:
    #     print(f'\n starting from scratch \n')
    #     row_index, column_index = reset()
        
    
    #choose which action to take (i.e., where to move next)
    action_index = action(row_index, column_index, agent.epsilon)

    #perform the chosen action, and transition to the next state (i.e., move to the next location)
    old_row_index, old_column_index = row_index, column_index #store the old row and column indexes
    row_index, column_index = next_move(row_index, column_index, action_index)

    # to insert the row index to the first number of the list, and the column index to the second number of the list
    # This list is meant to be used to choose the next coordinate for the movement of the block.
    RowandColumn.insert(0, row_index)
    RowandColumn.insert(1, column_index)
    
    #receive the reward for moving to the new state, and calculate the temporal difference
    reward = rewards[row_index, column_index]
    old_q_value = Q_table[old_row_index, old_column_index, action_index]
    temporal_difference = reward + (agent.discount_factor * np.max(Q_table[row_index, column_index])) - old_q_value

    #update the Q-value for the previous state and action pair
    new_q_value = old_q_value + (agent.learning_rate * temporal_difference)
    Q_table[old_row_index, old_column_index, action_index] = new_q_value

     # this is the index of the starting location/subsequent locations
    idx = Point(row_index, column_index)
    game.blocks.insert(0, idx)
    game.drawGrid()
    game.draw_Block()
    game.draw_target()
    pygame.display.flip()
    FPSCLOCK.tick(FPS)

if __name__ == '__main__':
    game = blocks()
    player = Agent()

    N_EPISODES = 0

    for episode in range(n_iterations):
        print(N_EPISODES)
        N_EPISODES += 1
        # if n_iterations - LS == episode:
        #     player.epsilon = 0
        #     print('\n Last episodes \n')
        train()


        game_over = game.play_step()

        if game_over == True:
           game.reset()
    
