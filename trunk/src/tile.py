import re

from const import *
from game import *
from util import *

class Tile:
    """Map tile, representing a single location on the map."""

    def __init__(self, type):
        self.type = type
        
        if re.findall('wall', type):
            self.block_movement = True
            self.block_sight = True
            self.tile_class = 'wall'
        else:
            self.block_movement = False
            self.block_sight = False
            self.tile_class = 'floor'

#        self.tile_class = tile_class_dict[type]
        self.tile = create_tile(type)
        
        # All tiles start unexplored
        self.explored = False
                
        # Which color to display in text mode
        self.color = None

        # Value from 0 to 1, indicating degree of illumination.
        self.illumination = None
        
        self.explored = False
        
    def dig():
        self.block_movement = False
        self.block_signt = False
