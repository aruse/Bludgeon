import os
import time
import re
import textwrap
import pygame
from pygame.locals import *

from const import *
from game import *

        
def mouse_coords_to_map_coords(x, y):
    # Compensate for the relative position of the map surface.
    y -= GV.map_py
    # Convert into map coords
    x /= TILE_PW
    y /= TILE_PH
    return x, y
    
def message(msg, color=GV.default_font_color):
    # Split the message if necessary, among multiple lines
    # FIXME: This should wrap based on the current size of the text buffer, not at a blind 60 characters.

    if len(GC.msgs) >= MAX_MSGS:
        GC.msgs.pop(0)

    GC.msgs.append((msg, color))


    return


    lines = textwrap.wrap(msg, 60)

    for line in lines:
        if len(GC.msgs) >= MAX_MSGS:
            GC.msgs.pop(0)

        GC.msgs.append((line, color))

def load_image(name):
    """ Load image and return image object"""
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

    # Read in tile mapping document, line-by-line, and build a dictionary pointing to coordinates of the graphic
    map = open('data/tiles.map')

    for line in map:
        (loc, name) = re.findall(r'(\d+) "(.*)"', line)[0]
        x = (int(loc) % 38) * TILE_PW
        y = (int(loc) / 38) * TILE_PH        
        tile_dict[name] = pygame.Rect(x, y, TILE_PW, TILE_PH)

    return tile_dict

def convert_to_grayscale(surf):
    gray = pygame.Surface(surf.get_size(), 0, 8)
    width, height = surf.get_size()
    for x in range(width):
        for y in range(height):
            red, green, blue, alpha = surf.get_at((x, y))
            average = (red + green + blue) // 3
            gs_color = (average, average, average, alpha)
            gray.set_at((x, y), gs_color)
    return gray
