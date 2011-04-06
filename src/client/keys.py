# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

"""KeyHandler class and dictionaries use to map keys to handlers."""

import pygame.locals as pgl

import common.cfg as cfg
from client_state import ClientState as CS
from common.network import Network
from client_util import quit_game
import gui


def show_fov():
    """Toggle a flag to visually outline the FOV on the map."""
    CS.fov_outline = not CS.fov_outline


def scroll_map(coords):
    """Scroll the map in the direction given."""
    CS.x_scrollbar.move_slider(coords[0] * cfg.SCROLL_AMT)
    CS.y_scrollbar.move_slider(coords[1] * cfg.SCROLL_AMT)


def scroll_log(coords):
    """Scroll the log window up or down."""
    CS.log_scrollbar.move_slider(coords[1] * cfg.SCROLL_AMT)


def scroll_log_end(coords):
    """Scroll the log window all the way to the top or bottom."""
    CS.log_scrollbar.move_slider(coords[1] * CS.log_rect.h)


def request_pick_up():
    """Tell server to pick up an item at the player's feet."""
    items = []
    for item in CS.map.grid[CS.u.x][CS.u.y].items:
        items.append(item.oid)

    Network.request(',', (tuple(items),))


class KeyHandler(object):
    """Handle the actions of a specific keystroke."""
    def __init__(self, action, args, turn, desc=None):
        """Arguments:
        @param action: Action to perform when the key is pressed.
        @param args: List of arguments to give to action
        @param desc: Short description of what this keystroke does.
        """
        self.action = action
        self.args = args
        self.turn = turn
        self.desc = desc

    def perform_action(self):
        """Perform the action associated with this key press."""
        self.action(*self.args)


def attach_key_actions():
    """Set up dictionaries to map keys to actions."""

    # Keystroke handlers for 'playing' mode.
    # Accessed like pkeys[mod][KEY]
    # mod can be one of pgl.KMOD_NONE, pgl.KMOD_CTRL, pgl.KMOD_ALT
    CS.pkeys = {
        pgl.KMOD_NONE: {
            pgl.K_KP1: KeyHandler(CS.u.try_move, (cfg.DIRH['dl'],), ""),
            pgl.K_KP2: KeyHandler(CS.u.try_move, (cfg.DIRH['d'],), ""),
            pgl.K_KP3: KeyHandler(CS.u.try_move, (cfg.DIRH['dr'],), ""),
            pgl.K_KP4: KeyHandler(CS.u.try_move, (cfg.DIRH['l'],), ""),
            pgl.K_KP5: KeyHandler(None, (), ""),
            pgl.K_KP6: KeyHandler(CS.u.try_move, (cfg.DIRH['r'],), ""),
            pgl.K_KP7: KeyHandler(CS.u.try_move, (cfg.DIRH['ul'],), ""),
            pgl.K_KP8: KeyHandler(CS.u.try_move, (cfg.DIRH['u'],), ""),
            pgl.K_KP9: KeyHandler(CS.u.try_move, (cfg.DIRH['ur'],), ""),

            pgl.K_ESCAPE: KeyHandler(None, (), "Cancel command."),
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
            '.': KeyHandler(CS.u.rest, (), "Rest for one turn."),
            ':': KeyHandler(None, (),
                            "Describe the floor at the current location."),
            ';': KeyHandler(None, (),
                            "How is this different than '/'?"),
            ',': KeyHandler(
                request_pick_up, (),
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
            'd': KeyHandler(gui.inventory_menu, (cfg.DELETE_HEADER, 'drop'),
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
            'i': KeyHandler(gui.inventory_menu, (cfg.USE_HEADER, 'use'),
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
            'S': KeyHandler(
                Network.request, ('S', ()),
                "Save the game.  There is only one savefile per character, "
                "so this will overwrite any existing savefile.  This is by "
                "design."),
            'T': KeyHandler(None, (),
                            "Take off one piece of worn armor."),
            'U': KeyHandler(None, (), "Move"),
            'V': KeyHandler(None, (), "Show game history."),
            'W': KeyHandler(None, (), "Wear one piece of armor."),
            'X': KeyHandler(None, (), "List all known spells."),
            'Y': KeyHandler(None, (), "Move"),
            'Z': KeyHandler(None, (), "Zap (a.k.a. cast) a known spell."),
            },
        pgl.KMOD_SHIFT: {
            pgl.K_KP1: KeyHandler(scroll_map, (cfg.DIRH['dl'],),
                              "Scroll the map window."),
            pgl.K_KP2: KeyHandler(scroll_map, (cfg.DIRH['d'],),
                              "Scroll the map window."),
            pgl.K_KP3: KeyHandler(scroll_map, (cfg.DIRH['dr'],),
                              "Scroll the map window."),
            pgl.K_KP4: KeyHandler(scroll_map, (cfg.DIRH['l'],),
                              "Scroll the map window."),
            pgl.K_KP6: KeyHandler(scroll_map, (cfg.DIRH['r'],),
                              "Scroll the map window."),
            pgl.K_KP7: KeyHandler(scroll_map, (cfg.DIRH['ul'],),
                              "Scroll the map window."),
            pgl.K_KP8: KeyHandler(scroll_map, (cfg.DIRH['u'],),
                              "Scroll the map window."),
            pgl.K_KP9: KeyHandler(scroll_map, (cfg.DIRH['ur'],),
                              "Scroll the map window."),
            pgl.K_PAGEUP: KeyHandler(scroll_log, (cfg.DIRH['u'],),
                              "Scroll the log window up."),
            pgl.K_PAGEDOWN: KeyHandler(scroll_log, (cfg.DIRH['d'],),
                              "Scroll the log window down."),
            pgl.K_HOME: KeyHandler(scroll_log_end, (cfg.DIRH['u'],),
                              "Scroll the log window to the top."),
            pgl.K_END: KeyHandler(scroll_log_end, (cfg.DIRH['d'],),
                              "Scroll the log window to the bottom."),
            },
        pgl.KMOD_CTRL: {
            pgl.K_a: KeyHandler(None, (), "Re-do the previous command."),
            pgl.K_d: KeyHandler(
                None, (),
                "Kick something (usually something locked that you wish to "
                "open)."),
#            pgl.K_b: KeyHandler(None, (), "Move"),
#            pgl.K_h: KeyHandler(None, (), "Move"),
#            pgl.K_j: KeyHandler(None, (), "Move"),
#            pgl.K_k: KeyHandler(None, (), "Move"),
#            pgl.K_l: KeyHandler(None, (), "Move"),
#            pgl.K_n: KeyHandler(None, (), "Move"),
#            pgl.K_u: KeyHandler(None, (), "Move"),
#            pgl.K_y: KeyHandler(None, (), "Move"),
            pgl.K_t: KeyHandler(None, (), "Teleport, if you are able."),
            pgl.K_x: KeyHandler(None, (), ""),
            },
        pgl.KMOD_ALT: {
            pgl.K_QUESTION: KeyHandler(None, (),
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
    CS.pkeys[pgl.KMOD_NONE][pgl.K_UP] = CS.pkeys[pgl.KMOD_NONE][pgl.K_KP8]
    CS.pkeys[pgl.KMOD_NONE][pgl.K_DOWN] = CS.pkeys[pgl.KMOD_NONE][pgl.K_KP2]
    CS.pkeys[pgl.KMOD_NONE][pgl.K_LEFT] = CS.pkeys[pgl.KMOD_NONE][pgl.K_KP4]
    CS.pkeys[pgl.KMOD_NONE][pgl.K_RIGHT] = CS.pkeys[pgl.KMOD_NONE][pgl.K_KP6]
    CS.pkeys[pgl.KMOD_NONE][pgl.K_HOME] = CS.pkeys[pgl.KMOD_NONE][pgl.K_KP7]
    CS.pkeys[pgl.KMOD_NONE][pgl.K_END] = CS.pkeys[pgl.KMOD_NONE][pgl.K_KP1]
    CS.pkeys[pgl.KMOD_NONE][pgl.K_PAGEUP] = CS.pkeys[pgl.KMOD_NONE][pgl.K_KP9]
    CS.pkeys[pgl.KMOD_NONE][pgl.K_PAGEDOWN] = CS.pkeys[pgl.KMOD_NONE][pgl.K_KP3]

    CS.pkeys[pgl.KMOD_SHIFT][pgl.K_UP] = CS.pkeys[pgl.KMOD_SHIFT][pgl.K_KP8]
    CS.pkeys[pgl.KMOD_SHIFT][pgl.K_DOWN] = CS.pkeys[pgl.KMOD_SHIFT][pgl.K_KP2]
    CS.pkeys[pgl.KMOD_SHIFT][pgl.K_LEFT] = CS.pkeys[pgl.KMOD_SHIFT][pgl.K_KP4]
    CS.pkeys[pgl.KMOD_SHIFT][pgl.K_RIGHT] = CS.pkeys[pgl.KMOD_SHIFT][pgl.K_KP6]

    CS.pkeys[pgl.KMOD_NONE][1] = CS.pkeys[pgl.KMOD_NONE][pgl.K_KP1]
    CS.pkeys[pgl.KMOD_NONE][2] = CS.pkeys[pgl.KMOD_NONE][pgl.K_KP2]
    CS.pkeys[pgl.KMOD_NONE][3] = CS.pkeys[pgl.KMOD_NONE][pgl.K_KP3]
    CS.pkeys[pgl.KMOD_NONE][4] = CS.pkeys[pgl.KMOD_NONE][pgl.K_KP4]
    CS.pkeys[pgl.KMOD_NONE][6] = CS.pkeys[pgl.KMOD_NONE][pgl.K_KP6]
    CS.pkeys[pgl.KMOD_NONE][7] = CS.pkeys[pgl.KMOD_NONE][pgl.K_KP7]
    CS.pkeys[pgl.KMOD_NONE][8] = CS.pkeys[pgl.KMOD_NONE][pgl.K_KP8]
    CS.pkeys[pgl.KMOD_NONE][9] = CS.pkeys[pgl.KMOD_NONE][pgl.K_KP9]

    CS.pkeys[pgl.KMOD_NONE][' '] = CS.pkeys[pgl.KMOD_NONE]['.']
    CS.pkeys[pgl.KMOD_NONE]['+'] = CS.pkeys[pgl.KMOD_NONE]['X']

    CS.pkeys[pgl.KMOD_CTRL][pgl.K_c] = CS.pkeys['ext']['quit']
    CS.pkeys[pgl.KMOD_NONE][pgl.K_y] = CS.pkeys['ext']['youpoly']
    CS.pkeys[pgl.KMOD_ALT][pgl.K_2] = CS.pkeys['ext']['2weapon']
    CS.pkeys[pgl.KMOD_ALT][pgl.K_a] = CS.pkeys['ext']['adjust']
    CS.pkeys[pgl.KMOD_ALT][pgl.K_b] = CS.pkeys['ext']['borrow']
    CS.pkeys[pgl.KMOD_ALT][pgl.K_c] = CS.pkeys['ext']['chat']
    CS.pkeys[pgl.KMOD_ALT][pgl.K_d] = CS.pkeys['ext']['dip']
    CS.pkeys[pgl.KMOD_ALT][pgl.K_e] = CS.pkeys['ext']['enhance']
    CS.pkeys[pgl.KMOD_ALT][pgl.K_f] = CS.pkeys['ext']['force']
    CS.pkeys[pgl.KMOD_ALT][pgl.K_i] = CS.pkeys['ext']['invoke']
    CS.pkeys[pgl.KMOD_ALT][pgl.K_j] = CS.pkeys['ext']['jump']
    CS.pkeys[pgl.KMOD_ALT][pgl.K_l] = CS.pkeys['ext']['loot']
    CS.pkeys[pgl.KMOD_ALT][pgl.K_m] = CS.pkeys['ext']['monster']
    CS.pkeys[pgl.KMOD_ALT][pgl.K_n] = CS.pkeys['ext']['name']
    CS.pkeys[pgl.KMOD_ALT][pgl.K_o] = CS.pkeys['ext']['offer']
    CS.pkeys[pgl.KMOD_ALT][pgl.K_p] = CS.pkeys['ext']['pray']
    CS.pkeys[pgl.KMOD_ALT][pgl.K_q] = CS.pkeys['ext']['quit']
    CS.pkeys[pgl.KMOD_ALT][pgl.K_r] = CS.pkeys['ext']['rub']
    CS.pkeys[pgl.KMOD_ALT][pgl.K_s] = CS.pkeys['ext']['sit']
    CS.pkeys[pgl.KMOD_ALT][pgl.K_t] = CS.pkeys['ext']['technique']
    CS.pkeys[pgl.KMOD_ALT][pgl.K_u] = CS.pkeys['ext']['untrap']
    CS.pkeys[pgl.KMOD_ALT][pgl.K_w] = CS.pkeys['ext']['wipe']
    CS.pkeys[pgl.KMOD_ALT][pgl.K_y] = CS.pkeys['ext']['youpoly']

    # Define actions for special debug mode keystrokes.
    if CS.debug:
        CS.pkeys[pgl.KMOD_CTRL][pgl.K_e] = KeyHandler(
            None, (), "Search an entire room.")
#        CS.pkeys[pgl.KMOD_CTRL][pgl.K_f] = KeyHandler(
#            magic_mapping, (), "Map the entire level.")
        CS.pkeys[pgl.KMOD_CTRL][pgl.K_f] = KeyHandler(
            Network.request, ('^f', ()), "Map the entire level.")
        CS.pkeys[pgl.KMOD_CTRL][pgl.K_g] = KeyHandler(
            None, (), "Create a monster.")
        CS.pkeys[pgl.KMOD_CTRL][pgl.K_i] = KeyHandler(
            None, (), "Identify all items in inventory.")
        CS.pkeys[pgl.KMOD_CTRL][pgl.K_j] = KeyHandler(
            None, (), "Go up one experience level.")
        CS.pkeys[pgl.KMOD_CTRL][pgl.K_o] = KeyHandler(
            None, (), "Show the layout of the entire dungeon.")
        CS.pkeys[pgl.KMOD_CTRL][pgl.K_v] = KeyHandler(
            None, (5, 6), "Level teleport.")
        CS.pkeys[pgl.KMOD_CTRL][pgl.K_w] = KeyHandler(
            None, (), "Wish.")

        CS.pkeys['ext']['levelchange'] = KeyHandler(
            None, (), "Change experience level.")
        CS.pkeys['ext']['lightsources'] = KeyHandler(
            None, (), "Highlight light sources.")
        CS.pkeys['ext']['monpolycontrol'] = KeyHandler(
            None, (), "Control polymorphs of monsters.")
        CS.pkeys['ext']['panic'] = KeyHandler(
            None, (), "Test the panic system.")
        CS.pkeys['ext']['polyself'] = KeyHandler(
            None, (), "Polymorph self.")
        CS.pkeys['ext']['seenv'] = KeyHandler(
            None, (), "Show seen vectors.")
        CS.pkeys['ext']['stats'] = KeyHandler(
            None, (), "Show memory statistics.")
        CS.pkeys['ext']['timeout'] = KeyHandler(
            None, (), "Show timeout queue.")
        CS.pkeys['ext']['vision'] = KeyHandler(
            None, (), "Highlight field of view.")
        CS.pkeys['ext']['wmode'] = KeyHandler(
            None, (), "Show all wall modes.")

        # FIXME: This should actually be handled under #vision
        CS.pkeys[pgl.KMOD_CTRL][pgl.K_z] = KeyHandler(show_fov, (), False)

    # Dictionary of key presses to ignore.  Note that this includes
    # modifier keys, as they are handled above in the sections that
    # handle the key modified.
    CS.ignore_keys = {
        pgl.K_NUMLOCK: True,
        pgl.K_CAPSLOCK: True,
        pgl.K_SCROLLOCK: True,
        pgl.K_RSHIFT: True,
        pgl.K_LSHIFT: True,
        pgl.K_RCTRL: True,
        pgl.K_LCTRL: True,
        pgl.K_RALT: True,
        pgl.K_LALT: True,
        pgl.K_RMETA: True,
        pgl.K_LMETA: True,
        pgl.K_LSUPER: True,
        pgl.K_RSUPER: True,
        }
