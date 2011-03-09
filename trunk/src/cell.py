# Copyright (c) 2011, Andy Ruse

import re

from const import *
from game import *
from util import *


class Cell:
    """Map cell, representing a single location on the map."""

    def __init__(self, name, explored=False):
        self.set_tile(name)

        # All tiles start unexplored
        self.explored = explored
                
        # Which color to display in text mode
        self.color = None

        # Value from 0 to 1, indicating degree of illumination.
        self.illumination = None

        # Monsters and items in this cell
        self.monsters = []
        self.items = []
        

    def set_tile(self, name):
        self.name = name
        
        # FIXME: this is just dummy code.
        # Need a real database of tiles to load from.
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
        
    def draw(self, x, y):
        """Draw this Cell on the map at the given coords."""
        # Remember to offset by 1 tile so that there's room
        # for the border.
        GV.map_surf.blit(GV.tiles_img,
                         cell2pixel(x, y),
                         self.tile)
 
    def draw_gray(self, x, y):
        """Draw this Cell on the map at the given coords, grayed out."""
        GV.map_surf.blit(GV.gray_tiles_img,
                         ((x + 1) * TILE_W, (y + 1) * TILE_H),
                         self.tile)
