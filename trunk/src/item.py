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
from monster import *
from gui import *

# FIXME: dummy values
HEAL_AMOUNT = 4
LIGHTNING_DAMAGE = 20
LIGHTNING_RANGE = 5
CONFUSE_RANGE = 8
CONFUSE_NUM_TURNS = 10
FIREBALL_RADIUS = 3
FIREBALL_DAMAGE = 12



def cast_heal():
    if GC.u.hp == GC.u.max_hp:
        message('You are already at full health.', GV.light_violet)
        return 'cancelled'
 
    message('Your wounds start to feel better!', GV.light_violet)
    GC.u.heal(HEAL_AMOUNT)

def closest_monster(max_range):
    # find closest enemy, up to a maximum range, and in the player's FOV
    closest_enemy = None
    closest_dist = max_range + 1  #start with (slightly more than) maximum range

    for m in GC.monsters:
        if m != GC.u and GC.u.fov_map.lit(m.x, m.y):
            # calculate distance between this object and the player
            dist = GC.u.distance_to(m)
            if dist < closest_dist:  #it's closer, so remember it
                closest_enemy = m
                closest_dist = dist
    return closest_enemy
                                                        
    
def cast_lightning():
    #find closest enemy (inside a maximum range) and damage it
    target = closest_monster(5)
    if target is None:  #no enemy found within maximum range
        target = GC.u
        message('A lightning bolt arcs out from you and then returns to strike you in the head!', GV.light_blue)
    else:
        message('A lighting bolt strikes the ' + target.name + ' with a loud thunder!', GV.light_blue)
        
    target.take_damage(LIGHTNING_DAMAGE)



    
def cast_fireball():
    #ask the GC.u for a target tile to throw a fireball at
    message('Left-click a target tile for the fireball, or right-click to cancel.', GV.light_cyan)
    (x, y) = target_tile()

    if x is None:
        return 'cancelled'
    message('The fireball explodes, burning everything within ' + str(FIREBALL_RADIUS) + ' tiles!', GV.orange)
 
    for m in GC.monsters:  #damage every fighter in range, including the GC.u
        if m.distance(x, y) <= FIREBALL_RADIUS:
            message('The ' + m.name + ' gets burned for ' + str(FIREBALL_DAMAGE) + ' hit points.', GV.orange)
            m.take_damage(FIREBALL_DAMAGE)
 
def cast_confuse():
    #ask the GC.u for a target to confuse
    message('Left-click an enemy to confuse it, or right-click to cancel.', GV.light_cyan)
    monster = target_monster(CONFUSE_RANGE)
    if monster is None: return 'cancelled'
 
    #replace the monster's AI with a "confused" one; after some turns it will restore the old AI
    old_ai = monster.ai
    monster.ai = ConfusedMonster(old_ai)
    monster.ai.owner = monster  #tell the new component who owns it
    message('The eyes of the ' + monster.name + ' look vacant, as he starts to stumble around!', GV.light_green)
 
 



class Item(Object):
    """Anything that can be picked up."""
    
    def __init__(self, x, y, name, use_function=None, prev_monster=None):
        Object.__init__(self, x, y, name)
        self.blocks_sight = False
        self.blocks_movement = False

        # For items which were previously a monster.  Used for resurrection, de-stoning, etc.
        self.prev_monster = prev_monster

        
        if self.name == 'fizzy':
            self.use_function = cast_heal
        elif self.name == 'THARR':
            self.use_function = cast_fireball
        elif self.name == 'YUM YUM':
            self.use_function = cast_lightning
        elif self.name == 'NR 9':
            self.use_function = cast_confuse
