'''
CMSI 2130 - Classwork 2
Author: <Kate Galvin, Milo Fritzen>

Modify only this file as part of your submission, as it will contain all of the logic
necessary for implementing the breadth-first tree search that solves the basic maze
pathfinding problem.
'''

from queue import Queue
from maze_problem import *
from dataclasses import *

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
    
    def __str__(self) -> str:
        return "@: " + str(self.player_loc)

def pathfind(problem: MazeProblem) -> Optional[list[str]]:
    """
    The main workhorse method of the package that performs Breadth-first search to find the optimal
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

    frontier: Queue[SearchTreeNode] = Queue()
    initial_state_loc: tuple[int, int] = problem.get_initial_loc()
    goal_state_loc: tuple[int, int] = problem.get_goal_loc()
    initial_state_node: SearchTreeNode = SearchTreeNode(initial_state_loc, "", None)

    frontier.put(initial_state_node)

    while not frontier.empty():
        expanded_node: SearchTreeNode = frontier.get()
        transitions: dict[Any, Any] = problem.get_transitions(expanded_node.player_loc)
        generated_children: List[SearchTreeNode] = []

        for key in transitions:
            generated_children.append(SearchTreeNode(transitions[key], key, expanded_node))
        
        for generated_child in generated_children:
            if generated_child.player_loc == goal_state_loc:
                return _trace_path(generated_child)
            frontier.put(generated_child)

    return None

def _trace_path(node: SearchTreeNode) -> Optional[list[str]]:
    """
    The method that finds the path taken to reach the given node from the initial state node using 
    breadth first search.

    Parameters:
        node (SearchTreeNode):
            The search tree node whose path is to be found.

    Returns:
        Optional[list[str]]:
            A sequence of actions leading from the initial state node to given node. If given node 
            is initial state, returns None.
    """

    actions: List[str] = []
    while node.parent is not None:
        actions.insert(0, node.action)
        node = node.parent
    if(actions == []):
        return None
    return actions
