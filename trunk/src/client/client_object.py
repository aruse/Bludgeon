# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

import random
import math

import pygame
from pygame.locals import *

from const import *
from client_state import ClientState as CS
from client_util import *
from fov import *
from common import *

class ClientObject(object):
    """
    Generic object to be displayed in the client.  Base class for Item
    and Monster.
    """

    # Mapping of oids to objects
    obj_dict = {}

    def __init__(self, x, y, name, oid):
        self.oid = oid
        ClientObject.obj_dict[self.oid] = self

        # What kind of object is this?  e.g. "potion"
        self.kind = None
        # What spedific object is this?  e.g. "potion of confusion"
        self.name = name
        # The name to display to the player
        self.display_name = name

        self.x = x
        self.y = y

        self.tile = CS.tile_dict[name]
        
        # Which color to display in text mode
        self.color = None

        self.blocks_sight = False
        self.blocks_movement = False
        
    def distance_to(self, obj):
        """Distance to another object."""
        return self.distance(obj.x, obj.y)

    def distance(self, x, y):
        """Distance to coords."""
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def draw(self):
        """Draw this Object on the map at the current location."""
        CS.map_surf.blit(CS.tiles_img,
                         cell2pixel(self.x, self.y),
                         self.tile)
 
    def draw_gray(self):
        """Draw this Object on the map at the current location, grayed out."""
        CS.map_surf.blit(CS.gray_tiles_img,
                         cell2pixel(self.x, self.y),
                         self.tile)

    def can_move_dir(self, x, y=None):
        """Can the character move in this direction?"""
        x, y = flatten_args(x, y)
        return self.can_move(self.x + x, self.y + y)
        
    def can_move(self, x, y=None):
        """Can the object move into this location?"""
        x, y = flatten_args(x, y)
        can_move = True

        if x < 0 or y < 0 or x >= len(CS.map) or y >= len(CS.map[0]):
            can_move = False

        if S.map[x][y].blocks_movement:
            can_move = False

        for m in S.monsters + [S.u]:
            if x == m.x and y == m.y:
                can_move = False
                break
            
        return can_move
