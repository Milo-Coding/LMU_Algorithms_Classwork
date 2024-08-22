"""
Artificial Intelligence responsible for playing the game of T3!
Implements the alpha-beta-pruning mini-max search algorithm
"""
from dataclasses import *
from typing import *
from t3_state import *
    
def choose(state: "T3State") -> Optional["T3Action"]:
    """
    Main workhorse of the T3Player that makes the optimal decision from the max node
    state given by the parameter to play the game of Tic-Tac-Total.
    
    [!] Remember the tie-breaking criteria! Moves should be selected in order of:
    1. Best utility
    2. Smallest depth of terminal
    3. Earliest move (i.e., lowest col, then row, then move number)
    
    You can view tiebreaking as something of an if-ladder: i.e., only continue to
    evaluate the depth if two candidates have the same utility, only continue to
    evaluate the earliest move if two candidates have the same utility and depth.
    
    Parameters:
        state (T3State):
            The board state from which the agent is making a choice. The board
            state will be either the odds or evens player's turn, and the agent
            should use the T3State methods to simplify its logic to work in
            either case.
    
    Returns:
        Optional[T3Action]:
            If the given state is a terminal (i.e., a win or tie), returns None.
            Otherwise, returns the best T3Action the current player could take
            from the given state by the criteria stated above.
    """
    # if a move needs to be made, find the best move to make using minimax with alpha-beta-pruning
    best_move: "DataClass" = minimax(state, -float("inf"), float("inf"), True, 0)
    return best_move.action

def minimax(state: "T3State", alpha: float, beta: float, isMaxNode: bool, depth: float) -> "DataClass":
    children = state.get_transitions()  # set of "child" nodes
    temp: "DataClass"
    # ininital best_move_data and next_move with awful stats so it gets replaced by ANY other move
    best_move_data: "DataClass" = DataClass(-float("inf"), float("inf"), None)
    worst_move_data: "DataClass" = DataClass(float("inf"), float("inf"), None)
    next_move_data: "DataClass"

    # check base cases and return data class with appropriate values (the action is None in case no move is needed)
    if state.is_tie():  # if we tie util is 0
        return DataClass(0, depth, None)
    elif (state.is_win() and isMaxNode):  # agent loses if our turn is a terminal node, util = -1
        return DataClass(-1, depth, None)
    elif (state.is_win() and not isMaxNode):  # agent wins if the terminal node is a min, util = 1
        return DataClass(1, depth, None)

    # if not terminal, take utility of "child" nodes
    # the agent moves at max nodes
    if (isMaxNode):
        for next_move in children:
            temp = minimax(next_move[1], alpha, beta, False, depth + 1)
            alpha = max(alpha, temp.utility)
            next_move_data = DataClass(temp.utility, temp.depth, next_move[0])

            # if our next move is better then track that instead (max node)
            if best_move_data.is_next_better(next_move_data):
                best_move_data = next_move_data

            if (alpha >= beta):
                break
        
        return best_move_data
    
    # min nodes represent the player's turn
    else:
        for next_move in children:
            temp = minimax(next_move[1], alpha, beta, True, depth + 1)
            beta = min(beta, temp.utility)
            next_move_data = DataClass(temp.utility, temp.depth, next_move[0])

            # if our next worse is better then track that instead (min node)
            if worst_move_data.is_next_worse(next_move_data):
                    worst_move_data = next_move_data

            if (alpha >= beta):
                break
        
        return worst_move_data
    
@dataclass
class DataClass:
    utility: float
    depth: float
    action: Optional["T3Action"]

    def is_next_better(self, other: "DataClass") -> bool:
        # if the other move has a better utility, then it is a better move
        if other.utility > self.utility:
            return True
        
        # we nesting loops to make sure things get checked in the right order
        elif other.utility == self.utility:
            # if the other move has a lower depth, it is better
            if other.depth < self.depth:
                return True
            
            # more nests
            elif other.depth == self.depth:
                # None checks are for edge cases where action has not been defined yet
                if self.action is not None and other.action is not None:
                    # finally check action tiebreaker criteria
                    return other.action < self.action

        return False
    
    def is_next_worse(self, other: "DataClass") -> bool:
        # if the other move has a better utility, then it is a better move
        if other.utility < self.utility:
            return True
        
        # if the utility is the same we still want tie broken moves
        elif other.utility == self.utility:
            # if the other move has a lower depth, it is better
            if other.depth < self.depth:
                return True
            
            # more nests
            elif other.depth == self.depth:
                # None checks are for edge cases where action has not been defined yet
                if self.action is not None and other.action is not None:
                    # finally check action tiebreaker criteria
                    return other.action < self.action

        return False