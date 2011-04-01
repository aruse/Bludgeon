# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

"""
Routines for saving and loading games.
"""

from const import *
from server_state import ServerState as SS
from cell import Cell
from item import Item
from monster import Monster
from player import Player
from util import *

simple_save_objs = [
    'SS.dlevel',
    'SS.branch',
    'Object.oid_seq',
    'SS.random_seed',
    'SS.cmd_history',
    ]
complex_save_objs = [
    'SS.u',
    'SS.map',
    'SS.monsters',
    'SS.items',
    ]
#    'SS.dlevel_dict',
#    'SS.monsters_dict',
#    'SS.items_dict',


def save_game(file):
    f = open(file, 'w')

    for obj in simple_save_objs:
        f.write('{0} = {1}\n'.format(obj, repr(eval(obj))))

    f.write('map = [')

    for x in xrange(len(SS.map)):
        f.write('[')
        for y in xrange(len(SS.map[0])):
            f.write("{{'n': {0}, 'e': {1}}}, ".format(
                    repr(SS.map[x][y].name),  repr(SS.map[x][y].explored)))
        f.write('],')
    f.write(']\n')


    # For references to Objects, just save the oid
    f.write('monsters = ' + repr([mon.oid for mon in SS.monsters]) + '\n')
    f.write('items = ' + repr([item.oid for item in SS.items]) + '\n')

    # Save all monsters in existence.
    f.write('monster_defs = [')
    for oid, o in Object.obj_dict.iteritems():
        if oid != SS.u.oid and o.__class__.__name__ == 'Monster':
            f.write(repr(o.serialize()) + ',')
    f.write(']\n')

    # Save all items in existence.
    f.write('item_defs = [')
    for oid, o in Object.obj_dict.iteritems():
        if o.__class__.__name__ == 'Item':
            f.write(repr(o.serialize()) + ',')
    f.write(']\n')

    # Save the player's state.
    f.write('u = ' + repr(SS.u.serialize()) + '\n')

    f.close()
    message('Saved game to {0}.'.format(file))


def load_game(file):
    f = open(file, 'r')
    exec(f.read())
    f.close()

    # Replace the map structure in the save file with actual cells.
    SS.map = map

    for x in xrange(len(SS.map)):
        for y in xrange(len(SS.map[0])):
            SS.map[x][y] = Cell(SS.map[x][y]['n'], explored=SS.map[x][y]['e'])

    # Re-create monsters
    for m_str in monster_defs:
        mon = Monster.unserialize(m_str)
        mon.place_on_map()
        
    # Re-create items
    for i_str in item_defs:
        item = Item.unserialize(i_str)
        item.place_on_map()
        
    # Re-create the player
    SS.u = Player.unserialize(u)


# FIXME: This is now handled by place_on_map().  I'm not sure if I need to save these at all.
#    SS.monsters = [Object.obj_dict[m] for m in monsters]
#    SS.items = [Object.obj_dict[i] for i in items]

def run_history():
    old_history = SS.cmd_history
    SS.cmd_history = []
    SS.mode = ST_PLAYBACK

    for cmd in old_history:
        print 'Running ' + str(cmd)
        if cmd[0] == 'm':
            SS.u.move(cmd[1], cmd[2])
        elif cmd[0] == 'a':
            SS.u.attack(Object.obj_dict[cmd[1]])
        elif cmd[0] == ',':
            SS.u.pick_up(Object.obj_dict[cmd[1]])
        elif cmd[0] == 'd':
            SS.u.drop(Object.obj_dict[cmd[1]])
        elif cmd[0] == 'u':
            SS.u.targeted_use(Object.obj_dict[cmd[1]], cmd[2], cmd[3])

        server_tick()
        client_tick()

    SS.mode = ST_PLAYING
