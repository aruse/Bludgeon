# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

"""
Routines for loading and manipulating images.
"""

import os
import re

import pygame
from pygame.locals import *

from const import *


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
        raise SystemExit(message)
    return image


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


def convert_to_grayscale(surf):
    """Convert a Surface to grayscale, pixel by pixel.  Quite slow."""
    gray = pygame.Surface(surf.get_size(), 0, 8)
    w, h = surf.get_size()
    for x in xrange(w):
        for y in xrange(h):
            red, green, blue, alpha = surf.get_at((x, y))
            average = (red + green + blue) // 3
            gs_color = (average, average, average, alpha)
            gray.set_at((x, y), gs_color)
    return gray
