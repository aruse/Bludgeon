# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

import math

import pygame
from pygame.locals import *

from const import *
from client import Client as C
from network import Network
from util import *
from fov import *
from client_object import *                    
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

        if self.x != old_x or self.y != old_y:
            C.map[old_x][old_y].monsters.remove(self)
            C.map[self.x][self.y].monsters.append(self)

class ClientPlayer(ClientMonster):
    """Representation of the player character in the client."""

    def __init__(self, x, y, name, oid, hp=None, max_hp=None,
                 mp=None, max_mp=None, fov_radius=TORCH_RADIUS,
                 inventory=[]):
        ClientMonster.__init__(self, x, y, name, oid, hp=hp,
                         max_hp=max_hp, mp=mp, max_mp=max_mp,
                         fov_radius=fov_radius, inventory=inventory)

    def attack(self, target):
        Network.request('F', (target.oid))

    def move(self, dx, dy=None):
        Network.request('m', (dx, dy))

    def rest(self):
       self.move(0, 0)

    def try_move(self, dx, dy=None):
        """
        Try to move dx and dy spaces.  If there's a monster in the
        way, attack instead.
        """
        if type(dx) == type(tuple()):
            dx, dy = dx[0], dx[1]

        x = self.x + dx
        y = self.y + dy

        # Search for an attackable object.
        target = None
        for m in C.map[x][y].monsters:
            print m.x, m.y, m.oid
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
