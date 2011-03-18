# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

"""FIXME: need a better name for this stuff.  Used to be called "actions"."""

import pygame
from pygame.locals import *

from const import *
from server import Server as S
from util import *
from cell import *
from monster import *
from item import *


def client_pick_up():
    """Tell server to pick up an item at the player's feet."""
    for i in S.items:
        if i.x == S.u.x and i.y == S.u.y:
            request(',', (i.oid,))


def pick_up(oid):
    """Try to pick up an item at the player's feet."""
    item_here = False

    for i in S.items:
        if i.x == S.u.x and i.y == S.u.y and i.oid == oid:
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

def quit_game(signum=None, frame=None):
    """Gracefully exit."""
    S.state = ST_QUIT

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
