# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

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
    GV.screen_rect.w = GV.eq_rect.w + GV.status_rect.w + MIN_LOG_W
    if GV.screen_rect.w < INIT_SCREEN_W:
        GV.screen_rect.w = INIT_SCREEN_W
    GV.screen_rect.h = GV.status_rect.h + MIN_MAPVIEW_H
    if GV.screen_rect.h < INIT_SCREEN_H:
        GV.screen_rect.h = INIT_SCREEN_H

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

class GV:
    """Stores the global game client state."""
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

    x_scrollbar = None
    y_scrollbar = None
    log_scrollbar = None

    pkeys = None
