# Copyright (c) 2011, Andy Ruse

"""Player/monster actions other than fighting, using items, casting spells,
or using techniques.
"""

import pygame
from pygame.locals import *

from const import *
from game import *
from util import *



simple_save_objs = [
    'GC.dlevel',
    'GC.branch',
    'GC.msgs',
    'GC.oid_seq',
    'GC.random_seed',
    'GC.random_state',
    'GC.cmd_history',
    ]
complex_save_objs = [
    'GC.u',
    'GC.map',
    'GC.monsters',
    'GC.items',
    ]

#    'GC.dlevel_dict',
#    'GC.monsters_dict',
#    'GC.items_dict',


def save_game(file):
    f = open(file, 'w')

    for obj in simple_save_objs:
        f.write('{0} = {1}\n'.format(obj, repr(eval(obj))))

    GC.map[GC.u.x+1][GC.u.y+1].set_tile('cmap, wall, horizontal, mine')

    f.write('map = [')

    for x in range(len(GC.map)):
        f.write('[')
        for y in range(len(GC.map[0])):
            f.write("{{'n': {0}, 'e': {1}}}, ".format(
                    repr(GC.map[x][y].name),  repr(GC.map[x][y].explored)))
        f.write('],\n')
    f.write(']\n')


    # For references to Objects, just save the oid
    f.write(repr([m.oid for m in GC.monsters]) + '\n')
    f.write(repr([m.oid for m in GC.items]) + '\n')

# Uncomment to work out save files
#    f.write('objects = [')
#    
#
#    for oid, o in GC.obj_dict.iter:
#        if oid == GC.u.oid:
#            continue
#        elif 
#    f.write(']\n')


    f.close()

#    f.write('GC.cmd_history = {0}\n'.format(GC.cmd_history))
#    for var in dir(GC):
#        print 'GC.{0} = {1}'.format(var, eval('GC.' + var))


    message('Saved game to {0}.'.format(save_file))



def pick_up(m):
    """Try to make m pick up an item at its feet."""
    item_here = False

    for i in GC.items:
        if i.x == GC.u.x and i.y == GC.u.y:
            GC.u.pick_up(i)
            item_here = True

    if item_here:
        GC.u_took_turn = True
    else:
        GC.u_took_turn = False
        message('Nothing to pick up!')

def magic_mapping():
    """Reveal all tiles on the map."""
    for x in range(MAP_W):
        for y in range(MAP_H):
            GC.map[x][y].explored = True
