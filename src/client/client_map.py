# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

"""ClientMap class"""

from client_cell import ClientCell


class ClientMap(object):
    """
    Map of dungeon level, containing a grid of CleintCell objects.
    """

    @classmethod
    def unserialize(cls, m_str):
        """
        Create a new ClientMap from a serialized string recieved from the
        server.
        """
        m_dict = eval(m_str)
        amap = ClientMap(m_dict['w'], m_dict['h'],
                         layout=m_dict['layout'], grid=m_dict['grid'])

        for x in xrange(amap.w):
            for y in xrange(amap.h):
                amap.grid[x][y] = ClientCell.unserialize(amap.grid[x][y])

        return amap

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
                          for j in xrange(self.h)]
                         for i in xrange(self.w)]
        self.rooms = []
