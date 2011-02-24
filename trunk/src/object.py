import random
import pygame
from pygame.locals import *

from const import *
from game import *
from util import *
from mon_class import *

class Object:
    """Generic object.  Can be sub-classed into players, monsters, items, etc."""
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        
        # The category of this Object: human, dwarf, lich, etc.
        self.obj_class = mon_class_dict[type]

        self.tile = create_tile(type)
        
        # Which color to display in text mode
        self.color = None
 
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
 
    def draw(self):
        """Draw this Object on the map at the current location."""
        GV.map_surf.blit(self.tile,  (self.x * TILE_PW, self.y * TILE_PH))
 
    def can_move_dir(self, x, y=None):
        """Can the character move in this direction?"""
        if type(x) == type(tuple()):
            x, y = x[0], x[1]
            
        return self.can_move(self.x + x, self.y + y)
        
    def can_move(self, x, y=None):
        """Can the character move into this location?"""
        if type(x) == type(tuple()):
            x, y = x[0], x[1]
            
        can_move = True

        if x < 0 or y < 0 or x >= MAP_W or y >= MAP_H:
            can_move = False

        if GC.map[x][y].block_movement:
            can_move = False

        for mon in GC.monsters:
            if x == mon.x and y == mon.y:
                can_move = False
                break
            
        return can_move
            
        
    def move_randomly(self):
        direction = random.randrange(len(DIR))
        if self.can_move_dir(DIR[direction]):
            return self.move(DIR[direction])
        

class Monster(Object):
    """Anything that moves and acts under its own power.  Players and NPCs count as monsters.  Pretty much any Object that's not an Item."""
    
    def __init__(self, x, y, type, ai=None):
        Object.__init__(self, x, y, type)
        self.ai = ai
        
