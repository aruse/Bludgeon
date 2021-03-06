# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

"""ClientItem class"""

from client_state import ClientState as CS
from client_object import ClientObject


class ClientItem(ClientObject):
    """Game item to be displayed in the client."""

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

    def place_on_map(self, amap=None):
        """Place the item object on the current game map."""
        if amap is None:
            amap = CS.map

        CS.map.items.append(self)
        amap.grid[self.x][self.y].items.append(self)

    def delete(self, dict_remove=False):
        """
        Remove map references to this Item.
        @param dict_remove: Also remove the Item from the object dictionary.
        """
        CS.map.items.remove(self)
        CS.map.grid[self.x][self.y].items.remove(self)
        if dict_remove:
            del ClientObject.obj_dict[self.oid]

    def update_from_string(self, i_str):
        """Update attributes from a serialized string."""
        # Convert string to dict
        i_dict = eval(i_str)
        old_x, old_y = self.x, self.y

        if 'x' in i_dict:
            self.x = i_dict['x']
        if 'y' in i_dict:
            self.y = i_dict['y']
        if 'name' in i_dict:
            self.name = i_dict['name']
        if 'blocks_sight' in i_dict:
            self.blocks_sight = i_dict['blocks_sight']
        if 'blocks_movement' in i_dict:
            self.blocks_movement = i_dict['blocks_movement']

        if self in CS.map.grid[old_x][old_y].items:
            CS.map.grid[old_x][old_y].items.remove(self)
        if self not in CS.map.grid[self.x][self.y].items:
            CS.map.grid[self.x][self.y].items.append(self)
        if self not in CS.map.items:
            CS.map.items.append(self)
