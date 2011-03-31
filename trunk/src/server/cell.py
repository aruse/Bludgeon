# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

import re

from const import *
from server import Server as S
from util import *


class Cell:
    """
    Map cell, representing a single location on the map.
    """

    def __init__(self, name, explored=False):
        self.set_attr(name)
        self.explored = explored

        # Monsters and items in this cell
        self.monsters = []
        self.items = []
        
        # Set to true if this cell has been modified.
        self.dirty = True

    def set_attr(self, name):
        """
        Set cell attributes.

        @param name: Name of this cell.  Used as a key to look up attributes.
        """
        self.name = name
        
        # FIXME: this is just dummy code.
        # Need a real database of tiles to load from.
        if re.findall('wall', name):
            self.blocks_movement = True
            self.blocks_sight = True
            self.kind = 'wall'
        else:
            self.blocks_movement = False
            self.blocks_sight = False
            self.kind = 'floor'

