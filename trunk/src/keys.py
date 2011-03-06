# Copyright (c) 2011, Andy Ruse

"""KeyHandler class and dictionaries use to map keys to handlers."""

import pygame
from pygame.locals import *

from const import *
from game import *
from util import *
from monster import *
from item import *
from dlevel import *
from cell import *
from ai import *
from gui import *
from spell import *
from actions import *

def shifta(x, y):
    print "shift-a" + str(x) + str(y)

class KeyHandler:
    """Handle the actions of a specific keystroke."""
    def __init__(self, action, args, turn):
        """Arguments:
        action -- Action to perform when the key is pressed.
        args -- List of arguments to give to action
        turn -- Whether or not this action counts as taking a turn.  If this
                depends on the outcome of the action, set it to None and let
                the action handler take care of it.
        """
        self.action = action
        self.args = args
        self.turn = turn

    def do(self):
        """Perform the action associated with this key press."""
        GC.u_took_turn = self.turn
        self.action(*self.args)


def attach_key_actions():
    """Set up dictionaries to map keys to actions."""
    
    # Keystroke handlers for 'playing' mode.
    # Accessed like pkeys[MODIFICATION_KEY][KEY]
    GC.pkeys = {
        KMOD_NONE: {
            K_UP: KeyHandler(GC.u.try_move, (DIRH['u'],), True),
            K_DOWN: KeyHandler(GC.u.try_move, (DIRH['d'],), True),
            K_LEFT: KeyHandler(GC.u.try_move, (DIRH['l'],), True),
            K_RIGHT: KeyHandler(GC.u.try_move, (DIRH['r'],), True),
            K_KP1: KeyHandler(GC.u.try_move, (DIRH['dl'],), True),
            K_KP2: KeyHandler(GC.u.try_move, (DIRH['d'],), True),
            K_KP3: KeyHandler(GC.u.try_move, (DIRH['dr'],), True),
            K_KP4: KeyHandler(GC.u.try_move, (DIRH['l'],), True),
            K_KP5: KeyHandler(None, (), True),
            K_KP6: KeyHandler(GC.u.try_move, (DIRH['r'],), True),
            K_KP7: KeyHandler(GC.u.try_move, (DIRH['ul'],), True),
            K_KP8: KeyHandler(GC.u.try_move, (DIRH['u'],), True),
            K_KP9: KeyHandler(GC.u.try_move, (DIRH['ur'],), True),

            K_ESCAPE: KeyHandler(None, (), True),
            K_CARET: KeyHandler(None, (), True),
            K_LESS: KeyHandler(None, (), True),
            K_GREATER: KeyHandler(None, (), True),
            K_SLASH: KeyHandler(None, (), True),
            K_QUESTION: KeyHandler(None, (), True),
            K_AMPERSAND: KeyHandler(None, (), True),
            K_BACKQUOTE: KeyHandler(None, (), True),
            K_EXCLAIM: KeyHandler(None, (), True),
            K_BACKSLASH: KeyHandler(None, (), True),
            K_UNDERSCORE: KeyHandler(None, (), True),
            K_PERIOD: KeyHandler(GC.u.rest, (), True),
            K_SPACE: KeyHandler(None, (), True),
            K_COLON: KeyHandler(None, (), True),
            K_COMMA: KeyHandler(pick_up, (GC.u,), None),
            K_AT: KeyHandler(None, (), True),
            K_RIGHTPAREN: KeyHandler(None, (), True),
            K_LEFTPAREN: KeyHandler(None, (), True),
            K_LEFTBRACKET: KeyHandler(None, (), True),
            K_EQUALS: KeyHandler(None, (), True),
            K_QUOTEDBL: KeyHandler(None, (), True),
            K_DOLLAR: KeyHandler(None, (), True),
            K_PLUS: KeyHandler(None, (), True),
            K_HASH: KeyHandler(None, (), True),
            K_ASTERISK: KeyHandler(None, (), True),
            K_0: KeyHandler(None, (), True),
            K_1: KeyHandler(None, (), True),
            K_2: KeyHandler(None, (), True),
            K_3: KeyHandler(None, (), True),
            K_4: KeyHandler(None, (), True),
            K_5: KeyHandler(None, (), True),
            K_6: KeyHandler(None, (), True),
            K_7: KeyHandler(None, (), True),
            K_8: KeyHandler(None, (), True),
            K_9: KeyHandler(None, (), True),
            K_a: KeyHandler(None, (), True),
            K_b: KeyHandler(None, (), True),
            K_c: KeyHandler(None, (), True),
            K_d: KeyHandler(inventory_menu, (DELETE_HEADER, 'drop'), None),
            K_e: KeyHandler(None, (), True),
            K_f: KeyHandler(None, (), True),
            K_g: KeyHandler(None, (), True),
            K_h: KeyHandler(None, (), True),
            K_i: KeyHandler(inventory_menu, (USE_HEADER, 'use'), None),
            K_j: KeyHandler(None, (), True),
            K_k: KeyHandler(None, (), True),
            K_l: KeyHandler(None, (), True),
            K_m: KeyHandler(None, (), True),
            K_n: KeyHandler(None, (), True),
            K_o: KeyHandler(None, (), True),
            K_p: KeyHandler(None, (), True),
            K_q: KeyHandler(None, (), True),
            K_r: KeyHandler(None, (), True),
            K_s: KeyHandler(save_game, ('save.bludgeon',), False),
            K_t: KeyHandler(None, (), True),
            K_u: KeyHandler(None, (), True),
            K_v: KeyHandler(None, (), True),
            K_w: KeyHandler(None, (), True),
            K_x: KeyHandler(None, (), True),
            K_y: KeyHandler(None, (), True),
            K_z: KeyHandler(None, (), True),
            },
        KMOD_SHIFT: {
            K_a: KeyHandler(shifta, (1, 2), True),
            K_b: KeyHandler(None, (), True),
            K_c: KeyHandler(None, (), True),
            K_d: KeyHandler(None, (), True),
            K_e: KeyHandler(None, (), True),
            K_f: KeyHandler(None, (), True),
            K_g: KeyHandler(None, (), True),
            K_h: KeyHandler(None, (), True),
            K_i: KeyHandler(None, (), True),
            K_j: KeyHandler(None, (), True),
            K_k: KeyHandler(None, (), True),
            K_l: KeyHandler(None, (), True),
            K_m: KeyHandler(None, (), True),
            K_n: KeyHandler(None, (), True),
            K_o: KeyHandler(None, (), True),
            K_p: KeyHandler(None, (), True),
            K_q: KeyHandler(None, (), True),
            K_r: KeyHandler(None, (), True),
            K_s: KeyHandler(None, (), True),
            K_t: KeyHandler(None, (), True),
            K_u: KeyHandler(None, (), True),
            K_v: KeyHandler(None, (), True),
            K_w: KeyHandler(None, (), True),
            K_x: KeyHandler(None, (), True),
            K_y: KeyHandler(None, (), True),
            K_z: KeyHandler(None, (), True),
            },
        KMOD_CTRL: {
            K_a: KeyHandler(None, (), True),
            K_b: KeyHandler(None, (), True),
            K_c: KeyHandler(None, (), True),
            K_d: KeyHandler(None, (), True),
            K_e: KeyHandler(None, (), True),
            K_f: KeyHandler(magic_mapping, (), False),
            K_g: KeyHandler(None, (), True),
            K_h: KeyHandler(None, (), True),
            K_i: KeyHandler(None, (), True),
            K_j: KeyHandler(None, (), True),
            K_l: KeyHandler(None, (), True),
            K_n: KeyHandler(None, (), True),
            K_o: KeyHandler(None, (), True),
            K_p: KeyHandler(None, (), True),
            K_r: KeyHandler(None, (), True),
            K_t: KeyHandler(None, (), True),
            K_v: KeyHandler(None, (), True),
            K_u: KeyHandler(None, (), True),
            K_w: KeyHandler(None, (), True),
            K_x: KeyHandler(None, (), True),
            K_y: KeyHandler(None, (), True),
            K_z: KeyHandler(None, (), True),
            },
        KMOD_ALT: {
            K_QUESTION: KeyHandler(None, (), True),
            K_a: KeyHandler(None, (), True),
            K_b: KeyHandler(None, (), True),
            K_c: KeyHandler(None, (), True),
            K_d: KeyHandler(None, (), True),
            K_e: KeyHandler(None, (), True),
            K_f: KeyHandler(None, (), True),
            K_i: KeyHandler(None, (), True),
            K_j: KeyHandler(None, (), True),
            K_k: KeyHandler(None, (), True),
            K_l: KeyHandler(None, (), True),
            K_m: KeyHandler(None, (), True),
            K_n: KeyHandler(None, (), True),
            K_o: KeyHandler(None, (), True),
            K_p: KeyHandler(None, (), True),
            K_q: KeyHandler(None, (), True),
            K_r: KeyHandler(None, (), True),
            K_s: KeyHandler(None, (), True),
            K_t: KeyHandler(None, (), True),
            K_u: KeyHandler(None, (), True),
            K_v: KeyHandler(None, (), True),
            K_w: KeyHandler(None, (), True),
            K_y: KeyHandler(None, (), True),
            },
        }

# Dictionary of key presses to ignore.  Note that this includes modifier keys,
# as they are handled above in the sections that handle the key modified.
ignore_keys = {
    K_NUMLOCK: True,
    K_CAPSLOCK: True,
    K_SCROLLOCK: True,
    K_RSHIFT: True,
    K_LSHIFT: True,
    K_RCTRL: True,
    K_LCTRL: True,
    K_RALT: True,
    K_LALT: True,
    K_RMETA: True,
    K_LMETA: True,
    K_LSUPER: True,
    K_RSUPER: True,
    }
