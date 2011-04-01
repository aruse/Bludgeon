# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

import random

from const import *
from server_state import ServerState as SS
from ai import *

from util import *

def cast_heal(item, x=None, y=None):
    if SS.u.hp == SS.u.max_hp:
        message('You are already at full health.', CLR['light_violet'])
        return 'cancelled'
 
    message('Your wounds start to feel better!', CLR['light_violet'])
    SS.u.heal(HEAL_AMOUNT)
    return 'success'
    
def closest_monster(max_range):
    # Find closest enemy, up to a maximum range and in the player's FOV
    closest_enemy = None
    # Start just out of max range
    closest_dist = max_range + 1

    for mon in SS.monsters:
        if mon != SS.u and SS.u.fov_map.in_fov(mon.x, mon.y):
            dist = SS.u.distance_to(mon)
            if dist < closest_dist:
                closest_enemy = mon
                closest_dist = dist

    return closest_enemy
                                                        
    
def cast_lightning(item, x=None, y=None):
    target = closest_monster(5)

    if target is None:
        target = SS.u
        message('A lightning bolt arcs out from you and then returns to '
                'strike you in the head!', CLR['light_blue'])
    else:
        message('A lighting bolt strikes the ' + target.name
                + ' with a loud thunder!', CLR['light_blue'])
        
    target.take_damage(LIGHTNING_DAMAGE)
    return 'success'

    
def cast_fireball(item, x=None, y=None):
    """Begin the casting of a fireball spell.  Ask the player to
    target a cell.
    """
    if x == None and y == None:
        message('Left-click a target for the fireball, or right-click to '
                'cancel.', CLR['light_cyan'])
        SS.mode = ST_TARGETING
        SS.targeting_function.append(finish_fireball)
        SS.targeting_item = item
        return 'targeting'
    else:
        finish_fireball(item, x, y)
    
    
def finish_fireball(item, x=None, y=None):
    """Finish the casting of a fireball spell after a cell has been selected.
    Return whether or not the fireball was cast.
    """
    if x is None:
        return False
    message('The fireball explodes, burning everything within '
            + str(FIREBALL_RADIUS) + ' spaces!', CLR['orange'])
 
    for mon in SS.monsters + [SS.u]:
        if mon.distance(x, y) <= FIREBALL_RADIUS:
            message('The ' + mon.name + ' gets burned for '
                    + str(FIREBALL_DAMAGE) + ' hit points.', CLR['orange'])
            mon.take_damage(FIREBALL_DAMAGE)

    return True
 
def cast_confuse(item, x=None, y=None):
    if x == None and y == None:
        message('Left-click an enemy to confuse it, or right-click to '
                'cancel.', CLR['light_cyan'])
        SS.mode = ST_TARGETING
        SS.targeting_function.append(finish_confuse)
        SS.targeting_item = item
        return 'targeting'
    else:
        finish_confuse(item, x, y)

def finish_confuse(item, x, y):
    # FIXME: should be able to target myself
    target = None
    for mon in SS.monsters:
        if (mon.x == x and mon.y == y
            and mon.distance(SS.u.x, SS.u.y) <= CONFUSE_RANGE):
            target = mon
            break

    if target is None:
        return False
 
    # Replace the monster's AI with a confused one
    old_ai = target.ai
    target.ai = ConfusedAI(old_ai)
    target.ai.owner = target  #tell the new component who owns it
    message('The eyes of the ' + target.name
            + ' look vacant, as he starts to stumble around!',
            CLR['light_green'])
    return True
