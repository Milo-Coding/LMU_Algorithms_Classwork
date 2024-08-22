from typing import *

class Constants:
    '''
    Simulation / Maze constants important for the pathfinding problem
    
    [!] IMPORTANT: YOU MUST NOT TOUCH THIS FILE AT ALL, NO EDITS OR ADDITIONS!
        Any changes will be overwritten during testing
    '''
    
    # Movement constants + location modifiers
    MOVES = ["U", "D", "L", "R"]
    MOVE_DIRS = {"U": (0, -1), "D": (0, 1), "L": (-1, 0), "R": (1, 0)}
    
    # Maze content constants
    WALL_BLOCK  = "X"
    SAFE_BLOCK  = "."
    GOAL_BLOCK  = "G"
    PLR_BLOCK   = "@"
