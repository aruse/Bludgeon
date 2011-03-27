# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

"""KeyHandler class and dictionaries use to map keys to handlers."""

import pygame
from pygame.locals import *

from const import *
from client import Client as C
from network import Network

from util import *
from client_monster import *
from client_item import *
from client_cell import *
from gui import *
from stuff import *


class KeyHandler:
    """Handle the actions of a specific keystroke."""
    def __init__(self, action, args, turn, desc=None):
        """Arguments:
        @param action: Action to perform when the key is pressed.
        @param args: List of arguments to give to action
        @param desc: Short description of what this keystroke does.
        """
        self.action = action
        self.args = args

    def do(self):
        """Perform the action associated with this key press."""
        self.action(*self.args)


def attach_key_actions():
    """Set up dictionaries to map keys to actions."""
    
    # Keystroke handlers for 'playing' mode.
    # Accessed like pkeys[mod][KEY]
    # mod can be one of KMOD_NONE, KMOD_CTRL, KMOD_ALT
    C.pkeys = {
        KMOD_NONE: {
            K_KP1: KeyHandler(C.u.try_move, (DIRH['dl'],), ""),
            K_KP2: KeyHandler(C.u.try_move, (DIRH['d'],), ""),
            K_KP3: KeyHandler(C.u.try_move, (DIRH['dr'],), ""),
            K_KP4: KeyHandler(C.u.try_move, (DIRH['l'],), ""),
            K_KP5: KeyHandler(None, (), ""),
            K_KP6: KeyHandler(C.u.try_move, (DIRH['r'],), ""),
            K_KP7: KeyHandler(C.u.try_move, (DIRH['ul'],), ""),
            K_KP8: KeyHandler(C.u.try_move, (DIRH['u'],), ""),
            K_KP9: KeyHandler(C.u.try_move, (DIRH['ur'],), ""),

            K_ESCAPE: KeyHandler(None, (), "Cancel command."),
            '^': KeyHandler(None, (), "Examine a trap."),
            '<': KeyHandler(None, (), "Go up a staircase or ladder."),
            '>': KeyHandler(None, (), "Go down a staircase or ladder."),
            '/': KeyHandler(None, (),
                            "Describe a particular symbol on the map."),
            '?': KeyHandler(None, (), "Open the help menu."),
            '&': KeyHandler(None, (),
                            "Explain what the following command does."),
            '`': KeyHandler(None, (), "Open the command menu."),
            '\\': KeyHandler(None, (),
                             "List which objects have been discovered."),
            '_': KeyHandler(None, (),
                            "Travel to a particular point on the map."),
            '.': KeyHandler(C.u.rest, (), "Rest for one turn."),
            ':': KeyHandler(None, (),
                            "Describe the floor at the current location."),
            ';': KeyHandler(None, (),
                            "How is this different than '/'?"),
            ',': KeyHandler(
                client_pick_up, (),
                "Pick things up from the current location.  May be preceded "
                "by 'm' to select which things to pick up."),
            '@': KeyHandler(None, (), "Toggle the autopickup option.  "
                            "When this option is on, you will automatically "
                            "pick up any item that you walk over."),
            '(': KeyHandler(None, (), "Show the currently used tools."),
            ')': KeyHandler(None, (),
                            "Show the currently wielded weapon."),
            '[': KeyHandler(None, (), "Show the currently worn armor."),
            '=': KeyHandler(None, (), "Show the currently worn rings."),
            '"': KeyHandler(None, (), "Show the currently worn amulet."),
            '$': KeyHandler(None, (),
                            "Count all of your gold pieces in all of your "
                            "carried containers."),
            '#': KeyHandler(None, (), "Perform an extended command.  "
                            "You'll be given a list of extended commands and "
                            "be prompted to type which one you want to use."),
            '*': KeyHandler(None, (), "Show all worn equipment."),
            'a': KeyHandler(
                None, (),
                "Apply (a.k.a. use) a tool, such as a bag, torch, pick-axe, "
                "etc."),
            'b': KeyHandler(None, (), "Move"),
            'c': KeyHandler(None, (), "Close a door"),
            'd': KeyHandler(inventory_menu, (DELETE_HEADER, 'drop'),
                            "Drop one item from your inventory."),
            'e': KeyHandler(
                None, (),
                "Eat something, either from your inventory or the ground at "
                "your location.  If you are a vampire, instead drain blood"
                "from a corpse."),
            'f': KeyHandler(
                None, (),
                "Fire objects in your quiver.  You will launch them using the "
                "currently equiped weapon (such as a bow) if it makes sense "
                "to do so."),
            'g': KeyHandler(
                None, (),
                "Prefix: When followed by a direction, move until you are "
                "next to something interesting."),
            'h': KeyHandler(None, (), "Move"),
            'i': KeyHandler(inventory_menu, (USE_HEADER, 'use'),
                            "Show your current inventory."),
            'j': KeyHandler(None, (), "Move"),
            'k': KeyHandler(None, (), "Move"),
            'l': KeyHandler(None, (), "Move"),
            'm': KeyHandler(
                None, (),
                "Prefix: When followed by a direction, move without fighting "
                "or picking anything up."),
            'n': KeyHandler(None, (), "Move"),
            'o': KeyHandler(None, (), "Open a door."),
            'p': KeyHandler(
                None, (),
                "Pay a shopkeeper for items or inquire about shopkeeper "
                "services."),
            'q': KeyHandler(
                None, (),
                "Quaff (a.k.a. drink) something.  Usually a potion or a "
                "water source."),
            'r': KeyHandler(
                None, (),
                "Read something.  Usually a scroll, a spellbook, or writing "
                "on the floor."),
            's': KeyHandler(None, (),
                            "Search for traps or secret doors for one turn."),
            't': KeyHandler(None, (),
                            "Throw something, usually a weapon."),
            'u': KeyHandler(None, (), "Move"),
            'v': KeyHandler(None, (), "Display the software version."),
            'w': KeyHandler(
                None, (), 
                "Wield (a.k.a. put in your hand, ready to use) a weapon.  "
                "In order to wield nothing and fight with your bare hands, "
                "use '-' when asked for which weapon to wield."),
            'x': KeyHandler(
                None, (),
                "Exchange your wielded weapon with your secondary weapon.  "
                "If you have no secondary weapon, move your wielded weapon to "
                "your secondary weapon and fight with your bare hands."),
            'y': KeyHandler(None, (), "Move"),
            'z': KeyHandler(None, (), "Zap a wand."),
            'A': KeyHandler(None, (), "Remove all worn armor."),
            'B': KeyHandler(None, (), "Move"),
            'C': KeyHandler(
                None, (),
                "Call (a.k.a. name) an individual monster.  Useful if you "
                "want to be able to distinguish between monsters in combat."),
            'D': KeyHandler(None, (),
                            "Drop several items from your inventory."),
            'E': KeyHandler(
                None, (),
                "Engrave on the floor.  You can use a weapon, or type '-' to "
                "write with your fingers.  There are other items with which "
                "you can engrave as well."),
            'F': KeyHandler(None, (),
                            "Fight a monster in a particular direction."),
            'G': KeyHandler(
                None, (),
                "Prefix: When followed by a direction, fight a monster, even "
                "if you're not sure if there's a monster there."),
            'H': KeyHandler(None, (), "Move"),
            'I': KeyHandler(None, (),
                            "List sub-groups of items in your inventory."),
            'J': KeyHandler(None, (), "Move"),
            'K': KeyHandler(None, (), "Move"),
            'L': KeyHandler(None, (), "Move"),
            'M': KeyHandler(None, (), "Move"),
            'N': KeyHandler(None, (), "Move"),
            'O': KeyHandler(None, (), "Set game options."),
            'P': KeyHandler(
                None, (),
                "Put on an accessory, such as a ring, amulet, or blindfold."),
            'Q': KeyHandler(
                None, (),
                "Put ammunition into your quiver.  This ammunition will then "
                "be used with the 'f' command."),
            'R': KeyHandler(
                None, (),
                "Remove a worn accessory, such as a ring, amulet, or "
                "blindfold."),
#            'S': KeyHandler(
#                save_game, ('save.bludgeon',),
#                "Save the game.  There is only one savefile per character, "
#                "so this will overwrite any existing savefile.  This is by "
#                "design."),
            'T': KeyHandler(None, (),
                            "Take off one piece of worn armor."),
            'U': KeyHandler(None, (), "Move"),
            'V': KeyHandler(None, (), "Show game history."),
            'W': KeyHandler(None, (), "Wear one piece of armor."),
            'X': KeyHandler(None, (), "List all known spells."),
            'Y': KeyHandler(None, (), "Move"),
            'Z': KeyHandler(None, (), "Zap (a.k.a. cast) a known spell."),
            },
        KMOD_SHIFT: {
            K_KP1: KeyHandler(scroll_map, (DIRH['dl'],),
                              "Scroll the map window."),
            K_KP2: KeyHandler(scroll_map, (DIRH['d'],),
                              "Scroll the map window."),
            K_KP3: KeyHandler(scroll_map, (DIRH['dr'],),
                              "Scroll the map window."),
            K_KP4: KeyHandler(scroll_map, (DIRH['l'],),
                              "Scroll the map window."),
            K_KP6: KeyHandler(scroll_map, (DIRH['r'],),
                              "Scroll the map window."),
            K_KP7: KeyHandler(scroll_map, (DIRH['ul'],),
                              "Scroll the map window."),
            K_KP8: KeyHandler(scroll_map, (DIRH['u'],),
                              "Scroll the map window."),
            K_KP9: KeyHandler(scroll_map, (DIRH['ur'],),
                              "Scroll the map window."),
            K_PAGEUP: KeyHandler(scroll_log, (DIRH['u'],),
                              "Scroll the log window up."),
            K_PAGEDOWN: KeyHandler(scroll_log, (DIRH['d'],),
                              "Scroll the log window down."),
            K_HOME: KeyHandler(scroll_log_end, (DIRH['u'],),
                              "Scroll the log window to the top."),
            K_END: KeyHandler(scroll_log_end, (DIRH['d'],),
                              "Scroll the log window to the bottom."),
            },
        KMOD_CTRL: {
            K_a: KeyHandler(None, (), "Re-do the previous command."),
            K_d: KeyHandler(
                None, (),
                "Kick something (usually something locked that you wish to "
                "open)."),
#            K_b: KeyHandler(None, (), "Move"),
#            K_h: KeyHandler(None, (), "Move"),
#            K_j: KeyHandler(None, (), "Move"),
#            K_k: KeyHandler(None, (), "Move"),
#            K_l: KeyHandler(None, (), "Move"),
#            K_n: KeyHandler(None, (), "Move"),
#            K_u: KeyHandler(None, (), "Move"),
#            K_y: KeyHandler(None, (), "Move"),
            K_t: KeyHandler(None, (), "Teleport, if you are able."),
            K_x: KeyHandler(None, (), ""),
            },
        KMOD_ALT: {
            K_QUESTION: KeyHandler(None, (),
                                   "Display help with extended commands."),
            },
        'ext': {
            '2weapon': KeyHandler(
                None, (),
                "Wield both your primary and secondary weapons "
                "simultaneously."),
            'adjust': KeyHandler(
                None, (),
                "Adjust which inventory letters are assigned to which items."),
            'borrow': KeyHandler(None, (),
                                 "Attempt to steal from a someone."),
            'chat': KeyHandler(None, (), "Talk to someone."),
            'conduct': KeyHandler(
                None, (),
                "List which voluntary challenges you've followed so far."),
            'dip': KeyHandler(None, (), "Dip an object into something."),
            'enhance': KeyHandler(
                None, (),
                "Advance or check character skills."),
            'force': KeyHandler(None, (),
                                "Attempt to force open a lock."),
            'invoke': KeyHandler(None, (),
                                 "Invoke the special powers of an artifact."),
            'jump': KeyHandler(None, (), "Jump."),
            'loot': KeyHandler(
                None, (),
                "Loot a box or bag in the same location as you, or remove "
                "the saddle from a horse."),
            'monster': KeyHandler(
                None, (),
                "When polymorphed into a monster, use that monster's special "
                "ability."),
            'name': KeyHandler(
                None, (),
                "Add a label to a specific item or class of items."),
            'offer': KeyHandler(None, (), "Offer a sacrifice to a god."),
            'pray': KeyHandler(None, (), "Pray to a god for help."),
            'quit': KeyHandler(
                quit_game, (),
                "Quit the game permanently.  This will end your character's "
                "life, and you'll have to start over with a new character."),
            'rub': KeyHandler(
                None, (),
                "Rub something (usually a lamp or a stone)."),
            'sit': KeyHandler(None, (),
                              "Sit on the floor or on an object."),
            'technique': KeyHandler(
                None, (),
                "Use a special technique available to your role or race."),
            'untrap': KeyHandler(
                None, (), "Attempt to disarm a trap."),
            'vanquished': KeyHandler(
                None, (),
                "Show a list of all monsters vanquished in this game."),
            'wipe': KeyHandler(None, (), "Wipe your face."),
            'youpoly': KeyHandler(
                None, (), "Polymorph, if you are able."),
            }
        }


    # Key bindings that do the same as ones already defined above.
    C.pkeys[KMOD_NONE][K_UP] = C.pkeys[KMOD_NONE][K_KP8]
    C.pkeys[KMOD_NONE][K_DOWN] = C.pkeys[KMOD_NONE][K_KP2]
    C.pkeys[KMOD_NONE][K_LEFT] = C.pkeys[KMOD_NONE][K_KP4]
    C.pkeys[KMOD_NONE][K_RIGHT] = C.pkeys[KMOD_NONE][K_KP6]
    C.pkeys[KMOD_NONE][K_HOME] = C.pkeys[KMOD_NONE][K_KP7]
    C.pkeys[KMOD_NONE][K_END] = C.pkeys[KMOD_NONE][K_KP1]
    C.pkeys[KMOD_NONE][K_PAGEUP] = C.pkeys[KMOD_NONE][K_KP9]
    C.pkeys[KMOD_NONE][K_PAGEDOWN] = C.pkeys[KMOD_NONE][K_KP3]

    C.pkeys[KMOD_SHIFT][K_UP] = C.pkeys[KMOD_SHIFT][K_KP8]
    C.pkeys[KMOD_SHIFT][K_DOWN] = C.pkeys[KMOD_SHIFT][K_KP2]
    C.pkeys[KMOD_SHIFT][K_LEFT] = C.pkeys[KMOD_SHIFT][K_KP4]
    C.pkeys[KMOD_SHIFT][K_RIGHT] = C.pkeys[KMOD_SHIFT][K_KP6]

    C.pkeys[KMOD_NONE][1] = C.pkeys[KMOD_NONE][K_KP1]
    C.pkeys[KMOD_NONE][2] = C.pkeys[KMOD_NONE][K_KP2]
    C.pkeys[KMOD_NONE][3] = C.pkeys[KMOD_NONE][K_KP3]
    C.pkeys[KMOD_NONE][4] = C.pkeys[KMOD_NONE][K_KP4]
    C.pkeys[KMOD_NONE][6] = C.pkeys[KMOD_NONE][K_KP6]
    C.pkeys[KMOD_NONE][7] = C.pkeys[KMOD_NONE][K_KP7]
    C.pkeys[KMOD_NONE][8] = C.pkeys[KMOD_NONE][K_KP8]
    C.pkeys[KMOD_NONE][9] = C.pkeys[KMOD_NONE][K_KP9]

    C.pkeys[KMOD_NONE][' '] = C.pkeys[KMOD_NONE]['.']
    C.pkeys[KMOD_NONE]['+'] = C.pkeys[KMOD_NONE]['X']

    C.pkeys[KMOD_CTRL][K_c] = C.pkeys['ext']['quit'] 
    C.pkeys[KMOD_NONE][K_y] = C.pkeys['ext']['youpoly']
    C.pkeys[KMOD_ALT][K_2] = C.pkeys['ext']['2weapon']
    C.pkeys[KMOD_ALT][K_a] = C.pkeys['ext']['adjust']
    C.pkeys[KMOD_ALT][K_b] = C.pkeys['ext']['borrow']
    C.pkeys[KMOD_ALT][K_c] = C.pkeys['ext']['chat']
    C.pkeys[KMOD_ALT][K_d] = C.pkeys['ext']['dip']
    C.pkeys[KMOD_ALT][K_e] = C.pkeys['ext']['enhance']
    C.pkeys[KMOD_ALT][K_f] = C.pkeys['ext']['force']
    C.pkeys[KMOD_ALT][K_i] = C.pkeys['ext']['invoke']
    C.pkeys[KMOD_ALT][K_j] = C.pkeys['ext']['jump']
    C.pkeys[KMOD_ALT][K_l] = C.pkeys['ext']['loot']
    C.pkeys[KMOD_ALT][K_m] = C.pkeys['ext']['monster']
    C.pkeys[KMOD_ALT][K_n] = C.pkeys['ext']['name']
    C.pkeys[KMOD_ALT][K_o] = C.pkeys['ext']['offer']
    C.pkeys[KMOD_ALT][K_p] = C.pkeys['ext']['pray']
    C.pkeys[KMOD_ALT][K_q] = C.pkeys['ext']['quit']
    C.pkeys[KMOD_ALT][K_r] = C.pkeys['ext']['rub']
    C.pkeys[KMOD_ALT][K_s] = C.pkeys['ext']['sit']
    C.pkeys[KMOD_ALT][K_t] = C.pkeys['ext']['technique']
    C.pkeys[KMOD_ALT][K_u] = C.pkeys['ext']['untrap']
    C.pkeys[KMOD_ALT][K_w] = C.pkeys['ext']['wipe']
    C.pkeys[KMOD_ALT][K_y] = C.pkeys['ext']['youpoly']


    # Define actions for special debug mode keystrokes.
    if C.debug:
        C.pkeys[KMOD_CTRL][K_e] = KeyHandler(
            None, (), "Search an entire room.")
#        C.pkeys[KMOD_CTRL][K_f] = KeyHandler(
#            magic_mapping, (), "Map the entire level.")
        C.pkeys[KMOD_CTRL][K_f] = KeyHandler(
            Network.request, ('^f', ()), "Map the entire level.")
        C.pkeys[KMOD_CTRL][K_g] = KeyHandler(
            None, (), "Create a monster.")
        C.pkeys[KMOD_CTRL][K_i] = KeyHandler(
            None, (), "Identify all items in inventory.")
        C.pkeys[KMOD_CTRL][K_j] = KeyHandler(
            None, (), "Go up one experience level.")
        C.pkeys[KMOD_CTRL][K_o] = KeyHandler(
            None, (), "Show the layout of the entire dungeon.")
        C.pkeys[KMOD_CTRL][K_v] = KeyHandler(
            None, (5, 6), "Level teleport.")
        C.pkeys[KMOD_CTRL][K_w] = KeyHandler(
            None, (), "Wish.")

        C.pkeys['ext']['levelchange'] = KeyHandler(
            None, (), "Change experience level.")
        C.pkeys['ext']['lightsources'] = KeyHandler(
            None, (), "Highlight light sources.")
        C.pkeys['ext']['monpolycontrol'] = KeyHandler(
            None, (), "Control polymorphs of monsters.")
        C.pkeys['ext']['panic'] = KeyHandler(
            None, (), "Test the panic system.")
        C.pkeys['ext']['polyself'] = KeyHandler(
            None, (), "Polymorph self.")
        C.pkeys['ext']['seenv'] = KeyHandler(
            None, (), "Show seen vectors.")
        C.pkeys['ext']['stats'] = KeyHandler(
            None, (), "Show memory statistics.")
        C.pkeys['ext']['timeout'] = KeyHandler(
            None, (), "Show timeout queue.")
        C.pkeys['ext']['vision'] = KeyHandler(
            None, (), "Highlight field of view.")
        C.pkeys['ext']['wmode'] = KeyHandler(
            None, (), "Show all wall modes.")

        # FIXME: This should actually be handled under #vision
        C.pkeys[KMOD_CTRL][K_z] = KeyHandler(show_fov, (), False)


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
