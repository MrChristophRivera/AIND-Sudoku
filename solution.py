from itertools import permutations

assignments = []


def assign_value(values, box, value):
    """ Updates the values dictionary. 
    Assigns a value to a given box. If it updates the board record it.
    
    Args: 
        values(dict): The sudoku board
        box(str): tbe box to update
        value(str): the value to update
    Returns
        values(dict)
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def remove_digit(values, box, digit):
    """removes a digit with in a particular box values
    Args:
        values(dict): the sudoku
        box(str): the box 
        digit(str): the digit to remove
    Returns: 
        values(dict) with update digits
    """
    new_values = values[box].replace(digit, '')
    return assign_value(values, box, new_values)


def is_twin(pair, values):
    """Determine if two boxes in a unit are twin
    Args:
        pair(tuple): tuple with first element as the first box and the second element as the second box. 
        values(dict): the sudoku
    Returns:
        bool: True if twin (same value)
    """
    box1, box2 = pair
    return values[box1] == values[box2]


def find_twins(unit, values):
    """finds all pairs of twins for a given unit
    Args:
        unit(list): the boxes in a given unitlist
        values(dict): The sudoku 
    Returns:
        list or None
    """

    return [(pair[0], pair[1]) for pair in permutations(unit) if is_twin(pair, values)]


def eliminate_twins(unit, twins, values):
    """Eliminates the values for in twin for all non twin pairs within a given unit
    Args:
        unit(list): the unit of boxes
        twins(tuple): the twins
        values(dict): the sudoku
    Returns:
        values with the removed digits
    """
    boxes_not_in_twin = [box for box in unit if box not in twins]
    digits = values[twins[0]]

    for box in boxes_not_in_twin:
        remove_digit(values, box, digits)

    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins

    for unit in units:
        twins_list = find_twins(unit, values)
        for twins in twins_list:
            values = eliminate_twins(unit, twins, values)
    return values


def cross(a, b):
    """Cross product of elements in a and elements in b.
    Args:
        a(iterable):
        b(iterable)
    Returns:
        list
    """
    return [s + t for s in a for t in b]


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
    assert (len(grid) == 81)
    return dict([(boxes[i], '123456789') if grid[i] == '.' else (boxes[i], grid[i]) for i in range(81)])


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF':
            print(line)
    return None


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values(dict): Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        val = values[box]  # get the specific value
        if len(val) == 1:
            for peer in peers[box]:
                new_values = values[peer].replace(val, '')
                values = assign_value(values, peer, new_values)
                # values[peer]= values[peer].replace(val,'')

    return values


def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.
    
    Args
        values(dict): the sudoku puzzle in dictionary form
    Returns: 
        values(dict): Resulting Sudoku in dictionary form after filling in only choices.

    """
    # Go through each unit, identify the boxes that are unassigned and if only one value fits assign it. 
    for unit in unitlist:
        for digit in '123456789':
            places = [box for box in unit if digit in values[box]]
            if len(places) == 1:
                box = places[0]
                values = assign_value(values, box, digit)

    return values


def count_solved(values):
    """helper function to count the number of boxes that are solved
    Args: 
        values(dict): the Sudoku puzzle in dict format
    Returns: 
        (int): the number solved
    """
    return len([box for box in values if len(values[box]) == 1])


def is_solved(values):
    """ Deterines if a sudoku is solved by checking if each box has only one value
    # Note does not check if one value for each unit
    Args: 
        values(dict): a dict of the values
    Returns 
        bool: True if solved else false
    """

    return count_solved(values) == 81


def reduce_puzzle(values):
    """Uses constraint propagation with iterative eliminate and only choice strategies reduce a Sudoku puzzle. 
    Args: 
        values(dict): Sudoku puzzle in dict form
    Returns: 
        values(dict) or False: If can reduce the puzzle returns reduced values. If can't and reaches dead end 
        returns False. This allows for recursion
    """
    stalled = False

    # Apply eliminate and only_choice to the Sudoku puzzle to simplify until can no longer. 
    while not stalled:
        solved_values_before = count_solved(values)

        # Use the elimination strategy and then the only choice. 
        values = eliminate(values)
        values = only_choice(values)

        # determine if stalled
        solved_values_after = count_solved(values)
        stalled = solved_values_before == solved_values_after

        # Check to see if the there is a box with zero values, If so, return False since reached dead end
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def smallest_box(values):
    """Helper function to find the smallest box with multiple options"""

    return min((len(values[box]), box) for box in values if len(values[box]) > 1)[1]


def search(values):
    """ Solve the Sudoku puzzle using DFS with reduce puzzle
    Args: 
        values(dict): Sudoku puzzle in dict form 
    Returns: 
        values, False
    """
    values = reduce_puzzle(values)

    # Set up the base cases for recursion    
    if values is False:
        return False

    if is_solved(values):
        return values

    # Choose one of the unfilled squares with the fewest possibilities
    box = smallest_box(values)

    # get the possibilities
    vals = values[box]

    for val in vals:
        new_sudoku = values.copy()
        new_sudoku = assign_value(new_sudoku, box, val)
        # new_sudoku[box]=v

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
    pass


rows = 'ABCDEFGHI'
cols = '123456789'

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)


def test_sudoku():
    """ This checks the suduku solution for my own interal test"""

    sudoku = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
    values = grid_values(sudoku)
    print('Initial')
    display(values)

    # test eliminate:
    values = eliminate(values)
    print('\n\n After elimination')
    display(values)

    print('\n\n after only_choice')
    values = only_choice(values)
    display(values)

    print('\n\n after reduce_puzzle')
    values = reduce_puzzle(values)
    display(values)

    print('\n\n Harder puzzle after Search')

    grid2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
    values = grid_values(grid2)
    display(values)
    values = search(values)
    display(values)


if __name__ == '__main__':
    test_sudoku()

    '''
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
        '''
