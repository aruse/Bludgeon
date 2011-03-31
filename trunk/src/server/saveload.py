# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

"""
Routines for saving and loading games.
"""

import pygame
from pygame.locals import *

from const import *
from server import Server as S
from cell import *
from monster import *
from item import *
from util import *

simple_save_objs = [
    'S.dlevel',
    'S.branch',
    'Object.oid_seq',
    'S.random_seed',
    'S.cmd_history',
    ]
complex_save_objs = [
    'S.u',
    'S.map',
    'S.monsters',
    'S.items',
    ]
#    'S.dlevel_dict',
#    'S.monsters_dict',
#    'S.items_dict',


def save_game(file):
    f = open(file, 'w')

    for obj in simple_save_objs:
        f.write('{0} = {1}\n'.format(obj, repr(eval(obj))))

    f.write('map = [')

    for x in xrange(len(S.map)):
        f.write('[')
        for y in xrange(len(S.map[0])):
            f.write("{{'n': {0}, 'e': {1}}}, ".format(
                    repr(S.map[x][y].name),  repr(S.map[x][y].explored)))
        f.write('],')
    f.write(']\n')


    # For references to Objects, just save the oid
    f.write('monsters = ' + repr([mon.oid for mon in S.monsters]) + '\n')
    f.write('items = ' + repr([item.oid for item in S.items]) + '\n')

    # Save all monsters in existence.
    f.write('monster_defs = [')
    for oid, o in Object.obj_dict.iteritems():
        if oid != S.u.oid and o.__class__.__name__ == 'Monster':
            f.write(repr(o.serialize()) + ',')
    f.write(']\n')

    # Save all items in existence.
    f.write('item_defs = [')
    for oid, o in Object.obj_dict.iteritems():
        if o.__class__.__name__ == 'Item':
            f.write(repr(o.serialize()) + ',')
    f.write(']\n')

    # Save the player's state.
    f.write('u = ' + repr(S.u.serialize()) + '\n')

    f.close()
    message('Saved game to {0}.'.format(file))


def load_game(file):
    f = open(file, 'r')
    exec(f.read())
    f.close()

    # Replace the map structure in the save file with actual cells.
    S.map = map

    for x in xrange(len(S.map)):
        for y in xrange(len(S.map[0])):
            S.map[x][y] = Cell(S.map[x][y]['n'], explored=S.map[x][y]['e'])

    # Re-create monsters
    for m_str in monster_defs:
        mon = Monster.unserialize(m_str)
        mon.place_on_map()
        
    # Re-create items
    for i_str in item_defs:
        item = Item.unserialize(i_str)
        item.place_on_map()
        
    # Re-create the player
    S.u = Player.unserialize(u)


# FIXME: This is now handled by place_on_map().  I'm not sure if I need to save these at all.
#    S.monsters = [Object.obj_dict[m] for m in monsters]
#    S.items = [Object.obj_dict[i] for i in items]

def run_history():
    old_history = S.cmd_history
    S.cmd_history = []
    S.mode = ST_PLAYBACK

    for cmd in old_history:
        print 'Running ' + str(cmd)
        if cmd[0] == 'm':
            S.u.move(cmd[1], cmd[2])
        elif cmd[0] == 'a':
            S.u.attack(Object.obj_dict[cmd[1]])
        elif cmd[0] == ',':
            S.u.pick_up(Object.obj_dict[cmd[1]])
        elif cmd[0] == 'd':
            S.u.drop(Object.obj_dict[cmd[1]])
        elif cmd[0] == 'u':
            S.u.targeted_use(Object.obj_dict[cmd[1]], cmd[2], cmd[3])

        server_tick()
        client_tick()

    S.mode = ST_PLAYING
