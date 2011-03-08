# Copyright (c) 2011, Andy Ruse

"""Player/monster actions other than fighting, using items, casting spells,
or using techniques.
"""

import pygame
from pygame.locals import *

from const import *
from game import *
from util import *
from cell import *
from monster import *
from item import *


simple_save_objs = [
    'GC.dlevel',
    'GC.branch',
    'GC.oid_seq',
    'GC.random_seed',
    'GC.map_rand_state',
    'GC.rand_state',
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

#    GC.map[GC.u.x+1][GC.u.y+1].set_tile('cmap, wall, horizontal, mine')

    f.write('map = [')

    for x in range(len(GC.map)):
        f.write('[')
        for y in range(len(GC.map[0])):
            f.write("{{'n': {0}, 'e': {1}}}, ".format(
                    repr(GC.map[x][y].name),  repr(GC.map[x][y].explored)))
        f.write('],')
    f.write(']\n')


    # For references to Objects, just save the oid
    f.write('monsters = ' + repr([m.oid for m in GC.monsters]) + '\n')
    f.write('items = ' + repr([m.oid for m in GC.items]) + '\n')
    print repr([m.oid for m in GC.monsters])
    print repr([m.oid for m in GC.items])
    print GC.u.oid

    # Save all monsters in existence.
    f.write('monster_defs = [')
    for oid, o in GC.obj_dict.iteritems():
        if oid == GC.u.oid:
            continue
        if o.__class__.__name__ == 'Monster':
            f.write("{{'oid':{0},'x':{1},'y':{2},'name':{3},'blocks_sight':{4},'blocks_movement':{5},'hp':{6},'max_hp':{7},'mp':{8},'max_mp':{9},'ai':{10},'death':{11}}},".format(
                    repr(oid), repr(o.x), repr(o.y), repr(o.name),
                    repr(o.blocks_sight), repr(o.blocks_movement),
                    repr(o.hp), repr(o.max_hp), repr(o.mp), repr(o.max_mp),
                    repr(o.ai.__class__.__name__), repr(o.death.__name__)))
    f.write(']\n')

    # Save all items in existence.
    f.write('item_defs = [')
    for oid, o in GC.obj_dict.iteritems():
        if o.__class__.__name__ == 'Item':
            if o.use_function is None:
                use_function = None
            else:
                use_function = o.use_function.__name__
            f.write("{{'oid':{0},'x':{1},'y':{2},'name':{3},'blocks_sight':{4},'blocks_movement':{5},'use_function':{6}}},".format(
                    repr(oid), repr(o.x), repr(o.y), repr(o.name),
                    repr(o.blocks_sight), repr(o.blocks_movement),
                    repr(use_function)))
    f.write(']\n')

    # Save the player's state.
    inventory = repr([i.oid for i in GC.u.inventory])
    f.write('u = ')
    f.write("{{'oid':{0},'x':{1},'y':{2},'name':{3},'blocks_sight':{4},'blocks_movement':{5},'hp':{6},'max_hp':{7},'mp':{8},'max_mp':{9},'ai':{10},'death':{11},'inventory':{12}}}".format(
            repr(GC.u.oid), repr(GC.u.x), repr(GC.u.y), repr(GC.u.name),
            repr(GC.u.blocks_sight), repr(GC.u.blocks_movement),
            repr(GC.u.hp), repr(GC.u.max_hp), repr(GC.u.mp), repr(GC.u.max_mp),
            repr(None), repr(GC.u.death.__name__), inventory))
    f.write('\n')


    f.close()

    message('Saved game to {0}.'.format(file))


def load_game(file):
    f = open(file, 'r')
    exec(f.read())
    f.close()

    # Replace the map structure in the save file with actual cells.
    GC.map = map

    for x in range(len(GC.map)):
        for y in range(len(GC.map[0])):
            GC.map[x][y] = Cell(GC.map[x][y]['n'], explored=GC.map[x][y]['e'])

    # Re-create monsters
    for m in monster_defs:
        GC.map[m['x']][m['y']].monsters.append(
            Monster(m['x'], m['y'], m['name'], oid=m['oid'], ai=eval(m['ai'])(), hp=m['hp'],
                    max_hp=m['max_hp'], mp=m['mp'], max_mp=m['max_mp'], death=eval(m['death'])))
        
    # Re-create items
    for i in item_defs:
        if i['use_function'] is None:
            use_function = None
        else:
            use_function = eval(i['use_function'])
        GC.map[i['x']][i['y']].items.append(
            Item(i['x'], i['y'], i['name'], oid=i['oid'], use_function=use_function))

        
    # Re-create the player
    if u['ai'] is not None:
        u['ai'] = eval(u['ai'])()
    GC.u = Player(u['x'], u['y'], u['name'], oid=u['oid'], ai=u['ai'], hp=u['hp'],
                max_hp=u['max_hp'], mp=u['mp'], max_mp=u['max_mp'], death=eval(u['death']))
    
    # Replace oids with references to the actual objects.
    GC.u.inventory = [GC.obj_dict[i] for i in u['inventory']]
    GC.monsters = [GC.obj_dict[m] for m in monsters]
    GC.items = [GC.obj_dict[i] for i in items]

    print monsters
    print items
    print GC.u.oid


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

def quit_game(signum=None, frame=None):
    """Gracefully exit."""
    GC.state = ST_QUIT

def show_fov():
    """Toggle a flag to visually outline the FOV on the map."""
    GC.fov_outline = not GC.fov_outline

def scroll_map(coords):
    """Scroll the map in the direction given."""
    GV.x_scrollbar.move_slider(coords[0] * SCROLL_AMT)
    GV.y_scrollbar.move_slider(coords[1] * SCROLL_AMT)

def scroll_log(coords):
    """Scroll the log window up or down."""
    GV.log_scrollbar.move_slider(coords[1] * SCROLL_AMT)

def scroll_log_end(coords):
    """Scroll the log window all the way to the top or bottom."""
    GV.log_scrollbar.move_slider(coords[1] * GV.log_rect.h)
