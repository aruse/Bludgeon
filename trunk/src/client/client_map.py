# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

import re

from const import *
from client_state import ClientState as CS
from client_cell import ClientCell
#from room import Room
#from monster import Monster
#from item import Item
#from ai import *

class ClientMap(object):
    """
    Map of dungeon level, containing a grid of CleintCell objects.
    """

    def __init__(self, w, h, layout='connected_rooms'):
        self.w, self.h = w, h
        self.layout = layout

        # Lists of all items and monsters on this level.
        self.items = []
        self.monsters = []

        self.upstairs = None
        self.downstairs = None

        self.grid = [[ClientCell('cmap, wall, dark')
                      for y in xrange(self.h)]
                     for x in xrange(self.w)]
        self.rooms = []
