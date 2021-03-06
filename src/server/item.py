# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

"""Item class"""

from server_state import ServerState as SS
from object import Object
import spell


class Item(Object):
    """
    Game items.  Anything that can be picked up.
    """

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
                self.use_function = spell.cast_heal
            elif self.name == 'scroll of fireball':
                self.use_function = spell.cast_fireball
            elif self.name == 'scroll of lightning':
                self.use_function = spell.cast_lightning
            elif self.name == 'scroll of confusion':
                self.use_function = spell.cast_confuse
            else:
                self.use_function = None
        else:
            self.use_function = use_function

    def place_on_map(self, amap=None):
        """Place the item object on the current game map."""
        if amap is None:
            amap = SS.map

        amap.items.append(self)
        amap.grid[self.x][self.y].items.append(self)

    def delete(self, dict_remove=False):
        """
        Remove map references to this Item.
        @param dict_remove: Also remove the Item from the object dictionary.
        """
        print 'in delete', self.oid
        SS.map.items.remove(self)
        SS.map.grid[self.x][self.y].items.remove(self)
        if dict_remove:
            del Object.obj_dict[self.oid]

        SS.items_to_delete.append((self.oid, dict_remove))

    def move(self, dx, dy=None):
        """Move item by dx, dy amounts."""
        oldx, oldy = self.x, self.y
        if Object.move(self, dx, dy):
            # Let the map know that this item has moved.
            SS.map.grid[oldx][oldy].items.remove(self)
            SS.map.grid[self.x][self.y].items.append(self)
            self.dirty = True

    def serialize(self):
        """
        Convert Item to a string, suitable for saving to a file.
        """
        # Need to trim off the trailing bracket from the Object serialization.
        obj = Object.serialize(self)[:-1]

        if self.use_function is None:
            use_function = None
        else:
            use_function = self.use_function.__name__

        item = "'use_function':{0},}}".format(repr(use_function))

        return obj + item

    def client_serialize(self):
        """
        Convert Item to a string, suitable for transmission to the client.
        Only include attributes which the client cares about.
        """
        # Need to trim off the trailing bracket from the Object serialization.
        obj = Object.client_serialize(self)[:-1]
        item = "}}".format()

        return obj + item
