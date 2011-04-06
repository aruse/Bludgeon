# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

"""ClientCell class"""

import re

from client_state import ClientState as CS
from client_util import cell2pixel


class ClientCell(object):
    """
    Map cell, representing a single location on the map to be displayed
    in the client.
    """

    @classmethod
    def unserialize(cls, c_str):
        """
        Create a new ClientCell from a serialized string recieved from the
        server.
        """
        c_dict = eval(c_str)
        return ClientCell(c_dict['name'], explored=c_dict['explored'])

    def __init__(self, name, explored=False):
        self.kind = None
        self.name = None
        self.blocks_movement = False
        self.blocks_sight = False
        self.tile = None
        self.set_attr(name)

        self.explored = explored

        # Value from 0 to 1, indicating degree of illumination.
        self.illumination = None

        # Monsters and items in this cell
        self.monsters = []
        self.items = []

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

        self.tile = CS.tile_dict[name]

    def draw(self, x, y):
        """Draw this Cell on the map at the given coords."""
        CS.map_surf.blit(CS.tiles_img, cell2pixel(x, y), self.tile)

    def draw_gray(self, x, y):
        """Draw this Cell on the map at the given coords, grayed out."""
        CS.map_surf.blit(CS.gray_tiles_img, cell2pixel(x, y), self.tile)
