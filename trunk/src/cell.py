import re

from const import *
from game import *
from util import *


class Cell:
    """Map cell, representing a single location on the map."""

    def __init__(self, name):
        self.name = name
        
        if re.findall('wall', name):
            self.block_movement = True
            self.block_sight = True
            self.cell_class = 'wall'
        else:
            self.block_movement = False
            self.block_sight = False
            self.cell_class = 'floor'

#        self.cell_class = tile_class_dict[name]
        self.tile = create_tile(GV.tiles_img, name)
        self.gray_tile = create_tile(GV.gray_tiles_img, name)
        
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
