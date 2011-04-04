# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

import math

import pygame
from pygame.locals import *

from const import *
from common import *
from fov import *
from client_state import ClientState as CS
from network import Network
from client_util import *
from client_object import ClientObject
from client_monster import ClientMonster
from gui import *


class ClientPlayer(ClientMonster):
    """Representation of the player character in the client."""

    @classmethod
    def unserialize(cls, u_str):
        """Unserialize a string, returning a ClientMonster object."""
        # Convert string to dict
        u_dict = eval(u_str)

        return ClientPlayer(
            u_dict['x'], u_dict['y'], u_dict['name'], u_dict['oid'],
            hp=u_dict['hp'], max_hp=u_dict['max_hp'],
            mp=u_dict['mp'], max_mp=u_dict['max_mp'],
            inventory=u_dict['inventory'])

    def __init__(self, x, y, name, oid, hp=None, max_hp=None,
                 mp=None, max_mp=None, fov_radius=TORCH_RADIUS,
                 inventory=[]):
        ClientMonster.__init__(self, x, y, name, oid, hp=hp,
                         max_hp=max_hp, mp=mp, max_mp=max_mp,
                         fov_radius=fov_radius, inventory=inventory)

    def attack(self, target):
        Network.request('F', (target.oid,))

    def move(self, dx, dy=None):
        dx, dy = flatten_args(dx, dy)
        Network.request('m', (dx, dy))

    def rest(self):
        self.move(0, 0)

    def try_move(self, dx, dy=None):
        """
        Try to move dx and dy spaces.  If there's a monster in the
        way, attack instead.
        """
        dx, dy = flatten_args(dx, dy)
        x = self.x + dx
        y = self.y + dy

        # Search for an attackable object.
        target = None
        for m in CS.map.grid[x][y].monsters:
            target = m

        # attack if target found, move otherwise
        if target is not None:
            self.attack(target)
        else:
            self.move(dx, dy)

    def update_from_string(self, u_str):
        """Update attributes from a serialized string."""
        # Convert string to dict
        u_dict = eval(u_str)
        old_x, old_y = self.x, self.y

        if 'x' in u_dict:
            self.x = u_dict['x']
        if 'y' in u_dict:
            self.y = u_dict['y']
        if 'name' in u_dict:
            self.name = u_dict['name']
        if 'hp' in u_dict:
            self.hp = u_dict['hp']
        if 'max_hp' in u_dict:
            self.max_hp = u_dict['max_hp']
        if 'mp' in u_dict:
            self.mp = u_dict['mp']
        if 'max_mp' in u_dict:
            self.max_mp = u_dict['max_mp']
        if 'inventory' in u_dict:
            self.inventory = u_dict['inventory']
            # Convert oids to Items
            for i in xrange(len(self.inventory)):
                self.inventory[i] = ClientObject.obj_dict[self.inventory[i]]
