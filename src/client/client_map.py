# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

import re

from const import *
from client_state import ClientState as CS
from client_cell import ClientCell


class ClientMap(object):
    """
    Map of dungeon level, containing a grid of CleintCell objects.
    """

    @classmethod
    def unserialize(cls, m_str):
        m_dict = eval(m_str)
        map = ClientMap(m_dict['w'], m_dict['h'], layout=m_dict['layout'], grid=m_dict['grid'])

        for x in xrange(map.w):
            for y in xrange(map.h):
                map.grid[x][y] = ClientCell.unserialize(map.grid[x][y])

        return map

    def __init__(self, w, h, layout='connected_rooms', grid=None):
        self.w, self.h = w, h
        self.layout = layout

        # Lists of all items and monsters on this level.
        self.items = []
        self.monsters = []

        self.upstairs = None
        self.downstairs = None

        if grid:
            self.grid = grid
        else:
            self.grid = [[ClientCell('cmap, wall, dark')
                          for y in xrange(self.h)]
                         for x in xrange(self.w)]
        self.rooms = []
