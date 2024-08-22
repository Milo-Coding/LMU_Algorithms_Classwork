from constants import *

class MazeProblem:
    """
    MazeProblem class used to store all relevant information about the maze being solved
    by the Pathfinder, including the starting location of the player and the position of
    all other maze entities like walls and the goal.

    [!] Warning / Reminder: if an attribute or method begins with an underscore (_), it
    should not be accessed outside of this class. There are thus NO publicly accessible
    *attributes* to this class, but a variety of methods available for use.
    """
    
    # Constructor
    # ---------------------------------------------------------------------------
    def __init__(self, maze: list[str]) -> None:
        """
        Constructs a new pathfinding problem (finding the locations of any
        relevant maze entities) from a maze specified as a list of string rows.
        
        Parameters:
            maze (list[str]):
                A list of string rows of a rectangular maze consisting of the
                following traits:
                - A border of walls ("X"), with possibly others in the maze
                - Exactly 1 player starting position ("@")
                - Exactly 1 goal tile ("G")
        """
        self._maze: list[list[str]] = [[r for r in row] for row in maze]
        self._walls: set[tuple[int, int]] = set()
        
        for (row_num, row) in enumerate(maze):
            for (col_num, cell) in enumerate(row):
                loc = (col_num, row_num)
                if cell == Constants.WALL_BLOCK:
                    self._walls.add(loc)
                if cell == Constants.GOAL_BLOCK:
                    self._goal_loc: tuple[int, int] = loc
                if cell == Constants.PLR_BLOCK:
                    self._player_loc: tuple[int, int] = loc
        
    
    # Methods
    # ---------------------------------------------------------------------------
    def get_initial_loc (self) -> tuple[int, int]:
        """
        Returns the player's starting position in the maze ("@").
    
        Returns:
            tuple[int, int]:
                The player's starting location in the maze: (col, row) = (x, y).
        """
        return self._player_loc
    
    def get_goal_loc (self) -> tuple[int, int]:
        """
        Returns the location of the goal that must be reached.
    
        Returns:
            tuple[int, int]:
                The goal's location tuple: (col, row) = (x, y).
        """
        return self._goal_loc
    
    def get_transitions(self, player_loc: tuple[int, int]) -> dict:
        """
        Returns a dictionary describing all possible transitions that a player may take from their
        given position. 
        
        Parameters:
            player_loc (tuple[int, int]):
                The current location of the player in the maze.
        
        Returns:
            dict:
                A dictionary whose keys are the possible actions from the given player_loc, with mapped
                values next_loc (tuple[int, int]) values that show the player's location after taking that action.
        
        Example:
            For example, if only the actions "D", "U", and "L" were possible from the current player_loc of (3,3),
            we might see an output of:
            {
                "D": (3, 4),
                "U": (3, 2),
                "L": (2, 3)
            }
        """
        new_player_locs = {action: (player_loc[0] + offset[0], player_loc[1] + offset[1]) for action, offset in Constants.MOVE_DIRS.items()}
        transitions = {
            action: loc for action, loc in new_player_locs.items() if loc not in self._walls
        }
        return transitions
    
    def test_solution(self, solution: Optional[list[str]]) -> dict:
        """
        Given a solution (a sequence of actions), tests to ensure that the provided series of steps
        does indeed solve the problem. It is assumed that the current MazeProblem *is* solvable in
        order to use this method.
        
        [!] IMPORTANT NOTES:
            - You will never call this method in your implementation of pathfinder -- it is for test
              purposes only and does nothing for you during the actual solution
            - See the unit tests module for how this method is used
        
        Parameters:
            solution (Optional[list[str]]):
                A sequence of actions that possibly solves the maze, e.g., ["L", "L", "U", "U"]
        
        Returns:
            dict:
                A dictionary with 2 keys used by the test suite to validate the solution:
                    - is_solution (bool): whether or not the solution successfully navigates from the
                      initial to the goal state
                    - cost (int): the total cost of all actions taken, or -1 if is_solution is False
        """
        player_loc = self.get_initial_loc()
        cost = 0
        err_result = {"is_solution": False, "cost": -1}
        
        if solution is None:
            return err_result
        
        for action in solution:
            offset = Constants.MOVE_DIRS[action]
            player_loc = (player_loc[0] + offset[0], player_loc[1] + offset[1])
            if player_loc in self._walls:
                return err_result
            cost += 1
        
        return {"is_solution": player_loc == self._goal_loc, "cost": cost}
    
