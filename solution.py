assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diag1 = [[d[0]+d[1] for d in zip(rows,cols)]]
diag2 = [[d[0]+d[1] for d in zip(rows,cols[::-1])]]
# to solve the diagonal soduku we introduce two new units in the diagonal. 
unitlist = row_units + column_units + square_units +diag1 + diag2
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)



def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    digits ='123456789'
    pairs = [s + t for s in digits for t in digits if s!=t]     #all the possible 2 digit combinations, where digits dont repeat
    for unit in unitlist:                         # now we go through every unit
          for pair in pairs:
                dplaces = [box for box in unit if values[box] == pair] #creates a list of boxes that has 'pair' in it
                if len(dplaces) ==2:  #dplaces will create a list of lists with items in pair. some units will only have one
                                      # box with that pair, and we are only interested in the list that has two, the naked twins
                    boxes_to_replace = [box_temp for box_temp in unit if box_temp not in dplaces] # these are the boxes that
                                                                                                  # dont contain the pair 
                    for pairless_box in boxes_to_replace:
                        if len(values[pairless_box]) >2:  # I want to access those boxes that are longer than 2 only
                            values[pairless_box] =  values[pairless_box].replace(pair[0],'') # in case only 1 value in the pair needs to be replaced. 
                            values[pairless_box] =  values[pairless_box].replace(pair[1],'') # ie pair is '12' we want to elimiante '234' not just '1234'
   
    return values

def cross(A, B):
    "Cross product of elements in A and elements in B."
     return [s+t for s in A for t in B]

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    board= {k: v for k, v in zip(boxes, grid)}
    for key, value in board.items():
        if value == '.':
            board[key] = '123456789'
    return board 

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values."""
        
        
    for key, value in values.items():      # go through dict
        if len(value) == 1:                # check that there is only one value in box
            peer = peers[key]              # get that board's peers 
            eliminate_value = value        # keep track of value we want to delete
            for item in peer:              # go through the peers 
                original_values = values[item]  # look up the values the peer boxes have
                new_values = original_values.replace(eliminate_value,'') # delete single item
                values[item] = new_values   # update the peers boxes on the board
        
            
    return values 

def only_choice(values):
     """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        
        naked_twins(only_choice(eliminate(values)))
    
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
        "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    
    return search(reduce_puzzle(grid))

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
