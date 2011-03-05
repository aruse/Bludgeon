import pygame
from pygame.locals import *

from const import *

def move_surface_locations():
    """Set the x,y coords for each of the game's surfaces."""
    GV.map_rect.x, GV.map_rect.y = 0, GV.status_rect.h
    GV.mapview_rect.x, GV.mapview_rect.y = 0, GV.status_rect.h

    GV.log_rect.x, GV.log_rect.y = 0, 0
    GV.logview_rect.x, GV.logview_rect.y = 0, 0

    GV.eq_rect.x, GV.eq_rect.y = GV.logview_rect.w + SCROLLBAR_W, 0
    GV.status_rect.x, GV.status_rect.y = GV.eq_rect.x + GV.eq_rect.w, 0

def init_gv():
    GV.font = pygame.font.SysFont('Arial', FONT_SIZE)
    GV.font_h = GV.font.get_height()
    GV.font_w = GV.font.size('X')[0]

    # Size of the map surface
    GV.map_rect.w = (MAP_W + 2) * TILE_W 
    GV.map_rect.h = (MAP_H + 2) * TILE_H

    # Size of the status panel
    GV.status_rect.w = STATUS_W * GV.font_w
    GV.status_rect.h = STATUS_H * GV.font_h

    # Size of the equipment panel
    GV.eq_rect.w = EQ_W * TILE_W
    GV.eq_rect.h = GV.status_rect.h

    # Size of the full game screen
    GV.screen_rect.w = GV.eq_rect.w + GV.status_rect.w + 400
    GV.screen_rect.h = GV.status_rect.h + 400

    # Size of the log surface
    GV.log_rect.w = GV.screen_rect.w - (GV.eq_rect.w + GV.status_rect.w) \
        - SCROLLBAR_W - 50
    GV.log_rect.h = GV.status_rect.h
    GV.logview_rect.w, GV.logview_rect.h = GV.log_rect.w, GV.log_rect.h


    # The mapview size.  May be smaller or larger than the actual map size.
    # This is the location on the screen where the map or a piece thereof
    # is drawn.  It's not an actual surface, but a logical rectangle.
    GV.mapview_rect.w = GV.screen_rect.w - SCROLLBAR_W
    GV.mapview_rect.h = GV.screen_rect.h - GV.status_rect.h - SCROLLBAR_W

    # Locations to blit equipment on the equipment panel
    eq_cent = (int(GV.eq_rect.w / 2.0 - TILE_W / 2),
               int(GV.eq_rect.h / 2.0 - TILE_W / 2))
    GV.eq_hands = (eq_cent[0], eq_cent[1])
    GV.eq_hands = (eq_cent[0], GV.eq_rect.y + TILE_H / 2 + 3 * TILE_H)
    GV.eq_rweap = (GV.eq_hands[0] - TILE_W, GV.eq_hands[1])
    GV.eq_lweap = (GV.eq_hands[0] + TILE_W, GV.eq_hands[1])
    GV.eq_rring = (GV.eq_hands[0] - TILE_W, GV.eq_hands[1] + TILE_H)
    GV.eq_lring = (GV.eq_hands[0] + TILE_W, GV.eq_hands[1] + TILE_H)
    GV.eq_boots = (GV.eq_hands[0], GV.eq_hands[1] + TILE_H * 2)
    GV.eq_armor = (GV.eq_hands[0], GV.eq_hands[1] - TILE_H)
    GV.eq_shirt = (GV.eq_hands[0] - TILE_W, GV.eq_hands[1] - TILE_H)
    GV.eq_cloak = (GV.eq_hands[0] + TILE_W, GV.eq_hands[1] - TILE_H)
    GV.eq_neck = (GV.eq_hands[0], GV.eq_hands[1] - TILE_H * 2)
    GV.eq_eyes = (GV.eq_hands[0] - TILE_W, GV.eq_hands[1] - TILE_H * 2)
    GV.eq_quiver = (GV.eq_hands[0] + TILE_W * 2, GV.eq_hands[1] - TILE_H * 3)
    GV.eq_light = (GV.eq_hands[0] - TILE_W * 2, GV.eq_hands[1] - TILE_H * 3)
    GV.eq_head = (GV.eq_hands[0], GV.eq_hands[1] - TILE_H * 3)


class GC:
    """Stores the controller state."""
    clock = None

    key = None       # The last pressed key
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


    x_scrollbar = None
    y_scrollbar = None

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
