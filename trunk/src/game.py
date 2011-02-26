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
