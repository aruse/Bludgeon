# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

import os
import time
import re
import textwrap
import pygame
from pygame.locals import *

from const import *
from game import *

def request(req, args):
    """Send a client request to the server.
    Currently implemented as a local queue.
    Arguments:
    req -- The request type, a string.
    args -- The arguments for the request, a tuple.
    """
    GC.client_requests.append((req, args))
    print 'Requests:', GC.client_requests


def handle_requests():
    while len(GC.client_requests):
        req, args = GC.client_requests.popleft()

        response = GC.requests[req].do(args)
#        GC.state = ST_QUIT
#        GC.server_responses.append(response)
        GC.cmd_history.append((req, args))

def message(msg, color=GC.default_font_color):
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
