# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

"""Room class"""

class Room(object):
    """A room in the dungeon level."""
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        """Return the center coordinates of the room."""
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) / 2
        return (center_x, center_y)

    def intersect(self, room):
        """Returns whether or not this room intersects another one."""
        return (self.x1 <= room.x2 and self.x2 >= room.x1 and
                self.y1 <= room.y2 and self.y2 >= room.y1)
