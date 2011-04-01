# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

import re

from const import *
from server_state import ServerState as SS
from cell import Cell


class Map(object):
    """
    Map of dungeon level, containing a grid of Cell objects.
    """

    def __init__(self, x, y, layout='connected_rooms'):
        # x and y dimensions, in cells
        self.x, self.y = x, y
        self.layout = layout

        # Lists of all items and monsters on this level.
        self.items = []
        self.monsters = []

        self.upstairs = None
        self.downstairs = None

        self.grid = [[Cell('cmap, wall, dark')
                      for y in xrange(self.y)]
                     for x in xrange(self.w)]
        self.rooms = []

        # Set to true if this map (not the individual cells) has been modified.
        self.dirty = True

        
