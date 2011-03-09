# Copyright (c) 2011, Andy Ruse

import os
import time
import re
import textwrap
import pygame
from pygame.locals import *

from const import *
from game import *

def message(msg, color=GV.default_font_color):
    """Add a message to the game log and tell the log surface to update."""
    if len(GC.msgs) >= MAX_MSGS:
        GC.msgs.pop(0)

    GC.msgs.append((msg, color))
    GC.log_updated = True


def convert_to_grayscale(surf):
    """Convert a Surface to grayscale, pixel by pixel.  Quite slow."""
    gray = pygame.Surface(surf.get_size(), 0, 8)
    w, h = surf.get_size()
    for x in range(w):
        for y in range(h):
            red, green, blue, alpha = surf.get_at((x, y))
            average = (red + green + blue) // 3
            gs_color = (average, average, average, alpha)
            gray.set_at((x, y), gs_color)
    return gray

def cell2pixel(x, y):
    """Take in (x, y) cell coords and return (x, y) pixel coords on the map."""
    return ((x + 1) * TILE_W, (y + 1) * TILE_H)
