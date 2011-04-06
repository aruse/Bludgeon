# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

"""ClientState class"""

from collections import deque
from pygame import Rect

import common.cfg as cfg
from common.color import CLR


class ClientState(object):
    """
    Static class that stores any game client state that needs to be shared
    everywhere.
    """
    # Debug mode
    debug = True

    clock = None

    key = None       # The last key event
    button = None    # The last clicked mouse button

    # Whether or not an action has been handled this clock cycle
    action_handled = False

    tiles_img = None
    gray_tiles_img = None
    menu_bg_img = None

    tile_dict = None
    glyph_dict = None

    screen = None       # Root Surface
    log_surf = None     # Surface for the game log text
    eq_surf = None      # Surface to show player's equipment
    status_surf = None  # Surface for the character stats
    map_surf = None     # Surface for the current level map
    dialog_surf = None  # Surface for pop-up dialogs

    # Rects for the various surfaces
    log_rect = Rect(0, 0, 0, 0)
    eq_rect = Rect(0, 0, 0, 0)
    status_rect = Rect(0, 0, 0, 0)
    map_rect = Rect(0, 0, 0, 0)
    screen_rect = Rect(0, 0, 0, 0)
    dialog_rect = Rect(0, 0, 0, 0)

    logview_rect = Rect(0, 0, 0, 0)
    mapview_rect = Rect(0, 0, 0, 0)

    font = None
    font_h = None
    font_w = None

    # What to blit over an area that's not visible
    blank_tile = None

    # Cell locations to blit equipment on the equipment panel
    eq_hands = None
    eq_rweap = None
    eq_lweap = None
    eq_rring = None
    eq_lring = None
    eq_boots = None
    eq_armor = None
    eq_shirt = None
    eq_cloak = None
    eq_neck = None
    eq_eyes = None
    eq_quiver = None
    eq_light = None
    eq_head = None

    x_scrollbar = None
    y_scrollbar = None
    log_scrollbar = None

    pkeys = None
    ignore_keys = None

    menu = None
    menu_options = []

    # When state is 'targeting', set this to the function to call with
    # default_fontthe x, y coords targetted
    targeting_function = []
    targeting_item = None

    # The map of the current level, a two dimensional array
    map = None

    # The player object
    u = None

    branch = 'doom'
    dlevel = 1

    fov_outline = False

    mode = cfg.ST_PLAYING
    msgs = deque(maxlen=cfg.MAX_MSGS)

    # Color definitions
    log_bg_color = CLR['black']
    # If the background is closer to black than white, use white for the font.
    # Otherwise, use black for the font
    if sum(log_bg_color) < sum(CLR['white']):
        default_font_color = CLR['white']
    else:
        default_font_color = CLR['black']

    menu_font_color = CLR['black']

    hp_bar_color = (200, 32, 32)
    hp_bar_bg_color = (63, 0, 0)
    mp_bar_color = (32, 32, 200)
    mp_bar_bg_color = (0, 0, 95)
    xp_bar_color = (32, 200, 32)
    xp_bar_bg_color = (0, 63, 0)

