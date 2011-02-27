import pygame
from pygame.locals import *

from const import *

def init_gv():
    GV.font = pygame.font.SysFont('Arial', FONT_SIZE)
    GV.font_ph = GV.font.get_height()
    GV.font_pw = GV.font.size('X')[0]

    # Size of the map surface
    GV.map_pw = MAP_W * TILE_PW
    GV.map_ph = MAP_H * TILE_PH

    # Size of the alert surface
    GV.alert_pw = MAP_W * TILE_PW
    GV.alert_ph = GV.font_ph
    
    # Size of the status panel
    GV.status_pw = STATUS_W * GV.font_pw
    GV.status_ph = STATUS_H * GV.font_ph

    # Size of the equipment panel
    GV.eq_pw = EQ_W * TILE_PW
    GV.eq_ph = GV.status_ph

    # Size of the text buffer
    GV.text_pw = GV.map_pw - (GV.eq_pw + GV.status_pw)
    GV.text_ph = GV.status_ph

    # Size of the full game window
    GV.screen_pw = GV.map_pw
    GV.screen_ph = GV.map_ph + GV.status_ph

    # Locations to blit the various surfaces
    GV.map_px, GV.map_py = 0, GV.text_ph + GV.alert_ph
    GV.alert_px, GV.alert_py = 0, GV.text_ph
    GV.text_px, GV.text_py = 0, 0
    GV.eq_px, GV.eq_py = GV.text_pw, 0
    GV.status_px, GV.status_py = GV.eq_px + GV.eq_pw, 0

    # Locations to blit equipment on the equipment panel
    GV.eq_cent = (GV.eq_pw / 2.0 - TILE_PW / 2, GV.eq_ph / 2 - TILE_PW / 2)
    GV.eq_hands = GV.eq_cent
    GV.eq_rweap = (GV.eq_cent[0] - TILE_PW, GV.eq_cent[1])
    GV.eq_lweap = (GV.eq_cent[0] + TILE_PW, GV.eq_cent[1])
    GV.eq_rring = (GV.eq_cent[0] - TILE_PW, GV.eq_cent[1] + TILE_PH)
    GV.eq_lring = (GV.eq_cent[0] + TILE_PW, GV.eq_cent[1] + TILE_PH)
    GV.eq_boots = (GV.eq_cent[0], GV.eq_cent[1] + TILE_PH * 2)
    GV.eq_armor = (GV.eq_cent[0], GV.eq_cent[1] - TILE_PH)
    GV.eq_shirt = (GV.eq_cent[0] - TILE_PW, GV.eq_cent[1] - TILE_PH)
    GV.eq_cloak = (GV.eq_cent[0] + TILE_PW, GV.eq_cent[1] - TILE_PH)
    GV.eq_neck = (GV.eq_cent[0], GV.eq_cent[1] - TILE_PH * 2)
    GV.eq_eyes = (GV.eq_cent[0] - TILE_PW, GV.eq_cent[1] - TILE_PH * 2)
    GV.eq_quiver = (GV.eq_cent[0] + TILE_PW * 2, GV.eq_cent[1] - TILE_PH * 3)
    GV.eq_light = (GV.eq_cent[0] - TILE_PW * 2, GV.eq_cent[1] - TILE_PH * 3)
    GV.eq_head = (GV.eq_cent[0], GV.eq_cent[1] - TILE_PH * 3)


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

    screen = None
    
    # pygame Surface for the current level
    map_surf = None
    
    # pygame Surface for the character stats
    status_surf = None

    # pygame Surface for the text buffer
    text_surf = None

    alert_surf = None
    eq_surf = None
    
    font = None
    font_ph = None
    
    # What to blit over an area that's not visible
    blank_tile = None
    
    map_pw, map_ph = None, None
    alert_pw, alert_ph = None, None
    status_pw, status_ph = None, None
    eq_pw, eq_ph = None, None
    text_pw, text_ph = None, None
    screen_pw, screen_ph = None, None

    # Locations to blit the various surfaces
    map_px, map_py = None, None
    alert_px, alert_py = None, None
    text_px, text_py = None, None
    eq_px, eq_py = None, None
    status_px, status_py = None, None

    # Locations to blit equipment on the equipment panel
    eq_cent = None
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
