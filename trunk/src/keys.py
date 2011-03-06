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

def test_handler(x, y):
    print "test " + str(x) + str(y)

class KeyHandler:
    """Handle the actions of a specific keystroke."""
    def __init__(self, action, args, turn, desc=None):
        """Arguments:
        action -- Action to perform when the key is pressed.
        args -- List of arguments to give to action
        turn -- Whether or not this action counts as taking a turn.  If this
                depends on the outcome of the action, set it to None and let
                the action handler take care of it.
        desc -- Short description of what this keystroke does.
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
    # Accessed like pkeys[mod][KEY]
    # mod can be one of KMOD_NONE, KMOD_CTRL, KMOD_ALT
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
            '^': KeyHandler(None, (), True),
            '<': KeyHandler(None, (), True),
            '>': KeyHandler(None, (), True),
            '/': KeyHandler(None, (), True),
            '?': KeyHandler(None, (), True),
            '&': KeyHandler(None, (), True),
            '`': KeyHandler(None, (), True),
            '!': KeyHandler(test_handler, (1, 2), True),
            '\\': KeyHandler(None, (), True),
            '_': KeyHandler(None, (), True),
            '.': KeyHandler(GC.u.rest, (), True),
            ' ': KeyHandler(None, (), True),
            ':': KeyHandler(None, (), True),
            ',': KeyHandler(pick_up, (GC.u,), None),
            '@': KeyHandler(None, (), True),
            '(': KeyHandler(None, (), True),
            ')': KeyHandler(None, (), True),
            '[': KeyHandler(None, (), True),
            '=': KeyHandler(None, (), True),
            '"': KeyHandler(None, (), True),
            '$': KeyHandler(None, (), True),
            '+': KeyHandler(None, (), True),
            '#': KeyHandler(None, (), True),
            '*': KeyHandler(None, (), True),
            '0': KeyHandler(None, (), True),
            '1': KeyHandler(None, (), True),
            '2': KeyHandler(None, (), True),
            '3': KeyHandler(None, (), True),
            '4': KeyHandler(None, (), True),
            '5': KeyHandler(None, (), True),
            '6': KeyHandler(None, (), True),
            '7': KeyHandler(None, (), True),
            '8': KeyHandler(None, (), True),
            '9': KeyHandler(None, (), True),
            'a': KeyHandler(None, (), True),
            'b': KeyHandler(None, (), True),
            'c': KeyHandler(None, (), True),
            'd': KeyHandler(inventory_menu, (DELETE_HEADER, 'drop'), None),
            'e': KeyHandler(None, (), True),
            'f': KeyHandler(None, (), True),
            'g': KeyHandler(None, (), True),
            'h': KeyHandler(None, (), True),
            'i': KeyHandler(inventory_menu, (USE_HEADER, 'use'), None),
            'j': KeyHandler(None, (), True),
            'k': KeyHandler(None, (), True),
            'l': KeyHandler(None, (), True),
            'm': KeyHandler(None, (), True),
            'n': KeyHandler(None, (), True),
            'o': KeyHandler(None, (), True),
            'p': KeyHandler(None, (), True),
            'q': KeyHandler(None, (), True),
            'r': KeyHandler(None, (), True),
            's': KeyHandler(save_game, ('save.bludgeon',), False),
            't': KeyHandler(None, (), True),
            'u': KeyHandler(None, (), True),
            'v': KeyHandler(None, (), True),
            'w': KeyHandler(None, (), True),
            'x': KeyHandler(None, (), True),
            'y': KeyHandler(None, (), True),
            'z': KeyHandler(None, (), True),
            'A': KeyHandler(test_handler, (1, 2), True),
            'B': KeyHandler(None, (), True),
            'C': KeyHandler(None, (), True),
            'D': KeyHandler(None, (), True),
            'E': KeyHandler(None, (), True),
            'F': KeyHandler(None, (), True),
            'G': KeyHandler(None, (), True),
            'H': KeyHandler(None, (), True),
            'I': KeyHandler(None, (), True),
            'J': KeyHandler(None, (), True),
            'K': KeyHandler(None, (), True),
            'L': KeyHandler(None, (), True),
            'M': KeyHandler(None, (), True),
            'N': KeyHandler(None, (), True),
            'O': KeyHandler(None, (), True),
            'P': KeyHandler(None, (), True),
            'Q': KeyHandler(None, (), True),
            'R': KeyHandler(None, (), True),
            'S': KeyHandler(None, (), True),
            'T': KeyHandler(None, (), True),
            'U': KeyHandler(None, (), True),
            'V': KeyHandler(None, (), True),
            'W': KeyHandler(None, (), True),
            'X': KeyHandler(None, (), True),
            'Y': KeyHandler(None, (), True),
            'Z': KeyHandler(None, (), True),
            },
        KMOD_CTRL: {
            K_a: KeyHandler(None, (), True),
            K_b: KeyHandler(None, (), True),
            K_c: KeyHandler(None, (), True),
            K_d: KeyHandler(None, (), True),
            K_e: KeyHandler(None, (), True),
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

    # Define actions for special debug mode commands.
    if GC.debug:
        GC.pkeys[KMOD_CTRL][K_f] = KeyHandler(magic_mapping, (), False)

        # FIXME: This should actually be handled under #vision
        GC.pkeys[KMOD_CTRL][K_z] = KeyHandler(show_fov, (), False)


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
