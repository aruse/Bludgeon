import random
import math

import pygame
from pygame.locals import *

from const import *
from game import *
from util import *
from ai import *

def cast_heal(item):
    if GC.u.hp == GC.u.max_hp:
        message('You are already at full health.', GV.light_violet)
        return 'cancelled'
 
    message('Your wounds start to feel better!', GV.light_violet)
    GC.u.heal(HEAL_AMOUNT)
    return 'success'
    
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
                                                        
    
def cast_lightning(item):
    #find closest enemy (inside a maximum range) and damage it
    target = closest_monster(5)
    if target is None:  #no enemy found within maximum range
        target = GC.u
        message('A lightning bolt arcs out from you and then returns to strike you in the head!', GV.light_blue)
    else:
        message('A lighting bolt strikes the ' + target.name + ' with a loud thunder!', GV.light_blue)
        
    target.take_damage(LIGHTNING_DAMAGE)
    return 'success'

    
def cast_fireball(item):
    """Begin the casting of a fireball spell.  Ask the player to target a cell."""
    #ask the GC.u for a target tile to throw a fireball at
    message('Left-click a target tile for the fireball, or right-click to cancel.', GV.light_cyan)
    GC.state = 'targetting'
    GC.targetting_function.append(finish_fireball)
    GC.targetting_item = item
    return 'targetting'
    
    
def finish_fireball(item, x, y):
    """Finish the casting of a fireball spell after a cell has been selected.
    Return whether or not the fireball was cast.
    """
    if x is None:
        return False
    message('The fireball explodes, burning everything within ' + str(FIREBALL_RADIUS) + ' tiles!', GV.orange)
 
    for m in GC.monsters + [GC.u]:  #damage every fighter in range, including the GC.u
        if m.distance(x, y) <= FIREBALL_RADIUS:
            message('The ' + m.name + ' gets burned for ' + str(FIREBALL_DAMAGE) + ' hit points.', GV.orange)
            m.take_damage(FIREBALL_DAMAGE)

    return True
 
def cast_confuse(item):
    #ask the GC.u for a target to confuse
    message('Left-click an enemy to confuse it, or right-click to cancel.', GV.light_cyan)
    GC.state = 'targetting'
    GC.targetting_function.append(finish_confuse)
    GC.targetting_item = item
    return 'targetting'

def finish_confuse(item, x, y):
    # FIXME: should be able to target myself
    target = None
    for m in GC.monsters:
        if (m.x == x and m.y == y and
            m.distance(GC.u.x, GC.u.y) <= CONFUSE_RANGE):
            target = m
            break
    
    if target is None:
        return False
 
    # replace the monster's AI with a "confused" one; after some turns it will restore the old AI
    old_ai = target.ai
    target.ai = ConfusedAI(old_ai)
    target.ai.owner = target  #tell the new component who owns it
    message('The eyes of the ' + target.name + ' look vacant, as he starts to stumble around!', GV.light_green)
    return True