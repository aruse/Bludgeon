import random
import pygame
from pygame.locals import *

from const import *
from game import *
from util import *

class Object:
    """Generic object.  Can be sub-classed into players, monsters, items, etc."""
    def __init__(self, x, y, name):
        pygame.sprite.Sprite.__init__(self) # Call sprite initializer
        self.image = create_tile(name)
        self.rect = Rect(GV.map_x, GV.map_y, TILE_W, TILE_H)
        self.x = 0
        self.y = 0
        

    def can_move_dir(self, x, y=None):
        """Can the character move in this direction?"""
        # If we passed in a tuple instead of a pair of ints, convert to a pair of ints
        if type(x) == type(tuple()):
            y = x[1]
            x = x[0]

        return self.can_move(self.x + x, self.y + y)
        
    def can_move(self, x, y=None):
        """Can the character move into this location?"""
        # If we passed in a tuple instead of a pair of ints, convert to a pair of ints
        if type(x) == type(tuple()):
            y = x[1]
            x = x[0]

        if x >= 0 and y >= 0 and x < MAP_W and y < MAP_H and not is_blocked(x, y):
            return True
        else:
            return False
    
    def move_randomly(self):
        direction = random.randrange(len(DIR))
        if self.can_move_dir(DIR[direction]):
            return self.move(DIR[direction])
                             
    def move(self, dx, dy=None):
        """Move dx and dy spaces, if possible."""

        # If we passed in a tuple instead of a pair of ints, convert to a pair of ints
        if type(dx) == type(tuple()):
            dy = dx[1]
            dx = dx[0]
            
        if self.can_move_dir(dx, dy):
            self.x += dx
            self.y += dy
            self.rect = self.rect.move(dx * TILE_W, dy * TILE_H)
            return True
        else:
            return False
