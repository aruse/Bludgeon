# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

"""FIXME: need a better name for this stuff.  Used to be called "actions".  Needs to be split into client and server functions."""

import pygame
from pygame.locals import *

from const import *
from server.server import Server as S
from network import Network
from util import *
from server.cell import *
from server.monster import *
from server.item import *


def client_pick_up():
    """Tell server to pick up an item at the player's feet."""
    items = []
    for i in C.map[C.u.x][C.u.y].items:
        items.append(i.oid)

    Network.request(',', (tuple(items),))


def pick_up(oids):
    """Try to pick up one or more items at the player's feet."""
    print oids
    items = [Object.obj_dict[oid] for oid in oids]
    item_here = False

    for i in items:
        if i.x == S.u.x and i.y == S.u.y:
            S.u.pick_up(i)
            item_here = True

    if item_here:
        S.u_took_turn = True
    else:
        S.u_took_turn = False
        message('Nothing to pick up!')

def magic_mapping():
    """Reveal all tiles on the map."""
    for x in range(MAP_W):
        for y in range(MAP_H):
            S.map[x][y].explored = True

def show_fov():
    """Toggle a flag to visually outline the FOV on the map."""
    S.fov_outline = not S.fov_outline

def scroll_map(coords):
    """Scroll the map in the direction given."""
    C.x_scrollbar.move_slider(coords[0] * SCROLL_AMT)
    C.y_scrollbar.move_slider(coords[1] * SCROLL_AMT)

def scroll_log(coords):
    """Scroll the log window up or down."""
    C.log_scrollbar.move_slider(coords[1] * SCROLL_AMT)

def scroll_log_end(coords):
    """Scroll the log window all the way to the top or bottom."""
    C.log_scrollbar.move_slider(coords[1] * C.log_rect.h)
