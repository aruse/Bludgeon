# Copyright (c) 2011, Andy Ruse

import pygame
from pygame.locals import *
from pygame.color import THECOLORS as colors

from const import *

class GC:
    """Stores the controller state."""
    # Debug mode
    debug = True

    clock = None

    key = None       # The last key event
    button = None    # The last clicked mouse button
    
    # Whether or not an action has been handled this clock cycle
    action_handled = False
    
    # The map of the current level, a two dimensional array
    map = None

    branch = 'doom'
    dlevel = 1

    # A Hash of all levels.  Accessed like dlevel['doom'][1]
    dlevel_dict = {}

    # The player object
    u = None

    # Dict of all monsters and all items across all levels
    monsters_dict = {}
    items_dict = {}
    
    # List of all characters on the current level
    monsters = []

    # All free items (not in inventory) on the current level
    items = []

    # two dimensional array showing which locations are in the field of view
    fov_map = None

    # Whether or not we need to recompute the FOV
    fov_recompute = True

    # State of the game.
    state = ST_PLAYING

    menu = None
    menu_options = []

    # When state is 'targeting', set this to the function to call with
    # default_fontthe x, y coords targetted
    targeting_function = []
    targeting_item = None
    
    u_action = None

    # Messages in the game log to be output to the log surface.
    msgs = []

    # The complete history of commands used in this game
    cmd_history = []

    random_seed = None

    # The random number generator used for building maps and other data that
    # needs to be the same for all games using the same random seed.
    map_rand = None
    # The random number generator used for everything else.
    rand = None

    # The state of the random number generators
    map_rand_state = None
    rand_state = None

    # Keeps track of the oid of the next object to be created
    oid_seq = 1

    # Mapping of oids to objects
    obj_dict = {}

    fov_outline = False

    # Whether or not the message log has been updated this cycle.
    log_updated = True

    # Queue of actions coming from the client to the server.
    client_actions = None
    # Queue of responses from the server to the client.
    server_updates = None


    # Color definitions
    black = (0, 0, 0)
    darker_gray = (31, 31, 31)
    dark_gray = (63, 63, 63)
    gray = (128, 128, 128)
    light_gray = (191, 191, 191)
    white = (255, 255, 255)

    red = (255, 0, 0)
    orange = (255, 127, 0)
    yellow = (255, 255, 0)
    chartreuse = (127, 255, 0)
    green = (0, 255, 0)
    sea = (0, 255, 127)
    cyan = (0, 255, 255)
    sky = (0, 127, 255)
    blue = (0, 0, 255)
    violet = (127, 0, 255)
    magenta = (255, 0, 255)
    pink = (255, 0, 127)

    dark_red = (127, 0, 0)
    dark_orange = (127, 63, 0)
    dark_yellow = (127, 127, 0)
    dark_chartreuse = (63, 127, 0)
    dark_green = (0, 127, 0)
    dark_sea = (0, 127, 63)
    dark_cyan = (0, 127, 127)
    dark_sky = (0, 63, 127)
    dark_blue = (0, 0, 127)
    dark_violet = (63, 0, 127)
    dark_magenta = (127, 0, 127)
    dark_pink = (127, 0, 63)

    darker_red = (63, 0, 0)
    darker_orange = (63, 31, 0)
    darker_yellow = (63, 63, 0)
    darker_chartreuse = (31, 63, 0)
    darker_green = (0, 63, 0)
    darker_sea = (0, 63, 31)
    darker_cyan = (0, 63, 63)
    darker_sky = (0, 31, 63)
    darker_blue = (0, 0, 63)
    darker_violet = (31, 0, 63)
    darker_magenta = (63, 0, 63)
    darker_pink = (63, 0, 31)

    light_red = (255, 127, 127)
    light_orange = (255, 191, 127)
    light_yellow = (255, 255, 127)
    light_chartreuse = (191, 255, 127)
    light_green = (127, 255, 127)
    light_sea = (127, 255, 191)
    light_cyan = (127, 255, 255)
    light_sky = (127, 191, 255)
    light_blue = (127, 127, 255)
    light_violet = (191, 127, 255)
    light_magenta = (255, 127, 255)
    light_pink = (255, 127, 191)

    desaturated_red = (127, 63, 63)
    desaturated_orange = (127, 95, 63)
    desaturated_yellow = (127, 127, 63)
    desaturated_chartreuse = (95, 127, 63)
    desaturated_green = (63, 127, 63)
    desaturated_sea = (63, 127, 95)
    desaturated_cyan = (63, 127, 127)
    desaturated_sky = (63, 95, 127)
    desaturated_blue = (63, 63, 127)
    desaturated_violet = (95, 63, 127)
    desaturated_magenta = (127, 63, 127)
    desaturated_pink = (127, 63, 95)

    silver = (203, 203, 203)
    gold = (255, 255, 102)
    floor_blue = (71, 108, 108)

    log_bg_color = black
    # If the background is closer to black than white, use white for the font.
    # Otherwise, use black for the font
    if sum(log_bg_color) < sum(white):
        default_font_color = white
    else:
        default_font_color = black

    menu_font_color = black

    hp_bar_color = (200, 32, 32)
    hp_bar_bg_color = darker_red
    mp_bar_color = (32, 32, 200)
    mp_bar_bg_color = (0, 0, 95)
    xp_bar_color = (32, 200, 32)
    xp_bar_bg_color = darker_green

# From Slash'EM
#CLR_BLACK = (0, 0, 0)
#CLR_D_GRAY = (64, 64, 64)
#CLR_GRAY = (128, 128, 128)
#CLR_L_GRAY = (192, 192, 192)
#CLR_WHITE = (255, 255, 255)
#
#CLR_RED = (192, 0, 0)
#CLR_BROWN = (192, 128, 0)
#CLR_GREEN = (0, 192, 0)
#CLR_CYAN = (0, 192, 192)
#CLR_BLUE = (0, 0, 192)
#CLR_MAGENTA = (192, 0, 192)
#
#CLR_B_RED = (255, 0, 0)
#CLR_B_YELLOW = (255, 255, 0)
#CLR_B_ORANGE = (255, 192, 0)
#CLR_B_GREEN = (0, 255, 0)
#CLR_B_CYAN = (0, 255, 255)
#CLR_B_BLUE = (0, 0, 255)
#CLR_B_MAGENTA = (255, 0, 255)
