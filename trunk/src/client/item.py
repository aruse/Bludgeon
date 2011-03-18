# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

import math

import pygame
from pygame.locals import *

from const import *
from client.client import Client as C
from client.object import *                    

class ClientItem(Object):
    """Game items to be displayed in the client."""

    def __init__(self, x, y, name, oid):
        Object.__init__(self, x, y, name, oid)
        self.blocks_sight = False
        self.blocks_movement = False
