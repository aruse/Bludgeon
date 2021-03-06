# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

"""Object class"""

import math

import common.cfg as cfg
from server_state import ServerState as SS
from common.common import flatten_args


class Object(object):
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
        dx, dy = flatten_args(dx, dy)
        self.dirty = True

        if self.can_move_dir(dx, dy):
            self.x += dx
            self.y += dy
            return True
        else:
            return False

    def move_to(self, x, y=None):
        """Move to (x, y), if possible."""
        x, y = flatten_args(x, y)
        self.dirty = True

        if self.can_move(x, y):
            self.x = x
            self.y = y
            return True
        else:
            return False

    def move_randomly(self):
        """Move one space in a random direction."""
        adir = SS.rand.randrange(len(cfg.DIR))
        if self.can_move_dir(cfg.DIR[adir]):
            self.move(cfg.DIR[adir])

    def move_towards(self, x, y=None):
        """Move towards the x, y coords, if possible."""
        x, y = flatten_args(x, y)
        dx = x - self.x
        dy = y - self.y

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
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def can_move_dir(self, x, y=None):
        """Can the object move in this direction?"""
        x, y = flatten_args(x, y)
        return self.can_move(self.x + x, self.y + y)

    def can_move(self, x, y=None):
        """Can the object move into this location?"""
        x, y = flatten_args(x, y)
        can_move = True

        if x < 0 or y < 0 or x >= SS.map.w or y >= SS.map.h:
            can_move = False

        if SS.map.grid[x][y].blocks_movement:
            can_move = False

        for mon in SS.map.grid[x][y].monsters:
            if mon.blocks_movement:
                can_move = False
                break

        if SS.u.x == x and SS.u.y == y:
            can_move = False

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
