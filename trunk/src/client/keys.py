# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

"""KeyHandler class and dictionaries use to map keys to handlers."""

import pygame
from pygame.locals import *

from const import *
from server import Server as S
from client import Client as C
from util import *
from monster import *
from item import *
from dlevel import *
from cell import *
from ai import *
from gui import *
from spell import *
from saveload import *
from stuff import *


class KeyHandler:
    """Handle the actions of a specific keystroke."""
    def __init__(self, action, args, turn, desc=None):
        """Arguments:
        @param action: Action to perform when the key is pressed.
        @param args: List of arguments to give to action
        @param turn: Whether or not this action counts as taking a turn.  If 
        this depends on the outcome of the action, set it to None and let
        the action handler take care of it.
        @param desc: Short description of what this keystroke does.
        """
        self.action = action
        self.args = args
        self.turn = turn

    def do(self):
        """Perform the action associated with this key press."""
        S.u_took_turn = self.turn
        self.action(*self.args)


def attach_key_actions():
    """Set up dictionaries to map keys to actions."""
    
    # Keystroke handlers for 'playing' mode.
    # Accessed like pkeys[mod][KEY]
    # mod can be one of KMOD_NONE, KMOD_CTRL, KMOD_ALT
    S.pkeys = {
        KMOD_NONE: {
            K_KP1: KeyHandler(S.u.try_move, (DIRH['dl'],), True, ""),
            K_KP2: KeyHandler(S.u.try_move, (DIRH['d'],), True, ""),
            K_KP3: KeyHandler(S.u.try_move, (DIRH['dr'],), True, ""),
            K_KP4: KeyHandler(S.u.try_move, (DIRH['l'],), True, ""),
            K_KP5: KeyHandler(None, (), True, ""),
            K_KP6: KeyHandler(S.u.try_move, (DIRH['r'],), True, ""),
            K_KP7: KeyHandler(S.u.try_move, (DIRH['ul'],), True, ""),
            K_KP8: KeyHandler(S.u.try_move, (DIRH['u'],), True, ""),
            K_KP9: KeyHandler(S.u.try_move, (DIRH['ur'],), True, ""),

            K_ESCAPE: KeyHandler(None, (), True, "Cancel command."),
            '^': KeyHandler(None, (), "Examine a trap."),
            '<': KeyHandler(None, (), True, "Go up a staircase or ladder."),
            '>': KeyHandler(None, (), True, "Go down a staircase or ladder."),
            '/': KeyHandler(None, (), True,
                            "Describe a particular symbol on the map."),
            '?': KeyHandler(None, (), True, "Open the help menu."),
            '&': KeyHandler(None, (), True,
                            "Explain what the following command does."),
            '`': KeyHandler(None, (), True, "Open the command menu."),
            '\\': KeyHandler(None, (), True,
                             "List which objects have been discovered."),
            '_': KeyHandler(None, (), True,
                            "Travel to a particular point on the map."),
            '.': KeyHandler(S.u.rest, (), True, "Rest for one turn."),
            ':': KeyHandler(None, (), True,
                            "Describe the floor at the current location."),
            ';': KeyHandler(None, (), True,
                            "How is this different than '/'?"),
            ',': KeyHandler(
                client_pick_up, (), None,
                "Pick things up from the current location.  May be preceded "
                "by 'm' to select which things to pick up."),
            '@': KeyHandler(None, (), True, "Toggle the autopickup option.  "
                            "When this option is on, you will automatically "
                            "pick up any item that you walk over."),
            '(': KeyHandler(None, (), True, "Show the currently used tools."),
            ')': KeyHandler(None, (), True,
                            "Show the currently wielded weapon."),
            '[': KeyHandler(None, (), True, "Show the currently worn armor."),
            '=': KeyHandler(None, (), True, "Show the currently worn rings."),
            '"': KeyHandler(None, (), True, "Show the currently worn amulet."),
            '$': KeyHandler(None, (), True,
                            "Count all of your gold pieces in all of your "
                            "carried containers."),
            '#': KeyHandler(None, (), True, "Perform an extended command.  "
                            "You'll be given a list of extended commands and "
                            "be prompted to type which one you want to use."),
            '*': KeyHandler(None, (), True, "Show all worn equipment."),
            'a': KeyHandler(
                None, (), True,
                "Apply (a.k.a. use) a tool, such as a bag, torch, pick-axe, "
                "etc."),
            'b': KeyHandler(None, (), True, "Move"),
            'c': KeyHandler(None, (), True, "Close a door"),
            'd': KeyHandler(inventory_menu, (DELETE_HEADER, 'drop'), None,
                            "Drop one item from your inventory."),
            'e': KeyHandler(
                None, (), True,
                "Eat something, either from your inventory or the ground at "
                "your location.  If you are a vampire, instead drain blood"
                "from a corpse."),
            'f': KeyHandler(
                None, (), True,
                "Fire objects in your quiver.  You will launch them using the "
                "currently equiped weapon (such as a bow) if it makes sense "
                "to do so."),
            'g': KeyHandler(
                None, (), True,
                "Prefix: When followed by a direction, move until you are "
                "next to something interesting."),
            'h': KeyHandler(None, (), True, "Move"),
            'i': KeyHandler(inventory_menu, (USE_HEADER, 'use'), None,
                            "Show your current inventory."),
            'j': KeyHandler(None, (), True, "Move"),
            'k': KeyHandler(None, (), True, "Move"),
            'l': KeyHandler(None, (), True, "Move"),
            'm': KeyHandler(
                None, (), True,
                "Prefix: When followed by a direction, move without fighting "
                "or picking anything up."),
            'n': KeyHandler(None, (), True, "Move"),
            'o': KeyHandler(None, (), True, "Open a door."),
            'p': KeyHandler(
                None, (), True,
                "Pay a shopkeeper for items or inquire about shopkeeper "
                "services."),
            'q': KeyHandler(
                None, (), True,
                "Quaff (a.k.a. drink) something.  Usually a potion or a "
                "water source."),
            'r': KeyHandler(
                None, (), True,
                "Read something.  Usually a scroll, a spellbook, or writing "
                "on the floor."),
            's': KeyHandler(None, (), True,
                            "Search for traps or secret doors for one turn."),
            't': KeyHandler(None, (), True,
                            "Throw something, usually a weapon."),
            'u': KeyHandler(None, (), True, "Move"),
            'v': KeyHandler(None, (), True, "Display the software version."),
            'w': KeyHandler(
                None, (), True, 
                "Wield (a.k.a. put in your hand, ready to use) a weapon.  "
                "In order to wield nothing and fight with your bare hands, "
                "use '-' when asked for which weapon to wield."),
            'x': KeyHandler(
                None, (), True,
                "Exchange your wielded weapon with your secondary weapon.  "
                "If you have no secondary weapon, move your wielded weapon to "
                "your secondary weapon and fight with your bare hands."),
            'y': KeyHandler(None, (), True, "Move"),
            'z': KeyHandler(None, (), True, "Zap a wand."),
            'A': KeyHandler(None, (), True, "Remove all worn armor."),
            'B': KeyHandler(None, (), True, "Move"),
            'C': KeyHandler(
                None, (), True,
                "Call (a.k.a. name) an individual monster.  Useful if you "
                "want to be able to distinguish between monsters in combat."),
            'D': KeyHandler(None, (), True,
                            "Drop several items from your inventory."),
            'E': KeyHandler(
                None, (), True,
                "Engrave on the floor.  You can use a weapon, or type '-' to "
                "write with your fingers.  There are other items with which "
                "you can engrave as well."),
            'F': KeyHandler(None, (), True,
                            "Fight a monster in a particular direction."),
            'G': KeyHandler(
                None, (), True,
                "Prefix: When followed by a direction, fight a monster, even "
                "if you're not sure if there's a monster there."),
            'H': KeyHandler(None, (), True, "Move"),
            'I': KeyHandler(None, (), True,
                            "List sub-groups of items in your inventory."),
            'J': KeyHandler(None, (), True, "Move"),
            'K': KeyHandler(None, (), True, "Move"),
            'L': KeyHandler(None, (), True, "Move"),
            'M': KeyHandler(None, (), True, "Move"),
            'N': KeyHandler(None, (), True, "Move"),
            'O': KeyHandler(None, (), True, "Set game options."),
            'P': KeyHandler(
                None, (), True,
                "Put on an accessory, such as a ring, amulet, or blindfold."),
            'Q': KeyHandler(
                None, (), True,
                "Put ammunition into your quiver.  This ammunition will then "
                "be used with the 'f' command."),
            'R': KeyHandler(
                None, (), True,
                "Remove a worn accessory, such as a ring, amulet, or "
                "blindfold."),
            'S': KeyHandler(
                save_game, ('save.bludgeon',), False,
                "Save the game.  There is only one savefile per character, "
                "so this will overwrite any existing savefile.  This is by "
                "design."),
            'T': KeyHandler(None, (), True,
                            "Take off one piece of worn armor."),
            'U': KeyHandler(None, (), True, "Move"),
            'V': KeyHandler(None, (), True, "Show game history."),
            'W': KeyHandler(None, (), True, "Wear one piece of armor."),
            'X': KeyHandler(None, (), True, "List all known spells."),
            'Y': KeyHandler(None, (), True, "Move"),
            'Z': KeyHandler(None, (), True, "Zap (a.k.a. cast) a known spell."),
            },
        KMOD_SHIFT: {
            K_KP1: KeyHandler(scroll_map, (DIRH['dl'],), False,
                              "Scroll the map window."),
            K_KP2: KeyHandler(scroll_map, (DIRH['d'],), False,
                              "Scroll the map window."),
            K_KP3: KeyHandler(scroll_map, (DIRH['dr'],), False,
                              "Scroll the map window."),
            K_KP4: KeyHandler(scroll_map, (DIRH['l'],), False,
                              "Scroll the map window."),
            K_KP6: KeyHandler(scroll_map, (DIRH['r'],), False,
                              "Scroll the map window."),
            K_KP7: KeyHandler(scroll_map, (DIRH['ul'],), False,
                              "Scroll the map window."),
            K_KP8: KeyHandler(scroll_map, (DIRH['u'],), False,
                              "Scroll the map window."),
            K_KP9: KeyHandler(scroll_map, (DIRH['ur'],), False,
                              "Scroll the map window."),
            K_PAGEUP: KeyHandler(scroll_log, (DIRH['u'],), False,
                              "Scroll the log window up."),
            K_PAGEDOWN: KeyHandler(scroll_log, (DIRH['d'],), False,
                              "Scroll the log window down."),
            K_HOME: KeyHandler(scroll_log_end, (DIRH['u'],), False,
                              "Scroll the log window to the top."),
            K_END: KeyHandler(scroll_log_end, (DIRH['d'],), False,
                              "Scroll the log window to the bottom."),
            },
        KMOD_CTRL: {
            K_a: KeyHandler(None, (), True, "Re-do the previous command."),
            K_d: KeyHandler(
                None, (), True,
                "Kick something (usually something locked that you wish to "
                "open)."),
#            K_b: KeyHandler(None, (), True, "Move"),
#            K_h: KeyHandler(None, (), True, "Move"),
#            K_j: KeyHandler(None, (), True, "Move"),
#            K_k: KeyHandler(None, (), True, "Move"),
#            K_l: KeyHandler(None, (), True, "Move"),
#            K_n: KeyHandler(None, (), True, "Move"),
#            K_u: KeyHandler(None, (), True, "Move"),
#            K_y: KeyHandler(None, (), True, "Move"),
            K_t: KeyHandler(None, (), True, "Teleport, if you are able."),
            K_x: KeyHandler(None, (), True, ""),
            },
        KMOD_ALT: {
            K_QUESTION: KeyHandler(None, (), True,
                                   "Display help with extended commands."),
            },
        'ext': {
            '2weapon': KeyHandler(
                None, (), True,
                "Wield both your primary and secondary weapons "
                "simultaneously."),
            'adjust': KeyHandler(
                None, (), True,
                "Adjust which inventory letters are assigned to which items."),
            'borrow': KeyHandler(None, (), True,
                                 "Attempt to steal from a someone."),
            'chat': KeyHandler(None, (), True, "Talk to someone."),
            'conduct': KeyHandler(
                None, (), True,
                "List which voluntary challenges you've followed so far."),
            'dip': KeyHandler(None, (), True, "Dip an object into something."),
            'enhance': KeyHandler(
                None, (), True,
                "Advance or check character skills."),
            'force': KeyHandler(None, (), True,
                                "Attempt to force open a lock."),
            'invoke': KeyHandler(None, (), True,
                                 "Invoke the special powers of an artifact."),
            'jump': KeyHandler(None, (), True, "Jump."),
            'loot': KeyHandler(
                None, (), True,
                "Loot a box or bag in the same location as you, or remove "
                "the saddle from a horse."),
            'monster': KeyHandler(
                None, (), True,
                "When polymorphed into a monster, use that monster's special "
                "ability."),
            'name': KeyHandler(
                None, (), True,
                "Add a label to a specific item or class of items."),
            'offer': KeyHandler(None, (), True, "Offer a sacrifice to a god."),
            'pray': KeyHandler(None, (), True, "Pray to a god for help."),
            'quit': KeyHandler(
                quit_game, (), False,
                "Quit the game permanently.  This will end your character's "
                "life, and you'll have to start over with a new character."),
            'rub': KeyHandler(
                None, (), True,
                "Rub something (usually a lamp or a stone)."),
            'sit': KeyHandler(None, (), True,
                              "Sit on the floor or on an object."),
            'technique': KeyHandler(
                None, (), True,
                "Use a special technique available to your role or race."),
            'untrap': KeyHandler(
                None, (), True, "Attempt to disarm a trap."),
            'vanquished': KeyHandler(
                None, (), True,
                "Show a list of all monsters vanquished in this game."),
            'wipe': KeyHandler(None, (), True, "Wipe your face."),
            'youpoly': KeyHandler(
                None, (), True, "Polymorph, if you are able."),
            }
        }


    # Key bindings that do the same as ones already defined above.
    S.pkeys[KMOD_NONE][K_UP] = S.pkeys[KMOD_NONE][K_KP8]
    S.pkeys[KMOD_NONE][K_DOWN] = S.pkeys[KMOD_NONE][K_KP2]
    S.pkeys[KMOD_NONE][K_LEFT] = S.pkeys[KMOD_NONE][K_KP4]
    S.pkeys[KMOD_NONE][K_RIGHT] = S.pkeys[KMOD_NONE][K_KP6]
    S.pkeys[KMOD_NONE][K_HOME] = S.pkeys[KMOD_NONE][K_KP7]
    S.pkeys[KMOD_NONE][K_END] = S.pkeys[KMOD_NONE][K_KP1]
    S.pkeys[KMOD_NONE][K_PAGEUP] = S.pkeys[KMOD_NONE][K_KP9]
    S.pkeys[KMOD_NONE][K_PAGEDOWN] = S.pkeys[KMOD_NONE][K_KP3]

    S.pkeys[KMOD_SHIFT][K_UP] = S.pkeys[KMOD_SHIFT][K_KP8]
    S.pkeys[KMOD_SHIFT][K_DOWN] = S.pkeys[KMOD_SHIFT][K_KP2]
    S.pkeys[KMOD_SHIFT][K_LEFT] = S.pkeys[KMOD_SHIFT][K_KP4]
    S.pkeys[KMOD_SHIFT][K_RIGHT] = S.pkeys[KMOD_SHIFT][K_KP6]

    S.pkeys[KMOD_NONE][1] = S.pkeys[KMOD_NONE][K_KP1]
    S.pkeys[KMOD_NONE][2] = S.pkeys[KMOD_NONE][K_KP2]
    S.pkeys[KMOD_NONE][3] = S.pkeys[KMOD_NONE][K_KP3]
    S.pkeys[KMOD_NONE][4] = S.pkeys[KMOD_NONE][K_KP4]
    S.pkeys[KMOD_NONE][6] = S.pkeys[KMOD_NONE][K_KP6]
    S.pkeys[KMOD_NONE][7] = S.pkeys[KMOD_NONE][K_KP7]
    S.pkeys[KMOD_NONE][8] = S.pkeys[KMOD_NONE][K_KP8]
    S.pkeys[KMOD_NONE][9] = S.pkeys[KMOD_NONE][K_KP9]

    S.pkeys[KMOD_NONE][' '] = S.pkeys[KMOD_NONE]['.']
    S.pkeys[KMOD_NONE]['+'] = S.pkeys[KMOD_NONE]['X']

    S.pkeys[KMOD_CTRL][K_c] = S.pkeys['ext']['quit'] 
    S.pkeys[KMOD_NONE][K_y] = S.pkeys['ext']['youpoly']
    S.pkeys[KMOD_ALT][K_2] = S.pkeys['ext']['2weapon']
    S.pkeys[KMOD_ALT][K_a] = S.pkeys['ext']['adjust']
    S.pkeys[KMOD_ALT][K_b] = S.pkeys['ext']['borrow']
    S.pkeys[KMOD_ALT][K_c] = S.pkeys['ext']['chat']
    S.pkeys[KMOD_ALT][K_d] = S.pkeys['ext']['dip']
    S.pkeys[KMOD_ALT][K_e] = S.pkeys['ext']['enhance']
    S.pkeys[KMOD_ALT][K_f] = S.pkeys['ext']['force']
    S.pkeys[KMOD_ALT][K_i] = S.pkeys['ext']['invoke']
    S.pkeys[KMOD_ALT][K_j] = S.pkeys['ext']['jump']
    S.pkeys[KMOD_ALT][K_l] = S.pkeys['ext']['loot']
    S.pkeys[KMOD_ALT][K_m] = S.pkeys['ext']['monster']
    S.pkeys[KMOD_ALT][K_n] = S.pkeys['ext']['name']
    S.pkeys[KMOD_ALT][K_o] = S.pkeys['ext']['offer']
    S.pkeys[KMOD_ALT][K_p] = S.pkeys['ext']['pray']
    S.pkeys[KMOD_ALT][K_q] = S.pkeys['ext']['quit']
    S.pkeys[KMOD_ALT][K_r] = S.pkeys['ext']['rub']
    S.pkeys[KMOD_ALT][K_s] = S.pkeys['ext']['sit']
    S.pkeys[KMOD_ALT][K_t] = S.pkeys['ext']['technique']
    S.pkeys[KMOD_ALT][K_u] = S.pkeys['ext']['untrap']
    S.pkeys[KMOD_ALT][K_w] = S.pkeys['ext']['wipe']
    S.pkeys[KMOD_ALT][K_y] = S.pkeys['ext']['youpoly']


    # Define actions for special debug mode keystrokes.
    if S.debug:
        S.pkeys[KMOD_CTRL][K_e] = KeyHandler(
            None, (), True, "Search an entire room.")
#        S.pkeys[KMOD_CTRL][K_f] = KeyHandler(
#            magic_mapping, (), False, "Map the entire level.")
        S.pkeys[KMOD_CTRL][K_f] = KeyHandler(
            request, ('^f', ()), False, "Map the entire level.")
        S.pkeys[KMOD_CTRL][K_g] = KeyHandler(
            None, (), True, "Create a monster.")
        S.pkeys[KMOD_CTRL][K_i] = KeyHandler(
            None, (), True, "Identify all items in inventory.")
        S.pkeys[KMOD_CTRL][K_j] = KeyHandler(
            None, (), True, "Go up one experience level.")
        S.pkeys[KMOD_CTRL][K_o] = KeyHandler(
            None, (), True, "Show the layout of the entire dungeon.")
        S.pkeys[KMOD_CTRL][K_v] = KeyHandler(
            None, (5, 6), True, "Level teleport.")
        S.pkeys[KMOD_CTRL][K_w] = KeyHandler(
            None, (), True, "Wish.")

        S.pkeys['ext']['levelchange'] = KeyHandler(
            None, (), True, "Change experience level.")
        S.pkeys['ext']['lightsources'] = KeyHandler(
            None, (), True, "Highlight light sources.")
        S.pkeys['ext']['monpolycontrol'] = KeyHandler(
            None, (), True, "Control polymorphs of monsters.")
        S.pkeys['ext']['panic'] = KeyHandler(
            None, (), True, "Test the panic system.")
        S.pkeys['ext']['polyself'] = KeyHandler(
            None, (), True, "Polymorph self.")
        S.pkeys['ext']['seenv'] = KeyHandler(
            None, (), True, "Show seen vectors.")
        S.pkeys['ext']['stats'] = KeyHandler(
            None, (), True, "Show memory statistics.")
        S.pkeys['ext']['timeout'] = KeyHandler(
            None, (), True, "Show timeout queue.")
        S.pkeys['ext']['vision'] = KeyHandler(
            None, (), True, "Highlight field of view.")
        S.pkeys['ext']['wmode'] = KeyHandler(
            None, (), True, "Show all wall modes.")

        # FIXME: This should actually be handled under #vision
        S.pkeys[KMOD_CTRL][K_z] = KeyHandler(show_fov, (), False)


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
