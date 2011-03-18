# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

import re

from const import *
from server.server import Server as S
from util import *


class Cell:
    """Map cell, representing a single location on the map."""

    def __init__(self, name, explored=False):
        self.set_name_attr(name)
        self.explored = explored

        # Monsters and items in this cell
        self.monsters = []
        self.items = []
        
        # Set to true if this cell has been modified in any way and needs
        # to be updated in the Client.
        self.dirty = True

    def set_name_attr(self, name):
        """Set cell attributes that are dependent on the name."""
        self.name = name
        
        # FIXME: this is just dummy code.
        # Need a real database of tiles to load from.
        if re.findall('wall', name):
            self.blocks_movement = True
            self.block_sight = True
            self.kind = 'wall'
        else:
            self.blocks_movement = False
            self.block_sight = False
            self.kind = 'floor'

