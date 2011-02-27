import random
import math

import pygame
from pygame.locals import *

from const import *
from game import *
from util import *
from mon_class import *
from fov import *
from ai import *
from object import *                    
from item import *

def die_leave_corpse(monster):
    message(monster.name.capitalize() + ' dies!')
    GC.monsters.pop(GC.monsters.index(monster))
    corpse = Item(monster.x, monster.y, 'corpse', prev_monster=monster)
    GC.items.append(corpse)
    
class Monster(Object):
    """Anything that moves and acts under its own power.  Players and NPCs count as monsters.  Pretty much any Object that's not an Item."""
    
    def __init__(self, x, y, name, ai=None):
        Object.__init__(self, x, y, name)
        self.ai = ai
        if self.ai: # Let the AI component access its owner
            self.ai.owner = self
            
        self.blocks_sight = False
        self.blocks_movement = True

        # Function to call when this monster dies
        self.death = die_leave_corpse
        
        # Field of view map.
        self.fov_map = None

        if name == 'wizard':
            self.hp = 30
            self.atk_power = 5
            self.defense = 2
        elif name == 'orc':
            self.hp = 10
            self.atk_power = 3
            self.defense = 0
        elif name == 'troll':
            self.hp = 16
            self.atk_power = 4
            self.defense = 1

        self.max_hp = self.hp

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

    def attack(self, target):
        """Attack target with wielded weapon."""
        damage = self.atk_power - target.defense
 
        if damage > 0:
            message(self.name.capitalize() + ' attacks ' + target.name +
                    ' for ' + str(damage) + ' hit points.')
            target.take_damage(damage)
        else:
            message(self.name.capitalize() + ' attacks ' + target.name + ' but it has no effect!')
 
    def take_damage(self, damage):
        if damage > 0:
            self.hp -= damage
 
            # If dead, call death function
            if self.hp <= 0:
                self.death(self)
 
    def heal(self, amount):
        #heal by the given amount, without going over the maximum
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp

        
    def try_move(self, dx, dy=None):
        """Try to move dx and dy spaces.  If there's a monster in the way, attack instead."""
        if type(dx) == type(tuple()):
            dx, dy = dx[0], dx[1]

        # the coordinates the player is moving to/attacking
        x = self.x + dx
        y = self.y + dy

        # try to find an attackable object there
        target = None

        for o in GC.monsters:
            if o.x == x and o.y == y:
                target = o
                break

        # attack if target found, move otherwise
        if target is not None:
            self.attack(target)
        else:
            self.move(dx, dy)
