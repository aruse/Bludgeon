import pygame
from pygame.locals import *

from const import *


class GC:
    """Stores the controller state."""
    clock = None

    key = None       # The key currently held down
    prev_key = None  # The key from last clock cycle

    # Number of clock cycles the key has been held down
    key_held = 0
    
    # Whether or not an action has been handled this clock cycle
    action_handled = False
    
    # The map of the current level, a two dimensional array
    map = None

    # A Hash of all levels.  Accessed like dlevel{"Doom"}[1]
    dlevel = None

    # The player object
    u = None

    # List of all characters on the current level
    monsters = []

    # All free items (not in inventory) on the current level
    items = []

    # two dimensional array showing which locations are in the field of view
    fov_map = None

    # Whether or not we need to recompute the FOV
    fov_recompute = True

    # State of the game.  Can be one of 'playing', 'exit', or 'menu'
    state = 'playing'

    u_action = None

    # Messages to put in the text buffer
    msgs = []

class GV:
    """Stores the view state."""
    tiles_img = None
    gray_tiles_img = None
    
    tile_dict = None
    glyph_dict = None

    background = None
    screen = None
    
    # pygame Surface for the current level
    map_surf = None
    
    # pygame Surface for the character stats
    status_surf = None

    # pygame Surface for the text buffer
    text_surf = None

    font = None

    # What to blit over an area that's not visible
    blank_tile = None
    
    # Size of the map surface
    map_pw = MAP_W * TILE_PW
    map_ph = MAP_H * TILE_PH

    # Size of the status panel
    status_pw = (STATUS_W * FONT_SIZE) / 2
    status_ph = STATUS_H * FONT_SIZE

    # Size of the equipment panel
    eq_pw = EQ_W * TILE_PW
    eq_ph = status_ph

    # Size of the text buffer
    text_pw = map_pw - (eq_pw + status_pw)
    text_ph = status_ph

    # Size of the full game window
    screen_pw = map_pw
    screen_ph = map_ph + status_ph

    # Locations to blit the various surfaces
    map_px, map_py = 0, status_ph
    text_px, text_py = 0, 0
    eq_px, eq_py = text_pw, 0
    status_px, status_py = eq_px + eq_pw, 0

    # Locations to blit equipment on the equipment panel
    eq_cent = (eq_pw / 2.0 - TILE_PW / 2, eq_ph / 2 - TILE_PW / 2)
    eq_hands = eq_cent
    eq_rweap = (eq_cent[0] - TILE_PW, eq_cent[1])
    eq_lweap = (eq_cent[0] + TILE_PW, eq_cent[1])
    eq_rring = (eq_cent[0] - TILE_PW, eq_cent[1] + TILE_PH)
    eq_lring = (eq_cent[0] + TILE_PW, eq_cent[1] + TILE_PH)
    eq_boots = (eq_cent[0], eq_cent[1] + TILE_PH * 2)
    eq_armor = (eq_cent[0], eq_cent[1] - TILE_PH)
    eq_shirt = (eq_cent[0] - TILE_PW, eq_cent[1] - TILE_PH)
    eq_cloak = (eq_cent[0] + TILE_PW, eq_cent[1] - TILE_PH)
    eq_neck = (eq_cent[0], eq_cent[1] - TILE_PH * 2)
    eq_eyes = (eq_cent[0] - TILE_PW, eq_cent[1] - TILE_PH * 2)
    eq_quiver = (eq_cent[0] + TILE_PW * 2, eq_cent[1] - TILE_PH * 3)
    eq_light = (eq_cent[0] - TILE_PW * 2, eq_cent[1] - TILE_PH * 3)
    eq_head = (eq_cent[0], eq_cent[1] - TILE_PH * 3)

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

    text_bg_color = black
    if sum(text_bg_color) < sum(white):
        default_font_color = white
    else:
        default_font_color = black




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
