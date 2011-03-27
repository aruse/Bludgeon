# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

import math

import pygame
from pygame.locals import *

from const import *
from client import Client as C
from client_object import *                    

class ClientItem(ClientObject):
    """Game items to be displayed in the client."""

    @classmethod
    def unserialize(cls, i_str):
        """Unserialize a string, returning a ClientItem object."""
        # Convert string to dict
        i_dict = eval(i_str)

        return ClientItem(
            i_dict['x'], i_dict['y'], i_dict['name'], i_dict['oid'])

    def __init__(self, x, y, name, oid):
        ClientObject.__init__(self, x, y, name, oid)
        self.blocks_sight = False
        self.blocks_movement = False
