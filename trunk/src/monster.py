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
from gui import *

def die_leave_corpse(monster):
    message(monster.name.capitalize() + ' dies!', GV.red)
    GC.monsters.remove(monster)
    corpse = Item(monster.x, monster.y, 'corpse', prev_monster=monster)
    GC.items.append(corpse)
    
class Monster(Object):
    """Anything that moves and acts under its own power.  Players and
    NPCs count as monsters.  Pretty much any Object that's not an
    Item.
    """
    
    def __init__(self, x, y, name, oid=None, ai=None):
        Object.__init__(self, x, y, name, oid=oid)

        self.ai = ai
        if self.ai: # Let the AI component access its owner
            self.ai.owner = self
            
        self.blocks_sight = False
        self.blocks_movement = True

        # Function to call when this monster dies
        self.death = None
        
        # Field of view map.
        self.fov_map = None

        if name == 'wizard':
            self.hp = 30
            self.atk_power = 5
            self.defense = 2
            self.death = None
        elif name == 'orc':
            self.hp = 1
            self.atk_power = 1
            self.defense = 0
            self.death = die_leave_corpse
        elif name == 'troll':
            self.hp = 2
            self.atk_power = 2
            self.defense = 0
            self.death = die_leave_corpse

        self.max_hp = self.hp
        self.inventory = []
        
        # FIXME dummy values
        self.mp = 13
        self.max_mp = 25
        self.xp = 1220
        self.xp_next_level = 2000
        self.weight = 580
        self.burdened = 1000
        self.hunger = 450
        self.max_hunger = 1000

    def pick_up(self, item):
        self.inventory.append(item)
        GC.items.remove(item)
        message('You picked up a ' + item.name + '.', GV.green)

    def set_fov_map(self, map):
        self.fov_map = FOVMap(map)

    def attack(self, target):
        """Attack target with wielded weapon."""
        damage = self.atk_power - target.defense
 
        if damage > 0:
            message(self.name.capitalize() + ' attacks ' + target.name
                    + ' for ' + str(damage) + ' hit points.')
            target.take_damage(damage)
        else:
            message(self.name.capitalize() + ' attacks ' + target.name
                    + ' but it has no effect!')
 
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


    def targeted_use(self, item, x, y):
        """Use an item, targetted on the given coords."""
        item.use_function(item, x, y)
        self.inventory.remove(item)

    def use(self, item):
        """Use an item."""
        if item.use_function is None:
                message('The ' + item.name + ' cannot be used.')
        else:
            use_result = item.use_function(item)
            if use_result != 'cancelled' and use_result != 'targeting':
                # Destroy after use, but only if it was actually used.
                self.inventory.remove(item)
            return use_result

    def drop(self, item):
        """Drop an item."""
        item.x, item.y = self.x, self.y
        self.inventory.remove(item)
        GC.items.append(item)
        message('You dropped the ' + item.name + '.')


class Player(Monster):
    def __init__(self, x, y, name, oid=None):
        Monster.__init__(self, x, y, name, oid=oid)

    def attack(self, target):
        GC.cmd_history.append(('a', target.oid))
        Monster.attack(self, target)

    def move(self, dx, dy=None):
        GC.cmd_history.append(('m', dx, dy))
        Monster.move(self, dx, dy)
        center_map()

    def pick_up(self, item):
        GC.cmd_history.append(('p', item.oid))
        Monster.pick_up(self, item)

    def targeted_use(self, item, x, y):
        GC.cmd_history.append(('u', item.oid, x, y))
        Monster.targeted_use(self, item, x, y)

    def drop(self, item):
        GC.cmd_history.append(('d', item.oid))
        Monster.drop(self, item)

    def try_move(self, dx, dy=None):
        """Try to move dx and dy spaces.  If there's a monster in the
        way, attack instead.
        """
        if type(dx) == type(tuple()):
            dx, dy = dx[0], dx[1]

        # the coordinates the player is moving to/attacking
        x = self.x + dx
        y = self.y + dy

        # try to find an attackable object there
        target = None

        for m in GC.monsters:
            if m.x == x and m.y == y:
                target = m
                break

        # attack if target found, move otherwise
        if target is not None:
            self.attack(target)
        else:
            self.move(dx, dy)

