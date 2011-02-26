# Routines for generating dungeon levels

import random

from const import *
from tile import *
from room import *

DIR_LEFT = 0
DIR_RIGHT = 1
DIR_UP = 2
DIR_DOWN = 3

def create_room(map, room):
    # Punch out the floor tiles
    for x in range(room.x1 + 1, room.x2):
       for y in range(room.y1 + 1, room.y2):
            map[x][y] = Tile("cmap, floor of a room")

    # Add wall tiles surrounding the room
    for x in range(room.x1 + 1, room.x2):
        map[x][room.y1] = Tile("cmap, wall, horizontal")
    for x in range(room.x1 + 1, room.x2):
        map[x][room.y2] = Tile("cmap, wall, horizontal")
    for y in range(room.y1 + 1, room.y2):
        map[room.x1][y] = Tile("cmap, wall, vertical")
    for y in range(room.y1 + 1, room.y2):
        map[room.x2][y] = Tile("cmap, wall, vertical")

    # Add corner tiles
    map[room.x1][room.y1] = Tile("cmap, wall, top left corner")
    map[room.x2][room.y1] = Tile("cmap, wall, top right corner")
    map[room.x1][room.y2] = Tile("cmap, wall, bottom left corner")
    map[room.x2][room.y2] = Tile("cmap, wall, bottom right corner")
            
def create_h_tunnel(map, x1, x2, y):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        map[x][y] = Tile("cmap, floor of a room")
 
def create_v_tunnel(map, y1, y2, x):
    for y in range(min(y1, y2), max(y1, y2) + 1):
        map[x][y] = Tile("cmap, floor of a room")


def gen_connected_rooms():
    map = [[ Tile("cmap, wall, dark") for y in range(MAP_H) ] for x in range(MAP_W)]
    rooms = []
    num_rooms = 0
    
    for r in range(MAX_ROOMS):
        w = random.randrange(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        h = random.randrange(ROOM_MIN_SIZE, ROOM_MAX_SIZE)

        x = random.randrange(0, MAP_W - w - 1)
        y = random.randrange(0, MAP_H - h - 1)
 
        new_room = Room(x, y, w, h)
        
        # Run through the other rooms and see if they intersect with this one
        failed = False
        for room in rooms:
            if new_room.intersect(room):
                failed = True
                break
 
        if not failed:
            create_room(map, new_room)
 
#            place_objects(new_room)
 
            # First room
            if num_rooms == 0:
                (new_x, new_y) = new_room.center()
                GC.u.x = new_x
                GC.u.y = new_y
 
            rooms.append(new_room)
            num_rooms += 1

    # Connect the rooms
    connected_rooms = []
    x = 0
    for room in rooms:
        if x > 0:
            (new_x, new_y) = room.center()
            (prev_x, prev_y) = rooms[x - 1].center()
            if random.randrange(0, 2):
                create_h_tunnel(map, prev_x, new_x, prev_y)
                create_v_tunnel(map, prev_y, new_y, new_x)
            else:
                create_v_tunnel(map, prev_y, new_y, prev_x)
                create_h_tunnel(map, prev_x, new_x, new_y)
        x += 1
        
    return map


def gen_perfect_maze(w, h):
    """Generate a perfect maze and return it"""
    # Create multi-dimensional list of dimensions w x h filled with walls
    map = [[ Tile("cmap, wall, dark") for y in range(h) ] for x in range(w)]

    # Map of all visited locations
    visited_map = [[ 0 for y in range(h) ] for x in range(w)]
    
    # Knock out a grid of holes in the walls
    total_cells = 0
    for x in range(0, w, 2):
        for y in range(0, h, 2):
            map[x][y] = Tile("cmap, floor of a room")
            total_cells += 1

    # Starting at a random point, move out in a random direction, knocking down walls as you go.  If you've been to a wall previously, backtrack.
    cur_cell = [random.randrange(w - 1), random.randrange(h - 1)]
    if(map[cur_cell[0]][cur_cell[1]].tile_class == 'wall'):
        cur_cell[0] += 1
    if(map[cur_cell[0]][cur_cell[1]].tile_class == 'wall'):
        cur_cell[1] += 1
    if(map[cur_cell[0]][cur_cell[1]].tile_class == 'wall'):
        cur_cell[0] -= 1

    visited_cells = 1
    visited_map[cur_cell[0]][cur_cell[1]] = 1
    cell_stack = [] # Cells to visit
    
    while visited_cells < total_cells:
        possible_moves = [0, 0, 0, 0] # left, right, up, down
        if cur_cell[0] - 2 >= 0 and \
               map[cur_cell[0] - 1][cur_cell[1]].tile_class == 'wall' and \
               not visited_map[cur_cell[0] - 2][cur_cell[1]]:
            possible_moves[DIR_LEFT] = 1
        if cur_cell[0] + 2 < w and \
               map[cur_cell[0] + 1][cur_cell[1]].tile_class == 'wall' and \
               not visited_map[cur_cell[0] + 2][cur_cell[1]]:
            possible_moves[DIR_RIGHT] = 1
        if cur_cell[1] - 2 >= 0 and \
               map[cur_cell[0]][cur_cell[1] - 1].tile_class == 'wall' and \
               not visited_map[cur_cell[0]][cur_cell[1] - 2]:
            possible_moves[DIR_UP] = 1
        if cur_cell[1] + 2 < h and \
               map[cur_cell[0]][cur_cell[1] + 1].tile_class == 'wall' and \
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
                map[cur_cell[0] - 1][cur_cell[1]] = Tile("cmap, floor of a room")
                cur_cell[0] -= 2
            elif move_direction == DIR_RIGHT:
                map[cur_cell[0] + 1][cur_cell[1]] = Tile("cmap, floor of a room")
                cur_cell[0] += 2
            elif move_direction == DIR_UP:
                map[cur_cell[0]][cur_cell[1] - 1] = Tile("cmap, floor of a room")
                cur_cell[1] -= 2
            elif move_direction == DIR_DOWN:
                map[cur_cell[0]][cur_cell[1] + 1] = Tile("cmap, floor of a room")
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

    return update_wall_tiles(map)

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
            if map[x][y].tile_class != 'wall':
                if x > 0 and map[x - 1][y].tile_class != 'wall':
                    connections += 1
                    connection = DIR_LEFT
                if x < w - 1 and map[x + 1][y].tile_class != 'wall':
                    connections += 1
                    connection = DIR_RIGHT
                if y > 0 and map[x][y - 1].tile_class != 'wall':
                    connections += 1
                    connection = DIR_UP
                if y < h - 1 and map[x][y + 1].tile_class != 'wall':
                    connections += 1
                    connection = DIR_DOWN

                # If there is only one connection, it's a dead-end
                if connections == 1 and random.random() < braid_degree :
                    if connection == DIR_LEFT and x < w - 1:
                        map[x + 1][y] = Tile("cmap, floor of a room")
                    if connection == DIR_RIGHT and x > 0:
                        map[x - 1][y] = Tile("cmap, floor of a room")
                    if connection == DIR_UP and y < h - 1:
                        map[x][y + 1] = Tile("cmap, floor of a room")
                    if connection == DIR_DOWN and y > 0 :
                        map[x][y - 1] = Tile("cmap, floor of a room")

    return update_wall_tiles(map)

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
                
    return update_wall_tiles(map)

def update_wall_tiles(map):
    """Goes through a level map and makes sure the correct tiles are used for walls, depending on what's in the adjacent spaces."""
    for x in range(MAP_W):
        for y in range(MAP_H):
            if map[x][y].tile_class == 'wall':
                wall_tile = "cmap, wall, horizontal"
                tee = 0

                if x > 0 and map[x - 1][y].tile_class == 'wall':
                    if y > 0 and map[x][y - 1].tile_class == 'wall' and y < MAP_H - 1 and map[x][y + 1].tile_class == 'wall':
                        wall_tile = "cmap, wall, tee left"
                        tee = 1
                    elif y > 0 and map[x][y - 1].tile_class == 'wall':
                        wall_tile = "cmap, wall, top left corner"
                    elif y < MAP_H - 1 and map[x][y + 1].tile_class == 'wall':
                        wall_tile = "cmap, wall, bottom left corner"
                        
                if x < MAP_W - 1 and map[x + 1][y].tile_class == 'wall':
                    if y > 0 and map[x][y - 1].tile_class == 'wall' and y < MAP_H - 1 and map[x][y + 1].tile_class == 'wall':
                        wall_tile = "cmap, wall, tee right"
                        tee = 1
                    elif y > 0 and map[x][y - 1].tile_class == 'wall':
                        wall_tile = "cmap, wall, top right corner"
                    elif y < MAP_H - 1 and map[x][y + 1].tile_class == 'wall':
                        wall_tile = "cmap, wall, bottom right corner"

                if not tee:
                    if y > 0 and map[x][y - 1].tile_class == 'wall':
                        wall_tile = "cmap, wall, vertical"
                        if x > 0 and map[x - 1][y].tile_class == 'wall' and x < MAP_W - 1 and map[x + 1][y].tile_class == 'wall':
                            wall_tile = "cmap, wall, tee up"
                        elif x > 0 and map[x - 1][y].tile_class == 'wall':
                            wall_tile = "cmap, wall, bottom right corner"
                        elif x < MAP_W - 1 and map[x + 1][y].tile_class == 'wall':
                            wall_tile = "cmap, wall, bottom left corner"
                        
                if y < MAP_H - 1 and map[x][y + 1].tile_class == 'wall':
                    wall_tile = "cmap, wall, vertical"
                    if x > 0 and map[x - 1][y].tile_class == 'wall' and x < MAP_W - 1 and map[x + 1][y].tile_class == 'wall':
                        wall_tile = "cmap, wall, tee down"
                    elif x > 0 and map[x - 1][y].tile_class == 'wall':
                        wall_tile = "cmap, wall, top right corner"
                    elif x < MAP_W - 1 and map[x + 1][y].tile_class == 'wall':
                        wall_tile = "cmap, wall, top left corner"

                if x > 0 and map[x - 1][y].tile_class == 'wall' and x < MAP_W - 1 and map[x + 1][y].tile_class == 'wall' and \
                        y > 0 and map[x][y - 1].tile_class == 'wall' and y < MAP_H - 1 and map[x][y + 1].tile_class == 'wall':
                    wall_tile = "cmap, wall, crosswall"

                map[x][y] = Tile(wall_tile)

    return map
