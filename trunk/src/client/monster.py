# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

import math

import pygame
from pygame.locals import *

from const import *
from client.client import Client as C
from util import *
from fov import *
from client.object import *                    
from client.gui import *

class ClientMonster(Object):
    """Monster represntation for the client."""

    def __init__(self, x, y, name, oid=None, hp=None, max_hp=None,
                 mp=None, max_mp=None, fov_radius=TORCH_RADIUS,
                 inventory=[]):
        Object.__init__(self, x, y, name, oid)

        self.blocks_sight = False
        self.blocks_movement = True
        self.fov_radius = fov_radius

        # Field of view map.
        self.fov_map = None

        # FIXME: this should be loaded from a database
        if name == 'wizard':
            if hp is None:
                self.hp = 30
            if death is None:
                self.death = None
            self.atk_power = 5
            self.defense = 2
        elif name == 'orc':
            if hp is None:
                self.hp = 1
            if death is None:
                self.death = die_leave_corpse
            self.atk_power = 1
            self.defense = 0
        elif name == 'troll':
            if hp is None:
                self.hp = 10
            if death is None:
                self.death = die_leave_corpse
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


class CleintPlayer(Monster):
    """Representation of the player character in the client."""

    def __init__(self, x, y, name, oid, hp=None, max_hp=None,
                 mp=None, max_mp=None, fov_radius=TORCH_RADIUS,
                 inventory=[]):
        Monster.__init__(self, x, y, name, oid, hp=hp,
                         max_hp=max_hp, mp=mp, max_mp=max_mp,
                         fov_radius=fov_radius, inventory=inventory)

    def attack(self, target):
        request('F', (target.oid, True))

    def move(self, dx, dy=None):
        request('m', (dx, dy, True))
