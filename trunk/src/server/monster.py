# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

import math

import pygame
from pygame.locals import *

from const import *
from server import Server as S
from ai import *
from object import *                    
from item import *

from util import *
from fov import *

def die_leave_corpse(m):
    message(m.name.capitalize() + ' dies!', CLR['red'])
    m.delete()
    corpse = Item(m.x, m.y, 'corpse', prev_monster=m)
    corpse.place_on_map()

def player_death(m):
    message(m.name.capitalize() + ' dies!', CLR['red'])
    m.delete()
    corpse = Item(m.x, m.y, 'corpse', prev_monster=m)
    corpse.place_on_map()
    
class Monster(Object):
    """
    Anything that moves and acts under its own power.  Players and
    NPCs count as monsters.
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


    def place_on_map(self, map=None):
        """Place the monster object on the current game map."""
        if map is None:
            map = S.map

        S.monsters.append(self)
        map[self.x][self.y].monsters.append(self)

    def delete(self, dict_remove=False):
        """
        Remove map references to this Monster.
        @param dict_remove: Also remove the Monster from the object dictionary.
        """
        S.monsters.remove(self)
        S.map[self.x][self.y].monsters.remove(self)
        if dict_remove:
            del Object.obj_dict[self.oid]
            
        S.monsters_to_delete.append((self.oid, dict_remove))

    def pick_up(self, item):
        self.inventory.append(item)
        item.delete()
        message('You picked up a ' + item.name + '.', CLR['green'])
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
        i.place_on_map()
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
        """
        Convert Monster to a string, suitable for saving to a file.
        """
        # Need to trim off the trailing bracket from the Object serialization.
        o = Object.serialize(self)[:-1]

        if self.ai is None:
            ai = None
        else:
            ai = repr(self.ai.__class__.__name__)

        inventory = repr([i.oid for i in self.inventory])
        m = ("'hp':{0},'max_hp':{1},'mp':{2},'max_mp':{3},'ai':{4},"
             "'death':{5},'inventory':{6}}}".format(
                repr(self.hp), repr(self.max_hp), repr(self.mp),
                repr(self.max_mp), ai, repr(self.death.__name__), inventory))

        return o + m

    def client_serialize(self):
        """
        Convert Monster to a string, suitable for transmission to the client.
        Only include attributes which the client cares about.
        """
        # Need to trim off the trailing bracket from the Object serialization.
        o = Object.client_serialize(self)[:-1]

        inventory = repr([i.oid for i in self.inventory])
        m = ("'hp':{0},'max_hp':{1},'mp':{2},'max_mp':{3},"
             "'inventory':{4}}}".format(
                repr(self.hp), repr(self.max_hp), repr(self.mp),
                repr(self.max_mp), inventory))

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

    def attack(self, target):
        Monster.attack(self, Object.obj_dict[target])

    def rest(self):
        self.move(0, 0)

    def targeted_use(self, item, x, y):
        S.cmd_history.append(('u', item.oid, x, y))
        Monster.targeted_use(self, item, x, y)

    def drop(self, item):
        Monster.drop(self, Object.obj_dict[item])


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
