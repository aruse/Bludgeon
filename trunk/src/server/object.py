# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

import random
import math

import pygame
from pygame.locals import *

from const import *
from server import Server as S
from ai import *

from util import *
from fov import *

class Object:
    """
    Generic object.  Can be sub-classed into players, monsters,
    items, etc.
    """
    # Keeps track of the oid of the next object to be created
    oid_seq = 1

    # Mapping of oids to objects
    obj_dict = {}

    def __init__(self, x, y, name, oid=None):
        if oid:
            self.oid = oid
        else:
            self.oid = Object.oid_seq
            Object.oid_seq += 1

        Object.obj_dict[self.oid] = self

        # What kind of object is this?  e.g. "potion"
        self.kind = None
        # What spedific object is this?  e.g. "potion of confusion"
        self.name = name
        # The name to display to the player
        self.display_name = name

        self.x = x
        self.y = y

        # Which color to display in text mode
        self.color = None

        self.blocks_sight = False
        self.blocks_movement = False

        # Set to true if this object has been modified.
        self.dirty = True

        # Set to true to delete.  This won't actually happen until after the
        # client is informed.
        self.delete_me = False
        
    def move(self, dx, dy=None):
        """Move dx and dy spaces, if possible."""
        if type(dx) == type(tuple()):
            dx, dy = dx[0], dx[1]

        self.dirty = True
            
        if self.can_move_dir(dx, dy):
            self.x += dx
            self.y += dy
            return True
        else:
            return False

    def move_randomly(self):
        dir = S.rand.randrange(len(DIR))
        if self.can_move_dir(DIR[dir]):
            self.move(DIR[dir])

    def move_towards(self, x, y=None):
        """Move towards the x, y coords, if possible."""
        if type(x) == type(tuple()):
            x, y = x[0], x[1]

        dx = x - self.x
        dy = y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
 
        # Normalize the distance to length 1 (preserving direction), then 
        # convert it to a movment direction.
        if dx > 0:
            x = 1
        elif dx < 0:
            x = -1
        else:
            x = 0

        if dy > 0:
            y = 1
        elif dy < 0:
            y = -1
        else:
            y = 0

        if self.can_move_dir(x, y):
            self.move(x, y)
        # If we can't move in the direction we want to, then try to
        # move vertically or horizontally
        else:
            if self.can_move_dir(x, 0):
                self.move(x, 0)
            else:
                self.move(0, y)

    def distance_to(self, obj):
        """Distance to another object."""
        return self.distance(obj.x, obj.y)

    def distance(self, x, y):
        """Distance to coords."""
        if type(x) == type(tuple()):
            x, y = x[0], x[1]
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def can_move_dir(self, x, y=None):
        """Can the object move in this direction?"""
        if type(x) == type(tuple()):
            x, y = x[0], x[1]
            
        return self.can_move(self.x + x, self.y + y)
        
    def can_move(self, x, y=None):
        """Can the object move into this location?"""
        if type(x) == type(tuple()):
            x, y = x[0], x[1]
            
        can_move = True

        if x < 0 or y < 0 or x >= MAP_W or y >= MAP_H:
            can_move = False

        if S.map[x][y].blocks_movement:
            can_move = False

        for m in S.monsters + [S.u]:
            if x == m.x and y == m.y:
                can_move = False
                break
            
        return can_move

    def serialize(self):
        """
        Convert Object to a string, suitable for saving to a file.
        """
        return ("{{'oid':{0},'x':{1},'y':{2},'name':{3},'blocks_sight':{4},"
                "'blocks_movement':{5},}}".format(
                repr(self.oid), repr(self.x), repr(self.y), repr(self.name),
                repr(self.blocks_sight), repr(self.blocks_movement)))

    def client_serialize(self):
        """
        Convert Object to a string, suitable for transmission to the client.
        Only include attributes which the client cares about.
        """
        return Object.serialize(self)
