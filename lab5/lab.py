#!/usr/bin/env python3
"""6.009 Lab -- Six Double-Oh Mines"""

# NO IMPORTS ALLOWED!

###----------------------------HELPER FUNCTIONS-------------------------------
def get_num_squares(dimensions):
    """
    Given dimensions, it returns the number of elements in an n dimensional array.
    """
    
    product = 1 
    for elem in dimensions:
        product *= elem
        
    return product

def create_nd_array(dimensions, val): 
    """ 
    Returns n-dimensional array given dimensions.
    """
    if len(dimensions) == 0:
        return val
    
    return [create_nd_array(dimensions[1:], val) for i in range(dimensions[0])]

def check_dimension(dimensions, coord):
    """
    Checks if a given coordinate is inside a nd_array
    """
    for x, y  in zip(dimensions, coord):
        if y not in range(x):
            return False
    return True
        


def create_nd_coordinate_array(dimensions, tup = ()):
    """
    Returns n-dimensional array, given dimensions, where the values of each square are its coordinates.
    """
    if len(dimensions) == 0: 
        return tup
    
    return [create_nd_coordinate_array(dimensions[1:], tup + (i,)) for i in range(dimensions[0])]

def list_of_coordinates(coord_array, lista = []):
    """
    Taking a n dimensional coordinate array, it returns a list of the coordinates 
    in that array.

    """    
    for elem in coord_array:
        if isinstance(elem, list):
            list_of_coordinates(elem, lista)
        else: 
            if elem not in set(lista):
                lista.append(elem)
           
    return lista
    
def get_val_nd(nd_array, coord):
    """
    Takes an nd array an coordinates to a specific location in the array as a tuple.
    Returns the value at that location in the array.
    """
    
    for elem in coord:
        nd_array = nd_array[elem]
    
    # print(nd_array)
    return nd_array

# def set_val_nd(nd_array, dimensions, coord, value, tup = ()):
#    """
#    Takes an nd array, its dimensions, a location in the array, and a value.
#    It creates an exact copy of the nd array, except for one location, coord,
#    where the value is replaced for a new one, value, thus replacing just that value
#    in the array.
#    """
   
#    if len(dimensions) == 0:
#         if tup == coord:
#             return value
#         else:
#             return get_val_nd(nd_array, tup) 
        
#    return [set_val_nd(nd_array, dimensions[1:], coord, value, tup +(i,)) for i in range(dimensions[0])]

def set_val_nd(nd_array, dimensions, coord, value):
    
    """
    Takes an nd array, its dimensions, a location in the array, and a value.
    It creates an exact copy of the nd array, except for one location, coord,
    where the value is replaced for a new one, value, thus replacing just that value
    in the array.
    """
    
    x = coord[0]
    
    if isinstance(nd_array[x], list):
        return set_val_nd(nd_array[x], dimensions, coord[1:], value)
    else:
        nd_array[x] = value
        return 
        

def check_nd_neighbors(tup, dimensions):
    """
    returns a list containing the neighbors of a square in n dimensions
    """
    if len(tup) == 1:
        return [(tup[0]-1,),(tup[0],), (tup[0]+1,)]
    
    smaller_problem = check_nd_neighbors(tup[1:], dimensions)
     
    result = []
    for tupple in smaller_problem:
        for x in [tup[0]-1, tup[0], tup[0]+1]:            
            new_tup = (x,) + tupple
            if len(new_tup) == len(tup):
                result.append(new_tup)
            if len(result) == 3**len(tup):
                return result
            
def update_game_state_nd(game, revealed, actual_coords):
    """
    Updates state of the game. Returns the number of revealed states unless
    a bomb is found in which case it returns 1.
    """
    
    bombs = 0
    covered_squares = 0
    
    coord_array = create_nd_coordinate_array(game['dimensions'])
    coords = list_of_coordinates(coord_array, lista = [])
    
    for coord in coords:
        if get_val_nd(game['board'], coord) == '.':
            if get_val_nd(game['mask'], coord) == True:
                bombs += 1
        elif get_val_nd(game['mask'], coord) == False:
            covered_squares +=1  
            
    if bombs != 0:
        set_val_nd(game['mask'], game['dimensions'], actual_coords, True) 
        game['state'] = 'defeat'
        return 1   
    elif covered_squares != 0:
        game['state'] = 'ongoing'
        return revealed
    else:
        game['state'] = 'victory'
        return revealed
    
    
def check_neighbor_and_reveal_nd(game, neighbor, flag): 
    """
    Returns a call to dig_nd if neighbor is an entry on the board. Returns 0 otherwise.
    """
    is_it_in = True
    for elem1, elem2 in zip(game['dimensions'], neighbor):
        if elem2 not in range(elem1):
            is_it_in = False 
                
    if is_it_in:
        board_loc = game['board'][:]
        mask_loc = game['mask'][:]
        for elem2 in neighbor:
            board_loc = board_loc[elem2]
            mask_loc = mask_loc[elem2]
        if board_loc != '.':
            if mask_loc == False:
                return dig_nd(game, neighbor, flag)
            
    return 0


def is_neighbor_bomb(neighbors, bombs):
    """
    RETURNS NUMBER OF BOMBS IN NEIGHBORS
    """
    revealed = 0
    for x in bombs:
        if x in set(neighbors):
            revealed +=1
    return revealed



###---------------------------2D HELPER FUNCTIONS------------------------------
def make_board_and_mask(num_rows, num_cols, bombs):
    """
    returns a tuple containing a a board array and a mask array.
    """
    board = [] 
    mask = []
    for r in range(num_rows):
        board_row = []
        mask_row = []
        for c in range(num_cols):
            if (r,c) in bombs:
                board_row.append('.') 
            else:
                board_row.append(0)
            mask_row.append(False)
        board.append(board_row)
        mask.append(mask_row)
    return (board, mask)

def check_neighbor(r, c, num_rows, num_cols, board):
        """
        Returns 1 if the location is in the board and it is a bomb. Returns 0 otherwise.
        """
        if 0 <= r < num_rows:
            if 0 <= c < num_cols:
                if board[r][c] == '.':
                    return 1
        return 0
    
def check_neighbor_and_reveal(game, r, c, num_rows, num_cols):
    """
    Returns a call to dig_2d if (r,c) is an entry on the board. Returns 0 otherwise.
    """
    if 0 <= r< num_rows:
            if 0 <= c < num_cols:
                if game['board'][r][c] != '.':
                    if game['mask'][r][c] == False:
                        return dig_2d(game, r, c)
    return 0

def update_game_state(game, row, col, revealed):
    """
    Updates state of the game. Returns the number of revealed states unless
    a bomb is found in which case it returns 1.
    """
    bombs = 0 
    covered_squares = 0
    for r in range(game['dimensions'][0]):
        for c in range(game['dimensions'][1]):
            if game['board'][r][c] == '.':
                if  game['mask'][r][c] == True:
                    bombs += 1
            elif game['mask'][r][c] == False: 
                covered_squares += 1   
    if bombs != 0: 
        game['mask'][row][col] = True
        game['state'] = 'defeat'
        return 1
    elif covered_squares != 0:
        game['state'] = 'ongoing'
        return revealed
    else:
        game['state'] = 'victory'
        return revealed
    
    
###----------------------------DUMP GAME HELPER--------------------------------

def dump(game):
    """
    Prints a human-readable version of a game (provided as a dictionary)
    """
    for key, val in sorted(game.items()):
        if isinstance(val, list) and val and isinstance(val[0], list):
            print(f'{key}:')
            for inner in val:
                print(f'    {inner}')
        else:
            print(f'{key}:', val)
   
    
# 2-D IMPLEMENTATION
def new_game_2d(num_rows, num_cols, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'mask' fields adequately initialized.

    Parameters:
       num_rows (int): Number of rows
       num_cols (int): Number of columns
       bombs (list): List of bombs, given in (row, column) pairs, which are
                     tuples

    Returns: 
       A game state dictionary

    >>> dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    mask:
        [False, False, False, False]
        [False, False, False, False]
    state: ongoing
    """
    
    board, mask = make_board_and_mask(num_rows, num_cols, bombs)
    
    for r in range(num_rows):
        for c in range(num_cols):
            if board[r][c] == 0: 
                neighbor_bombs = 0
                for i, j in [(r-1, c-1),(r, c-1),(r+1, c-1),(r-1, c),(r+1, c),(r-1, c+1),(r, c+1),(r+1, c+1)]:
                    neighbor_bombs += check_neighbor(i, j, num_rows, num_cols, board)
                board[r][c] = neighbor_bombs 
    return {
        'dimensions': (num_rows, num_cols),
        'board' : board,
        'mask' : mask,
        'state': 'ongoing'}

def dig_2d(game, row, col):
    """
    Reveal the cell at (row, col), and, in some cases, recursively reveal its
    neighboring squares.

    Update game['mask'] to reveal (row, col).  Then, if (row, col) has no
    adjacent bombs (including diagonally), then recursively reveal (dig up) its
    eight neighbors.  Return an integer indicating how many new squares were
    revealed in total, including neighbors, and neighbors of neighbors, and so
    on.

    The state of the game should be changed to 'defeat' when at least one bomb
    is visible on the board after digging (i.e. game['mask'][bomb_location] ==
    True), 'victory' when all safe squares (squares that do not contain a bomb)
    and no bombs are visible, and 'ongoing' otherwise.

    Parameters:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       int: the number of new squares revealed

    >>> game = {'dimensions': (2, 4),
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 3)
    4
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    mask:
        [False, True, True, True]
        [False, False, True, True]
    state: victory

    >>> game = {'dimensions': [2, 4],
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 0)
    1
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: [2, 4]
    mask:
        [True, True, False, False]
        [False, False, False, False]
    state: defeat
    """
    if game['mask'][row][col] != True:
        game['mask'][row][col] = True
        revealed = 1
    else:
        return 0

    if game['board'][row][col] == 0:
        num_rows, num_cols = game['dimensions']
        revealed += dig_2d(game, row-1, col-1)
        for i, j in [(row, col),(row, col-1),(row+1, col-1),(row-1, col),(row+1, col),(row-1, col+1),(row, col+1),(row+1, col+1)]:
            revealed += check_neighbor_and_reveal(game, i, j, num_rows, num_cols)
    
    return update_game_state(game, row, col, revealed)


def render_2d(game, xray=False):
    """
    Prepare a game for display.

    Returns a two-dimensional array (list of lists) of '_' (hidden squares), '.'
    (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring bombs).
    game['mask'] indicates which squares should be visible.  If xray is True (the
    default is False), game['mask'] is ignored and all cells are shown.

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['mask']

    Returns:
       A 2D array (list of lists)

    >>> render_2d({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask':  [[False, True, True, False],
    ...                   [False, False, True, False]]}, False)
    [['_', '3', '1', '_'], ['_', '_', '1', '_']]

    >>> render_2d({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask':  [[False, True, False, True],
    ...                   [False, False, False, True]]}, True)
    [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
    """
    array = []
    for i in range(game['dimensions'][0]):
        cols = []
        for j in range(game['dimensions'][1]):
            if game['mask'][i][j] == False and xray == False:
                cols.append('_')
            elif game['board'][i][j] == 0:
                cols.append(' ')
            else:
                cols.append(str(game['board'][i][j]))
        array.append(cols)
    return array


def render_ascii(game, xray=False):
    """
    Render a game as ASCII art.

    Returns a string-based representation of argument 'game'.  Each tile of the
    game board should be rendered as in the function 'render_2d(game)'.

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['mask']

    Returns:
       A string-based representation of game

    >>> print(render_ascii({'dimensions': (2, 4),
    ...                     'state': 'ongoing',
    ...                     'board': [['.', 3, 1, 0],
    ...                               ['.', '.', 1, 0]],
    ...                     'mask':  [[True, True, True, False],
    ...                               [False, False, True, False]]}))
    .31_
    __1_
    """
    art = ""
    for i in range(game['dimensions'][0]):
        for j in range(game['dimensions'][1]):
            if xray:
                if game['board'][i][j] == '.':
                    art += '.'
                elif game['board'][i][j] == 0:
                    art += ' '
                else: 
                    art = art + str(game['board'][i][j])
            else:
                if game['mask'][i][j] == False:
                    art += '_'
                elif game['board'][i][j] == '.':
                    art += '.'
                elif game['board'][i][j] == 0:
                    art += ' '
                else:
                    art = art + str(game['board'][i][j])
        if i != game['dimensions'][0] -1:
            art += '\n'
        
        
    return art
 


# N-D IMPLEMENTATION   
def new_game_nd(dimensions, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'mask' fields adequately initialized.


    Args:
       dimensions (tuple): Dimensions of the board 
       bombs (list): Bomb locations as a list of lists, each an
                     N-dimensional coordinate

    Returns:
       A game state dictionary

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    mask:
        [[False, False], [False, False], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    state: ongoing
    """
    
    def create_board(dimensions, bombs, tup = ()):
        if len(dimensions) == 0: 
            if tup in set(bombs):
                return '.'
            else:
                return 0 
        
        return [create_board(dimensions[1:], bombs, tup + (i,)) for i in range(dimensions[0])]
    
        
    def create_mask(dimensions):
        if len(dimensions) == 0: 
            return False
        
        return [create_mask(dimensions[1:]) for i in range(dimensions[0])]
    
    board = create_board(dimensions, bombs, tup = ())
    for bomb in set(bombs):
        neighbors = check_nd_neighbors(bomb, dimensions)
        for neighbor in neighbors:
            if neighbor not in set(bombs) and check_dimension(dimensions, neighbor):
                set_val_nd(board, dimensions, neighbor, get_val_nd(board, neighbor) + 1)
    
                    
    return { 
        'board': board, 
        'dimensions': dimensions, 
        'mask': create_mask(dimensions), 
        'state': 'ongoing'}

def dig_nd(game, coordinates, flag = True):
    """
    Recursively dig up square at coords and neighboring squares.

    Update the mask to reveal square at coords; then recursively reveal its
    neighbors, as long as coords does not contain and is not adjacent to a
    bomb.  Return a number indicating how many squares were revealed.  No
    action should be taken and 0 returned if the incoming state of the game
    is not 'ongoing'.

    The updated state is 'defeat' when at least one bomb is visible on the
    board after digging, 'victory' when all safe squares (squares that do
    not contain a bomb) and no bombs are visible, and 'ongoing' otherwise.

    Args:
        coordinates (tuple): Where to start digging

    Returns:
        int: number of squares revealed

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'mask': [[[False, False], [False, True], [False, False], [False, False]],
    ...               [[False, False], [False, False], [False, False], [False, False]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 3, 0))
    8
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    mask:
        [[False, False], [False, True], [True, True], [True, True]]
        [[False, False], [False, False], [True, True], [True, True]]
    state: ongoing
    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'mask': [[[False, False], [False, True], [False, False], [False, False]],
    ...               [[False, False], [False, False], [False, False], [False, False]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 0, 1))
    1
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    mask:
        [[False, True], [False, True], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    state: defeat
    """
    
    # board_loc = game['board']
    # mask_loc = game['mask']
    
    # for elem in coordinates:
    #     board_loc = board_loc[elem]
    #     mask_loc = mask_loc[elem]
        
    # if board_loc == '.':
    #     set_val_nd(game['mask'], None, coordinates, True )
    #     game['state'] = 'defeat'
    #     return 1
    
    # if mask_loc != True:
    #     set_val_nd(game['mask'], game['dimensions'], coordinates, True)
    #     revealed = 1
    # else:
    #     return 0

    # if board_loc == 0: 
    #     neighbors = check_nd_neighbors(coordinates, game['dimensions'])
    #     for neighbor in neighbors: 
    #         revealed += check_neighbor_and_reveal_nd(game, neighbor, flag = False) 
    
    # if flag:  
    #     return update_game_state_nd(game, revealed, coordinates)
    # else:
    #     return revealed

def render_nd(game, xray=False):
    """
    Prepare the game for display.

    Returns an N-dimensional array (nested lists) of '_' (hidden squares),
    '.' (bombs), ' ' (empty squares), or '1', '2', etc. (squares
    neighboring bombs).  The mask indicates which squares should be
    visible.  If xray is True (the default is False), the mask is ignored
    and all cells are shown.

    Args:
        xray (bool): Whether to reveal all tiles or just the ones allowed by
                    the mask

    Returns:
        An n-dimensional array of strings (nested lists)

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'mask': [[[False, False], [False, True], [True, True], [True, True]],
    ...               [[False, False], [False, False], [True, True], [True, True]]],
    ...      'state': 'ongoing'}
    >>> render_nd(g, False)
    [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
      [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

    >>> render_nd(g, True)
    [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
      [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
    """
    # array = game['board'][:]
    # coord_array = create_nd_coordinate_array(game['dimensions'])
    # coord_list = list_of_coordinates(coord_array, lista = [])
    
    # for coord in coord_list:
    #     if get_val_nd(game['mask'], coord) == False and xray == False:
    #         set_val_nd(array, game['dimensions'], coord, '_')
    #     elif get_val_nd(game['board'], coord) == 0:
    #         set_val_nd(array, game['dimensions'], coord, ' ')
    #     else:
    #         set_val_nd(array, game['dimensions'], coord, str(get_val_nd(array, coord)))
                
    # return array 
            
                
            
            
        


if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual lab.py functions.
    import doctest
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags) #runs ALL doctests
    
    # g = {'dimensions': (2, 4, 2),'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]], [['.', 3], [3, '.'], [1, 1], [0, 0]]],'mask': [[[False, False], [False, True], [True, True], [True, True]], [[False, False], [False, False], [True, True], [True, True]]],'state': 'ongoing'}
    # print(render_nd(g, True))
    # g = {'dimensions': (2, 4, 2), 'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]], [['.', 3], [3, '.'], [1, 1], [0, 0]]], 'mask': [[[False, False], [False, True], [True, True], [True, True]], [[False, False], [False, False], [True, True], [True, True]]], 'state': 'ongoing'}
    # array = render_nd(g, False)
    # print(array)
    
    # g = {'dimensions': (2, 4, 2), 'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]], [['.', 3], [3, '.'], [1, 1], [0, 0]]], 'mask': [[[False, False], [False, True], [False, False], [False, False]], [[False, False], [False, False], [False, False], [False, False]]], 'state': 'ongoing'}
    # a = dig_nd(g, (0, 3, 0))
    # dump(g) 
    # print("GOTEM: ", a)
    # print(render_ascii({'dimensions': (2, 4),'state': 'ongoing','board': [['.', 3, 1, 0],['.', '.', 1, 0]],'mask':  [[True, True, True, False],[False, False, True, False]]}))
    # my_game = new_game_nd((2,3,4), [(0, 0, 0), (1,1,1)])
    # print(check_neighbor_and_reveal_nd(my_game, (1,0,1)))
    
    # print(check_nd_neighbors((2,3,4)))
    # array = render_2d({'dimensions': (2, 4), 'state': 'ongoing', 'board': [['.', 3, 1, 0], ['.', '.', 1, 0]], 'mask':  [[False, True, True, False], [False, False, True, False]]}, False)
    # print(array)
    # Alternatively, can run the doctests JUST for specified function/methods,
    # e.g., for render_2d or any other function you might want.  To do so, comment
    # out the above line, and uncomment the below line of code. This may be
    # useful as you write/debug individual doctests or functions.  Also, the
    # verbose flag can be set to True to see all test results, including those
    # that pass.
    #
    #doctest.run_docstring_examples(render_2d, globals(), optionflags=_doctest_flags, verbose=False)
