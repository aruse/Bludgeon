import re

from const import *
from game import *
from util import *


class Cell:
    """Map cell, representing a single location on the map."""

    def __init__(self, type):
        self.type = type
        
        if re.findall('wall', type):
            self.block_movement = True
            self.block_sight = True
            self.cell_class = 'wall'
        else:
            self.block_movement = False
            self.block_sight = False
            self.cell_class = 'floor'

#        self.cell_class = tile_class_dict[type]
        self.tile = create_tile(GV.tiles_img, type)
        self.gray_tile = create_tile(GV.gray_tiles_img, type)
        
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
