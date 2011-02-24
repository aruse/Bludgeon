import os
import time
import re
import textwrap
import pygame
from pygame.locals import *

from const import *
from game import *

def message(msg, color=CLR_BLACK):
    # Split the message if necessary, among multiple lines
    lines = textwrap.wrap(msg, 40)

    for line in lines:
        if len(GC.msgs) == MAX_MSGS:
            GC.msgs.pop()

        GC.msgs.insert(0, (line, color))

def load_image(name):
    """ Load image and return image object"""
    fullname = os.path.join('../images', name)
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
    tile_dict_width = 38 * TILE_PW
    tile_dict = {}

    # Read in tile mapping document, line-by-line, and build a dictionary pointing to coordinates of the graphic
    map = open('../data/tiles.map')
    (map_x, map_y) = (0, 0)
    for line in map:
        tile_name = re.findall(r'"(.*)"', line)
        tile_dict[tile_name[0]] = pygame.Rect(map_x, map_y, TILE_PW, TILE_PH)
        map_x += TILE_PW
        if map_x >= tile_dict_width:
            map_x = 0
            map_y += TILE_PH
    return tile_dict


def create_tile(name):
    return GV.tiles_image.subsurface(GV.tile_dict[name])
