'''
Variety of functions related to computing the edit distance between
strings and, importantly, which WILL be used by the DistleGame to
provide feedback to the DistlePlayer during a game of Distle.

[!] Feel free to use any of these methods as needed in your DistlePlayer.

[!] Feel free to ADD any methods you see fit for use by your DistlePlayer,
e.g., some form of entropy computation.
'''


def get_edit_dist_table(row_str: str, col_str: str) -> list[list[int]]:
    '''
    Returns the completed Edit Distance memoization structure: a 2D list
    of ints representing the number of string manupulations required to
    minimally turn each subproblem's string into the other.

    Parameters:
        row_str (str):
            The string located along the table's rows
        col_str (col):
            The string located along the table's columns

    Returns:
        list[list[int]]:
            Completed memoization table for the computation of the
            edit_distance(row_str, col_str)
    '''
    # create the empty edit distance table
    edit_table: list[list[int]] = []
    for _ in range(len(row_str) + 1):
        edit_table.append([0] * (len(col_str) + 1))

    for row in range(len(edit_table)):
        for col in range(len(edit_table[0])):
            edit_table[row][col] = helper_get_edit_distance(
                edit_table, row, col, row_str, col_str)

    return edit_table


def helper_get_edit_distance(edit_table: list[list[int]], row: int, col: int, row_str: str, col_str: str) -> int:
    # gutters
    if row == 0:  # all deletions
        return col
    if col == 0:  # all insertions
        return row
    # we are at least at [1,1] now

    # deletion case
    del_case: int = edit_table[row-1][col] + 1
    # insertion case
    ins_case: int = edit_table[row][col-1] + 1
    # replacement case
    rep_case: int = edit_table[row-1][col-1]
    # if the characters is equal at the given row and col (-1 to account for empty string)
    if row_str[row-1] != col_str[col-1]:
        rep_case += 1
    # transposition case
    if row > 1 and col > 1 and row_str[row-1] == col_str[col-2] and row_str[row-2] == col_str[col-1]:
        tra_case: int = edit_table[row-2][col-2] + 1

    if 'tra_case' in locals():
        return min(del_case, ins_case, rep_case, tra_case)

    return min(del_case, ins_case, rep_case)


def edit_distance(s0: str, s1: str) -> int:
    '''
    Returns the edit distance between two given strings, defined as an
    int that counts the number of primitive string manipulations (i.e.,
    Insertions, Deletions, Replacements, and Transpositions) minimally
    required to turn one string into the other.

    [!] Given as part of the skeleton, no need to modify

    Parameters:
        s0, s1 (str):
            The strings to compute the edit distance between

    Returns:
        int:
            The minimal number of string manipulations
    '''
    if s0 == s1:
        return 0
    return get_edit_dist_table(s0, s1)[len(s0)][len(s1)]


def get_transformation_list(s0: str, s1: str) -> list[str]:
    '''
    Returns one possible sequence of transformations that turns String s0
    into s1. The list is in top-down order (i.e., starting from the largest
    subproblem in the memoization structure) and consists of Strings representing
    the String manipulations of:
        1. "R" = Replacement
        2. "T" = Transposition
        3. "I" = Insertion
        4. "D" = Deletion
    In case of multiple minimal edit distance sequences, returns a list with
    ties in manipulations broken by the order listed above (i.e., replacements
    preferred over transpositions, which in turn are preferred over insertions, etc.)

    [!] Given as part of the skeleton, no need to modify

    Example:
        s0 = "hack"
        s1 = "fkc"
        get_transformation_list(s0, s1) => ["T", "R", "D"]
        get_transformation_list(s1, s0) => ["T", "R", "I"]

    Parameters:
        s0, s1 (str):
            Start and destination strings for the transformation

    Returns:
        list[str]:
            The sequence of top-down manipulations required to turn s0 into s1
    '''

    return get_transformation_list_with_table(s0, s1, get_edit_dist_table(s0, s1))


def get_transformation_list_with_table(s0: str, s1: str, table: list[list[int]]) -> list[str]:
    '''
    See get_transformation_list documentation.

    This method does exactly the same thing as get_transformation_list, except that
    the memoization table is input as a parameter. This version of the method can be
    used to save computational efficiency if the memoization table was pre-computed
    and is being used by multiple methods.

    [!] MUST use the already-solved memoization table and must NOT recompute it.
    [!] MUST be implemented recursively (i.e., in top-down fashion)
    '''
    # get the min number of transions that we need to make
    row: int = len(s0)  # for clarity
    col: int = len(s1)
    new_s0: str = s0  # for recursion
    new_s1: str = s1
    current_spot: int = table[row][col]

    # base case: no more transitions need to be made
    if current_spot == 0:
        return []

    # calculate the next transition by tiebreaking order (reverse order check apear in so it can be overridden)
    next_move: list[str] = []

    # deletion
    if row > 0 and table[row - 1][col] <= current_spot:
        new_s0 = s0[0:row - 1]
        next_move = ['D']
        current_spot = table[row - 1][col]

    # insertion
    if col > 0 and table[row][col - 1] <= current_spot:
        new_s1 = s1[0:col - 1]
        next_move = ['I']
        current_spot = table[row][col - 1]

    # transpostion
    if row > 1 and col > 1 and s0[row-1] == s1[col-2] and s0[row-2] == s1[col-1] and table[row - 2][col - 2] <= current_spot:
        new_s0 = s0[0:row - 2]
        new_s1 = s1[0:col - 2]
        next_move = ['T']
        current_spot = table[row - 2][col - 2]

    # replacement
    if row > 0 and col > 0 and table[row - 1][col - 1] <= current_spot:
        new_s0 = s0[0:row - 1]
        new_s1 = s1[0:col - 1]
        # this stops us from counting extra replacements when the letters are the same
        if s0[row-1] != s1[col-1]:
            next_move = ['R']
        else:
            next_move = []
        current_spot = table[row - 1][col - 1]

    next_move.extend(get_transformation_list_with_table(new_s0, new_s1, table))
    return next_move
