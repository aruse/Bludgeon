import pygame
from pygame.locals import *

from const import *

def init_gv():
    GV.font = pygame.font.SysFont('Arial', FONT_SIZE)
    GV.font_h = GV.font.get_height()
    GV.font_w = GV.font.size('X')[0]

    # Size of the map surface
    GV.map_w = MAP_W * TILE_W
    GV.map_h = MAP_H * TILE_H

    # Size of the status panel
    GV.status_w = STATUS_W * GV.font_w
    GV.status_h = STATUS_H * GV.font_h

    # Size of the equipment panel
    GV.eq_w = EQ_W * TILE_W
    GV.eq_h = GV.status_h

    # Size of the full game window
    GV.screen_w = int(GV.map_w * .7)
    GV.screen_h = int(GV.map_h * .7) + GV.status_h

    # Size of the log window
    GV.log_w = GV.screen_w - (GV.eq_w + GV.status_w)
    GV.log_h = GV.status_h

    # The map window size.  Maybe be smaller than the actual map size.
    GV.map_window_w = GV.screen_w
    GV.map_window_h = GV.screen_h - GV.status_h

    # Locations to blit the various surfaces
    GV.map_x, GV.map_y = 0, GV.log_h
    GV.map_window_x, GV.map_window_y = 0, GV.log_h
    GV.log_x, GV.log_y = 0, 0
    GV.eq_x, GV.eq_y = GV.log_w, 0
    GV.status_x, GV.status_y = GV.eq_x + GV.eq_w, 0

    # Locations to blit equipment on the equipment panel
    GV.eq_cent = (GV.eq_w / 2.0 - TILE_W / 2, GV.eq_h / 2 - TILE_W / 2)
    GV.eq_hands = GV.eq_cent
    GV.eq_rweap = (GV.eq_cent[0] - TILE_W, GV.eq_cent[1])
    GV.eq_lweap = (GV.eq_cent[0] + TILE_W, GV.eq_cent[1])
    GV.eq_rring = (GV.eq_cent[0] - TILE_W, GV.eq_cent[1] + TILE_H)
    GV.eq_lring = (GV.eq_cent[0] + TILE_W, GV.eq_cent[1] + TILE_H)
    GV.eq_boots = (GV.eq_cent[0], GV.eq_cent[1] + TILE_H * 2)
    GV.eq_armor = (GV.eq_cent[0], GV.eq_cent[1] - TILE_H)
    GV.eq_shirt = (GV.eq_cent[0] - TILE_W, GV.eq_cent[1] - TILE_H)
    GV.eq_cloak = (GV.eq_cent[0] + TILE_W, GV.eq_cent[1] - TILE_H)
    GV.eq_neck = (GV.eq_cent[0], GV.eq_cent[1] - TILE_H * 2)
    GV.eq_eyes = (GV.eq_cent[0] - TILE_W, GV.eq_cent[1] - TILE_H * 2)
    GV.eq_quiver = (GV.eq_cent[0] + TILE_W * 2, GV.eq_cent[1] - TILE_H * 3)
    GV.eq_light = (GV.eq_cent[0] - TILE_W * 2, GV.eq_cent[1] - TILE_H * 3)
    GV.eq_head = (GV.eq_cent[0], GV.eq_cent[1] - TILE_H * 3)


class GC:
    """Stores the controller state."""
    clock = None

    key = None       # The key currently held down
    prev_key = None  # The key from last clock cycle

    button = None
    
    # Number of clock cycles the key has been held down
    key_held = 0
    
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

    # When state is 'targeting', set this to the function to call with the x, y coords targetted
    targeting_function = []
    targeting_item = None
    
    u_action = None

    # Messages to put in the log window
    msgs = []

    # The complete history of commands used in this game
    cmd_history = []

    random_seed = 1

    # Keeps track of the oid of the next object to be created
    oid_seq = 1

    # Mapping of oids to objects
    obj_dict = {}

    # The state of the random number generator
    random_state = None

    
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

    # pygame Surface for the log window
    log_surf = None

    eq_surf = None

    window_surf = None
    
    font = None
    font_h = None
    
    # What to blit over an area that's not visible
    blank_tile = None
    
    # Pixel size of various surfaces
    map_w, map_h = None, None
    map_rect = None
    status_w, status_h = None, None
    eq_w, eq_h = None, None
    log_w, log_h = None, None
    screen_w, screen_h = None, None
    map_window_w, map_window_h = None, None

    # Pixel locations to blit the various surfaces
    map_x, map_y = None, None
    map_window_x, map_window_y = None, None
    log_x, log_y = None, None
    eq_x, eq_y = None, None
    status_x, status_y = None, None
    window_x, window_y = None, None
    
    # Cell locations to blit equipment on the equipment panel
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
    floor_blue = (71, 108, 108)

    log_bg_color = dark_gray
    if sum(log_bg_color) < sum(white):
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
