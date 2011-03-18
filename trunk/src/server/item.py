# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

import math

import pygame
from pygame.locals import *

from const import *
from server.server import Server as S
from util import *
from fov import *
from server.ai import *
from server.object import *                    

class Item(Object):
    """Game items.  Anything that can be picked up."""
    
    @classmethod
    def unserialize(cls, i_str):
        """Unserialize a string, returning an Item object."""
        # Convert string to dict
        i_dict = eval(i_str)

        if i_dict['use_function'] is None:
            use_function = None
        else:
            use_function = eval(i_dict['use_function'])

        return Item(
            i_dict['x'], i_dict['y'], i_dict['name'], oid=i_dict['oid'],
            use_function=use_function)


    def __init__(self, x, y, name, oid=None, use_function=None,
                 prev_monster=None):
        Object.__init__(self, x, y, name, oid=oid)
        self.blocks_sight = False
        self.blocks_movement = False

        # For items which were previously a monster.  Used for
        # resurrection, de-stoning, etc.
        self.prev_monster = prev_monster

        if use_function is None:
            if self.name == 'healing potion':
                self.use_function = cast_heal
            elif self.name == 'scroll of fireball':
                self.use_function = cast_fireball
            elif self.name == 'scroll of lightning':
                self.use_function = cast_lightning
            elif self.name == 'scroll of confusion':
                self.use_function = cast_confuse
            else:
                self.use_function = None
        else:
            self.use_function = use_function

    def move(self, dx, dy=None):
        """Move item by dx, dy amounts."""
        oldx, oldy = self.x, self.y
        if Object.move(self, dx, dy):
            # Let the map know that this item has moved.
            S.map[oldx][oldy].items.remove(self)
            S.map[self.x][self.y].items.append(self)

    def serialize(self):
        """Convert Item to a string, suitable for saving or network
        transmission.
        """
        # Need to trim off the trailing bracket from the Object serialization.
        o = Object.serialize(self)[:-1]

        if self.use_function is None:
            use_function = None
        else:
            use_function = self.use_function.__name__

        i = "'use_function':{0},}}".format(repr(use_function))

        return o + i
