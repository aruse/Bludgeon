# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

"""Player class"""

import common.cfg as cfg
from common.color import CLR
from util import message
from server_state import ServerState as SS
from object import Object
from monster import Monster
from item import Item


def player_death(mon):
    """Take care of everything that happens when the player dies."""
    message(mon.name.capitalize() + ' dies!', CLR['red'])
    mon.delete()
    corpse = Item(mon.x, mon.y, 'corpse', prev_monster=mon)
    corpse.place_on_map()


class Player(Monster):
    """Representation of the player character."""

    @classmethod
    def unserialize(cls, u_str):
        """Unserialize a string, returning a Player object."""
        # Convert string to dict
        u_dict = eval(u_str)

        if u_dict['ai'] is not None:
            u_dict['ai'] = eval(u_dict['ai'])()

        return Player(
            u_dict['x'], u_dict['y'], u_dict['name'], oid=u_dict['oid'],
            ai=u_dict['ai'], hp=u_dict['hp'], max_hp=u_dict['max_hp'],
            mp=u_dict['mp'], max_mp=u_dict['max_mp'],
            death=eval(u_dict['death']), inventory=u_dict['inventory'])

    def __init__(self, x, y, name, oid=None, ai=None, hp=None, max_hp=None,
                 mp=None, max_mp=None, death=None, fov_radius=cfg.TORCH_RADIUS,
                 inventory=None):
        if death is None:
            death = player_death
        Monster.__init__(self, x, y, name, oid=oid, ai=ai, hp=hp,
                         max_hp=max_hp, mp=mp, max_mp=max_mp, death=death,
                         fov_radius=fov_radius, inventory=inventory)

    def attack(self, target):
        """Attack the target."""
        Monster.attack(self, Object.obj_dict[target])

    def rest(self):
        """Rest for a turn."""
        self.move(0, 0)

    def targeted_use(self, item, x, y):
        """Use an item on the given (x, y) coords."""
        SS.cmd_history.append(('u', item.oid, x, y))
        Monster.targeted_use(self, item, x, y)

    def drop(self, item):
        """Drop an item."""
        item = Object.obj_dict[item]
        Monster.drop(self, item)
        message('You dropped the ' + item.name + '.')

    def serialize(self):
        """
        Convert Player object to a string, suitable for saving to a file.
        """
        return Monster.serialize(self)

    def client_serialize(self):
        """
        Convert Player to a string, suitable for transmission to the client.
        Only include attributes which the client cares about.
        """
        return Monster.client_serialize(self)

    def use(self, item):
        """Use an item."""
        if item.use_function is None:
            message('The ' + item.name + ' cannot be used.')

#        elif needs target:
#            pass
#        elif needs direction:
#            pass
#        else:
#            doesn't need any other input
