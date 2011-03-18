# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

import math

import pygame
from pygame.locals import *

from const import *
from server import Server as S
from util import *
from fov import *
from ai import *
from object import *                    
from item import *
from gui import *

def die_leave_corpse(m):
    message(m.name.capitalize() + ' dies!', S.red)
    S.monsters.remove(m)
    S.map[m.x][m.y].monsters.remove(m)

    corpse = Item(m.x, m.y, 'corpse', prev_monster=m, oid=m.oid)
    S.items.append(corpse)
    S.map[m.x][m.y].items.append(corpse)


def player_death(m):
    message(m.name.capitalize() + ' dies!', S.red)
    S.monsters.remove(m)
    S.map[m.x][m.y].monsters.remove(m)

    corpse = Item(m.x, m.y, 'corpse', prev_monster=m)
    S.items.append(corpse)
    S.map[m.x][m.y].items.append(corpse)
    
class Monster(Object):
    """Anything that moves and acts under its own power.  Players and
    NPCs count as monsters.  Pretty much any Object that's not an
    Item.
    """

    @classmethod
    def unserialize(cls, m_str):
        """Unserialize a string, returning a Monster object."""
        # Convert string to dict
        m_dict = eval(m_str)

        return Monster(
            m_dict['x'], m_dict['y'], m_dict['name'], oid=m_dict['oid'], 
            ai=eval(m_dict['ai'])(), hp=m_dict['hp'], max_hp=m_dict['max_hp'],
            mp=m_dict['mp'], max_mp=m_dict['max_mp'],
            death=eval(m_dict['death']))

    
    def __init__(self, x, y, name, oid=None, ai=None, hp=None, max_hp=None,
                 mp=None, max_mp=None, death=None, fov_radius=TORCH_RADIUS,
                 inventory=[]):
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

    def pick_up(self, item):
        self.inventory.append(item)
        S.items.remove(item)
        S.map[item.x][item.y].items.remove(item)
        message('You picked up a ' + item.name + '.', S.green)
        self.dirty = True

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

        self.dirty = True
 
    def take_damage(self, damage):
        if damage > 0:
            self.hp -= damage
 
            # If dead, call death function
            if self.hp <= 0:
                self.death(self)

            self.dirty = True

    def heal(self, amount):
        #heal by the given amount, without going over the maximum
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp

        self.dirty = True

    def targeted_use(self, item, x, y):
        """Use an item, targetted on the given coords."""
        item.use_function(item, x, y)
        self.inventory.remove(item)
        del Object.obj_dict[item.oid]
        self.dirty = True

    def use(self, item):
        """Use an item."""

        if item.use_function is None:
            message('The ' + item.name + ' cannot be used.')
        else:
            use_result = item.use_function(item)
            if use_result != 'cancelled' and use_result != 'targeting':
                # Destroy after use, but only if it was actually used.
                self.inventory.remove(item)
                del Object.obj_dict[item.oid]
                self.dirty = True
            return use_result

    def drop(self, i):
        """Drop an item."""
        i.x, i.y = self.x, self.y
        self.inventory.remove(i)
        S.items.append(i)
        S.map[i.x][i.y].items.append(i)
        message('You dropped the ' + i.name + '.')
        self.dirty = True

    def move(self, dx, dy=None):
        oldx, oldy = self.x, self.y
        if Object.move(self, dx, dy):
            # Let the map know that this monster has moved.
            if self != S.u:
                S.map[oldx][oldy].monsters.remove(self)
                S.map[self.x][self.y].monsters.append(self)

    def serialize(self):
        """Convert Monster to a string, suitable for saving or network
        transmission.
        """
        # Need to trim off the trailing bracket from the Object serialization.
        o = Object.serialize(self)[:-1]

        inventory = repr([i.oid for i in self.inventory])
        if self.ai is None:
            ai = None
        else:
            ai = repr(self.ai.__class__.__name__)

        m = ("'hp':{0},'max_hp':{1},'mp':{2},'max_mp':{3},'ai':{4},"
             "'death':{5},'inventory':{6}}}".format(
                repr(self.hp), repr(self.max_hp), repr(self.mp),
                repr(self.max_mp), ai, repr(self.death.__name__), inventory))

        return o + m


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
                 mp=None, max_mp=None, death=None, fov_radius=TORCH_RADIUS,
                 inventory=[]):
        if death is None:
            death = player_death
        Monster.__init__(self, x, y, name, oid=oid, ai=ai, hp=hp,
                         max_hp=max_hp, mp=mp, max_mp=max_mp, death=death,
                         fov_radius=fov_radius, inventory=inventory)

    def attack(self, target, server=False):
        # This is a hack necessary because I haven't split the client Player from the server Player yet.  When I separate them, I won't need the "server" variable any more.
        if server:
            Monster.attack(self, Object.obj_dict[target])
        else:
            request('F', (target.oid, True))
#        S.cmd_history.append(('a', target.oid))

    def move(self, dx, dy=None, server=False):
        # This is a hack necessary because I haven't split the client Player from the server Player yet.  When I separate them, I won't need the "server" variable any more.
        if server:
            Monster.move(self, dx, dy)
        else:
            request('m', (dx, dy, True))

    def rest(self):
        self.move(0, 0)

    def pick_up(self, item):
#        S.cmd_history.append((',', item.oid))
        Monster.pick_up(self, item)

    def targeted_use(self, item, x, y):
        S.cmd_history.append(('u', item.oid, x, y))
        Monster.targeted_use(self, item, x, y)

    def drop(self, item):
        
#        S.cmd_history.append(('d', item.oid))
        Monster.drop(self, Object.obj_dict[item])

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

        for m in S.monsters:
            if m.x == x and m.y == y:
                target = m
                break

        # attack if target found, move otherwise
        if target is not None:
            self.attack(target)
        else:
            self.move(dx, dy)

    def serialize(self):
        """Convert Player object to a string, suitable for saving or network
        transmission.
        """
        return Monster.serialize(self)

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
