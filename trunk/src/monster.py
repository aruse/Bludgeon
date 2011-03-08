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

def die_leave_corpse(m):
    message(m.name.capitalize() + ' dies!', GV.red)
    GC.monsters.remove(m)
    GC.map[m.x][m.y].monsters.remove(m)

    corpse = Item(m.x, m.y, 'corpse', prev_monster=m, oid=m.oid)
    GC.items.append(corpse)
    GC.map[m.x][m.y].items.append(corpse)


def player_death(m):
    message(m.name.capitalize() + ' dies!', GV.red)
    GC.monsters.remove(m)
    GC.map[m.x][m.y].monsters.remove(m)

    corpse = Item(m.x, m.y, 'corpse', prev_monster=m)
    GC.items.append(corpse)
    GC.map[m.x][m.y].items.append(corpse)
    
class Monster(Object):
    """Anything that moves and acts under its own power.  Players and
    NPCs count as monsters.  Pretty much any Object that's not an
    Item.
    """
    
    def __init__(self, x, y, name, oid=None, ai=None, hp=None, max_hp=None,
                 mp=None, max_mp=None, death=None, fov_radius=TORCH_RADIUS):
        Object.__init__(self, x, y, name, oid=oid)

        self.ai = ai
        if self.ai: # Let the AI component access its owner
            self.ai.owner = self
            
        self.blocks_sight = False
        self.blocks_movement = True
        self.fov_radius = fov_radius

        # Function to call when this monster dies
        self.death = None
        
        # Field of view map.
        self.fov_map = None

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
        if death is not None:
            self.death = death

        if max_hp is None:
            self.max_hp = self.hp
        else:
            self.max_hp = max_hp

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

    def drop(self, i):
        """Drop an item."""
        i.x, i.y = self.x, self.y
        self.inventory.remove(i)
        GC.items.append(i)
        GC.map[i.x][i.y].append(i)

        message('You dropped the ' + i.name + '.')

    def move(self, dx, dy=None):
        oldx, oldy = self.x, self.y
        if Object.move(self, dx, dy):
            # Let the map know that this monster has moved.
            if self != GC.u:
                GC.map[oldx][oldy].monsters.remove(self)
                GC.map[self.x][self.y].monsters.append(self)



class Player(Monster):
    def __init__(self, x, y, name, oid=None, ai=None, hp=None, max_hp=None,
                 mp=None, max_mp=None, death=None, fov_radius=TORCH_RADIUS):
        if death is None:
            death = player_death
        Monster.__init__(self, x, y, name, oid=oid, ai=ai, hp=hp, max_hp=max_hp,
                         mp=mp, max_mp=max_mp, death=death,
                         fov_radius=fov_radius)

    def attack(self, target):
        GC.cmd_history.append(('a', target.oid))
        Monster.attack(self, target)

    def move(self, dx, dy=None):
        GC.cmd_history.append(('m', dx, dy))
        Monster.move(self, dx, dy)

    def rest(self):
        self.move(0, 0)

    def pick_up(self, item):
        GC.cmd_history.append((',', item.oid))
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

