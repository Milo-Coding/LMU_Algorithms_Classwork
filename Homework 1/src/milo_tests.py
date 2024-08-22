from pathfinder import *
import unittest

class MiloTests(unittest.TestCase):
    """
    Unit tests for validating the pathfinder's efficacy. Notes:
    - If this is the set of tests provided in the solution skeleton, it represents an
      incomplete set that you are expected to add to to adequately test your submission!
    - Your correctness score on the assignment will be assessed by a more complete,
      grading set of unit tests.
    - A portion of your style grade will also come from proper type hints; remember to
      validate your submission using `mypy .` and ensure that no issues are found.
    """
    
    def run_maze(self, maze: list[str], solution_expected: bool, optimal_cost: int = 0) -> None:
        """
        For a given maze (a list of strings denoting the maze contents), runs your pathfinder algorithm
        and determines whether or not it returns the correct and optimal solution, if one exists.
        
        Attributes:
            maze (list[str]):
                The 2D list of strings denoting the maze layout, including locations of the player's
                initial state, walls, mud tiles, and targets to hit.
            solution_expected (bool):
                Whether or not the maze can be solved. If True, it is expected that your pathfinder will
                yield the correct series of steps needed to shoot all targets in the lowest cost possible.
                If False, it is expected that your pathfinder will return None.
            optimal_cost (int):
                If there is indeed a solution expected, the optimal_cost will indicate the lowest cost
                possible in solving the maze. It is possible to have a solution that may solve mazes but
                not in the optimal way, which will not receive credit.
        """
        problem = MazeProblem(maze)
        solution = pathfind(problem)
        error_suffix = "Test Failure: " + self._testMethodName + "\nGiven Solution: " + str(solution) + "\nMaze:\n" + "\n".join(maze)
        
        if not solution_expected: 
            if not solution is None:
                self.fail("[X] You returned a solution where none was possible on this maze:\n" + error_suffix)
            else: 
                return
        elif solution is None:
            self.fail("[X] You returned an answer of no solution (None) where one was expected on maze:\n" + error_suffix)
        
        result = problem.test_solution(solution)
        
        self.assertTrue(result["is_solution"], "[X] You returned a solution that was incorrect on this maze:\n" + error_suffix)
        self.assertEqual(result["cost"], optimal_cost, "[X] You returned a suboptimal solution on this maze:\n" + error_suffix)
        
    # Tests I Wrote :)
    # ---------------------------------------------------------------------------
    def test_milo_t0(self) -> None:
        maze = [
           # 012345
            "XXXXXX", # 0
            "X....X", # 1
            "X....X", # 2
            "X@...X", # 3
            "XXXXXX", # 4
        ]
        
        self.run_maze(maze, True, 0)

    def test_milo_t1(self) -> None:
        maze = [
           # 0123456789ab
            "XXXXXXXXXXXX", # 0
            "X.........TX", # 1
            "X..........X", # 2
            "X@.........X", # 3
            "XXXXXXXXXXXX", # 4
        ]

        self.run_maze(maze, True, 4)

    def test_milo_t2(self) -> None:
        maze = [
           # 012345
            "XXXXXX", # 0
            "X...TX", # 1
            "X....X", # 2
            "X....X", # 3
            "X....X", # 4
            "X....X", # 5
            "X....X", # 6
            "X@...X", # 7
            "XXXXXX", # 8
        ]
        
        self.run_maze(maze, True, 5)

    def test_milo_t3(self) -> None:
        maze = [
           # 0123456789ab
            "XXXXXXXXXXXX", # 0
            "X.........TX", # 1
            "X.XXXXXXXXXX", # 2
            "X..........X", # 3
            "XXXXXXXXXX.X", # 4
            "X@.........X", # 5
            "XXXXXXXXXXXX", # 6
        ]

        self.run_maze(maze, True, 24)

    
        
if __name__ == '__main__':
    unittest.main()