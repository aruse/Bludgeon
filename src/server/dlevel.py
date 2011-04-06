# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

"""
Routines for generating dungeon levels.
"""

import common.cfg as cfg
from server_state import ServerState as SS

DIR_LEFT = 0
DIR_RIGHT = 1
DIR_UP = 2
DIR_DOWN = 3


def gen_perfect_maze(amap):
    """Generate a perfect maze and return it"""
    # Map of all visited locations
    visited_map = [[0 for j in xrange(amap.h)]
                   for i in xrange(amap.w)]

    # Knock out a grid of holes in the walls
    total_cells = 0
    for x in xrange(0, amap.w, 2):
        for y in xrange(0, amap.h, 2):
            amap.grid[x][y].set_attr('cmap, floor of a room')
            total_cells += 1

    # Starting at a random point, move out in a random direction,
    # knocking down walls as you go.  If you've been to a wall
    # previously, backtrack.
    cur_cell = [SS.map_rand.randrange(amap.w - 1),
                SS.map_rand.randrange(amap.h - 1)]
    if amap.grid[cur_cell[0]][cur_cell[1]].kind == 'wall':
        cur_cell[0] += 1
    if amap.grid[cur_cell[0]][cur_cell[1]].kind == 'wall':
        cur_cell[1] += 1
    if amap.grid[cur_cell[0]][cur_cell[1]].kind == 'wall':
        cur_cell[0] -= 1

    visited_cells = 1
    visited_map[cur_cell[0]][cur_cell[1]] = 1
    cell_stack = []  # Cells to visit

    while visited_cells < total_cells:
        possible_moves = [0, 0, 0, 0]  # Left, right, up, down
        if (cur_cell[0] - 2 >= 0 and
            amap.grid[cur_cell[0] - 1][cur_cell[1]].kind == 'wall' and
            not visited_map[cur_cell[0] - 2][cur_cell[1]]):
            possible_moves[DIR_LEFT] = 1
        if (cur_cell[0] + 2 < w and
            amap.grid[cur_cell[0] + 1][cur_cell[1]].kind == 'wall' and
            not visited_map[cur_cell[0] + 2][cur_cell[1]]):
            possible_moves[DIR_RIGHT] = 1
        if (cur_cell[1] - 2 >= 0 and
            amap.grid[cur_cell[0]][cur_cell[1] - 1].kind == 'wall' and
            not visited_map[cur_cell[0]][cur_cell[1] - 2]):
            possible_moves[DIR_UP] = 1
        if (cur_cell[1] + 2 < h and
            amap.grid[cur_cell[0]][cur_cell[1] + 1].kind == 'wall' and
            not visited_map[cur_cell[0]][cur_cell[1] + 2]):
            possible_moves[DIR_DOWN] = 1

        # If there are moves to make, select a random direction
        if possible_moves.count(1):
            # Select a number from 0 to number of possible moves - 1
            move_direction = SS.map_rand.randrange(possible_moves.count(1))
            # Map the direction to an index of the possible_moves list
            move_direction = possible_moves.index(1, move_direction)

            cell_stack.append([cur_cell[0], cur_cell[1]])

            # Knock down wall in the move direction, and then move
            # past the wall into the next cell
            if move_direction == DIR_LEFT:
                amap.grid[cur_cell[0] - 1][cur_cell[1]].set_attr(
                    'cmap, floor of a room')
                cur_cell[0] -= 2
            elif move_direction == DIR_RIGHT:
                amap.grid[cur_cell[0] + 1][cur_cell[1]].set_attr(
                    'cmap, floor of a room')
                cur_cell[0] += 2
            elif move_direction == DIR_UP:
                amap.grid[cur_cell[0]][cur_cell[1] - 1].set_attr(
                    'cmap, floor of a room')
                cur_cell[1] -= 2
            elif move_direction == DIR_DOWN:
                amap.grid[cur_cell[0]][cur_cell[1] + 1].set_attr(
                    'cmap, floor of a room')
                cur_cell[1] += 2

            visited_map[cur_cell[0]][cur_cell[1]] = 1
            visited_cells += 1

        # If there are no moves to make, pop a cell off the cell_stack
        # and go from there.
        else:
            if cell_stack:
                cur_cell = cell_stack.pop()
            else:
                break

    return update_wall_tiles(amap)


def gen_braid_maze(w, h, braid_degree=1.0):
    """Generate a braid maze.

    The braid_degree is a float between 0 and 1, indicating the chance
    of extending a dead-end through the wall.
    """

    # First get a perfect maze
    amap = gen_perfect_maze(w, h)

    # Go through the maze, looking for dead-ends, and extend them
    for x in xrange(0, w, 2):
        for y in xrange(0, h, 2):
            connections = 0
            if amap.grid[x][y].kind != 'wall':
                if x > 0 and amap.grid[x - 1][y].kind != 'wall':
                    connections += 1
                    connection = DIR_LEFT
                if x < w - 1 and amap.grid[x + 1][y].kind != 'wall':
                    connections += 1
                    connection = DIR_RIGHT
                if y > 0 and amap.grid[x][y - 1].kind != 'wall':
                    connections += 1
                    connection = DIR_UP
                if y < h - 1 and amap.grid[x][y + 1].kind != 'wall':
                    connections += 1
                    connection = DIR_DOWN

                # If there is only one connection, it's a dead-end
                if connections == 1 and SS.map_rand.random() < braid_degree:
                    if connection == DIR_LEFT and x < w - 1:
                        amap.grid[x + 1][y].set_attr('cmap, floor of a room')
                    if connection == DIR_RIGHT and x > 0:
                        amap.grid[x - 1][y].set_attr('cmap, floor of a room')
                    if connection == DIR_UP and y < h - 1:
                        amap.grid[x][y + 1].set_attr('cmap, floor of a room')
                    if connection == DIR_DOWN and y > 0:
                        amap.grid[x][y - 1].set_attr('cmap, floor of a room')

    return update_wall_tiles(amap)


def gen_sparse_maze(w, h, sparse_degree=0.1, braid_degree=0.9):
    """Generate a maze that has more open space than the braid maze."""

    amap = gen_braid_maze(w, h, braid_degree=braid_degree)

    for x in xrange(0, w):
        for y in xrange(0, h):
            if amap.grid[x][y] == 1:
                # Only punch out walls if there is a wall to either side
                walls_hor = 0
                walls_ver = 0

                if x > 0 and amap.grid[x - 1][y] == 1:
                    walls_hor += 1
                if x < w - 1 and amap.grid[x + 1][y] == 1:
                    walls_hor += 1
                if y > 0 and amap.grid[x][y - 1] == 1:
                    walls_ver += 1
                if y < h - 1 and amap.grid[x][y + 1] == 1:
                    walls_ver += 1

                if (((walls_hor == 2 and walls_ver == 0) or
                     (walls_ver == 2 and walls_hor == 0)) and
                    SS.map_rand.random() < sparse_degree):
                    amap.grid[x][y] = 0

    return update_wall_tiles(amap)


def update_wall_tiles(amap):
    """Goes through a level map and makes sure the correct tiles are
    used for walls, depending on what's in the adjacent spaces.
    """
    for x in xrange(cfg.MAP_W):
        for y in xrange(cfg.MAP_H):
            if amap.grid[x][y].kind == 'wall':
                wall_tile = 'cmap, wall, horizontal'
                tee = 0

                if x > 0 and amap.grid[x - 1][y].kind == 'wall':
                    if (y > 0 and
                        amap.grid[x][y - 1].kind == 'wall' and
                        y < cfg.MAP_H - 1 and
                        amap.grid[x][y + 1].kind == 'wall'):
                        wall_tile = 'cmap, wall, tee left'
                        tee = 1
                    elif y > 0 and amap.grid[x][y - 1].kind == 'wall':
                        wall_tile = 'cmap, wall, top left corner'
                    elif (y < cfg.MAP_H - 1 and
                          amap.grid[x][y + 1].kind == 'wall'):
                        wall_tile = 'cmap, wall, bottom left corner'

                if (x < cfg.MAP_W - 1 and
                    amap.grid[x + 1][y].kind == 'wall'):
                    if (y > 0 and
                        amap.grid[x][y - 1].kind == 'wall' and
                        y < cfg.MAP_H - 1 and
                        amap.grid[x][y + 1].kind == 'wall'):
                        wall_tile = 'cmap, wall, tee right'
                        tee = 1
                    elif y > 0 and amap.grid[x][y - 1].kind == 'wall':
                        wall_tile = 'cmap, wall, top right corner'
                    elif (y < cfg.MAP_H - 1 and
                          amap.grid[x][y + 1].kind == 'wall'):
                        wall_tile = 'cmap, wall, bottom right corner'

                if not tee:
                    if y > 0 and amap.grid[x][y - 1].kind == 'wall':
                        wall_tile = 'cmap, wall, vertical'
                        if (x > 0 and
                            amap.grid[x - 1][y].kind == 'wall' and
                            x < cfg.MAP_W - 1 and
                            amap.grid[x + 1][y].kind == 'wall'):
                            wall_tile = 'cmap, wall, tee up'
                        elif x > 0 and amap.grid[x - 1][y].kind == 'wall':
                            wall_tile = 'cmap, wall, bottom right corner'
                        elif (x < cfg.MAP_W - 1 and
                              amap.grid[x + 1][y].kind == 'wall'):
                            wall_tile = 'cmap, wall, bottom left corner'

                if (y < cfg.MAP_H - 1 and
                    amap.grid[x][y + 1].kind == 'wall'):
                    wall_tile = 'cmap, wall, vertical'
                    if (x > 0 and
                        amap.grid[x - 1][y].kind == 'wall' and
                        x < cfg.MAP_W - 1 and
                        amap.grid[x + 1][y].kind == 'wall'):
                        wall_tile = 'cmap, wall, tee down'
                    elif x > 0 and amap.grid[x - 1][y].kind == 'wall':
                        wall_tile = 'cmap, wall, top right corner'
                    elif (x < cfg.MAP_W - 1 and
                          amap.grid[x + 1][y].kind == 'wall'):
                        wall_tile = 'cmap, wall, top left corner'

                if (x > 0 and
                    amap.grid[x - 1][y].kind == 'wall' and
                    x < cfg.MAP_W - 1 and
                    amap.grid[x + 1][y].kind == 'wall' and
                    y > 0 and amap.grid[x][y - 1].kind == 'wall' and
                    y < cfg.MAP_H - 1 and
                    amap.grid[x][y + 1].kind == 'wall'):
                    wall_tile = 'cmap, wall, crosswall'

                amap.grid[x][y].set_attr(wall_tile)

    return amap
