import re

from const import *
from game import *
from util import *


class Cell:
    """Map cell, representing a single location on the map."""

    def __init__(self, name, explored=False):
        self.name = name
        
        self.set_tile(name)

        # All tiles start unexplored
        self.explored = explored
                
        # Which color to display in text mode
        self.color = None

        # Value from 0 to 1, indicating degree of illumination.
        self.illumination = None
        

    def set_tile(self, name):
        self.name = name
        
        # FIXME: this is just dummy code.  Need a real database of tiles to load from.
        if re.findall('wall', name):
            self.blocks_movement = True
            self.block_sight = True
            self.cell_class = 'wall'
        else:
            self.blocks_movement = False
            self.block_sight = False
            self.cell_class = 'floor'

#        self.cell_class = tile_class_dict[name]
        self.tile = GV.tile_dict[name]
        
        
    def dig():
        self.blocks_movement = False
        self.block_signt = False
