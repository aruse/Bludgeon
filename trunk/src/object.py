import random
import math

import pygame
from pygame.locals import *

from const import *
from game import *
from util import *
from mon_class import *
from fov import *
from ai import *

class Object:
    """Generic object.  Can be sub-classed into players, monsters,
    items, etc.
    """
    def __init__(self, x, y, name, oid=None):
        if oid:
            self.oid = oid
        else:
            self.oid = GC.oid_seq
            GC.oid_seq += 1

        GC.obj_dict[self.oid] = self

        self.x = x
        self.y = y
        self.name = name

        # The category of this Object: human, dwarf, lich, etc.
#        self.obj_class = mon_class_dict[name]

        self.tile = GV.tile_dict[name]
        
        # Which color to display in text mode
        self.color = None

        self.blocks_sight = False
        self.blocks_movement = False
        
    def move(self, dx, dy=None):
        """Move dx and dy spaces, if possible."""
        if type(dx) == type(tuple()):
            dx, dy = dx[0], dx[1]
            
        if self.can_move_dir(dx, dy):
            self.x += dx
            self.y += dy
            return True
        else:
            return False

    def move_randomly(self):
        dir = random.randrange(len(DIR))
        if self.can_move_dir(DIR[dir]):
            self.move(DIR[dir])

    def move_towards(self, x, y=None):
        """Move towards the x, y coords, if possible."""
        if type(x) == type(tuple()):
            x, y = x[0], x[1]

        dx = x - self.x
        dy = y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
 
        # Normalize the distance to length 1 (preserving direction), then 
        # convert it to a movment direction.
        if dx > 0:
            x = 1
        elif dx < 0:
            x = -1
        else:
            x = 0

        if dy > 0:
            y = 1
        elif dy < 0:
            y = -1
        else:
            y = 0

        if self.can_move_dir(x, y):
            self.move(x, y)
        # If we can't move in the direction we want to, then try to
        # move vertically or horizontally
        else:
            if self.can_move_dir(x, 0):
                self.move(x, 0)
            else:
                self.move(0, y)

    def distance_to(self, obj):
        """Distance to another object."""
        return self.distance(obj.x, obj.y)

    def distance(self, x, y):
        """Distance to coords."""
        if type(x) == type(tuple()):
            x, y = x[0], x[1]
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def draw(self):
        """Draw this Object on the map at the current location."""
        # Remember to offset by 1 tile so that there's room
        # for the border.
        GV.map_surf.blit(GV.tiles_img,
                         ((self.x + 1) * TILE_W, (self.y + 1) * TILE_H),
                         self.tile)
 
    def draw_gray(self):
        """Draw this Object on the map at the current location, grayed out."""
        GV.map_surf.blit(GV.gray_tiles_img,
                         ((self.x + 1) * TILE_W, (self.y + 1) * TILE_H),
                         self.tile)

    def can_move_dir(self, x, y=None):
        """Can the character move in this direction?"""
        if type(x) == type(tuple()):
            x, y = x[0], x[1]
            
        return self.can_move(self.x + x, self.y + y)
        
    def can_move(self, x, y=None):
        """Can the object move into this location?"""
        if type(x) == type(tuple()):
            x, y = x[0], x[1]
            
        can_move = True

        if x < 0 or y < 0 or x >= MAP_W or y >= MAP_H:
            can_move = False

        if GC.map[x][y].blocks_movement:
            can_move = False

        for m in GC.monsters + [GC.u]:
            if x == m.x and y == m.y:
                can_move = False
                break
            
        return can_move
