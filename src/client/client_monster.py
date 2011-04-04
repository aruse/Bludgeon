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
from gui import *


class ClientMonster(ClientObject):
    """Monster representation for the client."""

    @classmethod
    def unserialize(cls, m_str):
        """Unserialize a string, returning a ClientMonster object."""
        # Convert string to dict
        m_dict = eval(m_str)

        return ClientMonster(
            m_dict['x'], m_dict['y'], m_dict['name'], m_dict['oid'],
            hp=m_dict['hp'], max_hp=m_dict['max_hp'],
            mp=m_dict['mp'], max_mp=m_dict['max_mp'],
            inventory=m_dict['inventory'])

    def __init__(self, x, y, name, oid, hp=None, max_hp=None,
                 mp=None, max_mp=None, fov_radius=TORCH_RADIUS,
                 inventory=[]):
        ClientObject.__init__(self, x, y, name, oid)

        self.blocks_sight = False
        self.blocks_movement = True
        self.fov_radius = fov_radius

        # Field of view map.
        self.fov_map = None

        # FIXME: this should be loaded from a database
        if name == 'wizard':
            if hp is None:
                self.hp = 30
            self.atk_power = 5
            self.defense = 2
        elif name == 'orc':
            if hp is None:
                self.hp = 1
            self.atk_power = 1
            self.defense = 0
        elif name == 'troll':
            if hp is None:
                self.hp = 10
            self.atk_power = 2
            self.defense = 0

        if hp is not None:
            self.hp = hp

        if max_hp is None:
            self.max_hp = self.hp
        else:
            self.max_hp = max_hp

        self.inventory = inventory

        # FIXME dummy values
        self.mp = 13
        self.max_mp = 25
        self.xp = 1220
        self.xp_next_level = 2000
        self.weight = 580
        self.burdened = 1000
        self.hunger = 450
        self.max_hunger = 1000

    def place_on_map(self, map=None):
        """Place the monster object on the current game map."""
        if map is None:
            map = CS.map

        CS.map.monsters.append(self)
        map.grid[self.x][self.y].monsters.append(self)

    def delete(self, dict_remove=False):
        """
        Remove map references to this Monster.
        @param dict_remove: Also remove the Monster from the object dictionary.
        """
        CS.map.monsters.remove(self)
        CS.map.grid[self.x][self.y].monsters.remove(self)
        if dict_remove:
            del ClientObject.obj_dict[self.oid]

    def set_fov_map(self, map):
        self.fov_map = FOVMap(map)

    def update_from_string(self, m_str):
        """Update attributes from a serialized string."""
        # Convert string to dict
        m_dict = eval(m_str)
        old_x, old_y = self.x, self.y

        if 'x' in m_dict:
            self.x = m_dict['x']
        if 'y' in m_dict:
            self.y = m_dict['y']
        if 'name' in m_dict:
            self.name = m_dict['name']
        if 'hp' in m_dict:
            self.hp = m_dict['hp']
        if 'max_hp' in m_dict:
            self.max_hp = m_dict['max_hp']
        if 'mp' in m_dict:
            self.mp = m_dict['mp']
        if 'max_mp' in m_dict:
            self.max_mp = m_dict['max_mp']
        if 'inventory' in m_dict:
            self.inventory = m_dict['inventory']
            # Convert oids to Items
            for i in xrange(len(self.inventory)):
                self.inventory[i] = ClientObject.obj_dict[self.inventory[i]]
        if 'blocks_sight' in m_dict:
            self.blocks_sight = m_dict['blocks_sight']
        if 'blocks_movement' in m_dict:
            self.blocks_movement = m_dict['blocks_movement']

        if self in CS.map.grid[old_x][old_y].monsters:
            CS.map.grid[old_x][old_y].monsters.remove(self)
        if self not in CS.map.grid[self.x][self.y].monsters:
            CS.map.grid[self.x][self.y].monsters.append(self)
        if self not in CS.map.monsters:
            CS.map.monsters.append(self)
