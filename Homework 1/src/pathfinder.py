'''
CMSI 2130 - Homework 1
Author: Milo Fritzen

Modify only this file as part of your submission, as it will contain all of the logic
necessary for implementing the A* pathfinder that solves the target practice problem.
'''
from queue import *
from maze_problem import MazeProblem
from dataclasses import *
from typing import *
from queue import *

@dataclass
class SearchTreeNode:
    """
    SearchTreeNodes contain the following attributes to be used in generation of
    the Search tree:

    Attributes:
        player_loc (tuple[int, int]):
            The player's location in this node.
        action (str):
            The action taken to reach this node from its parent (or empty if the root).
        parent (Optional[SearchTreeNode]):
            The parent node from which this node was generated (or None if the root).
    """
    player_loc: tuple[int, int]
    action: str
    parent: Optional["SearchTreeNode"]
    cost: int  # actual cost
    guess: int  # heuristic guess
    targets_left: set[tuple[int, int]]

    def __str__(self) -> str:
        return "@: " + str(self.player_loc)
    
    def __lt__(self, other: "SearchTreeNode") -> bool:
        return (self.cost + self.guess) < (other.cost + other.guess)
    
def pathfind(problem: "MazeProblem") -> Optional[list[str]]:
    """
    The main workhorse method of the package that performs A* graph search to find the optimal
    sequence of actions that takes the agent from its initial state and shoots all targets in
    the given MazeProblem's maze, or determines that the problem is unsolvable.

    Parameters:
        problem (MazeProblem):
            The MazeProblem object constructed on the maze that is to be solved or determined
            unsolvable by this method.

    Returns:
        Optional[list[str]]:
            A solution to the problem: a sequence of actions leading from the 
            initial state to the goal (a maze with all targets destroyed). If no such solution is
            possible, returns None.
    """
    
    frontier: PriorityQueue[Tuple[int, SearchTreeNode]] = PriorityQueue()
    # >> [NO] Data structure choice alert! We use the graveyard for previously expanded nodes/states, 
    # requiring lots of membership tests -- a list will perform those in O(n) time whereas a set in O(1)! (-0.25)
    graveyard: List = []
    initial_state_loc: tuple[int, int] = problem.get_initial_loc()
    targets: set[tuple[int,int]] = problem.get_initial_targets()

    initial_state_node: SearchTreeNode = SearchTreeNode(initial_state_loc, "", None, 0, _calculate_heurisitc(initial_state_loc, targets), targets)
    # >> [NO] Remove commented out code from submission (-0.25)
    # print("\n\n", initial_state_node, initial_state_node.action, initial_state_node.parent, initial_state_node.cost, initial_state_node.guess)

    # adds the root to the frontier so we can start search
    # >> [NO] OK, but custom class objects like SearchTreeNodes can be stored directly inside of
    # a PriorityQueue as long as their __lt__ method is overridden, just like in CW1. Using the
    # tuple method (priority, item) isn't functionally wrong, but stylistically more verbose than
    # needed here.
    frontier.put(((initial_state_node.guess), initial_state_node))

    while not frontier.empty():
        # temp var to help extract the next node from the priotity queue
        top_of_queue: tuple[int, SearchTreeNode] = frontier.get()
        expanded_node: SearchTreeNode = top_of_queue[1]

        # checks goal state at generation
        # print(expanded_node.targets_left == set())
        if expanded_node.targets_left == set():
            return _trace_path(expanded_node)

        # adds the expanded node to the graveyard
        graveyard.append(expanded_node)
        
        generated_children: List[SearchTreeNode] = []
        transitions: dict = problem.get_transitions(expanded_node.player_loc, expanded_node.targets_left)

        # for each possible action, find what the new node will be and add it to our children list
        for action in transitions:
            next_loc: tuple[int,int] = transitions[action]["next_loc"]
            next_cost: int = transitions[action]["cost"] + expanded_node.cost  # cost of moving plus past cost
            next_targets: set[tuple[int,int]] = expanded_node.targets_left.difference(transitions[action]["targets_hit"])
            next_guess: int = _calculate_heurisitc(next_loc, next_targets)
            # print("\n\n", next_guess, next_targets, "\n\n")
            generated_children.append(SearchTreeNode(next_loc, action, expanded_node, next_cost, next_guess, next_targets))

        # check if any of the children are in the graveyard before adding them to the frontier
        for generated_child in generated_children:
            # check graveyard before adding new nodes to the frontier
            add_node: bool = True
            for node in graveyard:
                if _is_equal(node, generated_child):
                    add_node = False
            # if not in graveyard
            if add_node:
                frontier.put(((generated_child.cost + generated_child.guess), generated_child))
        # print("\n", frontier.qsize())

    # if a solution is not found in the search then we return None to represent no solution
    return None

def _calculate_heurisitc(location: tuple[int, int], targets_left: set[tuple[int,int]]) -> int:
    '''
    adds cost of shooting once to the cost of moving into line with the nearest target to give an
    admissable heuristic
    '''
    make_guess: int = 0
    # if there are no targets left the heuristic is returned while still at zero
    if len(targets_left) == 0:
        return make_guess
    else:  # cost to shoot (at least one) target
        make_guess += 2

    # shortest distance to a line with a target in it
    lines: dict = _get_heurisitc_lines(targets_left)
    nearest: int
    for i in range(len(lines["rows"])):
        man_dist: int = abs(location[0] - lines["rows"][i])
        if i == 0:
            nearest = man_dist
        elif man_dist < nearest:
            nearest = man_dist
    for i in range(len(lines["cols"])):
        man_dist = abs(location[0] - lines["cols"][i])
        if man_dist < nearest:
            nearest = man_dist
    make_guess += nearest

    return make_guess

def _get_heurisitc_lines(targets_left: set[tuple[int,int]]) -> dict[str,List[int]]:
    '''
    finds all the rows and colomns in line with targets
    '''
    lines: dict = {
        "rows": [],
        "cols": []
    }
    for positions in targets_left:
        lines["rows"].append(positions[0])
        lines["cols"].append(positions[1])

    return lines

def _trace_path(node: SearchTreeNode) -> Optional[list[str]]:
    '''
    The method that finds the path taken (including shooting) to reach the given node from the initial state node using 
    A* search.

    Parameters:
        node (SearchTreeNode):
            The search tree node whose path is to be found.

    Returns:
        Optional[list[str]]:
            A sequence of actions leading from the initial state node to given node. If given node 
            is initial state, returns None.
    '''

    actions: List[str] = []
    while node.parent is not None:
        actions.insert(0, node.action)
        node = node.parent
    return actions

def _is_equal(node: SearchTreeNode, other: SearchTreeNode) -> bool:
    '''
    If the location and remaining targets of two nodes are the same, we can assume that lowest
    cost path got us there first so we can ignore repeated states
    '''
    if node.player_loc == other.player_loc and node.targets_left == other.targets_left:
        return True

    return False

# ===================================================
# >>> [NO] Summary
# Great work here! You obviously a good grasp on the programming fundamentals
# needed for the problem as well as the concepts of A* itself. Keep
# up the good work on future assingments, it's looking good.
# ---------------------------------------------------
# >>> [NO] Style Checklist
# [X] = Good, [~] = Mixed bag, [ ] = Needs improvement
#
# [X] Variables and helper methods named and used well
# [X] Proper and consistent indentation and spacing
# [X] Proper docstrings provided for ALL methods
# [X] Logic is adequately simplified
# [X] Code repetition is kept to a minimum
# ---------------------------------------------------
# Correctness:          94/ 100 (-2 / missed unit test)
# Mypy Penalty:        -0 (-2 if mypy wasn't clean)
# Style Penalty:       -0.5
# Total:                93.5/ 100
# ===================================================
