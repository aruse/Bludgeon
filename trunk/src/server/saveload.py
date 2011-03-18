# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

"""Routines for saving and loading games, and doing file IO."""

import pygame
from pygame.locals import *

from const import *
from server.server import Server as S
from util import *
from server.cell import *
from server.monster import *
from server.item import *


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

    for x in range(len(S.map)):
        f.write('[')
        for y in range(len(S.map[0])):
            f.write("{{'n': {0}, 'e': {1}}}, ".format(
                    repr(S.map[x][y].name),  repr(S.map[x][y].explored)))
        f.write('],')
    f.write(']\n')


    # For references to Objects, just save the oid
    f.write('monsters = ' + repr([m.oid for m in S.monsters]) + '\n')
    f.write('items = ' + repr([m.oid for m in S.items]) + '\n')

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

    for x in range(len(S.map)):
        for y in range(len(S.map[0])):
            S.map[x][y] = Cell(S.map[x][y]['n'], explored=S.map[x][y]['e'])

    # Re-create monsters
    for m_str in monster_defs:
        m = Monster.unserialize(m_str)
        S.map[m.x][m.y].monsters.append(m)
        
    # Re-create items
    for i_str in item_defs:
        i = Item.unserialize(i_str)
        S.map[i.x][i.y].items.append(i)
        
    # Re-create the player
    S.u = Player.unserialize(u)

    # Replace oids with references to the actual objects.
    # FIXME: The inventory code should go into unserialize()
    S.u.inventory = [Object.obj_dict[i] for i in S.u.inventory]
    S.monsters = [Object.obj_dict[m] for m in monsters]
    S.items = [Object.obj_dict[i] for i in items]


def load_image(name):
    """Load image and return image object."""
    fullname = os.path.join('images', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    return image

def load_sound(name):
    """Load sound and return sound object"""
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join('sounds', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', fullname
        raise SystemExit, message
    return sound        

def create_tile_dict():
    tile_dict = {}

    # Read in tile mapping document, line-by-line, and build a
    # dictionary pointing to coordinates of the graphic
    map = open('data/tiles.map')

    for line in map:
        (loc, name) = re.findall(r'(\d+) "(.*)"', line)[0]
        x = (int(loc) % 38) * TILE_W
        y = (int(loc) / 38) * TILE_H        
        tile_dict[name] = pygame.Rect(x, y, TILE_W, TILE_H)

    return tile_dict
