# Routines for generating dungeon levels

import random

DIR_LEFT = 0
DIR_RIGHT = 1
DIR_UP = 2
DIR_DOWN = 3

def gen_perfect_maze(w, h):
    """Generate a perfect maze and return it"""
    # Create multi-dimensional list of dimensions w x h filled with walls
    map = [[ 1 for y in range(h) ] for x in range(w)]

    # Map of all visited locations
    visited_map = [[ 0 for y in range(h) ] for x in range(w)]
    
    # Knock out a grid of holes in the walls
    total_cells = 0
    for x in range(0, w, 2):
        for y in range(0, h, 2):
            map[x][y] = 0
            total_cells += 1

    # Starting at a random point, move out in a random direction, knocking down walls as you go.  If you've been to a wall previously, backtrack.
    cur_cell = [random.randrange(w - 1), random.randrange(h - 1)]
    if(map[cur_cell[0]][cur_cell[1]]):
        cur_cell[0] += 1
    if(map[cur_cell[0]][cur_cell[1]]):
        cur_cell[1] += 1
    if(map[cur_cell[0]][cur_cell[1]]):
        cur_cell[0] -= 1

    visited_cells = 1
    visited_map[cur_cell[0]][cur_cell[1]] = 1
    cell_stack = [] # Cells to visit
    
    while visited_cells < total_cells:
        possible_moves = [0, 0, 0, 0] # left, right, up, down
        if cur_cell[0] - 2 >= 0 and \
               map[cur_cell[0] - 1][cur_cell[1]] and \
               not visited_map[cur_cell[0] - 2][cur_cell[1]]:
            possible_moves[DIR_LEFT] = 1
        if cur_cell[0] + 2 < w and \
               map[cur_cell[0] + 1][cur_cell[1]] and \
               not visited_map[cur_cell[0] + 2][cur_cell[1]]:
            possible_moves[DIR_RIGHT] = 1
        if cur_cell[1] - 2 >= 0 and \
               map[cur_cell[0]][cur_cell[1] - 1] and \
               not visited_map[cur_cell[0]][cur_cell[1] - 2]:
            possible_moves[DIR_UP] = 1
        if cur_cell[1] + 2 < h and \
               map[cur_cell[0]][cur_cell[1] + 1] and \
               not visited_map[cur_cell[0]][cur_cell[1] + 2]:
            possible_moves[DIR_DOWN] = 1

        # If there are moves to make, select a random direction
        if possible_moves.count(1):
            # Select a number from 0 to number of possible moves - 1
            move_direction = random.randrange(possible_moves.count(1))
            # Map the direction to an index of the possible_moves list
            move_direction = possible_moves.index(1, move_direction)

            cell_stack.append([cur_cell[0], cur_cell[1]])
                        
            # Knock down wall in the move direction, and then move past the wall into the next cell
            if move_direction == DIR_LEFT:
                map[cur_cell[0] - 1][cur_cell[1]] = 0;
                cur_cell[0] -= 2
            elif move_direction == DIR_RIGHT:
                map[cur_cell[0] + 1][cur_cell[1]] = 0;
                cur_cell[0] += 2
            elif move_direction == DIR_UP:
                map[cur_cell[0]][cur_cell[1] - 1] = 0;
                cur_cell[1] -= 2
            elif move_direction == DIR_DOWN:
                map[cur_cell[0]][cur_cell[1] + 1] = 0;
                cur_cell[1] += 2
            else:
                pass # Raise an error here

            visited_map[cur_cell[0]][cur_cell[1]] = 1
            visited_cells += 1

        # If there are no moves to make, pop a cell off the cell_stack and go from there
        else:
            if cell_stack:
                cur_cell = cell_stack.pop()
            else:
                break
    return map

def gen_braid_maze(w, h, braid_degree=1.0):
    """Generate a braid maze.

    The braid_degree is a float between 0 and 1, indicating the chance
    of extending a dead-end through the wall."""

    # First get a perfect maze
    map = gen_perfect_maze(w, h)

    # Go through the maze, looking for dead-ends, and extend them
    for x in range(0, w, 2):
        for y in range(0, h, 2):
            connections = 0
            if map[x][y] == 0:
                if x > 0 and map[x - 1][y] == 0:
                    connections += 1
                    connection = DIR_LEFT
                if x < w - 1 and map[x + 1][y] == 0:
                    connections += 1
                    connection = DIR_RIGHT
                if y > 0 and map[x][y - 1] == 0:
                    connections += 1
                    connection = DIR_UP
                if y < h - 1 and map[x][y + 1] == 0:
                    connections += 1
                    connection = DIR_DOWN

                # If there is only one connection, it's a dead-end
                if connections == 1 and random.random() < braid_degree :
                    if connection == DIR_LEFT and x < w - 1:
                        map[x + 1][y] = 0
                    if connection == DIR_RIGHT and x > 0:
                        map[x - 1][y] = 0
                    if connection == DIR_UP and y < h - 1:
                        map[x][y + 1] = 0
                    if connection == DIR_DOWN and y > 0 :
                        map[x][y - 1] = 0

    return map

def gen_sparse_maze(w, h, sparse_degree=0.1, braid_degree=0.9):
    """Generate a maze that has more open space than the braid maze."""

    map = gen_braid_maze(w, h, braid_degree)

    for x in range(0, w):
        for y in range(0, h):
            if map[x][y] == 1:
                # Only punch out walls if there is a wall to either side
                walls_hor = 0
                walls_ver = 0

                if x > 0 and map[x - 1][y] == 1:
                    walls_hor += 1
                if x < w - 1 and map[x + 1][y] == 1:
                    walls_hor += 1
                if y > 0 and map[x][y - 1] == 1:
                    walls_ver += 1
                if y < h - 1 and map[x][y + 1] == 1:
                    walls_ver += 1

                if ((walls_hor == 2 and walls_ver == 0) or \
                    (walls_ver == 2 and walls_hor == 0)) and \
                    random.random() < sparse_degree:
                    map[x][y] = 0
                
    return map
